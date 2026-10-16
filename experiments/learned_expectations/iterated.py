"""Iterated randomized games: a different known game every round with the same partner.

Each episode is K rounds against one partner. Every round draws a symmetric 2x2 game from a family (prisoner's
dilemma, chicken, stag hunt, harmony) with fresh payoffs, shown to both players, each in its own randomly
ordered action labels, so the cooperative move has to be read off the matrix. In canonical labels (C = 0)
the row player's payoffs are [[R, S], [T, P]], four sorted draws from U[-1, 1] assigned by the family's order.

The player: a GRU carries the history (each past round's game, both moves, my payoff); a head reads the
state and the current game and gives the move and a critic. Training: self-play with shared weights,
REINFORCE on rewards-to-go against the batch mean per round; an honest critic (TD at discount NU) keeps its
per-round level outside the network (decision.md D8). Objective: "selfish" (my payoffs) or "team" (both
players' payoffs, the twin's objective in a symmetric game).
"""
import numpy as np
import torch

torch.set_default_dtype(torch.float64)

FAMILIES = ["prisoner's dilemma", "chicken", "stag hunt", "harmony"]
# rank (0 = largest of the four draws) of R, S, T, P in each family
RANKS = torch.tensor([[1, 3, 0, 2],      # PD:        T > R > P > S
                      [1, 2, 0, 3],      # chicken:   T > R > S > P
                      [0, 3, 1, 2],      # stag hunt: R > T > P > S
                      [0, 2, 1, 3]])     # harmony:   R > T > S > P
NU, K = 0.9, 10


def sample_round(G, gen, families=(0, 1, 2, 3)):
    """Canonical payoff matrices M (G, 2, 2) for the row player, the family index, and label flips."""
    fam = torch.tensor(families)[torch.randint(len(families), (G,), generator=gen)]
    v = torch.sort(torch.rand(G, 4, generator=gen) * 2 - 1, dim=1, descending=True).values
    RSTP = v.gather(1, RANKS[fam])
    M = torch.stack([torch.stack([RSTP[:, 0], RSTP[:, 1]], 1), torch.stack([RSTP[:, 2], RSTP[:, 3]], 1)], 1)
    flips = [torch.rand(G, generator=gen) < 0.5 for _ in range(2)]
    return M, fam, flips


def view(M, f_me, f_them):
    """(my payoffs, their payoffs) indexed [my label, their label], flattened to 8 numbers."""
    def relabel(X, fr, fc):
        X = torch.where(fr[:, None, None], X.flip(1), X)
        return torch.where(fc[:, None, None], X.flip(2), X)
    mine = relabel(M, f_me, f_them)
    theirs = relabel(M.transpose(1, 2), f_me, f_them)
    return torch.cat([mine.flatten(1), theirs.flatten(1)], 1)


class Player(torch.nn.Module):
    def __init__(self, width=96):
        super().__init__()
        self.gru = torch.nn.GRUCell(8 + 2 + 2 + 1 + 1, width)
        self.head = torch.nn.Sequential(torch.nn.Linear(width + 8 + 1, width), torch.nn.Tanh(),
                                        torch.nn.Linear(width, 2))

    def act(self, h, cur, t):
        out = self.head(torch.cat([h, cur, t], 1))
        return torch.sigmoid(out[:, 0]), out[:, 1]          # P(my label 0), critic

    def remember(self, h, cur, mine, theirs, r, t):
        x = torch.cat([cur, torch.nn.functional.one_hot(mine, 2), torch.nn.functional.one_hot(theirs, 2),
                       r[:, None], t], 1).double()
        return self.gru(x, h)


def rollout(player, G, gen, families=(0, 1, 2, 3), partner=None, K=K):
    """Self-play (partner None) or play against a scripted partner, a function of the partner's own and
    the player's canonical moves so far returning the partner's canonical move (0 = cooperate).
    Returns per-seat records in canonical terms: coop (G, K), payoff, logp, critic, family."""
    hs = [torch.zeros(G, player.gru.hidden_size) for _ in range(2)]
    rec = [{k: [] for k in ("coop", "label0", "r", "logp", "C")} for _ in range(2)]
    fams, hist = [], ([], [])
    for k in range(K):
        M, fam, (f1, f2) = sample_round(G, gen, families)
        fams.append(fam)
        t = torch.full((G, 1), (k + 1) / K)
        cur = [view(M, f1, f2), view(M, f2, f1)]
        flips = (f1, f2)
        moves, outs = [], []
        for i in range(2):
            if i == 1 and partner is not None:
                c = partner(hist[1], hist[0], gen, G)
                moves.append(c.long() ^ flips[1].long())
                outs.append(None)
                continue
            pi, C = player.act(hs[i], cur[i], t)
            moves.append((torch.rand(G, generator=gen) >= pi).long())
            outs.append((pi, C))
        canon = [moves[i] ^ flips[i].long() for i in range(2)]
        r = [M[torch.arange(G), canon[0], canon[1]], M[torch.arange(G), canon[1], canon[0]]]
        for i in range(2):
            hist[i].append(canon[i])
            rec[i]["coop"].append((canon[i] == 0).double())
            rec[i]["label0"].append((moves[i] == 0).double())
            rec[i]["r"].append(r[i])
            if outs[i] is not None:
                pi, C = outs[i]
                rec[i]["logp"].append(torch.where(moves[i] == 0, torch.log(pi.clamp_min(1e-12)),
                                                  torch.log((1 - pi).clamp_min(1e-12))))
                rec[i]["C"].append(C)
                hs[i] = player.remember(hs[i], cur[i], moves[i], moves[1 - i], r[i], t)
    fam = torch.stack(fams, 1)
    return [{k: torch.stack(v, 1) for k, v in R.items() if v} | {"fam": fam} for R in rec]


def train(objective="selfish", steps=3000, G=2048, seed=0, lr=3e-3, families=(0, 1, 2, 3), K=K, mixed=False,
          monitor=None):
    """mixed: half of each batch is self-play, the rest split evenly over the scripted partners."""
    gen = torch.Generator().manual_seed(seed)
    torch.manual_seed(seed)
    player = Player()
    opt = torch.optim.Adam(player.parameters(), lr=lr)
    level = torch.zeros(K)
    for it in range(steps):
        if monitor is not None and it % 250 == 0:
            monitor(it, player)
        rec = rollout(player, G // 2 if mixed else G, gen, families, K=K)
        learners = [(R, rec[0]["r"] + rec[1]["r"]) for R in rec]
        if mixed:
            for partner in PARTNERS.values():
                Rp = rollout(player, G // (2 * len(PARTNERS)), gen, families, partner=partner, K=K)
                learners.append((Rp[0], Rp[0]["r"] + Rp[1]["r"]))
        loss, targets = 0.0, []
        for R, joint in learners:
            reward = joint if objective == "team" else R["r"]
            ret = torch.flip(torch.cumsum(torch.flip(reward, [1]), 1), [1])
            loss = loss - (R["logp"] * (ret - ret.mean(0, keepdim=True))).mean()
            C = R["C"] + level
            target = R["r"] + NU * torch.cat([C[:, 1:].detach(), torch.zeros(len(C), 1)], 1)
            loss = loss + ((C - target) ** 2).mean()
            targets.append(target.detach().mean(0))
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(player.parameters(), 5.0)
        opt.step()
        # the level tracks the TD loss's own weighting (each learner's batch mean counts once), so the head
        # learns only deviations from it and carries no mean push on the shared state
        level += 0.1 * (torch.stack(targets).mean(0) - level)
    player.level = level                       # the critic's forecast is the head's output + level
    return player


# scripted partners: functions of (partner's own canonical moves, the player's canonical moves) -> move
def always(c):
    return lambda own, other, gen, G: torch.full((G,), c, dtype=torch.long)


def tit_for_tat(own, other, gen, G):
    return torch.zeros(G, dtype=torch.long) if not other else other[-1]


def coin(own, other, gen, G):
    return (torch.rand(G, generator=gen) < 0.5).long()


PARTNERS = {"always cooperate": always(0), "always defect": always(1), "tit for tat": tit_for_tat,
            "coin flip": coin}
