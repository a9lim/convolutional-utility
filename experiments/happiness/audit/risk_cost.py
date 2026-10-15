from lib import *
g, k = 0.888, 0.413
K = jump_k(g, k)
G = D["g"]; ev = (D["w"] + D["l"]) / 2
paid = (1 - G) * D["c"] + G * D["o"]
pos, neg = lambda x: np.maximum(x, 0), lambda x: np.minimum(x, 0)
def cols(rho, dummy):
    u = np.sign(paid) * (np.abs(paid) / 100.0) ** rho * 100.0
    ue = G * (np.sign(D["w"]) * (np.abs(D["w"]) / 100) ** rho * 100 + np.sign(D["l"]) * (np.abs(D["l"]) / 100) ** rho * 100) / 2
    ur = G * u - ue
    c = [pos(u), neg(u), ue, pos(ur), neg(ur)] + ([G * 100.0] if dummy else [])
    return Xr(np.stack(c, -1) / 100.0, K)
order = np.argsort(D["subj"], kind="stable")
grp = np.split(order, np.flatnonzero(np.diff(D["subj"][order])) + 1)
trs = np.flatnonzero(~test[[gg[0] for gg in grp]])
r = np.random.default_rng(2)
picks = [np.concatenate([grp[i] for i in r.choice(trs, len(trs))]) for _ in range(30)]
base_te = None
for rho, dummy in [(1.0, False), (1.0, True), (0.8, False), (0.8, True), (0.7, True)]:
    X = cols(rho, dummy)
    w, rss, n = fitX(X, ~test)
    _, rt, nt = fitX(X, test, w)
    if base_te is None: base_te = rt / nt
    lam = w[4] / w[3]; a = w[2] / w[0]
    bs = []
    for p in picks:
        sel = np.zeros(len(D["subj"]), bool)  # use index arrays directly
        Xs, ys = X[p][GOOD[p]], Zr[p][GOOD[p]]
        Xs = Xs - Xs.mean(1, keepdims=True); ys = ys - ys.mean(1, keepdims=True)
        wb = np.linalg.lstsq(Xs.reshape(-1, Xs.shape[-1]), ys.reshape(-1), rcond=None)[0]
        bs.append([wb[4] / wb[3], wb[2] / wb[0]] + ([wb[5]] if dummy else [0]))
    bs = np.array(bs)
    q = lambda c: f"[{np.quantile(bs[:, c], .025):.2f}, {np.quantile(bs[:, c], .975):.2f}]"
    print(f"rho {rho} dummy {dummy}: test MSE {rt/nt:.6f} ({100*(rt/nt/base_te-1):+.3f}% vs repo structural); lam {lam:.2f} {q(0)}, a {a:+.2f} {q(1)}" + (f", gambled {w[5]:+.4f} SD per gamble" if dummy else ""), flush=True)
