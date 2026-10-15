from lib import *
F, names = gbe.features(D, "none")
teR = 0.6604172644237672
ell = np.arange(L, dtype=float)
models = {
 "power (1+l)^-a [1p]": (lambda p: (1 + ell) ** -p[0], [1.0], ([0], [10])),
 "hyperbolic (1+h l)^-a [2p]": (lambda p: (1 + p[0] * ell) ** -p[1], [1.0, 1.0], ([0, 0], [50, 10])),
 "geometric + constant tail [2p]": (lambda p: (1 - p[1]) * p[0] ** ell + p[1], [0.5, 0.2], ([0, 0], [0.999, 1])),
 "double exponential [3p]": (lambda p: (1 - p[2]) * p[0] ** ell + p[2] * p[1] ** ell, [0.2, 0.9, 0.5], ([0, 0, 0], [0.999, 0.999, 1])),
}
for nm, (kf, p0, b) in models.items():
    p, w, tr, te = evaluate(F, kf, p0, b)
    k = kf(p)
    print(f"{nm}: p {np.round(p,3)} test {te:.5f} ({100*(te/teR-1):+.2f}% vs Rutledge); k[0:5] {np.round(k[:5],3)}", flush=True)
# free-lag shared kernel via ALS
tr = ~test
w = np.array([0.52, 0.33, 0.79]); k = jump_k(0.8815, 0.4188)
lagged = None
for it in range(15):
    c = F @ w                      # composite felt input, plays x 30
    # regress on lagged composite: column l = sum over rating rows of c[t-l]
    Xl = np.zeros((F.shape[0], len(ROWS), L))
    for i, t in enumerate(ROWS):
        if t == 0: continue
        for l in range(t + 1):
            Xl[:, i, l] = c[:, t - l]
    kk, rss, n = fitX(Xl, tr)
    k = kk / kk[0]
    w, rss2, n2 = fitX(Xr(F, k), tr)
    w = w * kk[0] / kk[0]
print("free kernel train MSE", rss2 / n2)
_, rsst, nt = fitX(Xr(F, k), test, w)
print(f"free kernel (29 free lags + 3 weights): test {rsst/nt:.5f} ({100*(rsst/nt/teR-1):+.2f}% vs Rutledge)")
print("free k lags 0..12:", np.round(k[:13], 3))
print("ratios k[l+1]/k[l]:", np.round(k[1:13] / k[:12], 3))
