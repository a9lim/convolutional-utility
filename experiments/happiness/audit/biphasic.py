"""Biphasic memory (afterglow minus adaptation, k(l) = m mu^l - c gamma^l): does a slow negative tail show up
within a play (Great Brain Experiment, the audit split) or within a block (Forbes & Bennett, 5-fold CV)?"""
import os, sys, numpy as np
from scipy.optimize import minimize
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
ell = np.arange(L, dtype=float)
F, names = gbe.features(D, "rpe")
def biph(p):                                # k(0) = 1; k(l) = m mu^l - c gamma^l
    m, mu, c, g = p
    k = m * mu ** ell - c * g ** ell; k[0] = 1.0; return k
def hypx(p):                                # hyperbola minus slow exponential
    h, om, c, g = p
    k = (1 + h * ell) ** -om - c * g ** ell; k[0] = 1.0; return k
def errs(k, w):
    X = Xr(F, k)[test & GOOD]; y = Zr[test & GOOD]
    X = X - X.mean(1, keepdims=True); y = y - y.mean(1, keepdims=True)
    return ((y - X @ w) ** 2).sum(1)
res = {}
specs = [("jump", lambda p: jump_k(*p), [0.89, 0.41], ([0, 0], [0.999, 2])),
         ("hyperbola", lambda p: (1 + p[0] * ell) ** -p[1], [2, 0.6], ([0, 0], [50, 10])),
         ("biphasic", biph, [0.46, 0.89, 0.05, 0.98], ([0, 0, 0, 0], [5, 0.999, 5, 0.9999])),
         ("hyperbola - exp", hypx, [2, 0.6, 0.05, 0.98], ([0, 0, 0, 0], [50, 10, 5, 0.9999]))]
for nm, kf, p0, b in specs:
    best = None
    starts = [p0] if nm in ("jump", "hyperbola") else [p0, [p0[0], p0[1], 0.2, 0.9], [p0[0], p0[1], 0.5, 0.97]]
    for s in starts:
        out = evaluate(F, kf, s, b)
        if best is None or out[2] < best[2]: best = out
    p, w, tr, te = best; k = kf(p)
    res[nm] = (te, errs(k, w))
    neg = np.flatnonzero(k < 0)
    print(f"{nm}: p {np.round(p, 4)} train {tr:.5f} test {te:.5f}; k[1..5] {np.round(k[1:6], 3)}; "
          f"k[10,20,29] {np.round(k[[10, 20, 29]], 4)}; first negative lag {neg[0] if len(neg) else 'none'}", flush=True)
subj = D["subj"][test & GOOD]; u, inv = np.unique(subj, return_inverse=True); r = np.random.default_rng(3)
for a_, b_ in [("biphasic", "jump"), ("hyperbola - exp", "hyperbola"), ("biphasic", "hyperbola")]:
    d = np.bincount(inv, res[a_][1] - res[b_][1]); tot = res[b_][1].sum()
    bs = [d[i].sum() / (tot * len(i) / len(u)) for i in (r.integers(0, len(u), len(u)) for _ in range(500))]
    print(f"{a_} vs {b_}: {100 * d.sum() / tot:+.3f}% [{100 * np.quantile(bs, .025):+.3f}, {100 * np.quantile(bs, .975):+.3f}]")

# ---- Forbes & Bennett: within-block shapes, 5-fold CV over people, fixed effect per block ----
import forbes; from gbe import fit
T = forbes.T; ellF = np.arange(T, dtype=float)
def design_k(F, k):
    X = np.zeros((F.shape[0], T + 1, F.shape[2]))
    for t in range(T):
        X[:, t + 1] = np.einsum("l,blf->bf", k[:t + 1], F[:, t::-1][:, :t + 1])
    return X
def biphF(p):
    m, mu, c, g = p; k = m * mu ** ellF - c * g ** ellF; k[0] = 1.0; return k
def hypxF(p):
    h, om, c, g = p; k = (1 + h * ellF) ** -om - c * g ** ellF; k[0] = 1.0; return k
def jumpF(p):
    gm, kp = p; k = np.r_[1.0, kp * gm ** np.arange(T - 1)]; return k
def hypF(p):
    return (1 + p[0] * ellF) ** -p[1]
specs = [("jump", jumpF, [[0.88, 0.5]], ([0, 0], [0.999, 2])),
         ("hyperbola", hypF, [[1.0, 0.7]], ([0, 0], [50, 10])),
         ("biphasic", biphF, [[0.5, 0.88, 0.05, 0.98], [0.5, 0.88, 0.2, 0.95]], ([0, 0, 0, 0], [5, 0.999, 5, 0.9999])),
         ("hyperbola - exp", hypxF, [[1.0, 0.7, 0.05, 0.98], [1.0, 0.7, 0.2, 0.95]], ([0, 0, 0, 0], [50, 10, 5, 0.9999]))]
for exp in ("exp1", "exp2"):
    Dx = forbes.load(exp); person = Dx["person"]
    # (2) kernel shapes, 5-fold CV over people
    z, mask = forbes.ratings(Dx); F, _ = forbes.features(Dx, "sign")
    people = np.unique(person); fold = dict(zip(np.random.default_rng(0).permutation(people), np.arange(len(people)) % 5))
    fo = np.array([fold[p] for p in person]); out = {}
    for nm, kf, starts, (lb, ub) in specs:
        sse = n = 0.0; ps = []
        for f in range(5):
            tr = fo != f
            obj = lambda p: fit(design_k(F[tr], kf(np.clip(p, lb, ub))), z[tr], mask[tr])[1]
            best = min((minimize(obj, s, method="Nelder-Mead", options=dict(xatol=1e-3, fatol=1e-6, maxiter=1500)) for s in starts), key=lambda r_: r_.fun)
            p = np.clip(best.x, lb, ub); ps.append(p)
            w = fit(design_k(F[tr], kf(p)), z[tr], mask[tr])[0]
            _, _, m, X, y = fit(design_k(F[~tr], kf(p)), z[~tr], mask[~tr]); sse += float(((y - X @ w) ** 2).sum()); n += m
        out[nm] = sse / n; pm = np.mean(ps, 0); k = kf(pm); neg = np.flatnonzero(k < 0)
        print(f"[{exp}] {nm}: CV MSE {sse / n:.5f}; mean params {np.round(pm, 3)}; k[1,5,20,52] {np.round(k[[1, 5, 20, 52]], 3)}; "
              f"first negative lag {neg[0] if len(neg) else 'none'}", flush=True)
    for a_, b_ in [("biphasic", "jump"), ("hyperbola - exp", "hyperbola")]:
        print(f"[{exp}] {a_} vs {b_}: {100 * (out[a_] / out[b_] - 1):+.2f}%")
