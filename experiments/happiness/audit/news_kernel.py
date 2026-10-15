from lib import *
G = D["g"]; ev = (D["w"] + D["l"]) / 2
paid = (1 - G) * D["c"] + G * D["o"]
F = np.stack([paid, G * ev, G * (D["o"] - ev)], -1) / 100.0
names = ["paid (base)", "EV (anticipation)", "RPE (news only, base in paid)"]
tr = ~test
par = np.array([[0.88, 0.42]] * 3)
def Xc(par, F):
    return np.stack([Xr(F[..., c:c + 1], jump_k(*par[c]))[..., 0] for c in range(3)], -1)
for sweep in range(3):
    for c in range(3):
        def obj(p, c=c):
            q = par.copy(); q[c] = np.clip(p, [0, 0], [0.999, 3]); return fitX(Xc(q, F), tr)[1]
        par[c] = np.clip(minimize(obj, par[c], method="Nelder-Mead", options=dict(xatol=1e-3, fatol=1e-4)).x, [0, 0], [0.999, 3])
w, rss, n = fitX(Xc(par, F), tr)
print("per-component jump kernels:", "; ".join(f"{nm}: gamma {g:.3f} kappa {k:.3f} weight {ww:+.3f}" for nm, (g, k), ww in zip(names, par, w)))
# bootstrap the news component's kernel quickly: 8 resamples, news kernel only, others held
order = np.argsort(D["subj"], kind="stable")
grp = np.split(order, np.flatnonzero(np.diff(D["subj"][order])) + 1)
trs = np.flatnonzero(~test[[gg[0] for gg in grp]])
r = np.random.default_rng(4); bs = []
for b in range(8):
    pick = np.concatenate([grp[i] for i in r.choice(trs, len(trs))])
    Fp = F[pick]; sel = np.ones(len(pick), bool)
    Zs, Gs = Zr[pick], GOOD[pick]
    def fitp(q):
        X = Xc(q, Fp)[Gs]; y = Zs[Gs]
        X = X - X.mean(1, keepdims=True); y = y - y.mean(1, keepdims=True)
        A = X.reshape(-1, 3); yy = y.reshape(-1)
        ww = np.linalg.lstsq(A, yy, rcond=None)[0]; return ((yy - A @ ww) ** 2).sum()
    out = []
    for c in range(3):
        def obj(p, c=c):
            q = par.copy(); q[c] = np.clip(p, [0, 0], [0.999, 3]); return fitp(q)
        out.append(np.clip(minimize(obj, par[c], method="Nelder-Mead", options=dict(xatol=1e-3, fatol=1e-4)).x, [0, 0], [0.999, 3]))
    bs.append(np.ravel(out)); print(b, np.round(bs[-1], 3), flush=True)
bs = np.array(bs)
print("bootstrap SD (gamma,kappa) per component:", np.round(bs.std(0), 3))
