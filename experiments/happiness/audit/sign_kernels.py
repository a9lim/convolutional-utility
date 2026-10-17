"""Does memory treat gains and losses alike? Local optima of the shared fit (with and without a
gambled dummy, from two starts), then split the paid kernel by sign starting from the best shared solution."""
import functools
print = functools.partial(print, flush=True)
from lib import *
G = D["g"]; ev = (D["w"] + D["l"]) / 2
paid = (1 - G) * D["c"] + G * D["o"]
pos, neg = lambda x: np.maximum(x, 0), lambda x: np.minimum(x, 0)
rpe = G * (D["o"] - ev); EV = G * ev
FULL = np.stack([pos(paid), neg(paid), pos(EV), neg(EV), pos(rpe), neg(rpe), G * 100.0], -1) / 100.0
NAMES = ["paid+", "paid-", "EV+", "EV-", "RPE+", "RPE-", "gambled"]
tr = ~test
def Xc(par, F, gr):
    out = [None] * F.shape[-1]
    for gi, cols in enumerate(gr):
        Xg = Xr(F[..., cols], jump_k(*par[gi]))
        for j, c in enumerate(cols): out[c] = Xg[..., j]
    return np.stack(out, -1)
def fit(F, gr, par, sweeps=4, only=None):
    par = np.array(par, float)
    for sweep in range(sweeps):
        for gi in (range(len(gr)) if only is None else only):
            def obj(p, gi=gi):
                q = par.copy(); q[gi] = np.clip(p, [0, 0], [0.999, 3]); return fitX(Xc(q, F, gr), tr)[1]
            par[gi] = np.clip(minimize(obj, par[gi], method="Nelder-Mead", options=dict(xatol=1e-3, fatol=1e-5)).x, [0, 0], [0.999, 3])
    w, rss, n = fitX(Xc(par, F, gr), tr)
    _, rt, nt = fitX(Xc(par, F, gr), test, w)
    return par, w, rss / n, rt / nt
mass = lambda g, k, J=29: k * (1 - g ** J) / (1 - g)
def show(tag, gr, names, par, w, trm, tem):
    print(f"\n== {tag}: train {trm:.6f} test {tem:.6f}")
    for gi, cols in enumerate(gr):
        print(f"  kernel {'+'.join(names[c] for c in cols):12s} gamma {par[gi][0]:.3f} kappa {par[gi][1]:.3f} mass {mass(*par[gi]):.2f}")
    print("  weights: " + "  ".join(f"{nm} {ww:+.3f}" for nm, ww in zip(names, w)))
NK = {"paid": [0.786, 0.558], "EV": [0.732, 0.616], "RPE": [0.999, 0.274], "gam": [0.888, 0.413]}  # news_kernel.py's solution
# A: no dummy, shared paid kernel, two starts
F6, n6, grA = FULL[..., :6], NAMES[:6], [[0, 1], [2, 3], [4, 5]]
best = {}
for start, p0 in [("default", [[0.88, 0.42]] * 3), ("news_kernel", [NK["paid"], NK["EV"], NK["RPE"]])]:
    r = fit(F6, grA, p0); show(f"A no dummy, start {start}", grA, n6, *r)
# B: dummy, shared paid kernel, two starts; keep the better train fit
grB = [[0, 1], [2, 3], [4, 5], [6]]
for start, p0 in [("default", [[0.88, 0.42]] * 4), ("news_kernel", [NK["paid"], NK["EV"], NK["RPE"], NK["gam"]])]:
    r = fit(FULL, grB, p0); show(f"B dummy, start {start}", grB, NAMES, *r)
    if "B" not in best or r[2] < best["B"][2]: best["B"] = r
parB, wB = best["B"][0], best["B"][1]
print(f"\n  best B: base ratio {wB[1]/wB[0]:.2f}; news lam {wB[5]/wB[4]:.2f}")
# C: split paid kernel by sign, initialized at best B (nested, so train cannot get worse)
grC = [[0], [1], [2, 3], [4, 5], [6]]
p0 = np.vstack([parB[0], parB[0], parB[1:]])
parC, wC, trC, teC = fit(FULL, grC, p0)
show("C paid kernel split by sign, from best B", grC, NAMES, parC, wC, trC, teC)
m1, m2 = mass(*parC[0]), mass(*parC[1])
print(f"  base ratio immediate {wC[1]/wC[0]:.2f}; echo {wC[1]*m2/(wC[0]*m1):.2f}; total {wC[1]*(1+m2)/(wC[0]*(1+m1)):.2f}")
print(f"  lag-j sign ratio of the echo, j=1,5,10,20: " + " ".join(f"{wC[1]*parC[1][1]*parC[1][0]**(j-1)/(wC[0]*parC[0][1]*parC[0][0]**(j-1)):.2f}" for j in (1, 5, 10, 20)))
# bootstrap C over participants: refit paid+ and paid- kernels per resample, others held
order = np.argsort(D["subj"], kind="stable")
grp = np.split(order, np.flatnonzero(np.diff(D["subj"][order])) + 1)
trs = np.flatnonzero(~test[[gg[0] for gg in grp]])
r = np.random.default_rng(5); bs = []
for b in range(16):
    pick = np.concatenate([grp[i] for i in r.choice(trs, len(trs))])
    Fp, Zs, Gs = FULL[pick], Zr[pick], GOOD[pick]
    def fitp(q, ret=False):
        X = Xc(q, Fp, grC)[Gs]; y = Zs[Gs]
        X = X - X.mean(1, keepdims=True); y = y - y.mean(1, keepdims=True)
        A = X.reshape(-1, X.shape[-1]); yy = y.reshape(-1)
        ww = np.linalg.lstsq(A, yy, rcond=None)[0]
        return ww if ret else ((yy - A @ ww) ** 2).sum()
    q = parC.copy()
    for sweep in range(2):
        for gi in (0, 1):
            def obj(p, gi=gi):
                qq = q.copy(); qq[gi] = np.clip(p, [0, 0], [0.999, 3]); return fitp(qq)
            q[gi] = np.clip(minimize(obj, q[gi], method="Nelder-Mead", options=dict(xatol=1e-3, fatol=1e-5)).x, [0, 0], [0.999, 3])
    ww = fitp(q, True); a1, a2 = mass(*q[0]), mass(*q[1])
    bs.append([ww[1] / ww[0], ww[1] * a2 / (ww[0] * a1), ww[1] * (1 + a2) / (ww[0] * (1 + a1)), a1, a2, q[0][0], q[1][0]])
    print(b, np.round(bs[-1], 3))
bs = np.array(bs)
for c, nm in enumerate(["immediate ratio", "echo ratio", "total ratio", "mass+", "mass-", "gamma+", "gamma-"]):
    print(f"  {nm}: {np.mean(bs[:, c]):.3f}, 2.5-97.5% [{np.quantile(bs[:, c], .025):.3f}, {np.quantile(bs[:, c], .975):.3f}]")
print("DONE")
