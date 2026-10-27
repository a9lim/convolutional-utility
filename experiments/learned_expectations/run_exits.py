"""Does a learner learn to exit? Sketched 2026-10-27, not yet run. Run:
python experiments/learned_expectations/run_exits.py   (writes exits_report.txt; configurations in parallel,
PROCS processes; tabular and CPU-only, an estimated hour on 8 processes at the default sizes, not yet timed)

A good life (u = 1, T = 30) with a one-period patch at level x after t0 = 12, the life calibration, at
lam = 1 and 2, without and with biphasic memory (h = 0.5, a short adaptation time g = 0.85 to fit T). For each
configuration the exact plan equilibria (never exit; exits near the patch) and the momentary self's preferred one
(death.md 17b), then the learned last-moment distributions: momentary learners from three starts (naive: expects to
continue; uniform: scheduling.learn's start, death uniform over the remaining dates; primed: a weakly held plan to
exit just before the patch), the remaining-life learner and the planner from the uniform start.

Predictions, written before any run:
1. lam = 1: one outcome per x, whatever the start: exit below the band's edge, never above it.
2. lam = 2, inside the band: the naive start stays with never exiting; the uniform and primed starts land on the
   exit. The second half is D3's earliest-credible-plan pattern carried to exit (uncertainty about one's own
   timing is felt as loss-averse news, so resolving it early pays), untested here.
3. The remaining-life learner and the planner never exit a life that is good on the whole.
4. With biphasic memory the edges move up, so patches at positive base levels sit in or below the band.
"""
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from exits import Exits, equilibria, learn  # noqa: E402
from felt import LIFE  # noqa: E402

T, T0 = 30, 12
PRM = {k: v for k, v in LIFE.items() if k != "lam"}
NEAR = range(T0 - 2, T0 + 3)                       # candidate exit dates around the patch
STARTS = ("naive", "uniform", "primed")
SEEDS = range(3)


def life(x):
    u = np.ones(T)
    u[T0 + 1] = x
    return u


def edges(lam, h, lo=-12.0, hi=1.0, steps=24):
    """The band at (lam, h): x_lo, the lowest x with never exiting an equilibrium, and x_hi, the highest with an
    exit near the patch one, searched above x_lo as in death.py 17a."""
    def never(x):
        return T - 1 in equilibria(Exits(life(x), **PRM, lam=lam, h=h, g=0.85), NEAR)

    def exit_eq(x):
        return any(t != T - 1 for t in equilibria(Exits(life(x), **PRM, lam=lam, h=h, g=0.85), NEAR))

    a, b = lo, hi
    for _ in range(steps):
        mid = (a + b) / 2
        a, b = (a, mid) if never(mid) else (mid, b)
    x_lo = b
    a, b = x_lo, hi
    for _ in range(steps):
        mid = (a + b) / 2
        a, b = (mid, b) if exit_eq(mid) else (a, mid)
    return x_lo, a


def one(cfg):
    torch.set_num_threads(1)
    lam, h, x = cfg
    ex = Exits(life(x), **PRM, lam=lam, h=h, g=0.85)
    eqs = equilibria(ex, NEAR)
    pref = max(eqs, key=lambda tau: float(eqs[tau][0])) if eqs else None     # the self at birth's pick
    out = dict(lam=lam, h=h, x=x, eqs=sorted(eqs), preferred=pref)
    for start in STARTS:
        out[f"momentary/{start}"] = [learn(ex, "momentary", start, T0, seed=s).numpy() for s in SEEDS]
    for kind in ("remaining", "planner"):
        out[kind] = [learn(ex, kind, "uniform", seed=s).numpy() for s in SEEDS]
    return out


def summary(P):
    """Probability of dying at or before the patch's end, and the modal last moment."""
    return float(P[:T0 + 2].sum()), int(np.argmax(P))


if __name__ == "__main__":
    t0, lines = time.time(), []
    say = lambda s: (print(s, flush=True), lines.append(s))
    bands = {(lam, h): edges(lam, h) for lam in (1.0, 2.0) for h in (0.0, 0.5)}
    for (lam, h), (lo_, hi_) in bands.items():
        say(f"lam {lam:g}, h {h}: never exiting an equilibrium from x = {lo_:+.3f}; exits near the patch up to {hi_:+.3f}")
    cfgs = []
    for (lam, h), (lo_, hi_) in bands.items():
        mid = (lo_ + hi_) / 2 if hi_ > lo_ else lo_
        cfgs += [(lam, h, round(x, 3)) for x in (lo_ - 1.0, mid, max(lo_, hi_) + 0.5)]
    with ProcessPoolExecutor(int(os.environ.get("PROCS", "8"))) as ex_:
        rows = list(ex_.map(one, cfgs))
    for r in rows:
        head = f"lam {r['lam']:g}, h {r['h']}, x {r['x']:+.3f}: equilibria {r['eqs']}, preferred {r['preferred']}"
        body = "; ".join(f"{k} " + ", ".join(f"{summary(P)[0]:.2f}@{summary(P)[1]}" for P in v)
                         for k, v in r.items() if "/" in k or k in ("remaining", "planner"))
        say(head + " | P(dead by the patch's end)@modal last moment: " + body)
    say(f"done in {time.time() - t0:.0f}s")
    open(os.path.join(os.path.dirname(__file__), "exits_report.txt"), "w").write("\n".join(lines) + "\n")
