from lib import *
E = dict(np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "data", "gbe", "extra.npz")))
F, names = gbe.features(D, "none")
g, k = 0.88152977, 0.41878555
w = np.array([0.52010725, 0.33389943, 0.78889811])
c = F @ w
gam = D["g"]
lat = np.log(E["lat"]); lat = (lat - np.nanmean(lat)) / np.nanstd(lat); lat = np.nan_to_num(lat)
gap2rows = {10, 21, 29}
def build(extra=True):
    cols = []
    X = np.zeros((F.shape[0], len(ROWS), L + 5))
    for i, t in enumerate(ROWS):
        if t == 0: continue
        for l in range(t + 1):
            X[:, i, l] = c[:, t - l]
        if extra and t >= 1:
            X[:, i, L] = c[:, t - 1] * gam[:, t]                 # lag-1 input x lag-0 trial was a gamble (spinner ~4.4 s)
            X[:, i, L + 1] = c[:, t - 1] * lat[:, t]             # lag-1 input x lag-0 choice latency (z log s)
            X[:, i, L + 2] = c[:, t] * gam[:, t]                 # lag-0 input x lag-0 was a gamble
            X[:, i, L + 3] = c[:, t - 1] * lat[:, t] * (1 - gam[:, t])   # latency effect within safe lag-0 trials
        if extra and t >= 2:
            X[:, i, L + 4] = c[:, t - 2] * (t in gap2rows)       # lag-2 input when lag-2 trial preceded the previous rating
    return X
X = build()
allp = np.ones(len(D["subj"]), bool)
kk, rss, n = fitX(X, allp)
print("free lags 0..5 (unnormalized):", np.round(kk[:6], 3))
lab = ["lag1 x lag0-gamble", "lag1 x lag0-latency", "lag0 x lag0-gamble", "lag1 x latency (safe lag0)", "lag2 x gap2 (boundary)"]
order = np.argsort(D["subj"], kind="stable")
grp = np.split(order, np.flatnonzero(np.diff(D["subj"][order])) + 1)
B = []
r = np.random.default_rng(1)
for b in range(20):
    pick = np.concatenate([grp[i] for i in r.integers(0, len(grp), len(grp))])
    Xs = X[pick]; ys = Zr[pick]; ok = GOOD[pick]
    Xs, ys = Xs[ok], ys[ok]
    Xs = Xs - Xs.mean(1, keepdims=True); ys = ys - ys.mean(1, keepdims=True)
    B.append(np.linalg.lstsq(Xs.reshape(-1, Xs.shape[-1]), ys.reshape(-1), rcond=None)[0])
B = np.array(B); se = B.std(0)
for j, nm in enumerate(lab):
    print(f"{nm}: {kk[L+j]:+.4f} (SE {se[L+j]:.4f})  relative to lag-1 weight {kk[1]:.3f} / lag-2 {kk[2]:.3f}")
print("lag0..3 SEs", np.round(se[:4], 4))
