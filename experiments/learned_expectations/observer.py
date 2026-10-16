"""The observer: an agent that chooses its beliefs to maximize its own felt life-sum (core N3, canonical).

An event is announced at 0 and resolves at s with outcome z_hi (objective probability p) or z_lo. At each t < s the
self holds a subjective probability q_t of the high outcome; its felt life is felt.BeliefPath. Welfare is the
objective expected life-sum, less a cost of self-deception sum_t KL(q_t || p) / tau.

- The reference optimizer: `optimal_beliefs` (multistart Adam plus the best step path; no certificate of global
  optimality).
- The learned observer: one network maps an event's features to a tilt of the calibrated belief at each period,
  q_t = sigmoid(logit p + f(features)), trained on felt welfare across random events (`train`).
"""
import functools

import numpy as np
import torch

from agents import Agent
from felt import LIFE, BeliefPath, kl

torch.set_default_dtype(torch.float64)


def objective(path, q, zh, zl, p, tau):
    return path.run(q, zh, zl, p)[0] - kl(q, p).sum() / tau


def best_step_path(path, zh, zl, p, tau, grid=49):
    """Best path that is calibrated far out and constant over the last L periods (a grid search)."""
    best = (-np.inf, None)
    with torch.no_grad():
        for L in range(1, path.s + 1):
            for ql in np.linspace(0.02, 0.98, grid):
                q = torch.tensor([p] * (path.s - L) + [ql] * L)
                f = float(objective(path, q, zh, zl, p, tau))
                if f > best[0]:
                    best = (f, q)
    return best


def optimal_beliefs(path, zh, zl, p, tau, steps=3000, lr=0.05):
    """Optimum of W - sum_t KL(q_t || p)/tau over belief paths. The objective has kinks wherever two
    consecutive beliefs agree (a zero revision, priced at lam on one side), so beliefs are sticky and
    smooth optimizers stall; Adam with a decaying rate, started from the calibrated path, two tilted
    ones and the best step path, handles them."""
    p_logit = float(np.log(p / (1 - p)))
    step = best_step_path(path, zh, zl, p, tau)
    inits = [torch.full((path.s,), p_logit + d) for d in (0.0, -1.0, 1.0)]
    inits.append(torch.logit(step[1].clamp(1e-6, 1 - 1e-6)))
    best = step
    for th0 in inits:
        th = th0.clone().requires_grad_(True)
        opt = torch.optim.Adam([th], lr=lr)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
        for _ in range(steps):
            opt.zero_grad()
            q = torch.sigmoid(th)
            f = objective(path, q, zh, zl, p, tau)
            (-f).backward()
            opt.step()
            sched.step()
            if f.item() > best[0]:
                best = (f.item(), q.detach().clone())
    return best


# the learned observer: events at the life calibration, lead s and 10 periods after it
S_RANGE = range(8, 31)
LAYOUT = dict(trunks={"main": ("mlp", 6, (64, 64))}, heads={"tilt": dict(trunk="main")})


@functools.cache
def event_path(s):
    return BeliefPath(s + 10, s, **LIFE)


def sample_event(rng):
    s = int(rng.choice(list(S_RANGE)))
    zh = rng.uniform(-0.5, 1.5)
    zl = zh - rng.uniform(0.5, 2.0)
    p = rng.uniform(0.1, 0.9)
    tau = float(np.exp(rng.uniform(np.log(1.0), np.log(30.0))))
    return s, zh, zl, p, tau


def beliefs(agent, s, zh, zl, p, tau):
    """The belief path from (periods until the event, event time, outcomes, objective probability, log tau)."""
    lead = torch.arange(s, 0, -1, dtype=torch.float64)
    x = torch.stack([lead / 30, torch.full((s,), s / 30), torch.full((s,), zh), torch.full((s,), zl),
                     torch.full((s,), p), torch.full((s,), float(np.log(tau)))], dim=1)
    return torch.sigmoid(torch.logit(torch.tensor(p)) + agent.heads_on(x, ("tilt",))[0]["tilt"].squeeze(1))


def train(steps=2000, batch=16, seed=0):
    rng = np.random.default_rng(seed)
    torch.manual_seed(seed)
    agent = Agent(**LAYOUT)
    opt = torch.optim.Adam(agent.parameters(), lr=2e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    for it in range(steps):
        opt.zero_grad()
        loss = 0.0
        for _ in range(batch):
            s, zh, zl, p, tau = sample_event(rng)
            q = beliefs(agent, s, zh, zl, p, tau)
            calib = objective(event_path(s), torch.full((s,), p), zh, zl, p, tau).detach()
            loss = loss - (objective(event_path(s), q, zh, zl, p, tau) - calib) / batch
        loss.backward()
        opt.step()
        sched.step()
        if it % 200 == 0:
            print(f"step {it}: mean gain over calibrated {-loss.item():.5f}", flush=True)
    return agent
