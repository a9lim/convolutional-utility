import os, sys, numpy as np, collections
from scipy.optimize import minimize
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import forbes
from gbe import fit
from run_forbes import best_kernel, cv_mse
T = 53
ell = np.arange(T, dtype=float)
def design_k(F, k):
    K = np.zeros((T, T))
    for t in range(T):
        K[t, :t + 1] = k[:t + 1][::-1]
    X = np.zeros((F.shape[0], T + 1, F.shape[2]))
    X[:, 1:] = np.einsum("ts,psk->ptk", K, F)
    return X
def cv_k(F, z, mask, person, kf, p0, b, folds=5):
    people = np.unique(person)
    fold = dict(zip(np.random.default_rng(0).permutation(people), np.arange(len(people)) % folds))
    f_of = np.array([fold[p] for p in person]); sse = n = 0.0; ps = []
    for f in range(folds):
        tr = f_of != f
        obj = lambda p: fit(design_k(F[tr], kf(np.clip(p, *b))), z[tr], mask[tr])[1]
        p = np.clip(minimize(obj, p0, method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-8)).x, *b)
        w = fit(design_k(F[tr], kf(p)), z[tr], mask[tr])[0]
        _, _, m, X, y = fit(design_k(F[~tr], kf(p)), z[~tr], mask[~tr])
        sse += float(((y - X @ w) ** 2).sum()); n += m; ps.append(p)
    return sse / n, np.mean(ps, 0)
for exp in ("exp1", "exp2"):
    D = forbes.load(exp); z, mask = forbes.ratings(D); person = D["person"]
    gaps = collections.Counter()
    for r in mask:
        pos_ = np.flatnonzero(r); gaps.update(np.diff(pos_))
    print(exp, "rating gaps", dict(gaps))
    F, names = forbes.features(D, "sign")
    out = {}
    for nm, kf, p0, b in [("geometric", lambda p: p[0] ** ell, [0.8], ([0], [0.999])),
                          ("jump", lambda p: np.r_[1, p[1] * p[0] ** ell[:-1]], [0.88, 0.5], ([0, 0], [0.999, 2])),
                          ("power 1p", lambda p: (1 + ell) ** -p[0], [0.8], ([0], [10])),
                          ("hyperbolic 2p", lambda p: (1 + p[0] * ell) ** -p[1], [2, 0.6], ([0, 0], [50, 10]))]:
        mse, p = cv_k(F, z, mask, person, kf, p0, b)
        out[nm] = mse
        print(f"   {nm}: CV MSE {mse:.5f} ({100*(mse/out['geometric']-1):+.2f}% vs geometric) params {np.round(p,3)}", flush=True)
    # spread regressor: lottery SD and half-range
    a1 = np.full(D["o"].shape, np.nan)
    # rebuild amounts/probs
    import csv, os
    rows = list(csv.DictReader(open(os.path.join(forbes.DATA, exp, "behav_data.csv"))))
    keys = sorted({(r["id"], int(r["block"])) for r in rows}); index = {k: i for i, k in enumerate(keys)}
    sd = np.zeros(D["o"].shape); prob = np.zeros(D["o"].shape)
    for r in rows:
        i, t = index[(r["id"], int(r["block"]))], int(r["trial"]) - 1
        x1, x2, p1, p2 = (float(r[k]) for k in ("chosen_amount_1", "chosen_amount_2", "chosen_prob_1", "chosen_prob_2"))
        sd[i, t] = np.sqrt(p1 * p2) * abs(x1 - x2); prob[i, t] = p1
    print("   prob values", np.unique(prob))
    o, ev = D["o"], D["ev"]; rpe = o - ev
    pos, neg = lambda x: np.maximum(x, 0), lambda x: np.minimum(x, 0)
    gam, kap = best_kernel(F, z, mask, True)
    for label, cols, nms in [("sign", [pos(o), neg(o), pos(rpe), neg(rpe)], ["paid+", "paid-", "RPE+", "RPE-"]),
                             ("sign + lottery SD", [pos(o), neg(o), pos(rpe), neg(rpe), sd], ["paid+", "paid-", "RPE+", "RPE-", "SD"]),
                             ("symmetric RPE + SD", [pos(o), neg(o), rpe, sd], ["paid+", "paid-", "RPE", "SD"]),
                             ("sign + |RPE|", [pos(o), neg(o), rpe, np.abs(rpe), sd], ["paid+", "paid-", "RPE", "|RPE|", "SD"])]:
        Fx = np.stack(cols, -1) / 100.0
        w, rss, n, _, _ = fit(forbes.design(Fx, gam, kap), z, mask)
        people = np.unique(person); groups = {p: np.flatnonzero(person == p) for p in people}
        rng = np.random.default_rng(0); B = []
        for _ in range(100):
            pick = np.concatenate([groups[p] for p in rng.choice(people, len(people))])
            B.append(fit(forbes.design(Fx[pick], gam, kap), z[pick], mask[pick])[0])
        B = np.array(B)
        print(f"   [{label}] RSS/n {rss/n:.5f}: " + ", ".join(f"{a} {b:+.3f} [{np.quantile(B[:,j],.025):+.3f},{np.quantile(B[:,j],.975):+.3f}]" for j, (a, b) in enumerate(zip(nms, w))))
