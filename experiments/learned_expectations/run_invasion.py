"""Selection at the canonical model: paired invasions. Run:
python experiments/learned_expectations/run_invasion.py   (writes invasion_report.txt, invasion_runs.json; parallel)

run_evolve.py is exploratory coevolution: founders range widely and genes are linked in small populations, so its
regressions measure associations, not the local selection gradient at symmetry (Codex). Here one focal learner in
a population of residents (run_evolve's hidden-game agents and lifetime, every sign ratio at 1) carries one ratio
at e^-eps, 1 or e^eps: the news loss/gain ratio lam (X4), dread a-/a+ (X1) or rumination m-/m+ (X2). Everything
else is held: initial weights, games, pairings and sampling draws (common random numbers), so the focal's lifetime
payoff differences estimate the local selection gradient on the log ratio, (f(e^eps) - f(e^-eps)) / 2 eps, and its
curvature, (f(e^eps) + f(e^-eps) - 2 f(1)) / eps^2. Zero slope with negative curvature is stabilizing selection at 1,
not neutrality. Per variant (felt critic, felt agents) and background (a, n), whose critic is rosy or braced
(a nu against n (1 - nu)). In the felt critic, rumination has no gradient path, so its rows must be exactly zero.
"""
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from run_evolve import GENES, LIFE, P, lifetime  # noqa: E402

HERE = os.path.dirname(__file__)
EPS = float(np.log(2.0))
RATIOS = ("lam", "dread", "rumination")
VARIANTS = ("felt critic", "felt agents")
BACKGROUNDS = {"rosy (a 0.3, n 0.3)": (0.3, 0.3), "braced (a 0.02, n 0.3)": (0.02, 0.3)}
SEEDS = int(os.environ.get("SEEDS", "8"))
ARMS = [("canonical", None, 0)] + [(f"{g} {'+' if s > 0 else '-'}", g, s) for g in RATIOS for s in (-1, 1)]


def one(job):
    variant, bg, seed = job
    torch.set_num_threads(int(os.environ.get("THREADS", "2")))
    base = np.log([*BACKGROUNDS[bg], 1.0, 1.0, 1.0])
    fits = {}
    for name, gene, sign in ARMS:
        genomes = np.tile(base, (P, 1))
        if gene:
            genomes[0, GENES.index(gene)] += sign * EPS
        torch.manual_seed(1000 + seed)
        fits[name] = lifetime(genomes, variant, np.random.default_rng(1000 + seed),
                              torch.Generator().manual_seed(1000 + seed)).tolist()
    return variant, bg, seed, fits


if __name__ == "__main__":
    t0, lines = time.time(), []
    say = lambda s: (print(s, flush=True), lines.append(s))  # noqa: E731
    jobs = [(v, b, s) for v in VARIANTS for b in BACKGROUNDS for s in range(SEEDS)]
    with ProcessPoolExecutor(int(os.environ.get("PROCS", "9"))) as ex:
        out = list(ex.map(one, jobs))
    json.dump(dict(config=dict(P=P, LIFE=LIFE, EPS=EPS, BACKGROUNDS=BACKGROUNDS, SEEDS=SEEDS),
                   runs=[dict(variant=v, background=b, seed=s, fits=f) for v, b, s, f in out]),
              open(os.path.join(HERE, "invasion_runs.json"), "w"))
    say(f"Population {P}, lifetime {LIFE} steps, {SEEDS} seeds; the focal learner (member 0) carries the ratio at "
        f"e^-eps, 1, e^eps (eps = log 2), residents at 1. Lifetime payoff x1000, mean (s.e. over seeds): the focal's")
    say("slope per unit log ratio and curvature, and the residents' mean slope (spillover). Canonical focal payoff "
        "and its s.d. over seeds set the scale.")
    for v in VARIANTS:
        for b in BACKGROUNDS:
            rs = [f for v_, b_, _, f in out if v_ == v and b_ == b]
            f0 = np.array([f["canonical"][0] for f in rs]) * 1000
            say(f"[{v}, {b}] canonical focal {f0.mean():.1f} (s.d. {f0.std(ddof=1):.1f})")
            for g in RATIOS:
                fp, fm = (np.array([f[f"{g} {s}"][0] for f in rs]) * 1000 for s in "+-")
                rp, rm = (np.array([np.mean(f[f"{g} {s}"][1:]) for f in rs]) * 1000 for s in "+-")
                sl, cu, sp = (fp - fm) / (2 * EPS), (fp + fm - 2 * f0) / EPS ** 2, (rp - rm) / (2 * EPS)
                se = lambda x: x.std(ddof=1) / np.sqrt(len(x))  # noqa: E731
                say(f"    {g:10s} slope {sl.mean():+7.2f} ({se(sl):5.2f})  curvature {cu.mean():+7.2f} ({se(cu):5.2f})  "
                    f"residents' slope {sp.mean():+6.2f} ({se(sp):4.2f})  focal higher at e^eps in "
                    f"{int((fp > fm).sum())}/{len(rs)}, equal in {int((fp == fm).sum())}")
    say(f"done in {time.time() - t0:.0f}s")
    open(os.path.join(HERE, "invasion_report.txt"), "w").write("\n".join(lines) + "\n")
