"""The hidden-game agent: repeated rounds of an unknown 2x2 game, an actor-critic whose critic is its felt
anticipation (core.md, the reinforcement-learning reading).

Each episode is K rounds of one random bimatrix game against a self-play partner (the same network on its
own history). The agent never sees the payoff matrix: only past moves and its own realized payoffs. A GRU
state feeds an action head and a critic C_k, the forecast of discounted payoffs from round k on.

Felt utility per round (direct echoes, news over base payoffs; a first pass, not the canonical model):
  e_k = r_k + a nu C_{k+1} + sum_j m mu^j r_{k-j} + n phi_lam(delta_k),   delta_k = r_k + nu C_{k+1} - C_k,
anticipation as the critic's forecast of what is to come and news as its felt TD error.
Training: REINFORCE with rewards-to-go against the batch mean; the policy ascends payoffs or felt utility
(over the critic's forecasts, held fixed), and the critic is one of
- "honest":    TD toward realized payoffs;
- "motivated": TD plus ascending felt utility, tethered by its TD loss (the affect head free to be rosy or
               braced, decision.md D7);
- "offset":    TD toward targets shifted by a fixed per-round offset (a bias with no felt objective);
- "expectile": asymmetric TD, weight 1 - x on overestimates and x on underestimates;
- "canonical": TD toward felt utility itself, recursive memory and news on the felt TD error, so its honest
               forecast includes anticipated news.
The variants of run_repeated.py: payoff (payoff, honest), calibrated (felt, honest), motivated (felt, motivated).
"""
import numpy as np
import torch

torch.set_default_dtype(torch.float64)

FEEL = dict(a=0.3, m=0.2, mu=0.6, n=0.3, nu=0.8, lam=2.0)


class Agent(torch.nn.Module):
    def __init__(self, width=64):
        super().__init__()
        self.gru = torch.nn.GRUCell(6, width)
        self.act = torch.nn.Linear(width, 1)
        self.critic = torch.nn.Linear(width, 1)

    def step(self, x, h):
        h = self.gru(x, h)
        return torch.sigmoid(self.act(h)[:, 0]), self.critic(h)[:, 0], h


def rollout(agent, A, Bm, K, gen, other=None):
    """Play K rounds, agent in seat 1 and other (default: agent itself) in seat 2. Returns per-round
    tensors for each seat (dicts)."""
    G = A.shape[0]
    players = (agent, agent if other is None else other)
    hs = [torch.zeros(G, agent.gru.hidden_size), torch.zeros(G, agent.gru.hidden_size)]
    xs = [torch.zeros(G, 6), torch.zeros(G, 6)]
    rec = [{k: [] for k in ("logp", "r", "C", "pi", "h")} for _ in range(2)]
    for k in range(K):
        out = [players[i].step(xs[i], hs[i]) for i in range(2)]
        moves = [(torch.rand(G, generator=gen) >= out[i][0]).long() for i in range(2)]    # 0 with prob pi
        a1, a2 = moves
        r = [A[torch.arange(G), a1, a2], Bm[torch.arange(G), a1, a2]]
        for i, (mine, theirs) in enumerate(((a1, a2), (a2, a1))):
            pi, C, h = out[i]
            rec[i]["logp"].append(torch.where(mine == 0, torch.log(pi.clamp_min(1e-12)), torch.log((1 - pi).clamp_min(1e-12))))
            rec[i]["r"].append(r[i])
            rec[i]["C"].append(C)
            rec[i]["pi"].append(pi)
            rec[i]["h"].append(h)
            hs[i] = h
            xs[i] = torch.cat([torch.nn.functional.one_hot(mine, 2), torch.nn.functional.one_hot(theirs, 2),
                               r[i][:, None], torch.full((G, 1), (k + 1) / K)], 1).double()
    for i in range(2):
        rec[i] = {k: torch.stack(v, 1) for k, v in rec[i].items()}
    return rec


def felt(rec, C_used, feel=FEEL):
    """Felt utility per round from realized payoffs and the critic values C_used (G, K)."""
    r = rec["r"]
    G, K = r.shape
    Cn = torch.cat([C_used[:, 1:], torch.zeros(G, 1)], 1)           # C_{k+1}, zero after the last round
    delta = r + feel["nu"] * Cn - C_used
    news = torch.where(delta >= 0, delta, feel["lam"] * delta) * feel["n"]
    mem = torch.zeros_like(r)
    for k in range(1, K):
        mem[:, k] = sum(feel["m"] * feel["mu"] ** j * r[:, k - j] for j in range(1, k + 1))
    return r + feel["a"] * feel["nu"] * Cn + mem + news


def felt_canonical(r, C, feel=FEEL):
    """Canonical felt utility over the critic's forecasts of felt utility: e_k = x_k + n phi(e_k + nu C_{k+1} - C_k),
    x_k = r_k + a nu C_{k+1} + sum_j m mu^j e_{k-j}; the root is on the branch of x_k + nu C_{k+1} - C_k."""
    G, K = r.shape
    Cn = torch.cat([C[:, 1:], torch.zeros(G, 1)], 1)
    es = []
    for k in range(K):
        mem = sum(feel["m"] * feel["mu"] ** j * es[k - j] for j in range(1, k + 1)) if k else 0.0
        x = r[:, k] + feel["a"] * feel["nu"] * Cn[:, k] + mem
        z = x + feel["nu"] * Cn[:, k] - C[:, k]
        c = torch.where(z >= 0, 1.0, feel["lam"])
        es.append(x + feel["n"] * c * z / (1 - feel["n"] * c))
    return torch.stack(es, 1)


def td_loss(rec, feel=FEEL, critic="honest", offset=None, expectile=None):
    r, C = rec["r"], rec["C"]
    G, K = r.shape
    base = felt_canonical(r, C.detach(), feel) if critic == "canonical" else r
    d = C - (base + feel["nu"] * torch.cat([C[:, 1:].detach(), torch.zeros(G, 1)], 1))
    if critic == "offset":
        return ((d - offset) ** 2).mean()
    if critic == "expectile":
        return (torch.where(d > 0, 1 - expectile, expectile) * 2 * d ** 2).mean()
    return (d ** 2).mean()


def train(policy="payoff", critic="honest", steps=3000, G=2048, K=10, seed=0, lr=3e-3, feel=FEEL,
          offset=None, expectile=None, detach=False, baseline="batch", reward_shift=0.0, center=False,
          monitor=None):
    """detach: the critic reads the state without training it, so it cannot shape what the policy sees.
    baseline: "batch" (the batch mean of rewards-to-go) or "critic" (the critic's forecast, so its level also
    enters the policy's update). reward_shift: a constant added to every payoff the learners see as reward
    (the state still sees the raw payoff), which moves the honest critic's level without biasing it.
    center: the critic's per-round level is a running mean of its targets kept outside the network, which
    learns only deviations from it (as PopArt-style normalization does), so the shared state never carries
    the level. monitor(step, agent), if given, is called every 250 steps."""
    gen = torch.Generator().manual_seed(seed)
    torch.manual_seed(seed)
    agent = Agent()
    opt = torch.optim.Adam(agent.parameters(), lr=lr)
    off = torch.tensor(offset) if offset is not None else None
    level = torch.zeros(K)
    for it in range(steps):
        if monitor is not None and it % 250 == 0:
            monitor(it, agent)
        A, Bm = torch.rand(G, 2, 2, generator=gen) * 2 - 1, torch.rand(G, 2, 2, generator=gen) * 2 - 1
        rec = rollout(agent, A, Bm, K, gen)
        loss = 0.0
        for i in range(2):
            R = rec[i]
            if reward_shift:
                R = dict(R, r=R["r"] + reward_shift)
            if detach:
                R = dict(R, C=agent.critic(R["h"].detach())[:, :, 0])
            if center:
                R = dict(R, C=R["C"] + level)
            reward = R["r"] if policy == "payoff" else felt(R, R["C"].detach(), feel)
            ret = torch.flip(torch.cumsum(torch.flip(reward.detach(), [1]), 1), [1])     # rewards-to-go
            base = R["C"].detach() if baseline == "critic" else ret.mean(0, keepdim=True)
            loss = loss - (R["logp"] * (ret - base)).mean()
            loss = loss + td_loss(R, feel, critic, off, expectile)
            if critic == "motivated":
                loss = loss - felt(R, R["C"], feel).sum(1).mean()                        # ascends felt utility
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(agent.parameters(), 5.0)
        opt.step()
        if center:
            with torch.no_grad():
                Cn = torch.cat([R["C"][:, 1:], torch.zeros(G, 1)], 1)
                level += 0.1 * ((R["r"] + feel["nu"] * Cn).mean(0) - level)
    return agent
