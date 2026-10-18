"""Rounds against a partner: the hidden-game agent and the iterated-games agent, one environment and one trainer.

Each episode is K rounds against one partner: seat 0 is a learner; seat 1 is the same network (self-play),
another network, or a script (a function of the script's own and its partner's canonical moves so far, returning
its canonical move). A source says what is played:
- `Hidden`: one random bimatrix game per episode, held for every round and never shown; the agent sees only past
  moves and its own payoffs (the hidden-game agent).
- `Iterated`: a new symmetric game every round from games.FAMILIES, shown to each player in its own random action
  labels, so the cooperative move must be read off the matrix (the iterated-games agent). `group` > 1 draws one
  game sequence and set of labels per group of consecutive episodes, for group baselines.
The agent (agents.Agent) carries GRU states over the record of past rounds (the shown game, both moves, my
payoff, the round), read by heads for the move and a critic C_k, the forecast of nu-discounted payoffs from round
k on. Every GRU trunk reads the same record. Layouts: `hidden_layout`, linear move and critic heads;
`iterated_layout`, a tanh head reading the state, the current game and the round. In both the critic shares the
policy's state by default; `detach` lets it read that state without training it, and `separate_critic` gives
it a GRU of its own (formalism/learning.md D8). The hidden-game agent steps its states once on an empty record before
round 1 (`Hidden.prime`); the iterated agent reads zero states.

Felt utility per round is the reinforcement-learning reading of core.md (felt.rounds_direct, a first pass:
echoes of base payoffs, news on the critic's TD error; felt.rounds_canonical when the critic forecasts felt
utility). Training: REINFORCE with rewards-to-go against a per-round baseline; the policy ascends payoffs, felt
utility, or both players' payoffs ("team", the twin's objective in self-play); the critic is one of
- "honest":    TD toward realized payoffs;
- "motivated": TD plus ascending felt utility, tethered by its TD loss (the affect head free to be rosy or
               braced, decision.md D7);
- "offset":    TD toward targets shifted by a fixed per-round offset (a bias with no felt objective);
- "expectile": asymmetric TD, weight 1 - x on overestimates and x on underestimates;
- "canonical": TD toward felt utility itself, so its honest forecast includes anticipated news.
`center` keeps the critic's per-round level outside the network, at the running mean of the TD targets over all
learners' episodes (each learner's batch counts once, as in the TD loss), so the network learns only deviations
and the shared state never carries the level (formalism/learning.md D8).

`adapt` adds a felt reference that persists across episodes (notes/adaptation.md, biphasic memory's slow lobe on
felt states): felt utility gets a term -h r, with r the running mean over training steps of the adapted felt
utility per round (one population-wide reference, advanced once per batch), so for a fixed input its steady level
is 1 / (1 + h) of the unadapted one (Naik et al.'s reward centering, incomplete). In the canonical form the term
sits inside the solve, so memory and news echo adapted states, and a unit of reference lowers mean felt utility
by a gain d (about 2.07 at the rounds calibration, a = 0.05; Codex): steady level 1 / (1 + d h). It enters where
a level can: felt rewards, the canonical critic's targets, and the motivated critic, which ascends welfare, whose
derivative in any felt ingredient far from the end of training is 1 / (1 + h); its push is weighed by that
interior life weight (a critic ascending only the current felt state would not change). For the motivated critic this is exactly a per-round TD offset profile
(Codex), so h is a dial on the strength of the felt push, and the reference itself does not touch training. A
batch-mean baseline removes the reference exactly.

`replay` trains the policy on episodes from `lag` steps back instead of the fresh batch (learning from memory:
a stale sampler, no importance weights), with log-probabilities recomputed under the current weights and the
rewards as they were felt then; the critic still trains on the fresh batch, and the policy starts learning once
memories are `lag` steps old, so each batch is replayed once. Off-policy the expected update splits, history by
history, as E_q[A s | H] = E_q[A | H] s_bar + Cov_q(A, s | H), s_bar = E_q[grad log p] (Marek & Ryabinin 2026): the
advantage's conditional level times a pull toward the old policy (on the move logit, s_bar = q - p). `center` in
replay subtracts s_bar (their score centering), leaving the covariance under the stale sampler; a batch-mean
baseline removes a constant shift of the level but not its variation across histories. `actor_shift` adds a
constant to the policy's rewards only, leaving the critic's objective as it was (its realized targets still follow
the trajectory the policy takes).
"""
from collections import deque

import torch
import torch.nn.functional as F

from agents import Agent
from felt import ROUNDS, rounds_canonical, rounds_direct
from games import family_round, relabeled

torch.set_default_dtype(torch.float64)

K = 10
ITERATED = dict(source="iterated", center=True, feel=dict(ROUNDS, nu=0.9))   # the iterated agent's training


def hidden_layout(width=64, detach=False, separate_critic=False):
    trunks = {"state": ("gru", 6, width)}
    if separate_critic:
        trunks["critic"] = ("gru", 6, width)
    return dict(trunks=trunks, heads={"act": dict(trunk="state"),
                                      "critic": dict(trunk="critic" if separate_critic else "state", detach=detach)},
                roles={"move": ("act", 0), "critic": ("critic", 0)})


def iterated_layout(width=96, detach=False, separate_critic=False):
    head = dict(extra=9, hidden=(width,))
    if not (detach or separate_critic):        # one head, both outputs
        return dict(trunks={"state": ("gru", 14, width)}, heads={"policy": dict(trunk="state", out=2, **head)},
                    roles={"move": ("policy", 0), "critic": ("policy", 1)})
    trunks = {"state": ("gru", 14, width)}
    if separate_critic:
        trunks["critic"] = ("gru", 14, width)
    return dict(trunks=trunks, heads={"policy": dict(trunk="state", **head),
                                      "critic": dict(trunk="critic" if separate_critic else "state", detach=detach,
                                                     **head)},
                roles={"move": ("policy", 0), "critic": ("critic", 0)})


class Hidden:
    """One bimatrix game per episode, held and never shown: A seat 0's payoffs, Bm seat 1's, both indexed
    [seat 0's move, seat 1's move]. Moves are their own labels."""
    prime, shown = True, False

    def __init__(self, A, Bm):
        self.A, self.Bm, self.G = A, Bm, len(A)

    @classmethod
    def draw(cls, G, gen):
        return cls(torch.rand(G, 2, 2, generator=gen) * 2 - 1, torch.rand(G, 2, 2, generator=gen) * 2 - 1)

    def next_round(self, gen):
        """Draws nothing; no round metadata."""
        return None

    def label(self, i, move):
        return move

    def payoffs(self, c):
        ar = torch.arange(self.G)
        return [self.A[ar, c[0], c[1]], self.Bm[ar, c[0], c[1]]]


class Iterated:
    """A new symmetric game every round, each player seeing it in its own random labels."""
    prime, shown = False, True

    def __init__(self, G, families=(0, 1, 2, 3), group=1):
        if group < 1 or G % group:
            raise ValueError(f"group {group} must divide G = {G}")
        self.G, self.families, self.group = G, families, group

    def next_round(self, gen):
        """Draws this round's games and labels; returns each episode's family."""
        M, fam, flips = family_round(self.G // self.group, gen, self.families)
        if self.group > 1:
            rep = lambda x: x.repeat_interleave(self.group, 0)  # noqa: E731
            M, fam, flips = rep(M), rep(fam), [rep(f) for f in flips]
        self.M, self.flips = M, flips
        return fam

    def view(self, i):
        return relabeled(self.M, self.flips[i], self.flips[1 - i])

    def label(self, i, move):
        """Seat i's label for a canonical move, and its canonical move for a label (the flip is an involution)."""
        return move ^ self.flips[i].long()

    def payoffs(self, c):
        ar = torch.arange(self.G)
        return [self.M[ar, c[0], c[1]], self.M[ar, c[1], c[0]]]


def rollout(agent, source, K, gen, other=None, horizon=None):
    """Play K rounds, agent in seat 0 and other in seat 1 (default: the agent itself). Returns per-seat records
    (G, K): logp, r, C, pi and h (the policy's state) for learners; r, coop (the canonical move 0) and label0 for
    every seat; fam when the source has families. A partner network needs only the "move" role. horizon (G,):
    each episode's length, at most K; play runs to K and `mask` marks the rounds inside the episode."""
    G = source.G
    players = (agent, agent if other is None else other)
    learner = [isinstance(p, Agent) for p in players]
    hs = [p.initial_state(G) if a else None for p, a in zip(players, learner)]
    xs = [torch.zeros(G, p.record_size()) if a else None for p, a in zip(players, learner)]
    rec = [{k: [] for k in ("logp", "r", "C", "pi", "h", "coop", "label0")} for _ in range(2)]
    hist, fams = ([], []), []
    for k in range(K):
        fam = source.next_round(gen)
        if fam is not None:
            fams.append(fam)
        t = torch.full((G, 1), (k + 1) / K)
        views = [source.view(i) for i in range(2)] if source.shown else [None, None]
        moves, outs = [], []
        for i, p in enumerate(players):
            if not learner[i]:
                moves.append(source.label(i, p(hist[i], hist[1 - i], gen, G).long()))
                outs.append(None)
                continue
            if k > 0 or source.prime:
                hs[i] = p.step(xs[i], hs[i])
            o = p.roles_at(hs[i], torch.cat([views[i], t], 1) if source.shown else None)
            pi = torch.sigmoid(o["move"])
            moves.append((torch.rand(G, generator=gen) >= pi).long())                   # 0 with prob pi
            outs.append((pi, o.get("critic")))
        canon = [source.label(i, moves[i]) for i in range(2)]
        r = source.payoffs(canon)
        for i in range(2):
            R = rec[i]
            hist[i].append(canon[i])
            R["coop"].append((canon[i] == 0).double())
            R["label0"].append((moves[i] == 0).double())
            R["r"].append(r[i])
            if outs[i] is not None:
                pi, C = outs[i]
                R["logp"].append(torch.where(moves[i] == 0, torch.log(pi.clamp_min(1e-12)),
                                             torch.log((1 - pi).clamp_min(1e-12))))
                if C is not None:
                    R["C"].append(C)
                R["pi"].append(pi)
                R["h"].append(hs[i][players[i].layout[players[i].roles["move"][0]]["trunk"]])
                xs[i] = torch.cat(([views[i]] if source.shown else []) + [
                    torch.nn.functional.one_hot(moves[i], 2), torch.nn.functional.one_hot(moves[1 - i], 2),
                    r[i][:, None], t], 1).double()
    out = []
    for R in rec:
        D = {k: torch.stack(v, 1) for k, v in R.items() if v}
        if fams:
            D["fam"] = torch.stack(fams, 1)
        if horizon is not None:
            D["mask"] = (torch.arange(K)[None, :] < horizon[:, None]).double()
        out.append(D)
    return out


def records(R, other):
    """The records a hidden-game learner read, rebuilt from its rollout record R and its partner's (moves are their
    own labels): x[:, 0] is the empty record it primes on, x[:, k] the record of round k - 1."""
    G, K = R["r"].shape
    own, oth = (1 - R["label0"]).long(), (1 - other["label0"]).long()
    t = (torch.arange(1, K + 1).double() / K).expand(G, K)
    rec = torch.cat([F.one_hot(own, 2), F.one_hot(oth, 2), R["r"][..., None], t[..., None]], 2).double()
    return torch.cat([torch.zeros(G, 1, rec.shape[2]), rec[:, :-1]], 1)


def replay_pass(agent, x):
    """The policy's logit for move 0 and the critic's forecast under the current weights, on stored records."""
    h, zs, Cs = agent.initial_state(len(x)), [], []
    for k in range(x.shape[1]):
        h = agent.step(x[:, k], h)
        o = agent.roles_at(h)
        zs.append(o["move"])
        Cs.append(o["critic"])
    return torch.stack(zs, 1), torch.stack(Cs, 1)


def replay_terms(agent, batch):
    """For each replayed learner: the log-probability of its played moves under the current weights, the stale
    sampler's expected log-probability sum_v q_v log p_v (score centering subtracts it), the advantage's inputs and
    the current move probability. Logs from logits, so the centered score stays exactly A (y - q) at saturation."""
    out = []
    for x, y0, q, rew in batch:
        z, C = replay_pass(agent, x)
        lp, lq = F.logsigmoid(z), F.logsigmoid(-z)
        out.append((torch.where(y0, lp, lq), q * lp + (1 - q) * lq, to_go(rew), C, y0, q, torch.sigmoid(z).detach()))
    return out


def to_go(rew):
    return torch.flip(torch.cumsum(torch.flip(rew.detach(), [1]), 1), [1])


def td_loss(rec, feel=ROUNDS, critic="honest", offset=None, expectile=None, adapted=0.0):
    """adapted: the felt reference's pull h r, subtracted from the canonical critic's felt targets."""
    r, C = rec["r"], rec["C"]
    G, K = r.shape
    base = rounds_canonical(r, C.detach(), feel, adapted) if critic == "canonical" else r
    d = C - (base + feel["nu"] * torch.cat([C[:, 1:].detach(), torch.zeros(G, 1)], 1))
    if critic == "offset":
        return ((d - offset) ** 2).mean()
    if critic == "expectile":
        return (torch.where(d > 0, 1 - expectile, expectile) * 2 * d ** 2).mean()
    return (d ** 2).mean()


def train(reward="payoff", critic="honest", steps=3000, G=2048, K=K, seed=0, lr=3e-3, feel=ROUNDS, offset=None,
          expectile=None, detach=False, separate_critic=False, baseline="batch", reward_shift=0.0, center=False,
          source="hidden", families=(0, 1, 2, 3), partners=None, monitor=None, adapt=None, replay=None,
          actor_shift=0.0, log=None):
    """source: "hidden" or "iterated" (with its layout). reward: "payoff", "felt" (felt utility over the critic's
    forecasts, held fixed) or "team" (both players' payoffs). partners: scripts that take half of each batch, split
    evenly (the other half is self-play). detach: the critic reads the policy's state without training it, so
    it cannot shape what the policy sees; separate_critic: the critic has a GRU of its own. baseline: "batch" (the
    batch mean of rewards-to-go), "critic" (the critic's forecast, so its level also enters the policy's update) or
    "none" (rewards-to-go as they are). reward_shift: a constant added to every payoff the learners see as reward
    (the state still sees the raw payoff), which moves the honest critic's level without biasing it; actor_shift:
    the same for the policy's rewards only. center: the level kept outside the network (an honest critic's), a
    buffer of the agent, so it travels with its state. adapt: dict(h, rate=0.01), the felt reference (module
    docstring), a buffer `ref`. replay: dict(lag, center=False, anchor=0.0), hidden source only; anchor c adds the
    analytic part of an actor shift c, the pull c (K - k) grad sum_v q_v log p_v toward the policy that played the
    memory, without the shift's sampling noise (Codex's control). log: a dict, given replay, that
    gets per step ("steps") the replayed advantage's mean, the RMS gap between old and current move probabilities
    and the sample logit-correction RMS over the raw-score RMS, |A (q - p)| / |A (y - p)|; and every 250 steps
    ("checks") the policy gradient on the replayed batch in parameter space: the norms of the raw ascent direction
    mean[A grad log p_y] and of its correction mean[A grad sum_v q_v log p_v] (what score centering removes), their
    cosine, and the correction's cosine with the way back to the weights that played the batch, over the parameters
    the policy reads (trunk and move head). The correction is the part of plain replay's direction that score
    centering removes, not the whole update.
    monitor(step, agent), if given, is called every 250 steps."""
    if (source not in ("hidden", "iterated") or reward not in ("payoff", "felt", "team")
            or baseline not in ("batch", "critic", "none")
            or critic not in ("honest", "motivated", "offset", "expectile", "canonical")):
        raise ValueError(f"unknown source, reward, critic or baseline: {source, reward, critic, baseline}")
    if (critic == "offset" and offset is None) or (critic == "expectile" and expectile is None):
        raise ValueError(f"critic {critic!r} needs its parameter")
    if center and critic != "honest":
        raise ValueError("the level kept outside is the mean of honest TD targets")
    if detach and separate_critic:
        raise ValueError("a detached critic on its own trunk would never train it")
    if replay is not None and (source != "hidden" or not isinstance(replay["lag"], int) or replay["lag"] < 0):
        raise ValueError("replay rebuilds hidden-game records only, at an integer lag >= 0")
    if adapt is not None:
        h, rate = adapt["h"], adapt.get("rate", 0.01)
        if h <= -1 or abs(1 - rate * (1 + h)) >= 1:
            raise ValueError(f"felt reference needs h > -1 and |1 - rate (1 + h)| < 1: {adapt}")
        if critic == "canonical" and reward == "felt":
            raise ValueError("one reference, two felt utilities (canonical critic, direct felt rewards)")
    gen = torch.Generator().manual_seed(seed)
    torch.manual_seed(seed)
    layout = hidden_layout if source == "hidden" else iterated_layout
    agent = Agent(**layout(detach=detach, separate_critic=separate_critic))
    opt = torch.optim.Adam(agent.parameters(), lr=lr)
    off = torch.tensor(offset) if offset is not None else None
    agent.register_buffer("level", torch.zeros(K))
    agent.register_buffer("ref", torch.zeros(()))
    level, ref = agent.level, agent.ref
    h = adapt["h"] if adapt else 0.0
    memory = deque(maxlen=replay["lag"] + 1) if replay is not None else None
    snaps = deque(maxlen=replay["lag"] + 1) if replay is not None and log is not None else None
    n_self = G // 2 if partners else G
    params = list(agent.parameters())
    critic_head = {id(p) for p in agent.heads["critic"].parameters()} if "critic" in agent.heads else set()
    acting = torch.cat([torch.full((p.numel(),), id(p) not in critic_head) for p in params])
    flat = lambda gs: torch.cat([(g if g is not None else torch.zeros_like(p)).flatten() for g, p in zip(gs, params)])  # noqa: E731

    def make(n):
        return Hidden.draw(n, gen) if source == "hidden" else Iterated(n, families)

    for it in range(steps):
        if monitor is not None and it % 250 == 0:
            monitor(it, agent)
        rec = rollout(agent, make(n_self), K, gen)
        learners = [(rec[i], rec[1 - i], rec[0]["r"] + rec[1]["r"]) for i in range(2)]
        for p in (partners or {}).values():
            Rp = rollout(agent, make(G // (2 * len(partners))), K, gen, other=p)
            learners.append((Rp[0], Rp[1], Rp[0]["r"] + Rp[1]["r"]))
        loss, targets, felt_means, kept = 0.0, [], [], []
        hr = h * float(ref) if adapt else 0.0                                  # the felt reference's pull, h r
        for R, other, joint in learners:
            x = records(R, other) if replay is not None else None
            if reward_shift:
                R = dict(R, r=R["r"] + reward_shift)
            if center:
                R = dict(R, C=R["C"] + level)
            if adapt:
                felt = (rounds_canonical(R["r"], R["C"].detach(), feel, hr) if critic == "canonical"
                        else rounds_direct(R["r"], R["C"].detach(), feel) - hr)
                felt_means.append(float(felt.mean()))
            rew = {"payoff": R["r"], "team": joint}.get(reward)
            rew = rounds_direct(R["r"], R["C"].detach(), feel) - hr if rew is None else rew
            if actor_shift:
                rew = rew + actor_shift
            if replay is None:
                ret = to_go(rew)                                                          # rewards-to-go
                base = {"critic": R["C"].detach(), "batch": ret.mean(0, keepdim=True), "none": 0.0}[baseline]
                loss = loss - (R["logp"] * (ret - base)).mean()
            else:
                kept.append((x, R["label0"].bool(), R["pi"].detach(), rew.detach()))          # moves are labels
            loss = loss + td_loss(R, feel, critic, off, expectile, hr)
            if critic == "motivated":
                loss = loss - rounds_direct(R["r"], R["C"], feel).sum(1).mean() / (1 + h)   # ascends welfare
            targets.append((R["r"] + feel["nu"] * torch.cat([R["C"][:, 1:], torch.zeros(len(R["r"]), 1)], 1))
                           .detach().mean(0))
        if replay is not None:
            memory.append(kept)
            if snaps is not None:
                snaps.append(torch.cat([p.detach().flatten() for p in params]))
        if replay is not None and len(memory) == memory.maxlen:                   # memories lag steps old
            terms = replay_terms(agent, memory[0])
            raw, cor, stats = 0.0, 0.0, []
            for logp, expected, ret, C, y0, q, p in terms:
                base = {"critic": C.detach() + (level if center else 0.0), "batch": ret.mean(0, keepdim=True),
                        "none": 0.0}[baseline]
                A = ret - base
                raw, cor = raw + (logp * A).mean(), cor + (expected * A).mean()
                stats.append([float(A.mean()), float(((q - p) ** 2).mean().sqrt()),
                              float((A * (q - p)).norm() / (A * (y0.double() - p)).norm().clamp_min(1e-12))])
            loss = loss - (raw - cor if replay.get("center") else raw)                # score centering removes cor
            if replay.get("anchor"):
                pull = replay["anchor"] * torch.arange(K, 0, -1).double()               # c (K - k), a shift's to-go
                loss = loss - sum((expected * pull).mean() for _, expected, *_ in terms)
            if log is not None:
                log.setdefault("steps", []).append([sum(c) / len(c) for c in zip(*stats)])
                if it % 250 == 0:
                    g_raw = flat(torch.autograd.grad(raw, params, retain_graph=True, allow_unused=True))
                    g_cor = flat(torch.autograd.grad(cor, params, retain_graph=True, allow_unused=True))
                    back, g_raw, g_cor = (snaps[0] - snaps[-1])[acting], g_raw[acting], g_cor[acting]
                    cos = lambda u, v: float(u @ v / (u.norm() * v.norm()).clamp_min(1e-30))  # noqa: E731
                    log.setdefault("checks", []).append(dict(step=it, level=log["steps"][-1][0], raw=float(g_raw.norm()),
                                                             correction=float(g_cor.norm()), cos_raw=cos(g_cor, g_raw),
                                                             cos_back=cos(g_cor, back)))
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(agent.parameters(), 5.0)
        opt.step()
        if center:
            level += 0.1 * (torch.stack(targets).mean(0) - level)       # in place: the critic's forecast is head + level
        if adapt:
            ref += rate * (sum(felt_means) / len(felt_means) - ref)
    return agent


# scripted partners: functions of (partner's own canonical moves, the player's canonical moves) -> canonical move
def always(c):
    return lambda own, other, gen, G: torch.full((G,), c, dtype=torch.long)


def tit_for_tat(own, other, gen, G):
    return torch.zeros(G, dtype=torch.long) if not other else other[-1]


def coin(own, other, gen, G):
    return (torch.rand(G, generator=gen) < 0.5).long()


def grim(own, other, gen, G):
    """Cooperate until the partner first defects."""
    return torch.zeros(G, dtype=torch.long) if not other else torch.stack(other, 1).max(1).values


def win_stay_lose_shift(own, other, gen, G):
    """Cooperate first, then whenever both made the same move last round (Pavlov)."""
    return torch.zeros(G, dtype=torch.long) if not other else (own[-1] != other[-1]).long()


def suspicious_tit_for_tat(own, other, gen, G):
    return torch.ones(G, dtype=torch.long) if not other else other[-1]


def generous_tit_for_tat(own, other, gen, G):
    """Tit for tat that forgives a defection with probability 1/3."""
    if not other:
        return torch.zeros(G, dtype=torch.long)
    return torch.where(torch.rand(G, generator=gen) < 1 / 3, 0, other[-1])


def alternate(own, other, gen, G):
    return torch.full((G,), len(own) % 2, dtype=torch.long)


def tit_for_two_tats(own, other, gen, G):
    return torch.zeros(G, dtype=torch.long) if len(other) < 2 else other[-1] & other[-2]


def reactive(p):
    """Cooperate first, then with probability p[outcome] after (CC, CD, DC, DD), own move first."""
    p = torch.tensor(p)

    def play(own, other, gen, G):
        if not other:
            return torch.zeros(G, dtype=torch.long)
        return (torch.rand(G, generator=gen) >= p[2 * own[-1] + other[-1]]).long()
    return play


PARTNERS = {"always cooperate": always(0), "always defect": always(1), "tit for tat": tit_for_tat,
            "coin flip": coin}


if __name__ == "__main__":
    # checks: python rounds.py. The critic's TD loss reaches the policy's state only when they share it.
    for source, layout in (("hidden", hidden_layout), ("iterated", iterated_layout)):
        for kw in (dict(), dict(detach=True), dict(separate_critic=True)):
            torch.manual_seed(0)
            agent = Agent(**layout(**kw))
            gen = torch.Generator().manual_seed(1)
            src = Hidden.draw(256, gen) if source == "hidden" else Iterated(256)
            R = rollout(agent, src, K, gen)[0]
            trunks = list(agent.trunks)
            gs = torch.autograd.grad(td_loss(R), [p for t in trunks for p in agent.trunks[t].parameters()],
                                     allow_unused=True)
            sizes = [len(list(agent.trunks[t].parameters())) for t in trunks]
            push = {t: max((float(g.abs().max()) for g in gs[sum(sizes[:j]):sum(sizes[:j + 1])] if g is not None),
                           default=0.0) for j, t in enumerate(trunks)}
            print(f"{source}, {kw or 'shared'}: largest TD gradient by trunk "
                  + ", ".join(f"{t} {v:.1e}" for t, v in push.items()))
    # Replay at lag 0 recomputes the fresh batch under the same weights: the policy gradient matches on-policy
    # training's, and score centering subtracts q - p = 0 there. Records rebuild what the agent read.
    torch.manual_seed(0)
    agent = Agent(**hidden_layout())
    gen = torch.Generator().manual_seed(1)
    rec = rollout(agent, Hidden.draw(512, gen), K, gen)
    params = list(agent.parameters())

    def flat_grad(loss):
        gs = torch.autograd.grad(loss, params, retain_graph=True, allow_unused=True)
        return torch.cat([(g if g is not None else torch.zeros_like(p)).flatten() for g, p in zip(gs, params)])
    for base in ("batch", "none"):
        grads = []
        for kind in ("rollout", "replay", "replay, centered"):
            loss = 0.0
            for i in range(2):
                R = rec[i]
                ret = to_go(R["r"])
                b = ret.mean(0, keepdim=True) if base == "batch" else 0.0
                if kind == "rollout":
                    logp = R["logp"]
                else:
                    logp, expected = replay_terms(agent, [(records(R, rec[1 - i]), R["label0"].bool(), R["pi"].detach(), R["r"])])[0][:2]
                    if kind.endswith("centered"):
                        logp = logp - expected
                loss = loss - (logp * (ret - b)).mean()
            grads.append(flat_grad(loss))
        print(f"replay at lag 0, {base} baseline: largest gradient gap to on-policy {float((grads[1] - grads[0]).abs().max()):.1e}, "
              f"centered {float((grads[2] - grads[0]).abs().max()):.1e} (scale {float(grads[0].abs().max()):.1e})")
    feel = dict(ROUNDS, a=0.05)
    C = torch.randn(64, K) * 0.5
    r = torch.rand(64, K) * 2 - 1
    e = rounds_canonical(r, C, feel, 0.4)
    Cn = torch.cat([C[:, 1:], torch.zeros(64, 1)], 1)
    mem = torch.stack([sum(feel["m"] * feel["mu"] ** j * e[:, k - j] for j in range(1, k + 1)) if k else torch.zeros(64)
                       for k in range(K)], 1)
    x = r + feel["a"] * feel["nu"] * Cn + mem - 0.4
    print(f"adapted canonical felt utility solves its own equation: residual "
          f"{float((e - x - feel['n'] * (e + feel['nu'] * Cn - C)).abs().max()):.1e}")
    z = torch.randn(1000, requires_grad=True)
    q, y0, A = torch.rand(1000), torch.rand(1000) < 0.5, torch.randn(1000)
    pi = torch.sigmoid(z)
    lp, lq = torch.log(pi), torch.log(1 - pi)
    g = torch.autograd.grad((A * (torch.where(y0, lp, lq) - (q * lp + (1 - q) * lq))).sum(), z)[0]
    print(f"score centering on the move logit is A (y - q): gap {float((g - A * (y0.double() - q)).abs().max()):.1e}")
