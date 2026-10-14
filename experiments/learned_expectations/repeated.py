"""The hidden-game agent: repeated rounds of an unknown 2x2 game, an actor-critic whose critic is its felt
anticipation (core.md, the reinforcement-learning reading).

Each episode is K rounds of one random bimatrix game against a self-play partner (the same network on its
own history). The agent never sees the payoff matrix: only past moves and its own realized payoffs. A GRU
state feeds an action head and a critic C_k, the forecast of discounted payoffs from round k on.

Felt utility per round (direct echoes, news over base payoffs; a first pass, not the canonical model):
  e_k = r_k + a nu C_{k+1} + sum_j m mu^j r_{k-j} + n phi_lam(delta_k),   delta_k = r_k + nu C_{k+1} - C_k,
anticipation as the critic's forecast of what is to come and news as its felt TD error.
Variants:
- "payoff":     the policy maximizes payoffs; the critic learns by TD only.
- "calibrated": the policy maximizes felt utility; the critic learns by TD only (honest forecasts).
- "motivated":  as calibrated, but the critic also ascends felt utility, tethered by its TD loss / tau
                (the affect head free to be rosy or braced, decision.md D7).
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


def rollout(agent, A, Bm, K, gen, feel=FEEL):
    """Play K rounds. Returns per-round tensors for player 1 and 2 (dicts) and the final states."""
    G = A.shape[0]
    hs = [torch.zeros(G, agent.gru.hidden_size), torch.zeros(G, agent.gru.hidden_size)]
    xs = [torch.zeros(G, 6), torch.zeros(G, 6)]
    rec = [{k: [] for k in ("logp", "r", "C", "pi", "h")} for _ in range(2)]
    for k in range(K):
        out = [agent.step(xs[i], hs[i]) for i in range(2)]
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


def td_loss(rec, feel=FEEL):
    r, C = rec["r"], rec["C"]
    G, K = r.shape
    target = r + feel["nu"] * torch.cat([C[:, 1:].detach(), torch.zeros(G, 1)], 1)
    return ((C - target) ** 2).mean()


def train(variant, steps=3000, G=2048, K=10, seed=0, tau=1.0, lr=3e-3):
    gen = torch.Generator().manual_seed(seed)
    torch.manual_seed(seed)
    agent = Agent()
    opt = torch.optim.Adam(agent.parameters(), lr=lr)
    for it in range(steps):
        A, Bm = torch.rand(G, 2, 2, generator=gen) * 2 - 1, torch.rand(G, 2, 2, generator=gen) * 2 - 1
        rec = rollout(agent, A, Bm, K, gen)
        loss = 0.0
        for i in range(2):
            R = rec[i]
            if variant == "payoff":
                reward = R["r"]
            else:
                reward = felt(R, R["C"].detach())
            ret = torch.flip(torch.cumsum(torch.flip(reward.detach(), [1]), 1), [1])     # rewards-to-go
            adv = ret - ret.mean(0, keepdim=True)
            loss = loss - (R["logp"] * adv).mean()
            loss = loss + td_loss(R) / (tau if variant == "motivated" else 1.0)
            if variant == "motivated":
                loss = loss - felt(R, R["C"]).sum(1).mean()                              # the critic ascends felt utility
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(agent.parameters(), 5.0)
        opt.step()
    return agent


def train_mix(policy_reward, critic_motivated, steps=3000, G=2048, K=10, seed=0, lr=3e-3):
    """Ablation: the policy's reward ("payoff" or "felt") and the critic (honest, or also ascending felt
    utility) chosen separately."""
    gen = torch.Generator().manual_seed(seed)
    torch.manual_seed(seed)
    agent = Agent()
    opt = torch.optim.Adam(agent.parameters(), lr=lr)
    for _ in range(steps):
        A, Bm = torch.rand(G, 2, 2, generator=gen) * 2 - 1, torch.rand(G, 2, 2, generator=gen) * 2 - 1
        rec = rollout(agent, A, Bm, K, gen)
        loss = 0.0
        for i in range(2):
            R = rec[i]
            reward = R["r"] if policy_reward == "payoff" else felt(R, R["C"].detach())
            ret = torch.flip(torch.cumsum(torch.flip(reward.detach(), [1]), 1), [1])
            loss = loss - (R["logp"] * (ret - ret.mean(0, keepdim=True))).mean() + td_loss(R)
            if critic_motivated:
                loss = loss - felt(R, R["C"]).sum(1).mean()
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(agent.parameters(), 5.0)
        opt.step()
    return agent
