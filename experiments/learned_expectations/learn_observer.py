"""The learned observer: one network chooses belief paths for any event, trained on felt welfare.
Run: python experiments/learned_expectations/learn_observer.py [steps]

The network maps (periods until the event, event time, outcomes, objective probability, log tau) to a
tilt of the calibrated belief, q_t = sigmoid(logit p + f(features)). It is trained by gradient ascent on
the felt objective W - KL/tau over random events (life calibration), then compared on held-out events with
the exact optimum from observer.optimal_beliefs.
"""
import os
import sys
import time

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from observer import World, kl, objective, optimal_beliefs  # noqa: E402
from run_observer import LIFE  # noqa: E402

S_RANGE = range(8, 31)
WORLDS = {s: World(s + 10, s, LIFE["a"], LIFE["al"], LIFE["m"], LIFE["mu"], LIFE["n"], LIFE["nu"], LIFE["lam"])
          for s in S_RANGE}


def sample_event(rng):
    s = int(rng.choice(list(S_RANGE)))
    zh = rng.uniform(-0.5, 1.5)
    zl = zh - rng.uniform(0.5, 2.0)
    p = rng.uniform(0.1, 0.9)
    tau = float(np.exp(rng.uniform(np.log(1.0), np.log(30.0))))
    return s, zh, zl, p, tau


class Net(torch.nn.Module):
    def __init__(self, width=64):
        super().__init__()
        self.f = torch.nn.Sequential(torch.nn.Linear(6, width), torch.nn.Tanh(), torch.nn.Linear(width, width),
                                     torch.nn.Tanh(), torch.nn.Linear(width, 1))

    def forward(self, s, zh, zl, p, tau):
        lead = torch.arange(s, 0, -1, dtype=torch.float64)
        x = torch.stack([lead / 30, torch.full((s,), s / 30), torch.full((s,), zh), torch.full((s,), zl),
                         torch.full((s,), p), torch.full((s,), float(np.log(tau)))], dim=1)
        return torch.sigmoid(torch.logit(torch.tensor(p)) + self.f(x).squeeze(1))


def train(steps=2000, batch=16, seed=0):
    rng = np.random.default_rng(seed)
    torch.manual_seed(seed)
    net = Net()
    opt = torch.optim.Adam(net.parameters(), lr=2e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    for it in range(steps):
        opt.zero_grad()
        loss = 0.0
        for _ in range(batch):
            s, zh, zl, p, tau = sample_event(rng)
            q = net(s, zh, zl, p, tau)
            calib = objective(WORLDS[s], torch.full((s,), p), zh, zl, p, tau).detach()
            loss = loss - (objective(WORLDS[s], q, zh, zl, p, tau) - calib) / batch
        loss.backward()
        opt.step()
        sched.step()
        if it % 200 == 0:
            print(f"step {it}: mean gain over calibrated {-loss.item():.5f}", flush=True)
    return net


if __name__ == "__main__":
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    t0 = time.time()
    net = train(steps)
    torch.save(net.state_dict(), os.path.join(os.path.dirname(__file__), "observer_net.pt"))
    print(f"trained in {time.time() - t0:.0f}s")
    rng = np.random.default_rng(12345)
    rows = []
    for _ in range(10):
        s, zh, zl, p, tau = sample_event(rng)
        w = WORLDS[s]
        calib = float(objective(w, torch.full((s,), p), zh, zl, p, tau))
        with torch.no_grad():
            ql = net(s, zh, zl, p, tau)
        learned = float(objective(w, ql, zh, zl, p, tau))
        exact, qe = optimal_beliefs(w, zh, zl, p, tau, steps=1500)
        share = (learned - calib) / (exact - calib) if exact > calib + 1e-9 else float("nan")
        rows.append(share)
        print(f"s={s:2d} z=({zh:+.2f},{zl:+.2f}) p={p:.2f} tau={tau:5.1f}: gain exact {exact - calib:+.5f}, "
              f"learned {learned - calib:+.5f} ({share:.0%}); last belief exact {qe[-1]:.3f}, learned {ql[-1]:.3f}",
              flush=True)
    print(f"held-out: learned captures a median {np.nanmedian(rows):.0%} of the exact gain")
