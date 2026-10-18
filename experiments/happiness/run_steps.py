"""Biphasic memory at step changes in luck (steps.py: Keren et al. 2021's and Jangraw et al. 2023's open-loop
up-down-up task). Run:
python experiments/happiness/run_steps.py   (writes steps_report.txt; needs data/keren, data/jangraw)

For each dataset (Keren's version; Jangraw's two weekly cohorts pooled, same design, most people in both):
- kernel shapes on the trial inputs (CR, EV, RPE), each with a linear drift and a fixed effect per session,
  5-fold cross-validated with folds by person (4 repeats): the jump kernel (afterglow), the hyperbola,
  biphasic memory (k(l) = m mu^l - c gamma^l for l >= 1, afterglow minus adaptation) and the hyperbola minus
  an exponential; paired bootstrap over people for each adaptation term against its afterglow-only kernel;
- running means of all earlier inputs as extra covariates, a reference built from the whole history (in the
  spirit of history-based references such as Keren's primacy model, not that model);
- the jump kernel's mean residual within each block, late half against early half (post-trial ratings only);
- distinguishability: ratings simulated without noise from the fitted jump model plus an adaptation tail that
  cancels a fraction f of the kernel's positive mass with reach 1/(1 - gamma), refitted by the jump model
  (kernel, weights, drift, fixed effects); what it cannot absorb, over the residual variance, is D^2, an
  uncalibrated distance (not the power of the cross-validated comparison);
- RestAfterWins: mood at rest after a closed-loop winning block, against the rating before it, with the rest
  period opening the weekly cohorts (no outcomes yet) as an illustrative drift control."""
import os
import sys
import time

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import steps  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SEC_TRIAL, SEC_RATING, SEC_REST = 9.4, 6.0, 15.0   # the weekly cohorts' timing: trial with response, rating


def fit_kernel(kf, starts, bounds, F, tau, z, pid, sel, T, extra=None):
    lb, ub = map(np.asarray, bounds)
    obj = lambda p: float((steps.lsq(steps.design(F, tau, pid, kf(np.clip(p, lb, ub)), T, extra), z, pid,
                                     sel)[1] ** 2).sum())
    best = min((minimize(obj, s, method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-7, maxiter=3000))
                for s in starts), key=lambda r: r.fun)
    p = np.clip(best.x, lb, ub)
    return p, steps.lsq(steps.design(F, tau, pid, kf(p), T, extra), z, pid, sel)[0]


def held_out(F, tau, z, pid, who, T, kf, starts, bounds, splits, extra=None):
    """Per-session held-out SSE (fixed effects refitted on the held-out session, weights and kernel held), folds
    by person, averaged over repeats; and the full-sample parameters."""
    n = pid.max() + 1
    tot = np.zeros(n)
    for folds in splits:
        for f in folds:
            te = np.isin(who, f)
            p, w = fit_kernel(kf, starts, bounds, F, tau, z, pid, ~te, T, extra)
            X = steps.design(F, tau, pid, kf(p), T, extra)
            _, r = steps.lsq(X, z, pid, te, w)
            tot += np.bincount(pid[te[pid]], r ** 2, n)
    p, w = fit_kernel(kf, starts, bounds, F, tau, z, pid, np.ones(n, bool), T, extra)
    return tot / len(splits), p, w


def by_person(x, who):
    """Sum a per-session quantity within each person."""
    return np.bincount(who, x)


def boot_people(x_person, rng, B=2000, denom=None):
    """Percentile interval of the resampled sum (or ratio to denom's resampled sum) over people."""
    m = len(x_person)
    out = []
    for _ in range(B):
        i = rng.integers(0, m, m)
        out.append(x_person[i].sum() / (denom[i].sum() if denom is not None else 1.0))
    return np.percentile(out, [2.5, 97.5])


if __name__ == "__main__":
    t0, lines = time.time(), []
    say = lambda s: (print(s, flush=True), lines.append(s))
    rng = np.random.default_rng(0)
    data = {name: steps.load(name) for name in ("keren", "covid02", "covid03")}
    sets = {"Keren et al. 2021 (27-trial blocks)": data["keren"],
            "Jangraw et al. 2023, Weekly-Rest-02 and -03 (22-trial blocks)":
                (data["covid02"][0] + data["covid03"][0], data["covid02"][1])}
    for label, (runs, T) in sets.items():
        runs = steps.zscore(runs)
        F, tau, z, pid = steps.stack(runs, T)
        n = len(runs)
        people, who = np.unique([r["person"] for r in runs], return_inverse=True)
        npl = len(people)
        rpe = F[..., 2]
        say(f"== {label}: {n} sessions from {npl} people, {len(z)} ratings ({len(runs[0]['tau'])} each, z-scored "
            f"within session); gambles {100 * np.mean([r['gamble'].mean() for r in runs]):.0f}% of trials; mean "
            "prediction error per trial by block " + ", ".join(
                f"{rpe[:, runs[0]['block'] == b].mean():+.2f}" for b in range(3)) + " points.")
        splits = [np.array_split(rng.permutation(npl), 5) for _ in range(4)]
        res = {}
        ks = steps.kernels(T)
        for nm, kf, starts, bounds in ks:
            sse, p, w = held_out(F, tau, z, pid, who, T, kf, starts, bounds, splits)
            res[nm] = sse
            k = kf(p)
            neg = np.flatnonzero(k < 0)
            extra = ""
            if nm == "biphasic":
                m_, mu, c, g = p
                if c < 1e-3 or g < 1e-3 or abs(mu - g) < 1e-3:  # no lobe of its own: the jump kernel
                    extra = "; collapses to the jump kernel (no adaptation term with a reach of its own)"
                else:
                    extra = f"; negative tail mass {c * g / (1 - g):.3f}, reach 1/(1 - gamma) {1 / (1 - g):.1f} trials"
            if nm == "hyperbola - exp":
                extra = f"; negative tail {p[2]:.4f} per lag at reach {1 / (1 - p[3]):.0f} trials"
            say(f"[{nm}] params {np.round(p, 4)}; CV MSE {sse.sum() / len(z):.5f}; weights CR {w[0]:+.3f} EV "
                f"{w[1]:+.3f} RPE {w[2]:+.3f} drift {w[3]:+.3f}; k[1, 5, 10, 20] {np.round(k[[1, 5, 10, 20]], 3)}; "
                f"first negative lag {neg[0] if len(neg) else 'none'}{extra}  ({time.time() - t0:.0f}s)")
        RM = steps.running_mean(F, tau, pid)
        nm, kf, starts, bounds = ks[0]
        sse, p, w = held_out(F, tau, z, pid, who, T, kf, starts, bounds, splits, extra=RM)
        res["jump + running means of earlier inputs"] = sse
        say(f"[jump + running means of earlier inputs] params {np.round(p, 4)}; CV MSE {sse.sum() / len(z):.5f}; "
            f"weights CR {w[0]:+.3f} EV {w[1]:+.3f} RPE {w[2]:+.3f} drift {w[3]:+.3f}; running means CR "
            f"{w[4]:+.3f} EV {w[5]:+.3f} RPE {w[6]:+.3f}")
        say("    held-out error, paired bootstrap over people (2000 resamples):")
        for a, b in (("biphasic", "jump"), ("hyperbola - exp", "hyperbola"), ("hyperbola", "jump"),
                     ("jump + running means of earlier inputs", "jump")):
            dp, bp = by_person(res[a] - res[b], who), by_person(res[b], who)
            lo, hi = boot_people(dp, rng, denom=bp)
            say(f"    {a} against {b}: {100 * dp.sum() / bp.sum():+.3f}% [{100 * lo:+.3f}, {100 * hi:+.3f}]")

        # residual within blocks under the jump kernel, post-trial ratings only
        p, w = fit_kernel(kf, starts, bounds, F, tau, z, pid, np.ones(n, bool), T)
        _, r = steps.lsq(steps.design(F, tau, pid, kf(p), T), z, pid, np.ones(n, bool), w)
        r0 = runs[0]
        blk = np.array([r0["block"][max(t, 0)] for t in r0["tau"]])
        start = {b: np.flatnonzero(r0["block"] == b)[0] for b in range(3)}
        pos = np.array([t - start[r0["block"][max(t, 0)]] for t in r0["tau"]])
        post = r0["kind"] == 1
        R = r.reshape(n, len(r0["tau"]))
        out = []
        for b in range(3):
            early = (blk == b) & post & (pos < T // 6)
            late = (blk == b) & post & (pos >= T // 6)
            diff = R[:, late].mean(1) - R[:, early].mean(1)
            dp, cnt = by_person(diff, who), np.bincount(who)
            lo, hi = boot_people(dp, rng, denom=cnt.astype(float))
            good = r0["happy"][start[b]] > 0
            out.append(f"block {b + 1} ({'good' if good else 'bad'}) {dp.sum() / cnt.sum():+.3f} [{lo:+.3f}, {hi:+.3f}]")
        say("    jump-kernel residual, late minus early half of each block (z, post-trial ratings): " + "; ".join(out))

        # distinguishability of an adaptation tail, by the fraction of the positive mass it cancels
        sig2 = float((r ** 2).mean())
        k0 = kf(p)
        Apos = 1 + p[1] / (1 - p[0])                    # asymptotic response to a constant input
        ones = np.ones(n, bool)
        say(f"    distinguishability D^2 (residual variance {sig2:.3f}; the jump kernel's positive mass {Apos:.2f}), "
            "by the fraction f = 0.25, 0.5, 1 of it an adaptation tail cancels, at reach 1/(1 - gamma):")
        for reach in (5, 10, 20, 50):
            g = 1 - 1 / reach
            row = []
            for f in (0.25, 0.5, 1.0):
                c = f * Apos * (1 - g) / g
                k_true = k0.copy()
                k_true[1:] -= c * g ** np.arange(1, T)
                y0 = steps.design(F, tau, pid, k_true, T) @ w
                obj = lambda q: float((steps.lsq(steps.design(F, tau, pid, kf(np.clip(q, *map(np.asarray, bounds))),
                                                              T), y0, pid, ones)[1] ** 2).sum())
                rmin = min(minimize(obj, s0, method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-9)).fun
                           for s0 in (p, starts[1]))
                row.append(f"{rmin / sig2:.1f}")
            say(f"        reach {reach}: " + ", ".join(row))
        say("")

    # after a sustained good step ends: mood at rest against the pre-task rating
    pre, last, rest, dflt = steps.rest_after_wins()
    D = rest - pre[:, None]
    n = len(pre)
    bs = [D[rng.integers(0, n, n), 20:30].mean() for _ in range(2000)]
    lo, hi = np.percentile(bs, [2.5, 97.5])
    say(f"== Jangraw et al., RestAfterWins: {n} people (rest ratings exactly at the slider's 0.5: median "
        f"{np.median(dflt):.2f} of a person's, more than half for {(dflt > 0.5).sum()}). Raw 0-1 ratings: before "
        f"the closed-loop winning block {pre.mean():.3f}, its last rating {last.mean():.3f}; at rest, 15 s apart, "
        f"minus the pre-task rating at ratings 1, 5, 10, 20, 30: "
        + ", ".join(f"{D[:, i].mean():+.3f}" for i in (0, 4, 9, 19, 29))
        + f"; ratings 21-30 {D[:, 20:30].mean():+.3f} [{lo:+.3f}, {hi:+.3f}], below it for "
        f"{100 * (D[:, 29] < 0).mean():.0f}% at the last.")
    slopes = []
    for c in ("covid02", "covid03"):
        R, gap = steps.rest_drift(c)
        slope = np.polyfit(np.arange(18) * gap / 60, R.mean(0), 1)[0]
        slopes.append(slope)
        say(f"    the rest period opening {c.upper()} ({len(R)} sessions, no outcomes yet, {gap:.1f} s apart): "
            f"{slope:+.4f} per minute, last minus first rest rating {(R[:, -1] - R[:, 0]).mean():+.3f}")
    minutes = (54 * SEC_TRIAL + 22 * SEC_RATING + 25 * SEC_REST) / 60   # to the middle of ratings 21-30
    drift = np.mean(slopes) * minutes
    say(f"    illustrative: at the weekly cohorts' timing ratings 21-30 come about {minutes:.0f} minutes after the "
        f"pre-task rating; if that opening-rest slope held throughout, drift alone gives {drift:+.3f}, leaving "
        f"{D[:, 20:30].mean() - drift:+.3f} [{lo - drift:+.3f}, {hi - drift:+.3f}] (drift treated as known).")
    say(f"({time.time() - t0:.0f}s)")
    open(os.path.join(HERE, "steps_report.txt"), "w").write("\n".join(lines) + "\n")
