"""Fit momentary affect in Forbes & Bennett (2024). Run:
python experiments/happiness/run_forbes.py   (writes forbes_report.txt; needs data/forbes, see README.md)

Per experiment: Rutledge's geometric kernel against the recursive model's jump kernel (5-fold cross-validation
over people, fixed effect per block); news by sign with a bootstrap over people; RPE by free and forced choice
(experiment 1) and the unchosen option's outcome (experiment 2); then each person's own kernel."""
import os
import sys
import time

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import forbes  # noqa: E402
from gbe import fit  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def best_kernel(F, z, mask, jump):
    def rss(p):
        gam = float(np.clip(p[0], 0.0, 0.999))
        kap = float(np.clip(p[1], 0.0, 2.0)) if jump else gam
        return fit(forbes.design(F, gam, kap), z, mask)[1]
    grid = [(g, k) for g in np.arange(0.1, 1.0, 0.1) for k in (np.arange(0.0, 1.01, 0.1) if jump else [g])]
    p0 = min(grid, key=rss)
    p = minimize(rss, p0 if jump else [p0[0]], method="Nelder-Mead", options=dict(xatol=1e-3, fatol=1e-8)).x
    gam = float(np.clip(p[0], 0.0, 0.999))
    return gam, float(np.clip(p[1], 0.0, 2.0)) if jump else gam


def cv_mse(F, z, mask, person, jump, folds=5, seed=0):
    people = np.unique(person)
    fold = dict(zip(np.random.default_rng(seed).permutation(people), np.arange(len(people)) % folds))
    f_of = np.array([fold[p] for p in person])
    sse = n = 0.0
    for f in range(folds):
        tr = f_of != f
        gam, kap = best_kernel(F[tr], z[tr], mask[tr], jump)
        w = fit(forbes.design(F[tr], gam, kap), z[tr], mask[tr])[0]
        _, _, m, X, y = fit(forbes.design(F[~tr], gam, kap), z[~tr], mask[~tr])
        sse += float(((y - X @ w) ** 2).sum())
        n += m
    return sse / n


if __name__ == "__main__":
    t0, lines = time.time(), []
    say = lambda s: (print(s, flush=True), lines.append(s))
    rng = np.random.default_rng(0)
    for exp in ("exp1", "exp2"):
        D = forbes.load(exp)
        z, mask = forbes.ratings(D)
        person = D["person"]
        people = np.unique(person)
        say(f"[{exp}] {len(people)} people, {len(person)} blocks, {int(mask.sum())} ratings (valence z-scored within person)")
        F, names = forbes.features(D, "sign")
        res = {}
        for jump in (False, True):
            gam, kap = best_kernel(F, z, mask, jump)
            w = fit(forbes.design(F, gam, kap), z, mask)[0]
            res[jump] = (gam, kap, w, cv_mse(F, z, mask, person, jump))
            say(f"    {'jump kernel' if jump else 'geometric (Rutledge)'}: gamma {gam:.3f} kappa {kap:.3f}; cross-validated "
                f"MSE {res[jump][3]:.4f}; " + ", ".join(f"{a} {b:+.3f}" for a, b in zip(names, w)))
        say(f"    jump against geometric: {100 * (res[True][3] / res[False][3] - 1):+.2f}% cross-validated MSE")
        gam, kap, w, _ = res[True]
        groups = {p: np.flatnonzero(person == p) for p in people}
        B = []
        for b in range(int(os.environ.get("BOOT", "100"))):
            pick = np.concatenate([groups[p] for p in rng.choice(people, len(people))])
            wb = fit(forbes.design(F[pick], gam, kap), z[pick], mask[pick])[0]
            B.append([wb[3] / wb[2], wb[3] - wb[2], wb[1] / wb[0]])
        B = np.array(B)
        q = lambda c: f"[{np.quantile(B[:, c], .025):.2f}, {np.quantile(B[:, c], .975):.2f}]"
        say(f"    news by sign (jump kernel held): RPE+ {w[2]:+.3f}, RPE- {w[3]:+.3f}, RPE- minus RPE+ "
            f"{w[3] - w[2]:+.3f} {q(1)}; paid-/paid+ {w[1] / w[0]:.2f} {q(2)} (bootstrap over people)")
        extra = "choice" if exp == "exp1" else "counterfactual"
        Fx, nx = forbes.features(D, extra)
        gx, kx = best_kernel(Fx, z, mask, True)
        wx = fit(forbes.design(Fx, gx, kx), z, mask)[0]
        say(f"    by {extra}: " + ", ".join(f"{a} {b:+.3f}" for a, b in zip(nx, wx)))
        # each person's own kernel: weights per person too, block fixed effects; grid over (gamma, kappa)
        grid = [(g, k) for g in np.arange(0.0, 0.96, 0.05) for k in np.arange(0.0, 1.01, 0.05)]
        own = []
        for p in people:
            i = groups[p]
            best = min(grid, key=lambda gk: fit(forbes.design(F[i], *gk), z[i], mask[i])[1])
            own.append(best)
        own = np.array(own)
        jumpy = np.mean(own[:, 1] < own[:, 0] - 0.05)
        say(f"    own kernels: median gamma {np.median(own[:, 0]):.2f}, kappa {np.median(own[:, 1]):.2f}; "
            f"kappa below gamma (by > 0.05) in {jumpy:.0%} of people, above in {np.mean(own[:, 1] > own[:, 0] + 0.05):.0%}")
    say(f"done in {time.time() - t0:.0f}s")
    open(os.path.join(HERE, "forbes_report.txt"), "w").write("\n".join(lines) + "\n")
