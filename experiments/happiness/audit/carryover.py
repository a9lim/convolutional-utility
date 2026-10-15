"""Carryover between plays in the Great Brain Experiment. Luck of play k (summed RPE, random given choices)
against the change in pre-trial baseline from play k to play k+1, by the gap between them. Raw ratings
(0-100), no z-scoring (within-person z-scores make a lucky play mechanically lower the person's other plays).
Then Forbes & Bennett: the same between consecutive blocks of a session (raw valence, 0-1)."""
import sys, os, numpy as np, scipy.io
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import gbe, forbes
D = gbe.load()
S = scipy.io.loadmat(gbe.MAT, struct_as_record=False, squeeze_me=True)["subjData"]
day, tod = [], []
for i, s in enumerate(S):                       # same loop and filter as gbe.tidy, so plays align
    d = s.data
    mats = [d] if isinstance(d, np.ndarray) and d.dtype != object else list(np.atleast_1d(d))
    dn, td = np.atleast_1d(s.dayNumber), np.atleast_1d(s.timeOfDay)
    for j, X in enumerate(mats):
        if np.asarray(X, dtype=float).shape != (30, 15): continue
        day.append(dn[min(j, len(dn) - 1)]); tod.append(td[min(j, len(td) - 1)])
day, tod = np.array(day, float), np.array(tod, float); assert len(day) == len(D["subj"])
T = day + tod
g = D["g"]; ev = (D["w"] + D["l"]) / 2; rpe = (g * (D["o"] - ev)).sum(1) / 100   # luck, hundreds of points
paid = ((1 - g) * D["c"] + g * D["o"]).sum(1) / 100
h = D["h"]; first, last = h[:, 0], h[:, 29]
subj = D["subj"]
same = subj[1:] == subj[:-1]
gap = T[1:] - T[:-1]
ok = same & np.isfinite(first[1:]) & np.isfinite(first[:-1]) & np.isfinite(last[:-1]) & np.isfinite(gap)
print("consecutive pairs:", int(ok.sum()), " negative gaps (ordering/clock):", int((ok & (gap < 0)).sum()))
ok &= gap >= 0
luck, dbase, dend = rpe[:-1][ok], (first[1:] - first[:-1])[ok], (last[:-1] - first[:-1])[ok]
gp, sj = gap[ok], subj[:-1][ok]
ver = D["version"][1:][ok]
def slope(x, y, cl, B=400, seed=0):
    X = np.c_[np.ones_like(x), x]; b = np.linalg.lstsq(X, y, rcond=None)[0][1]
    u, inv = np.unique(cl, return_inverse=True); r = np.random.default_rng(seed); bs = []
    idx = [np.flatnonzero(inv == k) for k in range(len(u))] if len(u) < 3000 else None
    for _ in range(B):
        w = np.bincount(r.integers(0, len(u), len(u)), minlength=len(u))[inv].astype(float)
        Xw = X * w[:, None]; bs.append(np.linalg.solve(X.T @ Xw, Xw.T @ y)[1])
    return b, np.quantile(bs, [.025, .975])
b_end, ci_end = slope(luck, dend, sj)
print(f"within play: last minus first rating per 100 points of luck: {b_end:+.2f} [{ci_end[0]:+.2f}, {ci_end[1]:+.2f}]")
bins = [(0, 10 / 1440, "< 10 min"), (10 / 1440, 1 / 24, "10 min - 1 h"), (1 / 24, 1, "1 h - 1 day"),
        (1, 7, "1 - 7 days"), (7, 1e9, "> 7 days")]
for lo, hi, nm in bins:
    s = (gp >= lo) & (gp < hi)
    b, ci = slope(luck[s], dbase[s], sj[s])
    print(f"gap {nm:13s} n={int(s.sum()):6d} (median {np.median(gp[s]) * 1440:8.1f} min): next baseline per 100 points "
          f"of luck {b:+.2f} [{ci[0]:+.2f}, {ci[1]:+.2f}] = {100 * b / b_end:+.0f}% [{100 * ci[0] / b_end:+.0f}, {100 * ci[1] / b_end:+.0f}]")
for vn, vs in [("cursor at 50 (v1-2)", ver <= 2), ("random cursor (v3-5)", ver >= 3)]:
    s = (gp < 10 / 1440) & vs
    b, ci = slope(luck[s], dbase[s], sj[s]); be, _ = slope(luck[vs], dend[vs], sj[vs])
    print(f"< 10 min, {vn}: {100 * b / be:+.0f}% [{100 * ci[0] / be:+.0f}, {100 * ci[1] / be:+.0f}] of that version's within-play effect (n={int(s.sum())})")

T = forbes.T
for exp in ("exp1", "exp2"):
    Dx = forbes.load(exp); person = Dx["person"]
    # (1) carryover between consecutive blocks of a person (blocks sorted by block number within person)
    luck = np.nansum(Dx["o"] - Dx["ev"], 1) / 100; pre = Dx["h"][:, 0]; endv = Dx["h"][:, T]
    same = person[1:] == person[:-1]
    d_end = endv - pre; okw = np.isfinite(d_end)
    b_end = np.polyfit(luck[okw], d_end[okw], 1)[0]
    d_pre = pre[1:] - pre[:-1]; ok = same & np.isfinite(d_pre)
    b_pre = np.polyfit(luck[:-1][ok], d_pre[ok], 1)[0]
    r = np.random.default_rng(0); u, inv = np.unique(person[:-1][ok], return_inverse=True); bs = []
    xl, yl = luck[:-1][ok], d_pre[ok]
    for _ in range(400):
        w = np.bincount(r.integers(0, len(u), len(u)), minlength=len(u))[inv].astype(float)
        X = np.c_[np.ones_like(xl), xl]; bs.append(np.linalg.solve(X.T @ (X * w[:, None]), (X * w[:, None]).T @ yl)[1])
    lo, hi = np.quantile(bs, [.025, .975])
    print(f"[{exp}] end-of-block minus pre-block valence per 100 points of luck {b_end:+.4f}; next pre-block "
          f"{b_pre:+.4f} [{lo:+.4f}, {hi:+.4f}] = {100 * b_pre / b_end:+.0f}% (n pairs {int(ok.sum())})", flush=True)
