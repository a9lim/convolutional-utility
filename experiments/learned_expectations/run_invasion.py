"""Selection at the canonical model: paired invasions. Run:
python experiments/learned_expectations/run_invasion.py   (writes invasion_report.txt, invasion_runs.json; parallel)

run_evolve.py is exploratory coevolution: founders range widely and genes are linked in small populations, so its
regressions measure associations, not the local selection gradient at symmetry (Codex). Here one focal learner in
a population of residents (run_evolve's hidden-game agents and lifetime, every sign ratio at 1, no felt reference)
carries one gene at e^-eps, 1 or e^eps: the news loss/gain ratio lam (X4), dread a-/a+ (X1), rumination m-/m+ (X2),
or adaptation, as 1 + h with h the felt reference's strength (rounds.py `adapt`; 1 / (1 + h) is the interior life
weight, so e^-eps is sensitization, h = -1/2). Everything else is held: initial weights, games, pairings and
sampling draws (common random numbers), so the focal's lifetime payoff differences estimate the local selection
gradient on the log gene, (f(e^eps) - f(e^-eps)) / 2 eps, and its curvature, (f(e^eps) + f(e^-eps) - 2 f(1)) / eps^2.
Zero slope with negative curvature is stabilizing selection at 1, not neutrality. Per variant (felt critic, felt
agents) and background (a, n), whose critic is rosy or braced (a nu against n (1 - nu)). In the felt critic,
rumination has no gradient path, so its rows must be exactly zero.

The level reading. The critic's level reaches the policy through the state they share (D8), and the motivated
critic's push is a per-round TD offset profile at the canonical model, so adaptation is a pure level intervention
(exactly an offset profile). Dread and lam make the push depend on the history (the sign of a forecast, of a TD
error); their mean-field arms keep each round's batch-mean push and drop that dependence. If a sign ratio acts
only through the per-round level of the critic's forcing, its mean-field arm matches it. The mean field removes the
covariance between each episode's push and the critic's parameter gradient, not the history dependence of the
critic's response; with felt agents the actor's felt rewards keep the gene in both arms; and where every episode
gets the same push (dread, whose forecasts rarely change sign) the arms coincide by construction, so the focal's
push spread is logged. Every arm's focal critic level is measured (forecast minus realized payoff-to-go, rounds
2-10, lifetime mean). eps = log 2 gives factor-of-two contrasts, not derivatives.
"""
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from felt import ROUNDS  # noqa: E402
from run_evolve import GENES, LIFE, P, lifetime, unpack  # noqa: E402

HERE = os.path.dirname(__file__)
EPS = float(np.log(2.0))
RATIOS = ("lam", "dread", "rumination", "adaptation")
MEANFIELD = ("lam", "dread")
VARIANTS = ("felt critic", "felt agents")
BACKGROUNDS = {"rosy (a 0.3, n 0.3)": (0.3, 0.3), "braced (a 0.02, n 0.3)": (0.02, 0.3)}
SEEDS = int(os.environ.get("SEEDS", "8"))
ARMS = ([("canonical", None, 0)] + [(f"{g} {'+' if s > 0 else '-'}", g, s) for g in RATIOS for s in (-1, 1)]
        + [(f"{g} {'+' if s > 0 else '-'}, mean field", g, s) for g in MEANFIELD for s in (-1, 1)])


def one(job):
    variant, bg, seed = job
    torch.set_num_threads(int(os.environ.get("THREADS", "2")))
    base = np.log([*BACKGROUNDS[bg], 1.0, 1.0, 1.0])
    fits, levels, spreads = {}, {}, {}
    for name, gene, sign in ARMS:
        genomes = np.tile(base, (P, 1))
        if gene in GENES:
            genomes[0, GENES.index(gene)] += sign * EPS
        feels = [dict(ROUNDS, **unpack(g)) for g in genomes]
        if gene == "adaptation":
            feels[0]["h"] = float(np.exp(sign * EPS)) - 1.0
        feels[0]["probe"] = True
        if name.endswith("mean field"):
            feels[0]["meanfield"] = True
        torch.manual_seed(1000 + seed)
        fit, lev, spread = lifetime(feels, variant, np.random.default_rng(1000 + seed),
                                    torch.Generator().manual_seed(1000 + seed))
        fits[name], levels[name], spreads[name] = fit.tolist(), lev.tolist(), float(spread[0])
    return variant, bg, seed, fits, levels, spreads


if __name__ == "__main__":
    t0, lines = time.time(), []
    say = lambda s: (print(s, flush=True), lines.append(s))  # noqa: E731
    se = lambda x: x.std(ddof=1) / np.sqrt(len(x))  # noqa: E731
    jobs = [(v, b, s) for v in VARIANTS for b in BACKGROUNDS for s in range(SEEDS)]
    with ProcessPoolExecutor(int(os.environ.get("PROCS", "9"))) as ex:
        out = list(ex.map(one, jobs))
    json.dump(dict(config=dict(P=P, LIFE=LIFE, EPS=EPS, BACKGROUNDS=BACKGROUNDS, SEEDS=SEEDS),
                   runs=[dict(variant=v, background=b, seed=s, fits=f, levels=lv, spread=sp) for v, b, s, f, lv, sp in out]),
              open(os.path.join(HERE, "invasion_runs.json"), "w"))
    say(f"Population {P}, lifetime {LIFE} steps, {SEEDS} seeds; the focal learner (member 0) carries the gene at "
        f"e^-eps, 1, e^eps (eps = log 2), residents at 1. Lifetime payoff x1000, mean (s.e. over seeds): the focal's")
    say("slope per unit log gene and curvature, and the residents' mean slope (spillover). Adaptation's gene is 1 + h.")
    say("Canonical focal payoff and its s.d. over seeds set the scale.")
    for v in VARIANTS:
        for b in BACKGROUNDS:
            rs = [(f, lv) for v_, b_, _, f, lv, _ in out if v_ == v and b_ == b]
            sps = [sp for v_, b_, _, _, _, sp in out if v_ == v and b_ == b]
            f0 = np.array([f["canonical"][0] for f, _ in rs]) * 1000
            l0 = np.array([lv["canonical"][0] for _, lv in rs])
            say(f"[{v}, {b}] canonical focal {f0.mean():.1f} (s.d. {f0.std(ddof=1):.1f}), critic level {l0.mean():+.2f}")
            for g in RATIOS:
                fp, fm = (np.array([f[f"{g} {s}"][0] for f, _ in rs]) * 1000 for s in "+-")
                rp, rm = (np.array([np.mean(f[f"{g} {s}"][1:]) for f, _ in rs]) * 1000 for s in "+-")
                sl, cu, sp = (fp - fm) / (2 * EPS), (fp + fm - 2 * f0) / EPS ** 2, (rp - rm) / (2 * EPS)
                say(f"    {g:10s} slope {sl.mean():+7.2f} ({se(sl):5.2f})  curvature {cu.mean():+7.2f} ({se(cu):5.2f})  "
                    f"residents' slope {sp.mean():+6.2f} ({se(sp):4.2f})  focal higher at e^eps in "
                    f"{int((fp > fm).sum())}/{len(rs)}, equal in {int((fp == fm).sum())}")
            arms = [a for a, _, _ in ARMS if a != "canonical"]
            dl = {a: np.array([lv[a][0] for _, lv in rs]) - l0 for a in arms}
            dp = {a: np.array([f[a][0] for f, _ in rs]) * 1000 - f0 for a in arms}
            say("    by arm, against the canonical focal: critic level and payoff; and the within-round spread of the felt")
            say("    push on the focal's critic (s.d. over episodes / |mean|; 0 when every episode gets the same push):")
            for a in arms:
                say(f"      {a:24s} level {dl[a].mean():+6.2f} ({se(dl[a]):4.2f})  payoff {dp[a].mean():+7.2f} ({se(dp[a]):5.2f})"
                    f"  push spread {np.mean([sp[a] for sp in sps]):.3f}")
            for g in MEANFIELD:
                for s_ in "+-":
                    d = dp[f"{g} {s_}"] - dp[f"{g} {s_}, mean field"]
                    say(f"    {g} {s_} against its mean field: payoff gap {d.mean():+7.2f} ({se(d):5.2f}), "
                        f"level gap {(dl[f'{g} {s_}'] - dl[f'{g} {s_}, mean field']).mean():+.2f}")
            h1 = dp["adaptation +"]
            say(f"    adaptation h = 1 against none (one-sided): payoff {h1.mean():+7.2f} ({se(h1):5.2f}), "
                f"higher in {int((h1 > 0).sum())}/{len(h1)}")
    say(f"done in {time.time() - t0:.0f}s")
    open(os.path.join(HERE, "invasion_report.txt"), "w").write("\n".join(lines) + "\n")
