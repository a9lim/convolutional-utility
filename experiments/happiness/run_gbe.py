"""Fit momentary happiness in the Great Brain Experiment data. Run:
python experiments/happiness/run_gbe.py   (writes gbe_report.txt, gbe.png; needs data/gbe, see README.md)

Models, fitted on 80% of participants and scored on the rest (play fixed effects refitted, weights held):
- Rutledge 2014: CR, EV and RPE through one geometric kernel gamma^lag;
- jump kernel: the recursive model's resolvent shape, (1, kappa, kappa gamma, ...);
- each with the RPE split by sign;
- the jump kernel fitted separately for CR, EV and RPE: does news echo like the rest of felt utility?
Bootstrap over participants for the kernel and the recursive parameters (mu = gamma - kappa, m = kappa/mu).
Not identified, so not fitted: RPE asymmetry within gain-only or loss-only trials, where a gamble's EV equals
the size of its RPE (EV = RPE+ - RPE- on gain trials), so the split there is a choice of basis."""
import os
import sys
import time

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gbe  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def best_kernel(F, z, mask, jump):
    """(gamma, kappa) minimizing the within-play residual sum of squares; kappa = gamma if not jump."""
    def rss(p):
        gam = float(np.clip(p[0], 0.0, 0.999))
        kap = float(np.clip(p[1], 0.0, 2.0)) if jump else gam
        return gbe.fit(gbe.filtered(F, gam, kap), z, mask)[1]
    grid = [(g, k) for g in np.arange(0.1, 1.0, 0.1) for k in (np.arange(0.0, 1.01, 0.1) if jump else [g])]
    p0 = min(grid, key=rss)
    p = minimize(rss, p0 if jump else [p0[0]], method="Nelder-Mead",
                 options=dict(xatol=1e-3, fatol=1e-6)).x
    gam = float(np.clip(p[0], 0.0, 0.999))
    return gam, float(np.clip(p[1], 0.0, 2.0)) if jump else gam


def test_mse(F, z, mask, gam, kap, w):
    _, _, _, X, y = gbe.fit(gbe.filtered(F, gam, kap), z, mask)
    r = y - X @ w
    return float(r @ r) / len(y), r


if __name__ == "__main__":
    t0, lines = time.time(), []
    say = lambda s: (print(s, flush=True), lines.append(s))
    D = gbe.load()
    z, mask = gbe.ratings(D, np.ones(len(D["subj"]), bool))
    rng = np.random.default_rng(0)
    subjects = np.unique(D["subj"])
    test = np.isin(D["subj"], rng.choice(subjects, len(subjects) // 5, replace=False))
    say(f"{len(D['subj'])} plays, {len(subjects)} participants, {int(mask.sum())} ratings (z-scored within "
        f"participant); test set {int(test.sum())} plays of a fifth of participants.")
    models = [("Rutledge 2014", "none", False), ("jump kernel", "none", True),
              ("Rutledge, RPE by sign", "rpe", False), ("jump, RPE by sign", "rpe", True)]
    fits = {}
    for name, split, jump in models:
        F, names = gbe.features(D, split)
        gam, kap = best_kernel(F[~test], z[~test], mask[~test], jump)
        w, rss, n, _, _ = gbe.fit(gbe.filtered(F[~test], gam, kap), z[~test], mask[~test])
        mse, r = test_mse(F[test], z[test], mask[test], gam, kap, w)
        fits[name] = dict(gam=gam, kap=kap, w=w, names=names, mse=mse, r=r, F=F)
        say(f"[{name}] gamma {gam:.3f} kappa {kap:.3f}; test MSE {mse:.4f}; "
            + ", ".join(f"{a} {b:+.3f}" for a, b in zip(names, w)) + f"  ({time.time() - t0:.0f}s)")
    base = fits["Rutledge 2014"]["r"]
    for name in list(fits)[1:]:
        say(f"    {name}: test MSE {100 * (fits[name]['mse'] / fits['Rutledge 2014']['mse'] - 1):+.2f}% against Rutledge 2014")
    # bootstrap over training participants: the jump kernel with RPE by sign
    F = fits["jump, RPE by sign"]["F"]
    tr_subj = np.unique(D["subj"][~test])
    order = np.argsort(D["subj"], kind="stable")
    groups = np.split(order, np.flatnonzero(np.diff(D["subj"][order])) + 1)
    play_idx = {int(D["subj"][g[0]]): g for g in groups}
    boots = []
    for b in range(int(os.environ.get("BOOT", "20"))):
        pick = np.concatenate([play_idx[s] for s in rng.choice(tr_subj, len(tr_subj))])
        gam, kap = best_kernel(F[pick], z[pick], mask[pick], True)
        w = gbe.fit(gbe.filtered(F[pick], gam, kap), z[pick], mask[pick])[0]
        boots.append([gam, kap, gam - kap, kap / (gam - kap), w[3] / w[2], w[1] / w[0]])
    B = np.array(boots)
    ci = lambda c: f"[{np.quantile(B[:, c], .025):.3f}, {np.quantile(B[:, c], .975):.3f}]"
    j = fits["jump, RPE by sign"]
    say(f"Jump kernel, RPE by sign, bootstrap 95% intervals ({len(B)} resamples of participants): "
        f"gamma {j['gam']:.3f} {ci(0)}, kappa {j['kap']:.3f} {ci(1)}; recursive reading mu = gamma - kappa "
        f"{j['gam'] - j['kap']:.3f} {ci(2)}, m = kappa/mu {j['kap'] / (j['gam'] - j['kap']):.2f} {ci(3)}; "
        f"RPE-/RPE+ {j['w'][3] / j['w'][2]:.2f} {ci(4)}; EV/CR {j['w'][1] / j['w'][0]:.2f} {ci(5)}")
    # per-component jump kernels (CR, EV, RPE), coordinate descent from the shared fit
    F, names = gbe.features(D, "none")
    j0 = fits["jump kernel"]
    par = np.array([[j0["gam"], j0["kap"]]] * 3)

    def comp_rss(par, F, z, mask):
        Ff = np.stack([gbe.filtered(F[..., c:c + 1], *par[c])[..., 0] for c in range(3)], -1)
        return gbe.fit(Ff, z, mask)

    for sweep in range(3):
        for c in range(3):
            def obj(p, c=c):
                q = par.copy()
                q[c] = np.clip(p, [0.0, 0.0], [0.999, 2.0])
                return comp_rss(q, F[~test], z[~test], mask[~test])[1]
            par[c] = np.clip(minimize(obj, par[c], method="Nelder-Mead", options=dict(xatol=1e-3, fatol=1e-6)).x,
                             [0.0, 0.0], [0.999, 2.0])
    w = comp_rss(par, F[~test], z[~test], mask[~test])[0]
    _, _, _, X, y = comp_rss(par, F[test], z[test], mask[test])
    mse = float(((y - X @ w) ** 2).mean())
    say(f"[jump kernel per component] " + ", ".join(f"{nm} gamma {g:.3f} kappa {k:.3f} (weight {ww:+.3f})"
                                                  for nm, (g, k), ww in zip(names, par, w))
        + f"; test MSE {100 * (mse / fits['Rutledge 2014']['mse'] - 1):+.2f}% against Rutledge 2014")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6, 3.8))
    lags = np.arange(12)
    for name, col in (("Rutledge 2014", "#7f7f7f"), ("jump, RPE by sign", "#e76f51")):
        f = fits[name]
        ax.plot(lags, np.r_[1.0, f["kap"] * f["gam"] ** np.arange(11)], "o-", color=col,
                label=f"{name}: gamma {f['gam']:.2f}, kappa {f['kap']:.2f}")
    ax.set_xlabel("trials since the outcome")
    ax.set_ylabel("weight in the next rating")
    ax.set_title("How long an outcome echoes in momentary happiness (GBE)", fontsize=10)
    ax.legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "gbe.png"), dpi=130)
    say(f"done in {time.time() - t0:.0f}s")
    open(os.path.join(HERE, "gbe_report.txt"), "w").write("\n".join(lines) + "\n")
