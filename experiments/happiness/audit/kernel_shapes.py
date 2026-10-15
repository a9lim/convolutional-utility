from lib import *
ell = np.arange(L, dtype=float)
F, names = gbe.features(D, "rpe")
res = {}
def errs(F, k, w):
    X = Xr(F, k)[test & GOOD]; y = Zr[test & GOOD]
    X = X - X.mean(1, keepdims=True); y = y - y.mean(1, keepdims=True)
    return ((y - X @ w) ** 2).sum(1)   # per-play SSE
for nm, kf, p0, b in [("Rutledge", lambda p: p[0] ** ell, [0.68], ([0], [0.999])),
                      ("jump", lambda p: jump_k(*p), [0.89, 0.41], ([0, 0], [0.999, 2])),
                      ("power 1p", lambda p: (1 + ell) ** -p[0], [0.8], ([0], [10])),
                      ("hyperbolic 2p", lambda p: (1 + p[0] * ell) ** -p[1], [2, 0.6], ([0, 0], [50, 10]))]:
    p, w, tr, te = evaluate(F, kf, p0, b)
    res[nm] = (te, errs(F, kf(p), w))
    print(f"[RPE by sign] {nm}: p {np.round(p,3)} test {te:.5f}", flush=True)
# paired bootstrap over test participants of MSE differences
subj = D["subj"][test & GOOD]
u, inv = np.unique(subj, return_inverse=True)
r = np.random.default_rng(3)
for a_, b_ in [("jump", "Rutledge"), ("power 1p", "jump"), ("hyperbolic 2p", "jump")]:
    d = np.bincount(inv, res[a_][1] - res[b_][1]); n = np.bincount(inv) * 12
    tot = res[b_][1].sum()
    bs = []
    for _ in range(500):
        i = r.integers(0, len(u), len(u))
        bs.append(d[i].sum() / res[b_][1][np.isin(inv, i)].sum() if False else d[i].sum() / (tot * len(i) / len(u)))
    bs = np.array(bs) * 100
    print(f"{a_} vs {b_}: {100*d.sum()/tot:+.3f}% [{np.quantile(bs,.025):+.3f}, {np.quantile(bs,.975):+.3f}]")
# per-version jump kernels (split none)
F0, _ = gbe.features(D, "none")
v = D["version"]
for grpn, sel in [("v1-2 (cursor at 50, ratio design)", v <= 2), ("v3-5 (random cursor, uncorrelated)", v >= 3)]:
    def obj(p):
        return fitX(Xr(F0, jump_k(*np.clip(p, 0, [0.999, 2]))), sel)[1]
    p = minimize(obj, [0.88, 0.42], method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-4)).x
    print(f"{grpn}: jump gamma {p[0]:.3f} kappa {p[1]:.3f}, B {p[1]/(1-p[0]+p[1]):.3f}")
