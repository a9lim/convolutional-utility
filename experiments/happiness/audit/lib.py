import os, sys, numpy as np
from scipy.optimize import minimize
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import gbe
D = gbe.load()
z, mask = gbe.ratings(D, np.ones(len(D["subj"]), bool))
rng = np.random.default_rng(0)
subjects = np.unique(D["subj"])
test = np.isin(D["subj"], rng.choice(subjects, len(subjects) // 5, replace=False))
ROWS = np.array([0, 2, 5, 8, 10, 13, 16, 19, 21, 24, 27, 29])
L = 30
def toeplitz(k):
    K = np.zeros((L, L))
    for t in range(L):
        K[t, :t + 1] = k[:t + 1][::-1]
    K[0] = 0.0  # pre-task rating sees nothing
    return K[ROWS]
def Xr(F, k):
    return np.einsum("rt,ptk->prk", toeplitz(k), F)
Zr = z[:, ROWS]
GOOD = ~np.isnan(Zr).any(1)
print("plays with partial NaN:", int((np.isnan(Zr).any(1) & ~np.isnan(Zr).all(1)).sum()), "dropped:", int((~GOOD).sum()))
def fitX(X, sel, w=None):
    """within-play demeaned LS on plays sel; X plays x 12 x k. returns w, rss, n"""
    sel = sel & GOOD
    Xs, ys = X[sel], Zr[sel]
    Xs = Xs - Xs.mean(1, keepdims=True); ys = ys - ys.mean(1, keepdims=True)
    A = Xs.reshape(-1, Xs.shape[-1]); y = ys.reshape(-1)
    if w is None:
        w = np.linalg.lstsq(A, y, rcond=None)[0]
    r = y - A @ w
    return w, float(r @ r), len(y)
def jump_k(gam, kap):
    k = np.r_[1.0, kap * gam ** np.arange(L - 1)]
    return k
def evaluate(F, kfun, p0, bounds=None):
    tr = ~test
    def obj(p):
        if bounds is not None:
            p = np.clip(p, bounds[0], bounds[1])
        return fitX(Xr(F, kfun(p)), tr)[1]
    res = minimize(obj, p0, method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-4, maxiter=2000))
    p = res.x if bounds is None else np.clip(res.x, bounds[0], bounds[1])
    w, rss, n = fitX(Xr(F, kfun(p)), tr)
    _, rsst, nt = fitX(Xr(F, kfun(p)), test, w)
    return p, w, rss / n, rsst / nt
