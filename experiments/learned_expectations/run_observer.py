"""Exact optimal belief paths for the observer. Run: python experiments/learned_expectations/run_observer.py
Writes observer_paths.png and prints a table."""
import os
import sys
import time

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from felt import BeliefPath, kl  # noqa: E402
from observer import FEEL, optimal_beliefs  # noqa: E402

T, S = 40, 30
EVENTS = {"risky event ±1, p = 0.5": (1.0, -1.0, 0.5),
          "likely good: +1 or 0, p = 0.8": (1.0, 0.0, 0.8),
          "likely bad: 0 or −1, p = 0.2": (0.0, -1.0, 0.2)}
TAUS = (1.0, 3.0, 10.0, 30.0)

if __name__ == "__main__":
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "observer_paths.png")
    fig, axes = plt.subplots(1, len(EVENTS), figsize=(14, 4.2), sharey=False)
    t0 = time.time()
    for ax, (name, (zh, zl, p)) in zip(axes, EVENTS.items()):
        w = BeliefPath(T, S, **FEEL)
        W0 = float(w.run(torch.full((S,), p), zh, zl, p)[0])
        lead = S - np.arange(S)
        for tau, col in zip(TAUS, ("#9ecae1", "#6baed6", "#3182bd", "#08519c")):
            val, q = optimal_beliefs(w, zh, zl, p, tau)
            W = float(w.run(q, zh, zl, p)[0])
            print(f"{name}, tau = {tau:4.0f}: q at lead 30/10/5/1 = {q[0]:.3f}/{q[20]:.3f}/{q[25]:.3f}/{q[-1]:.3f}; "
                  f"felt welfare {W - W0:+.4f}, deception cost {float(kl(q, p).sum()) / tau:.4f}")
            ax.plot(lead, q.numpy(), color=col, lw=2, label=f"τ = {tau:g}")
        ax.axhline(p, color="#999", lw=1, ls="--", label="calibrated")
        ax.invert_xaxis()
        ax.set_xlabel("periods until the event")
        ax.set_title(name, fontsize=10)
    axes[0].set_ylabel("belief in the high outcome")
    axes[0].legend(fontsize=8, frameon=False)
    fig.suptitle("Optimal felt beliefs under a cost of self-deception KL/τ (life calibration, weekly periods)",
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"saved {out} ({time.time() - t0:.0f}s)")
