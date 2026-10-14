"""Do gradient settings reproduce decision theories? Run: python experiments/learned_expectations/run_scheduling.py
Sweep: learned dates at w = 0 (with and without conditioning on reach) and w = 1 against the exact
fixed-past and commitment dates; dial: learned date against w. Writes scheduling_dial.png."""
import os
import sys
import time

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from scheduling import Schedule, learn, reference  # noqa: E402

T = 20


def draws(k, seed=11):
    rng = np.random.default_rng(seed)
    out = []
    while len(out) < k:
        a, m = rng.uniform(0.05, 1.0, 2)
        al, mu = rng.uniform(0.1, 0.85, 2)
        if a * al / (1 - al) + m * mu / (1 - mu) < 0.85:
            out.append((a, al, m, mu))
    return out


if __name__ == "__main__":
    t0 = time.time()
    rows = []
    for (a, al, m, mu) in draws(30):
        for n in (0.0, 0.3):
            sch = Schedule(T, a, al, m, mu, n, 0.7)
            cdt, commit, W = reference(sch)
            mode = lambda P: int(torch.argmax(P))
            r = dict(n=n, cdt=cdt, commit=commit,
                     w0=mode(learn(sch, 0.0)), w0u=mode(learn(sch, 0.0, conditional=False)), w1=mode(learn(sch, 1.0)))
            rows.append(r)
            print(r, flush=True)
    for n in (0.0, 0.3):
        R_ = [r for r in rows if r["n"] == n]
        print(f"n = {n}: {len(R_)} draws (fixed-past date differs from commitment in "
              f"{np.mean([r['cdt'] != r['commit'] for r in R_]):.0%}). Learned w = 0 matches the fixed-past date "
              f"{np.mean([r['w0'] == r['cdt'] for r in R_]):.0%} (unconditional gradients "
              f"{np.mean([r['w0u'] == r['cdt'] for r in R_]):.0%}); w = 1 matches commitment "
              f"{np.mean([r['w1'] == r['commit'] for r in R_]):.0%}")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    ws = np.linspace(0, 1, 21)
    for ax, (prm, n) in zip(axes, [((0.6478, 0.4727, 0.5384, 0.2856), 0.0), ((0.6478, 0.4727, 0.5384, 0.2856), 0.3)]):
        sch = Schedule(T, *prm, n, 0.7)
        cdt, commit, W = reference(sch)
        dates = [int(torch.argmax(learn(sch, w))) for w in ws]
        print(f"dial (n = {n}): " + " ".join(f"{w:.2f}:{d}" for w, d in zip(ws, dates)), flush=True)
        ax.plot(ws, dates, "o-", color="#3182bd", label="learned date")
        ax.axhline(cdt, color="#c0392b", ls="--", label=f"fixed-past (CDT) date {cdt}")
        ax.axhline(commit, color="#2a9d4b", ls="--", label=f"commitment date {commit}")
        ax.set_xlabel("w: share of the gradient through past selves' forecasts")
        ax.set_ylabel("date the pleasure is taken")
        ax.set_title(f"news strength n = {n}", fontsize=10)
        ax.legend(fontsize=8, frameon=False)
    fig.suptitle("Scheduling one pleasure: the J dial as a gradient setting", fontsize=11)
    fig.tight_layout()
    out = os.path.join(os.path.dirname(__file__), "scheduling_dial.png")
    fig.savefig(out, dpi=130)
    print(f"saved {out} ({time.time() - t0:.0f}s)")
