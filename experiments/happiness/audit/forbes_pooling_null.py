import os, sys, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import forbes
from gbe import fit
from run_forbes import best_kernel
ggrid = np.arange(0.0, 0.96, 0.05)
grid = [(g, k) for g in ggrid for k in np.arange(0.0, 1.01, 0.05)]
def own_grid(F, z, mask, i):
    return min(grid, key=lambda gk: fit(forbes.design(F[i], *gk), z[i], mask[i])[1])
def fitted(F, z, mask, i, g, k):
    X = forbes.design(F[i], g, k); zz = z[i]; mm = mask[i]
    w = fit(X, zz, mm)[0]
    pred = X @ w
    # add back block means: demeaned fit -> reconstruct per block
    out = np.full(zz.shape, np.nan)
    for b in range(len(i)):
        m = mm[b]
        r = zz[b, m] - pred[b, m]
        out[b, m] = pred[b, m] + r.mean()
    resid = np.where(mm, zz - out, np.nan)
    return out, np.nanstd(resid)
for exp in ("exp1", "exp2"):
    D = forbes.load(exp); z, mask = forbes.ratings(D); person = D["person"]
    F, _ = forbes.features(D, "sign")
    people = np.unique(person); groups = {p: np.flatnonzero(person == p) for p in people}
    rng = np.random.default_rng(0)
    zsim = np.full_like(z, np.nan); own_geo = []
    for p in people:
        i = groups[p]
        g = min(ggrid, key=lambda g: fit(forbes.design(F[i], g, g), z[i], mask[i])[1])
        own_geo.append(g)
        mu, sd = fitted(F, z, mask, i, g, g)
        zsim[i] = np.where(mask[i], mu + rng.normal(0, sd, mu.shape), np.nan)
    own_geo = np.array(own_geo)
    print(f"[{exp}] per-person geometric gamma: median {np.median(own_geo):.2f}, IQR {np.quantile(own_geo,.25):.2f}-{np.quantile(own_geo,.75):.2f}")
    # pooled fit on null data (each person geometric, heterogeneous)
    gj, kj = best_kernel(F, zsim, mask, True)
    gg, _ = best_kernel(F, zsim, mask, False)
    rj = fit(forbes.design(F, gj, kj), zsim, mask)[1]; rg = fit(forbes.design(F, gg, gg), zsim, mask)[1]
    print(f"   null (per-person geometric): pooled jump gamma {gj:.3f} kappa {kj:.3f} B {kj/(1-gj+kj):.2f}; pooled geometric {gg:.3f}; jump in-sample RSS {100*(rj/rg-1):+.2f}% vs geometric")
    own = np.array([own_grid(F, zsim, mask, groups[p]) for p in people])
    print(f"   null per-person jump grid: kappa below gamma by >0.05 in {np.mean(own[:,1] < own[:,0]-0.05):.0%}, above in {np.mean(own[:,1] > own[:,0]+0.05):.0%}")
    # same on real data for reference
    ownr = np.array([own_grid(F, z, mask, groups[p]) for p in people])
    Br = ownr[:, 1] / (1 - ownr[:, 0] + ownr[:, 1])
    print(f"   real per-person: below {np.mean(ownr[:,1] < ownr[:,0]-0.05):.0%}, above {np.mean(ownr[:,1] > ownr[:,0]+0.05):.0%}; B median {np.median(Br):.2f}")
