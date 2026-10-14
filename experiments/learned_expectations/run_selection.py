"""Which credible plan does learning select under loss-averse news? Run:
python experiments/learned_expectations/run_selection.py   (writes selection_report.txt)
For random echo parameters with n = 0.3, lam = 2: the credible set C_1 and commitment date (exact), and the
dates learned at w = 0 (fixed-past) and w = 1 (planner) from several initial policies."""
import os
import sys
import time

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from run_scheduling import T, draws  # noqa: E402
from scheduling import Schedule, learn, reference  # noqa: E402

if __name__ == "__main__":
    t0, lines = time.time(), []
    say = lambda s: (print(s, flush=True), lines.append(s))
    rows = []
    for prm in draws(16, seed=23):
        try:
            sch = Schedule(T, *prm, 0.3, 0.7, lam=2.0)
        except ValueError:
            continue
        cdt, commit, W = reference(sch)
        C = sch.C1
        w0 = [int(torch.argmax(learn(sch, 0.0, seed=s))) for s in range(5)]
        w1 = [int(torch.argmax(learn(sch, 1.0, seed=s))) for s in range(3)]
        rows.append((C, commit, cdt, w0, w1, W))
        say(f"C_1 {C}, commitment {commit}, preferred credible {cdt} | learned w = 0: {w0} | w = 1: {w1}")
    w0_in = np.mean([d in C or d == 0 for C, _, _, w0, _, _ in rows for d in w0])
    w0_pref = np.mean([d == cdt for C, _, cdt, w0, _, _ in rows for d in w0])
    multi = [r for r in rows if len(r[0]) > 1]
    w0_spread = np.mean([len(set(w0)) > 1 for _, _, _, w0, _, _ in multi]) if multi else float("nan")
    w1_commit = np.mean([d == commit for _, commit, _, _, w1, _ in rows for d in w1])
    w1_loss = np.median([1 - W[d] / W[commit] for _, commit, _, _, w1, W in rows for d in w1])
    say(f"{len(rows)} draws, {len(multi)} with several credible plans. w = 0: learned date credible {w0_in:.0%}, "
        f"the preferred credible plan {w0_pref:.0%}; seeds disagree in {w0_spread:.0%} of multi-plan draws. "
        f"w = 1: reaches the commitment date {w1_commit:.0%} (median welfare shortfall {w1_loss:.1%}).")
    say(f"done in {time.time() - t0:.0f}s")
    open(os.path.join(os.path.dirname(__file__), "selection_report.txt"), "w").write("\n".join(lines) + "\n")
