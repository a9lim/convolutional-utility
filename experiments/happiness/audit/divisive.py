"""Divisive (range) adaptation: is a trial's felt response smaller after a run of high-stakes trials? Recent
stakes are the mean of each trial's largest offered amount over the previous 5 trials (random draws, so not
chosen), z-scored within trial position. Each trial's regressors are multiplied by the recent stakes before it
and filtered through the best kernel; the interaction coefficients over the main ones give the change in
sensitivity per s.d. of recent stakes (divisive adaptation: negative). A level term for recent stakes is
included. Great Brain Experiment (the audit split) and Forbes & Bennett (5-fold CV over people)."""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

def recent(stake, K=5):
    """mean stake over the previous K trials (fewer at the start), z-scored within trial position"""
    n = stake.shape[1]; v = np.zeros_like(stake, dtype=float)
    for t in range(1, n):
        v[:, t] = stake[:, max(0, t - K):t].mean(1)
    for t in range(1, n):
        col = v[:, t]; v[:, t] = (col - col.mean()) / (col.std() + 1e-12)
    v[:, 0] = 0.0
    return v

def boot_ratio(Xs, ys, cl, nmain, B=200, seed=1):
    u, inv = np.unique(cl, return_inverse=True); r = np.random.default_rng(seed); out = []
    for _ in range(B):
        w = np.bincount(r.integers(0, len(u), len(u)), minlength=len(u))[inv].astype(float)
        A = Xs * w[:, None]; c = np.linalg.solve(Xs.T @ A + 1e-9 * np.eye(Xs.shape[1]), A.T @ ys)
        out.append(c[nmain:2 * nmain] / c[:nmain])
    return np.quantile(np.array(out), [.025, .975], axis=0)

# ---- Great Brain Experiment ----
ell = np.arange(L, dtype=float)
F, names = gbe.features(D, "rpe")
stake = np.maximum.reduce([np.abs(D["c"]), np.abs(D["w"]), np.abs(D["l"])])
v = recent(stake)
r_ = np.random.default_rng(3)
for kn, k in [("hyperbola", (1 + 2.2242 * ell) ** -0.578), ("jump", jump_k(0.8901, 0.4125))]:
    X0 = Xr(F, k); Xi = Xr(F * v[..., None], k); Xv = Xr(v[..., None], k)
    full = np.concatenate([X0, Xi, Xv], -1); base = np.concatenate([X0, Xv], -1)
    w1, _, _ = fitX(full, ~test); w0, _, _ = fitX(base, ~test)
    _, s1, n1 = fitX(full, test, w1); _, s0, n0 = fitX(base, test, w0)
    sel = GOOD
    Xs = full[sel] - full[sel].mean(1, keepdims=True); ys = Zr[sel] - Zr[sel].mean(1, keepdims=True)
    Xs = Xs.reshape(-1, Xs.shape[-1]); ys = ys.reshape(-1); cl = np.repeat(D["subj"][sel], len(ROWS))
    c = np.linalg.lstsq(Xs, ys, rcond=None)[0]; ratio = c[4:8] / c[:4]; ci = boot_ratio(Xs, ys, cl, 4)
    print(f"[GBE, {kn}] held-out MSE with interaction {s1 / n1:.5f} vs without {s0 / n0:.5f} ({100 * (s1 / n1 / (s0 / n0) - 1):+.3f}%)")
    print("   sensitivity change per s.d. of recent stakes: " + "; ".join(
        f"{nm} {100 * ratio[i]:+.1f}% [{100 * ci[0, i]:+.1f}, {100 * ci[1, i]:+.1f}]" for i, nm in enumerate(names))
          + f"; level {c[8]:+.4f}", flush=True)

# ---- Forbes & Bennett ----
import csv, forbes
from gbe import fit
T = forbes.T; ellF = np.arange(T, dtype=float)
def design_k(F, k):
    X = np.zeros((F.shape[0], T + 1, F.shape[2]))
    for t in range(T):
        X[:, t + 1] = np.einsum("l,blf->bf", k[:t + 1], F[:, t::-1][:, :t + 1])
    return X
for exp, (hh, om) in [("exp1", (1.042, 0.679)), ("exp2", (1.349, 0.67))]:
    Dx = forbes.load(exp); person = Dx["person"]
    keys = sorted({(r["id"], int(r["block"])) for r in csv.DictReader(open(os.path.join(forbes.DATA, exp, "behav_data.csv")))})
    idx = {kk: i for i, kk in enumerate(keys)}; st = np.zeros((len(keys), T))
    for r in csv.DictReader(open(os.path.join(forbes.DATA, exp, "behav_data.csv"))):
        st[idx[(r["id"], int(r["block"]))], int(r["trial"]) - 1] = max(abs(float(r[c_])) for c_ in
            ("left_amount_1", "left_amount_2", "right_amount_1", "right_amount_2"))
    v = recent(st)
    z, mask = forbes.ratings(Dx); F, names = forbes.features(Dx, "sign")
    k = (1 + hh * ellF) ** -om
    X0 = design_k(F, k); Xi = design_k(F * v[..., None], k); Xv = design_k(v[..., None], k)
    full = np.concatenate([X0, Xi, Xv], -1); base = np.concatenate([X0, Xv], -1)
    people = np.unique(person); fold = dict(zip(np.random.default_rng(0).permutation(people), np.arange(len(people)) % 5))
    fo = np.array([fold[p] for p in person]); sse = {0: 0.0, 1: 0.0}; nn = 0
    for f in range(5):
        tr = fo != f
        for j, X in ((1, full), (0, base)):
            w = fit(X[tr], z[tr], mask[tr])[0]; _, _, m, Xt, yt = fit(X[~tr], z[~tr], mask[~tr]); sse[j] += float(((yt - Xt @ w) ** 2).sum())
        nn += m
    c, _, _, Xs, ys = fit(full, z, mask)
    cl = np.repeat(person[:, None], T + 1, 1)[mask[:, :] & (mask.sum(1, keepdims=True) > 1)]
    ratio = c[4:8] / c[:4]; ci = boot_ratio(Xs, ys, cl, 4)
    print(f"[{exp}] CV MSE with interaction {sse[1] / nn:.5f} vs without {sse[0] / nn:.5f} ({100 * (sse[1] / sse[0] - 1):+.3f}%)")
    print("   sensitivity change per s.d. of recent stakes: " + "; ".join(
        f"{nm} {100 * ratio[i]:+.1f}% [{100 * ci[0, i]:+.1f}, {100 * ci[1, i]:+.1f}]" for i, nm in enumerate(names))
          + f"; level {c[8]:+.4f}", flush=True)
