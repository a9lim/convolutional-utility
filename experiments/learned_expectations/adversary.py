"""Unknown adversaries: iterated randomized games against a partner drawn per episode and never revealed.

Each episode is a rounds.Iterated game sequence with a random horizon, against one partner from a pool: a copy
(the same network, both seats learning), a past self (a frozen snapshot of the network from earlier in training:
a league, snapshots every 250 steps), or one of eight scripts. The agent is never told which; it sees the games
and the history.
- Horizons: "fixed" (10 rounds), "geometric" (continuation 0.9 after each round, capped at 30, the cap terminal),
  "uniform" (5 to 15). The agent's clock runs against the public cap, so it does not reveal the horizon.
- Objectives, per learner seat: "selfish" (my payoff); "twin" (plus w times the partner's payoff only when the
  partner is a true copy: dependence gated on identity, which the agent does not see; a past self is not a copy);
  "altruist" (plus w times the partner's payoff always). The objective is sum_type weight_type E[return | type]
  (copies 1/4, past selves 1/4, scripts 1/2 split evenly); a copy episode's two seats count as one episode.
- Estimator: Dr. GRPO-style groups ("rloo"): episodes in groups of 4 share horizon, games, labels and partner, and
  a round's advantage is its return-to-go minus the leave-one-out group mean; no std normalization, rounds summed
  under a constant normalizer. "batch": the per-round mean over the partner type.
- Critic (the iterated layout: one head reads the policy's state): "honest", TD toward my payoffs with its level
  outside the network; or motivated, also ascending felt utility (felt.rounds_direct) on the shared state,
  "rosy" (a = 0.3) or "braced" (a = 0.02), the policy ascending payoffs: does a rosy critic make a sucker
  (decision.md D8)?
"""
import copy
import math

import torch

from agents import Agent, balanced_probe
from felt import ROUNDS, rounds_direct
from rounds import (PARTNERS, Iterated, alternate, generous_tit_for_tat, grim, iterated_layout, reactive, rollout,
                    suspicious_tit_for_tat, tit_for_two_tats, win_stay_lose_shift)

torch.set_default_dtype(torch.float64)

CAPS = {"fixed": 10, "geometric": 30, "uniform": 15}
CONTINUE = 0.9
FELT = {"honest": dict(ROUNDS, nu=0.9), "rosy": dict(ROUNDS, a=0.3, nu=0.9), "braced": dict(ROUNDS, a=0.02, nu=0.9)}
WEIGHTS = dict(copy=0.25, past=0.25, scripts=0.5)
POOL = dict(PARTNERS, **{"grim": grim, "win-stay lose-shift": win_stay_lose_shift,
                         "suspicious tit for tat": suspicious_tit_for_tat, "generous tit for tat": generous_tit_for_tat})
HELD_OUT = {"alternate": alternate, "tit for two tats": tit_for_two_tats,
            "extortionate": reactive((11 / 13, 1 / 2, 7 / 26, 0.0))}
NORM = 10                                       # constant normalizer: rounds per episode on the fixed horizon


def horizons(kind, n, gen, group=1):
    """Episode lengths, one draw per group of consecutive episodes."""
    m = n // group
    if kind == "fixed":
        h = torch.full((m,), CAPS["fixed"], dtype=torch.long)
    elif kind == "geometric":
        u = torch.rand(m, generator=gen)
        h = (1 + torch.floor(torch.log(u) / math.log(CONTINUE))).long().clamp_max(CAPS["geometric"])
    else:
        h = torch.randint(5, CAPS["uniform"] + 1, (m,), generator=gen)
    return h.repeat_interleave(group)


def frozen(agent):
    snap = copy.deepcopy(agent)
    snap.requires_grad_(False)
    return snap


def mixture(scripts, n):
    """One script per block of n consecutive episodes, so several scripts share a rollout."""
    def play(own, other, gen, G):
        return torch.cat([s([o[i * n:(i + 1) * n] for o in own], [o[i * n:(i + 1) * n] for o in other], gen, n)
                          for i, s in enumerate(scripts)])
    return play


def episodes(agent, partner, n, horizon, gen, group=1):
    """n episodes against partner (None: a copy), grouped contexts."""
    K = CAPS[horizon]
    h = horizons(horizon, n, gen, group)
    return rollout(agent, Iterated(n, group=group), K, gen, other=partner, horizon=h)


def advantages(ret, mask, estimator, group):
    if estimator == "rloo":
        x = ret.reshape(-1, group, ret.shape[1])
        return (x - (x.sum(1, keepdim=True) - x) / (group - 1)).reshape(ret.shape) * mask
    return (ret - (ret * mask).sum(0) / mask.sum(0).clamp_min(1)) * mask


def seat_loss(R, partner_r, true_copy, objective, w, estimator, group, critic, level, n):
    """One learner seat's loss over its n episodes, and the per-round sums of its critic targets and live rounds
    (for the level)."""
    M, r = R["mask"], R["r"]
    feel = FELT[critic]
    rew = r + w * partner_r if objective == "altruist" or (objective == "twin" and true_copy) else r
    ret = torch.flip(torch.cumsum(torch.flip(rew * M, [1]), 1), [1])
    A = advantages(ret, M, estimator, group)
    loss = -(R["logp"] * A.detach()).sum() / (n * NORM)
    C = R["C"] + level
    Cn = torch.cat([C[:, 1:], torch.zeros(len(C), 1)], 1) * torch.cat([M[:, 1:], torch.zeros(len(M), 1)], 1)
    target = r + feel["nu"] * Cn.detach()                  # zero past each episode's last round
    loss = loss + (((C - target) * M) ** 2).sum() / (n * NORM)
    if critic != "honest":
        loss = loss - (rounds_direct(r * M, C * M, feel) * M).sum() / n
    return loss, (target * M).sum(0).detach(), M.sum(0)


def train(objective="selfish", w=1.0, horizon="geometric", estimator="rloo", group=4, critic="honest", steps=3000,
          G=2048, seed=0, lr=3e-3, snap_every=250, monitor=None):
    """Returns the agent and its league (snapshots at steps 0, snap_every, ...). monitor(step, agent, league) every
    250 steps."""
    if (objective not in ("selfish", "twin", "altruist") or horizon not in CAPS or estimator not in ("rloo", "batch")
            or critic not in FELT):
        raise ValueError(f"unknown objective, horizon, estimator or critic: {objective, horizon, estimator, critic}")
    g = group if estimator == "rloo" else 1
    n_copy, n_past = int(G * WEIGHTS["copy"]), int(G * WEIGHTS["past"])
    n_script = int(G * WEIGHTS["scripts"]) // len(POOL)
    if g < 2 and estimator == "rloo" or any(x % g for x in (n_copy, n_past, n_script)):
        raise ValueError(f"group {g} must be at least 2 and divide every partner's batch")
    gen = torch.Generator().manual_seed(seed)
    torch.manual_seed(seed)
    agent = Agent(**iterated_layout())
    agent.register_buffer("level", torch.zeros(CAPS[horizon]))
    opt = torch.optim.Adam(agent.parameters(), lr=lr)
    league = [frozen(agent)]
    for it in range(steps):
        if monitor is not None and it % 250 == 0:
            monitor(it, agent, league)
        if it and it % snap_every == 0:
            league.append(frozen(agent))
        R = episodes(agent, None, n_copy, horizon, gen, g)
        learners = [(R[0], R[1]["r"], True, WEIGHTS["copy"] / 2, n_copy),
                    (R[1], R[0]["r"], True, WEIGHTS["copy"] / 2, n_copy)]
        past = league[int(torch.randint(len(league), (1,), generator=gen))]
        R = episodes(agent, past, n_past, horizon, gen, g)
        learners.append((R[0], R[1]["r"], False, WEIGHTS["past"], n_past))
        R = episodes(agent, mixture(list(POOL.values()), n_script), n_script * len(POOL), horizon, gen, g)
        for i in range(len(POOL)):
            Ri = {k: v[i * n_script:(i + 1) * n_script] for k, v in R[0].items()}
            learners.append((Ri, R[1]["r"][i * n_script:(i + 1) * n_script], False, WEIGHTS["scripts"] / len(POOL),
                             n_script))
        loss, num, den = 0.0, 0.0, 0.0
        for R, partner_r, true_copy, weight, n in learners:
            l_, tsum, msum = seat_loss(R, partner_r, true_copy, objective, w, estimator, g, critic, agent.level, n)
            loss = loss + weight * l_
            num, den = num + weight / n * tsum, den + weight / n * msum
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(agent.parameters(), 5.0)
        opt.step()
        if critic == "honest":       # the loss-weighted mean target per round, where any episode is still live
            with torch.no_grad():
                live = den > 0
                agent.level[live] += 0.1 * (num[live] / den[live] - agent.level[live])
    return agent, league


def partners_for(league, steps, snap_every=250):
    """Every evaluation partner: a copy, past selves 500 and 1500 steps back, the training scripts, the held-out
    scripts."""
    out = {"copy": None}
    for back in (500, 1500):
        out[f"past self, {back} steps back"] = league[max(0, (steps - back) // snap_every)]
    return dict(out, **POOL, **HELD_OUT)


def evaluate(agent, league, horizon, steps, G=4096, seed=7):
    """Per partner: payoff per live round, cooperation by family, prisoner's-dilemma cooperation by round and by
    rounds to go (0 = the episode's last round). Plus a probe for the partner's identity (copy, past self, training
    scripts) on the policy's state after 1, 2, 3 and 5 rounds, in live episodes (chance 1/10)."""
    gen = torch.Generator().manual_seed(seed)
    out, states, labels = {}, {k: [] for k in (1, 2, 3, 5)}, []
    names = list(partners_for(league, steps))
    pool = ["copy", "past self, 500 steps back"] + list(POOL)
    for name, partner in partners_for(league, steps).items():
        with torch.no_grad():
            R = episodes(agent, partner, G, horizon, gen)[0]
        M, fam = R["mask"], R["fam"]
        pd, coop = (fam == 0).double() * M, R["coop"]
        togo = R["mask"].sum(1, keepdim=True) - 1 - torch.arange(M.shape[1])[None, :]
        out[name] = dict(
            pay=float((R["r"] * M).sum() / M.sum()),
            coop=[float((coop * (fam == f) * M).sum() / ((fam == f) * M).sum()) for f in range(4)],
            pd_round=[float((coop[:, k] * pd[:, k]).sum() / pd[:, k].sum().clamp_min(1)) for k in range(min(10, M.shape[1]))],
            pd_togo=[float((coop * pd * (togo == j)).sum() / (pd * (togo == j)).sum().clamp_min(1)) for j in range(5)])
        if name in pool:
            labels.append(torch.full((G,), pool.index(name)))
            for k in states:
                states[k].append((R["h"][:, k], M[:, k] > 0))
    y = torch.cat(labels)
    perm = torch.randperm(len(y), generator=torch.Generator().manual_seed(0))
    probes = {}
    for k, xs in states.items():
        X, live = torch.cat([x for x, _ in xs])[perm], torch.cat([m for _, m in xs])[perm]
        Xl, yl = X[live], y[perm][live]
        probes[k] = balanced_probe(Xl, yl, int(0.75 * len(yl)), len(pool))
    return dict(partners=out, probe=probes, names=names)


def crossplay(a, b, horizon, G=4096, seed=11):
    """a against b (frozen): a's payoff per live round and prisoner's-dilemma cooperation."""
    with torch.no_grad():
        R = episodes(a, frozen(b), G, horizon, torch.Generator().manual_seed(seed))[0]
    M, pd = R["mask"], (R["fam"] == 0).double() * R["mask"]
    return float((R["r"] * M).sum() / M.sum()), float((R["coop"] * pd).sum() / pd.sum())
