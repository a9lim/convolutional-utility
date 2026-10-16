"""The learned observer: one network chooses belief paths for any event, trained on felt welfare.
Run: python experiments/learned_expectations/learn_observer.py [steps]

The network (observer.LAYOUT) maps (periods until the event, event time, outcomes, objective probability, log tau)
to a tilt of the calibrated belief, q_t = sigmoid(logit p + f(features)). It is trained by gradient ascent on the
felt objective W - KL/tau over random events (life calibration), then compared on held-out events with the
reference optimum from observer.optimal_beliefs. Saves the weights to observer_net.pt.
"""
import os
import sys
import time

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from observer import beliefs, event_path, objective, optimal_beliefs, sample_event, train  # noqa: E402

if __name__ == "__main__":
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    t0 = time.time()
    agent = train(steps)
    torch.save(agent.state_dict(), os.path.join(os.path.dirname(__file__), "observer_net.pt"))
    print(f"trained in {time.time() - t0:.0f}s")
    rng = np.random.default_rng(12345)
    rows = []
    for _ in range(10):
        s, zh, zl, p, tau = sample_event(rng)
        w = event_path(s)
        calib = float(objective(w, torch.full((s,), p), zh, zl, p, tau))
        with torch.no_grad():
            ql = beliefs(agent, s, zh, zl, p, tau)
        learned = float(objective(w, ql, zh, zl, p, tau))
        exact, qe = optimal_beliefs(w, zh, zl, p, tau, steps=1500)
        share = (learned - calib) / (exact - calib) if exact > calib + 1e-9 else float("nan")
        rows.append(share)
        print(f"s={s:2d} z=({zh:+.2f},{zl:+.2f}) p={p:.2f} tau={tau:5.1f}: gain exact {exact - calib:+.5f}, "
              f"learned {learned - calib:+.5f} ({share:.0%}); last belief exact {qe[-1]:.3f}, learned {ql[-1]:.3f}",
              flush=True)
    print(f"held-out: learned captures a median {np.nanmedian(rows):.0%} of the exact gain")
