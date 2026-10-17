from lib import *
G = D["g"]; ev = (D["w"] + D["l"]) / 2
paid = (1 - G) * D["c"] + G * D["o"]
F = np.stack([paid, G * ev, G * (D["o"] - ev)], -1) / 100.0
names = ["paid (base)", "EV (anticipation)", "RPE (news only, base in paid)"]
tr = ~test
def Xc(par, F):
    return np.stack([Xr(F[..., c:c + 1], jump_k(*par[c]))[..., 0] for c in range(3)], -1)
def descend(par, rss, sweeps=4):
    par = np.array(par, float)
    for sweep in range(sweeps):
        for c in range(3):
            def obj(p, c=c):
                q = par.copy(); q[c] = np.clip(p, [0, 0], [0.999, 3]); return rss(q)
            par[c] = np.clip(minimize(obj, par[c], method="Nelder-Mead", options=dict(xatol=1e-3, fatol=1e-5)).x, [0, 0], [0.999, 3])
    return par
# two optima: persistent news (reached from the generic start) and persistent base with fast news
starts = {"generic start": [[0.88, 0.42]] * 3, "slow-base start": [[0.95, 0.40], [0.95, 0.25], [0.47, 0.69]]}
opt = {}
for nm, p0 in starts.items():
    par = descend(p0, lambda q: fitX(Xc(q, F), tr)[1])
    w, rss, n = fitX(Xc(par, F), tr); _, rt, nt = fitX(Xc(par, F), test, w)
    opt[nm] = par
    print(f"{nm}: train {rss/n:.6f} test {rt/nt:.6f} |", "; ".join(f"{c}: gamma {g:.3f} kappa {k:.3f} weight {ww:+.3f}" for c, (g, k), ww in zip(names, par, w)))
# bootstrap over participants: refit from both optima per resample, and record which fits better
order = np.argsort(D["subj"], kind="stable")
grp = np.split(order, np.flatnonzero(np.diff(D["subj"][order])) + 1)
trs = np.flatnonzero(~test[[gg[0] for gg in grp]])
r = np.random.default_rng(4); diffs = []
for b in range(8):
    pick = np.concatenate([grp[i] for i in r.choice(trs, len(trs))])
    Fp, Zs, Gs = F[pick], Zr[pick], GOOD[pick]
    def rssp(q):
        X = Xc(q, Fp)[Gs]; y = Zs[Gs]
        X = X - X.mean(1, keepdims=True); y = y - y.mean(1, keepdims=True)
        A = X.reshape(-1, 3); yy = y.reshape(-1)
        ww = np.linalg.lstsq(A, yy, rcond=None)[0]; return ((yy - A @ ww) ** 2).sum()
    res = {nm: descend(p, rssp, sweeps=2) for nm, p in opt.items()}
    d = rssp(res["generic start"]) - rssp(res["slow-base start"])
    diffs.append(d)
    print(b, " | ".join(f"{nm}: news gamma {p[2][0]:.3f}, base gamma {p[0][0]:.3f}" for nm, p in res.items()), f"| RSS(persistent news) - RSS(fast news) {d:+.2f}", flush=True)
print(f"fast news fits better in {sum(d > 0 for d in diffs)}/{len(diffs)} resamples; mean RSS difference {np.mean(diffs):+.2f} (total RSS ~{fitX(Xc(opt['generic start'], F), tr)[1]:.0f})")
