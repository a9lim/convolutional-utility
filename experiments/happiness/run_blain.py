"""News about later trials in Blain & Rutledge 2020. Run:
python experiments/happiness/run_blain.py   (writes blain_report.txt; needs data/blain, see README.md)

The learner (a delta rule per environment, fitted to choices, inverse temperature at most 50 as in the paper)
gives each trial's belief; the regressors are in blain.py. All fits: kernel (1, kappa, kappa gamma, ...), a
linear drift within each block, a fixed effect per participant-block; cross-validation over participants (5
folds, 4 repeats); intervals by bootstrap over participants. Likelihood-ratio intervals treat ratings as
independent, so they are nominal.

1. Free regressors: Blain & Rutledge's PPE model; arrival (the trial's own channels: magnitude EVm, RPEm and
   winning itself P, PPE); arrival plus the later-trial terms as free regressors.
2. The sign test. An outcome's news about later trials, dF = w_EVm dV + w_P dW (a later trial's expected felt
   contribution is its anticipated parts), mostly shares PPE's sign, but not after a win on the car believed
   worse. Felt news about later trials adds to PPE's weight where the two agree and subtracts where they
   oppose. The gap per unit of news strength is calibrated by injecting dF into the same design.
3. A plug-in sensitivity fit. In a restricted canonical setting (memory, no anticipation of later trials or at
   choice beyond P's base utility, away from the end), news on arrival in the win channel gives
   r = w_PPE / w_P = 1 / (1 - kappa), kappa the news loop gain, and the effective news kernel over base
   revisions is (r - 1) nu^h (core, the reduced form; Codex). News about later trials then enters as
   (r - 1) S(nu, R) dF with S(nu, R) = sum_{j=1}^{R} nu^j over the R trials left, the next trial's innovation
   applied to all of them. Profile nu with the kernel refitted at each value.
dF and the PPE split are rebuilt from the arrival fit of each training fold and each bootstrap resample.
"""
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blain  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
B = blain.B
R_LEFT = np.tile(B - 1 - np.arange(B), 2)


def S(x, R=R_LEFT):
    """sum_{j=1}^{R} x^j."""
    return R.astype(float) if x == 1 else x * (1 - x ** R) / (1 - x)


def per_person_sse(X, z, sel, w):
    """Held-out squared error per participant (rows of sel), with the participant-block fixed effects."""
    out = np.zeros(sel.sum())
    Xs, zs = X[sel], z[sel]
    for b in (0, 1):
        sl = slice(b * B, (b + 1) * B)
        m = ~np.isnan(zs[:, sl])
        cnt = m.sum(1, keepdims=True)
        xm = np.where(m[..., None], Xs[:, sl], 0).sum(1, keepdims=True) / cnt[..., None]
        ym = np.where(m, zs[:, sl], 0).sum(1, keepdims=True) / cnt
        r = np.where(m, (zs[:, sl] - ym) - (Xs[:, sl] - xm) @ w, 0.0)
        out += (r ** 2).sum(1)
    return out


def cv_sse(Fk, z, splits):
    """Per-participant held-out SSE, averaged over repeats of 5-fold splits."""
    n = len(z)
    tot = np.zeros(n)
    for folds in splits:
        for f in folds:
            te = np.zeros(n, bool); te[f] = True
            g, k = blain.best_kernel(Fk, z, ~te)
            X = blain.design(Fk, g, k)
            tot[te] += per_person_sse(X, z, te, blain.lsq(X, z, ~te)[0])
    return tot / len(splits)


def tied(cols, x, nu):
    """Arrival inputs with news about later trials at effective strength x and reach nu (before filtering)."""
    sc = x * S(nu)[None] if nu > 0 else 0.0
    return np.stack([cols["EVm"] + sc * cols["dV"], cols["RPEm"], cols["P"] + sc * cols["dW"], cols["PPE"]], -1)


def with_dF(cols, z, sel):
    """Fit arrival on sel; return its kernel and weights, and cols with dF = w_EVm dV + w_P dW and PPE split by
    whether dF shares its sign (built from sel's fit only)."""
    Fa = np.stack([cols[k] for k in ("EVm", "RPEm", "P", "PPE")], -1)
    g, k = blain.best_kernel(Fa, z, sel)
    w = blain.lsq(blain.design(Fa, g, k), z, sel)[0]
    c = dict(cols)
    c["dF"] = w[0] * cols["dV"] + w[2] * cols["dW"]
    agree = (np.sign(c["dF"]) == np.sign(cols["PPE"])).astype(float)
    c["PPE_same"], c["PPE_opp"] = cols["PPE"] * agree, cols["PPE"] * (1 - agree)
    return g, k, w, c, agree


def cv_sse_dF(keys, cols, z, splits):
    """As cv_sse, with dF and the split rebuilt from each training fold's arrival fit."""
    n = len(z)
    tot = np.zeros(n)
    for folds in splits:
        for f in folds:
            te = np.zeros(n, bool); te[f] = True
            _, _, _, c, _ = with_dF(cols, z, ~te)
            Fk = np.stack([c[k] for k in keys], -1)
            g, k = blain.best_kernel(Fk, z, ~te)
            X = blain.design(Fk, g, k)
            tot[te] += per_person_sse(X, z, te, blain.lsq(X, z, ~te)[0])
    return tot / len(splits)


SPLIT = ["EVm", "RPEm", "P", "PPE_same", "PPE_opp"]


def injection_slope(c, z, g, k, sel):
    """The split design's same-minus-opposite PPE coefficient per unit of dF injected into the felt input."""
    inj = blain.filtered(c["dF"][..., None], blain.kernel(g, k))[..., 0]
    inj = np.where(np.isnan(z), np.nan, inj)
    w = blain.lsq(blain.design(np.stack([c[x] for x in SPLIT], -1), g, k), inj, sel)[0]
    return w[3] - w[4]


NUS = (0.0, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)


def nu_profile(cols, z, sel):
    """RSS by nu at the effective strength r - 1 from arrival, kernel refitted at each nu."""
    Fa = np.stack([cols[k] for k in ("EVm", "RPEm", "P", "PPE")], -1)
    g, k = blain.best_kernel(Fa, z, sel)
    w = blain.lsq(blain.design(Fa, g, k), z, sel)[0]
    r = w[3] / w[2]
    out = []
    for nu in NUS:
        Ft = tied(cols, r - 1, nu)
        g2, k2 = blain.best_kernel(Ft, z, sel)
        out.append(blain.lsq(blain.design(Ft, g2, k2), z, sel)[1])
    return np.array(out), r


if __name__ == "__main__":
    t0, lines = time.time(), []
    say = lambda s: (print(s, flush=True), lines.append(s))
    D = blain.load()
    n = len(D["h"])
    fits = [blain.fit_learner(D, i) for i in range(n)]
    lr = np.array([f["lr"] for f in fits]); be = np.array([f["beta"] for f in fits])
    ph = np.array([f["phi"] for f in fits])
    say(f"{n} participants, {int((~np.isnan(D['h'])).sum())} ratings (46 each, z-scored within participant "
        f"and block), two 80-trial blocks each.")
    say(f"Learner fitted to choices, stable / volatile: learning rate {lr[:, 0].mean():.3f} / "
        f"{lr[:, 1].mean():.3f} (paper 0.16 / 0.47), probability weight phi {ph[:, 0].mean():.2f} / "
        f"{ph[:, 1].mean():.2f} (paper 0.57 / 0.44), median beta {np.median(be[:, 0]):.1f} / "
        f"{np.median(be[:, 1]):.1f} ({int((be >= blain.BETA_MAX - 1e-6).sum())} of {be.size} blocks at the cap "
        f"of 50).")
    F, names, ex = blain.regressors(D, fits)
    z = blain.ratings(D)
    cols = dict(zip(names, np.moveaxis(F, -1, 0)))
    stack = lambda keys, c=cols: np.stack([c[k] for k in keys], -1)
    arrival = ["EVm", "RPEm", "P", "PPE"]
    allp = np.ones(n, bool)
    cnt = int((~np.isnan(z)).sum())
    gA, kA, wA, full, agree = with_dF(cols, z, allp)
    dF = full["dF"]
    worse = ex["p"] < 0.5
    say(f"An outcome's news about later trials, dF = w_EVm dV + w_P dW (arrival weights {wA[0]:.3f}, {wA[2]:.3f}), "
        f"shares PPE's sign on {100 * agree.mean():.0f}% of trials ({100 * agree[~worse].mean():.0f}% when the "
        f"chosen car was believed better, {100 * agree[worse].mean():.0f}% when believed worse; corr(PPE, dF) "
        f"{np.corrcoef(cols['PPE'].ravel(), dF.ravel())[0, 1]:.2f}).")

    # 1. free regressors
    models = [("Blain & Rutledge: PPE", ["PPE"]),
              ("arrival", arrival),
              ("arrival + free dV, dW (news about later)", arrival + ["dV", "dW"]),
              ("arrival + free Vnext, Wnext (anticipation of later)", arrival + ["Vnext", "Wnext"]),
              ("arrival + dF (tied news about later, one free strength)", arrival + ["dF"]),
              ("arrival, PPE split by the sign of dF", ["EVm", "RPEm", "P", "PPE_same", "PPE_opp"])]
    rng = np.random.default_rng(0)
    splits = [np.array_split(rng.permutation(n), 5) for _ in range(4)]
    sse = {}
    say("")
    say("1. Free regressors (weights per unit of the regressor, in z; V, W per later trial):")
    for name, keys in models:
        Fk = stack(keys, full)
        g, k = blain.best_kernel(Fk, z, allp)
        w = blain.lsq(blain.design(Fk, g, k), z, allp)[0]
        sse[name] = cv_sse_dF(keys, cols, z, splits) if ("dF" in keys or "PPE_same" in keys) else cv_sse(Fk, z, splits)
        say(f"[{name}] gamma {g:.3f} kappa {k:.3f}; CV MSE {sse[name].sum() / cnt:.4f}; "
            + ", ".join(f"{a} {b:+.3f}" for a, b in zip(keys + ["drift"], w)) + f"  ({time.time() - t0:.0f}s)")
    say("Held-out error against arrival (paired bootstrap over participants, 2000 resamples):")
    base = sse["arrival"]
    for name in sse:
        if name == "arrival":
            continue
        d = sse[name] - base
        bs = [d[rng.integers(0, n, n)].sum() / base.sum() for _ in range(2000)]
        lo, hi = np.percentile(bs, [2.5, 97.5])
        say(f"    {name}: {100 * d.sum() / base.sum():+.2f}% [{100 * lo:+.2f}, {100 * hi:+.2f}]")

    # 2. the sign test, calibrated by injection into the same design
    per = injection_slope(full, z, gA, kA, allp)
    say("")
    say(f"2. The sign test: news about later trials at strength lam (lam dF in the felt input) raises PPE's weight "
        f"where dF shares its sign over where it opposes it by {per:.3f} lam (injected into the split design).")

    # 3. the tie: nu at the effective strength from arrival
    rnu, r = nu_profile(cols, z, allp)
    kap = 1 - 1 / r
    ok = np.array(NUS)[rnu <= rnu.min() + 3.84 * rnu.min() / cnt]
    say("")
    say(f"3. News on arrival in the win channel: r = w_PPE / w_P = {r:.3f}. If P's weight is the expected win's "
        f"base utility with no further anticipation at choice, the memory-only interior model reads it as loop gain "
        f"kappa = 1 - 1/r = {kap:.3f} and effective strength r - 1 = {r - 1:.3f} (the magnitude channel's ratio "
        f"w_RPEm / w_EVm is {wA[1] / wA[0]:.3f}; their difference is in the bootstrap). A plug-in sensitivity fit, "
        f"news about later trials at that strength with the same next-trial innovation over all remaining trials, "
        f"kernel refitted at each nu, MSE by nu: "
        + ", ".join(f"{x:.1f}: {v / cnt:.5f}" for x, v in zip(NUS, rnu))
        + f"; best tested nu {NUS[int(np.argmin(rnu))]:.1f} (nominal likelihood-ratio set {ok.min():.1f} to "
        f"{ok.max():.1f}; not a calibrated bound).")

    # bootstrap
    say("")
    say("Bootstrap over participants (200 resamples):")
    rows = []
    for b in range(200):
        pick = rng.integers(0, n, n)
        zb = z[pick]
        cols_b = {k: v[pick] for k, v in cols.items()}
        cb = cols_b
        g, k, wa, cb, _ = with_dF(cb, zb, allp)
        Fsb = stack(SPLIT, cb)
        gs, ks = blain.best_kernel(Fsb, zb, allp)
        ws = blain.lsq(blain.design(Fsb, gs, ks), zb, allp)[0]
        Fdb = stack(arrival + ["dF"], cb)
        gd, kd = blain.best_kernel(Fdb, zb, allp)
        wd = blain.lsq(blain.design(Fdb, gd, kd), zb, allp)[0]
        perb = injection_slope(cb, zb, gs, ks, allp)
        rb = wa[3] / wa[2]
        row = [ws[3], ws[4], ws[3] - ws[4], g, k, rb, 1 - 1 / rb, wa[1] / wa[0], rb - wa[1] / wa[0], wd[4],
               perb, (ws[3] - ws[4]) / perb]
        if b < 100:
            row.append(NUS[int(np.argmin(nu_profile(cols_b, zb, allp)[0]))])
        else:
            row.append(np.nan)
        rows.append(row)
        if b % 50 == 49:
            print(f"  bootstrap {b + 1}  ({time.time() - t0:.0f}s)", flush=True)
    rows = np.array(rows)
    for j, nm in enumerate(["PPE where dF shares its sign", "PPE where dF opposes it", "same - opposite",
                            "gamma", "kappa (kernel)", "r = w_PPE / w_P", "1 - 1/r", "w_RPEm / w_EVm",
                            "win minus magnitude channel ratio", "news about later, free strength (weight on dF)",
                            "injection slope", "same - opposite over the injection slope (implied strength)",
                            "nu at the effective strength (100 resamples)"]):
        col = rows[:, j] if j < 12 else rows[:, 12]
        lo, mid, hi = np.nanpercentile(col, [2.5, 50, 97.5])
        say(f"    {nm}: median {mid:+.3f} [{lo:+.3f}, {hi:+.3f}]")
    say(f"({time.time() - t0:.0f}s)")
    open(os.path.join(HERE, "blain_report.txt"), "w").write("\n".join(lines) + "\n")
