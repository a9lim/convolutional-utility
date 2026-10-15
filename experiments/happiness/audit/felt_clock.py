"""Felt time at the trial scale: does momentary happiness forget by trials or by seconds, and does its forgetting
rate scale with age as one felt clock running from seconds to years would require?

Felt rate ds/dt proportional to age^-q (Janet q = 1; Lemlich, ds/dt proportional to 1/s, q = 1/2). If memory
were stationary in felt time and that clock also ran the seconds of a task, the forgetting rate per clock second
would scale as age^-q, and the kernel's shape would not change with age, only its time scale.

Kernel for a rating made after trial t, on the outcome of trial t - lag: k(0) = 1, and for lag >= 1
  base(lag) * exp(-theta T) * eta^G * rho^R,
base the jump kernel kappa gamma^(lag - 1) or the hyperbola (1 + h lag)^-a; G gambles resolved in between; R
ratings in between; T seconds, either the reconstructed variable seconds between the two outcomes (choice
latencies, spins, intervening rating times) or their deviation from what the play's own average speed predicts.
Fixed display times are unobserved; a fixed time per trial on an exponential clock is absorbed exactly by the
jump kernel's parameters, not by the hyperbola's.

Stages: pooled (which clock, held out, paired participant bootstrap); age (trials-only kernels per age band and
the age elasticity of their time scale, Poisson bootstrap over participants); within (per band, sensitivity to
within-play timing deviations); null (recovery under one homogeneous hyperbolic Lemlich clock); mixture (a fast
transient plus a slow mood in felt seconds, slowed by Janet's or Lemlich's factor, reproduces the age pattern).
Limits: the exponential clock factor times a hyperbola in trials is not a hyperbola in seconds; for a hyperbolic
felt clock the sensitivity to an extra second need not scale with the clock's speed; the recovery is one draw
without z-scoring or heterogeneity; the direct test, a scale family in elapsed seconds with an age-scaled rate
and the rating delay on the current trial, is not run here.
"""
import sys
import scipy.io
from multiprocessing import Pool
from lib import *

E = dict(np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "data", "gbe", "extra.npz")))
S = scipy.io.loadmat(gbe.MAT, struct_as_record=False, squeeze_me=True)["subjData"]
SUBJ = D["subj"]
AGE = np.array([np.atleast_1d(s.age)[0] for s in S])[SUBJ]
def _kept(s):
    d = s.data
    mats = [d] if isinstance(d, np.ndarray) and d.dtype != object else list(np.atleast_1d(d))
    return [j for j, X in enumerate(mats) if np.asarray(X).shape == (30, 15)]
TP = np.concatenate([np.atleast_1d(s.timesPlayed)[_kept(s)] for s in S])   # attempt number of each kept play
MID = np.array([np.nan, 21, 27, 34.5, 44.5, 54.5, 64.5, 75])
F, _ = gbe.features(D, "none")
g = D["g"]
CAP = 30.0                                                  # app backgrounded: latencies run to days
VALID = GOOD & (np.nanmin(E["lat"], 1) >= 0) & (np.nanmin(np.where(np.isnan(E["rrt"]), 0, E["rrt"]), 1) >= 0)
lat = np.minimum(E["lat"], CAP)
spin = np.where(g == 1, np.minimum(np.abs(np.nan_to_num(E["spin"])), 6.0), 0.0)
rated = np.zeros(L); rated[ROWS[1:]] = 1                   # a rating right after trial r (row 0 is pre-task)
rrt = np.minimum(np.nan_to_num(E["rrt"]), CAP) * rated
step = np.zeros_like(lat)
step[:, 1:] = lat[:, 1:] + spin[:, 1:] + rrt[:, :-1]        # seconds from outcome i - 1 to outcome i that vary
SEC = step[:, 1:].mean(1)                                   # the play's mean variable seconds per trial
mlat, mrrt = lat[:, 1:].mean(1), rrt[:, ROWS[1:-1]].mean(1)
mspin = np.where(g.sum(1) > 0, spin.sum(1) / np.maximum(g.sum(1), 1), 0.0)
C, Gc, Rc = np.cumsum(step, 1), np.cumsum(g, 1), np.r_[0.0, np.cumsum(rated)]
pairs = [(i, t, lag) for i, t in enumerate(ROWS) if t > 0 for lag in range(t + 1)]
LAG = np.array([p[2] for p in pairs], float)
DS = np.stack([C[:, t] - C[:, t - lag] for _, t, lag in pairs], 1).astype(np.float32)
GG = np.stack([Gc[:, t] - Gc[:, t - lag] for _, t, lag in pairs], 1).astype(np.float32)
RR = np.array([Rc[t] - Rc[t - lag] for _, t, lag in pairs], np.float32)   # ratings after trials t-lag .. t-1
U = DS - LAG * mlat[:, None] - GG * mspin[:, None] - RR * mrrt[:, None]
U = (U - U[~test & VALID].mean(0)).astype(np.float32)      # less the average drift at that position (speed-up)
FF = np.stack([F[:, t - lag] for _, t, lag in pairs], 1).astype(np.float32)
START = np.flatnonzero(np.r_[True, np.diff([p[0] for p in pairs]) != 0])
ELL = np.arange(L, dtype=float)
PAR = dict(gamma=lambda v: 1 / (1 + np.exp(-v)), kappa=np.exp, h=np.exp, a=np.exp, theta=lambda v: v,
           eta=np.exp, rho=np.exp)
INV = dict(gamma=lambda x: np.log(x / (1 - x)), kappa=np.log, h=np.log, a=np.log, theta=lambda x: x,
           eta=np.log, rho=np.log)
START_VALUES = dict(gamma=0.88, kappa=0.42, h=2.0, a=0.6, theta=0.0, eta=1.0, rho=1.0)


def base_k(m):
    if "h" in m:
        return (1 + m["h"] * ELL) ** -m["a"]
    return jump_k(m["gamma"], m["kappa"])


def design(m, sel, clock=None):
    """Regressors for plays sel (rows elsewhere zero). clock: None, "ds" (raw seconds) or "u" (deviation)."""
    X = np.zeros((len(sel), len(ROWS), F.shape[-1]))
    if clock is None and m.get("eta", 1) == 1 and m.get("rho", 1) == 1:
        X[sel] = Xr(F[sel], base_k(m))
        return X
    lw = np.log(base_k(m))[LAG.astype(int)][None, :] + GG[sel] * np.log(m.get("eta", 1.0)) + RR * np.log(m.get("rho", 1.0))
    if clock is not None:
        lw = lw - m["theta"] * (DS if clock == "ds" else U)[sel]
    W = np.exp(lw); W[:, LAG == 0] = 1.0
    X[sel, 1:] = np.add.reduceat(W[..., None] * FF[sel], START, axis=1)
    return X


def rss(X, sel, wt=None):
    """Within-play demeaned least squares on plays sel, optionally weighted per play."""
    ok = sel & VALID & ((wt > 0) if wt is not None else True)
    Xs, ys = X[ok], Zr[ok]
    Xs = Xs - Xs.mean(1, keepdims=True); ys = ys - ys.mean(1, keepdims=True)
    s = np.sqrt(wt[ok] if wt is not None else np.ones(ok.sum()))
    A = (Xs * s[:, None, None]).reshape(-1, Xs.shape[-1]); y = (ys * s[:, None]).reshape(-1)
    w = np.linalg.lstsq(A, y, rcond=None)[0]
    r = y - A @ w
    return float(r @ r), w


def fit(free, sel, fixed=None, clock=None, wt=None, start=None):
    fixed = dict(fixed or {})
    m0 = {**START_VALUES, **(start or {})}
    p0 = np.array([INV[n](m0[n]) for n in free])
    def model(p):
        return {**fixed, **{n: PAR[n](v) for n, v in zip(free, p)}}
    obj = lambda p: rss(design(model(p), sel, clock), sel, wt)[0]
    res = minimize(obj, p0, method="Nelder-Mead", options=dict(xatol=1e-5, fatol=1e-4, maxiter=4000, adaptive=True))
    return model(res.x), res


def sse_by_play(m, clock, w):
    """Held-out per-play SSE with weights w fitted on the training plays."""
    sel = test & VALID
    X = design(m, sel, clock)[sel]; y = Zr[sel]
    X = X - X.mean(1, keepdims=True); y = y - y.mean(1, keepdims=True)
    return ((y - X @ w) ** 2).sum(1)


def pooled():
    tr = ~test
    specs = [("jump", ["gamma", "kappa"], None), ("hyperbola", ["h", "a"], None),
             ("jump + seconds", ["gamma", "kappa", "theta"], "ds"), ("jump + deviation", ["gamma", "kappa", "theta"], "u"),
             ("hyperbola + seconds", ["h", "a", "theta"], "ds"), ("hyperbola + deviation", ["h", "a", "theta"], "u"),
             ("hyperbola + deviation + events", ["h", "a", "theta", "eta", "rho"], "u")]
    out = {}
    for name, free, clock in specs:
        m, res = fit(free, tr, clock=clock)
        _, w = rss(design(m, tr, clock), tr)
        e = sse_by_play(m, clock, w)
        out[name] = e
        par = {k: round(float(v), 4) for k, v in m.items() if k in free}
        print(f"{name:32s} held-out MSE {e.sum() / (12 * len(e)):.5f}  {par}  nit {res.nit} ok {res.success}", flush=True)
    subj = SUBJ[test & VALID]
    _, inv = np.unique(subj, return_inverse=True)
    r = np.random.default_rng(5)
    idx = [r.integers(0, inv.max() + 1, inv.max() + 1) for _ in range(1000)]
    for a_, b_ in [("hyperbola", "jump"), ("jump + seconds", "jump"), ("hyperbola + seconds", "hyperbola"),
                   ("hyperbola + deviation", "hyperbola"), ("hyperbola + deviation + events", "hyperbola")]:
        d, base = np.bincount(inv, out[a_] - out[b_]), np.bincount(inv, out[b_])
        bs = np.array([d[i].sum() / base[i].sum() for i in idx]) * 100
        print(f"  {a_} vs {b_}: {100 * d.sum() / base.sum():+.3f}% [{np.quantile(bs, .025):+.3f}, {np.quantile(bs, .975):+.3f}]")


def band_fits(wt, sel):
    """Trials-only kernels per age band: jump, free hyperbola, hyperbola with the pooled exponent."""
    a_pool = fit(["h", "a"], sel, wt=wt, start=dict(h=2.6, a=0.55))[0]["a"]
    rows = []
    for b in range(1, 8):
        sb = sel & (AGE == b)
        j = fit(["gamma", "kappa"], sb, wt=wt)[0]
        hf = fit(["h", "a"], sb, wt=wt, start=dict(h=2.6, a=0.55))[0]
        hs = fit(["h"], sb, fixed=dict(a=a_pool), wt=wt, start=dict(h=2.6))[0]
        sec = np.average(SEC[sb & VALID], weights=None if wt is None else wt[sb & VALID])
        rows.append((-np.log(j["gamma"]), j["kappa"], hf["h"], hf["a"], hs["h"], sec))
    return a_pool, np.array(rows)


def elasticity(y, sec, c0, bands):
    """Slope of log(y / (seconds per trial + c0)) on log age over the given bands: the estimate of q."""
    x = np.log(MID[1:][bands]); z = np.log(y[bands] / (sec[bands] + c0))
    return -np.polyfit(x, z, 1)[0]


def boot_band(seed):
    r = np.random.default_rng(seed)
    wt = r.poisson(1.0, SUBJ.max() + 1)[SUBJ].astype(float)
    return band_fits(wt, np.ones(len(SUBJ), bool))[1]


def age():
    allp = np.ones(len(SUBJ), bool)
    a_pool, R = band_fits(None, allp)
    print(f"pooled hyperbola exponent a = {a_pool:.3f}")
    print("band  mid   -ln gamma  kappa   h_free  a_free  h(shared a)  sec/trial")
    for b in range(7):
        print(f"{b + 1:4d} {MID[b + 1]:5.1f}  {R[b, 0]:.4f}   {R[b, 1]:.3f}   {R[b, 2]:.3f}   {R[b, 3]:.3f}   {R[b, 4]:.3f}      {R[b, 5]:.2f}")
    with Pool(12) as pool:
        B = np.array(pool.map(boot_band, range(48)))
    six, seven = np.arange(6), np.arange(7)
    for label, col in [("jump decay -ln gamma", 0), ("hyperbola scale h, shared exponent", 4)]:
        for c0 in (0.0, 1.5):
            for bands, bl in [(six, "18-69"), (seven, "18-70+")]:
                q = elasticity(R[:, col], R[:, 5], c0, bands)
                qb = np.array([elasticity(Bk[:, col], Bk[:, 5], c0, bands) for Bk in B])
                print(f"q from {label:36s} c0={c0:.1f} {bl:6s}: {q:.3f} [{np.quantile(qb, .025):.3f}, {np.quantile(qb, .975):.3f}]")
    print("free hyperbola exponent a by band, bootstrap 95%:",
          [f"{R[b, 3]:.3f} [{np.quantile(B[:, b, 3], .025):.3f}, {np.quantile(B[:, b, 3], .975):.3f}]" for b in range(7)])
    for name, sel in [("first attempt (timesPlayed 1)", TP == 1), ("design v3-5", D["version"] >= 3)]:
        _, Rs = band_fits(None, sel)
        print(f"{name}: q (jump, c0=0, 18-69) {elasticity(Rs[:, 0], Rs[:, 5], 0.0, six):.3f};"
              f" q (hyperbola, shared a) {elasticity(Rs[:, 4], Rs[:, 5], 0.0, six):.3f}")


def within_band(args):
    b, seed = args
    wt = None
    if seed is not None:
        wt = np.random.default_rng(seed).poisson(1.0, SUBJ.max() + 1)[SUBJ].astype(float)
    m, _ = fit(["h", "a", "theta", "eta", "rho"], AGE == b, clock="u", wt=wt,
               start=dict(h=2.6, a=0.55, theta=0.01, eta=0.97, rho=1.1))
    return b, m["theta"], m["h"], m["a"]


def within():
    with Pool(14) as pool:
        point = pool.map(within_band, [(b, None) for b in range(1, 8)])
        boot = pool.map(within_band, [(b, s) for s in range(16) for b in range(1, 8)])
    th = {b: [t for bb, t, _, _ in boot if bb == b] for b in range(1, 8)}
    for b, t, h, a in point:
        print(f"band {b} ({MID[b]:.1f}): theta per second of deviation {t:+.4f} "
              f"[{np.quantile(th[b], .025):+.4f}, {np.quantile(th[b], .975):+.4f}]  h {h:.3f} a {a:.3f}")
    x = np.log(MID[1:7]); t = np.array([p[1] for p in point])[:6]
    if (t > 0).all():
        print("q from within-play theta, 18-69:", round(-np.polyfit(x, np.log(t), 1)[0], 3))


def null():
    """Recovery check: ratings simulated from a pure felt clock, a hyperbola in felt seconds with rate
    (age/35)^-1/2 and c0 = 1 s of fixed time per trial, on the real trials, timings and regressor weights. The age
    fits should then return one exponent at every age and a scale falling with age (q near 1/2)."""
    allp = np.ones(len(SUBJ), bool)
    m = dict(h=2.0, a=0.6)
    w = rss(design(m, allp), allp)[1]
    hs, c0 = m["h"] / (SEC[VALID].mean() + 1.0), 1.0
    T = (DS + c0 * LAG) * ((MID[AGE] / 35.0) ** -0.5)[:, None]
    W = (1 + hs * T) ** -m["a"]; W[:, LAG == 0] = 1.0
    X = np.zeros((len(SUBJ), len(ROWS), F.shape[-1]))
    X[:, 1:] = np.add.reduceat(W[..., None] * FF, START, axis=1)
    Zr[:] = X @ w + np.random.default_rng(7).normal(0, np.sqrt(0.7), Zr.shape)
    a_pool, R = band_fits(None, allp)
    print(f"simulated pure Lemlich clock: pooled exponent {a_pool:.3f}")
    print("band  free exponent a   h(shared a)   -ln gamma")
    for b in range(7):
        print(f"{b + 1:4d}   {R[b, 3]:.3f}            {R[b, 4]:.3f}         {R[b, 0]:.4f}")
    six = np.arange(6)
    print(f"recovered q (hyperbola, shared a, c0=1) {elasticity(R[:, 4], R[:, 5], 1.0, six):.3f};"
          f" (jump, c0=1) {elasticity(R[:, 0], R[:, 5], 1.0, six):.3f}")


def mixture():
    """No data: a fast transient plus a slow mood, K(T) = 0.6 exp(-0.5 T) + 0.4 exp(-0.015 T), T seconds from
    outcome to rating (3 s for the current trial, 7.3 s per trial), weights relative to the current trial. A
    slower clock leaves the current outcome more of its transient, so lag 1 falls relative to it while the tail
    lengthens, the age pattern in the data."""
    from scipy.optimize import curve_fit
    T = 3.0 + 7.3 * ELL
    for r, lab in [(1.0, "age 21"), ((64.5 / 21) ** -0.5, "64.5, Lemlich"), (21 / 64.5, "64.5, Janet")]:
        k = 0.6 * np.exp(-0.5 * r * T) + 0.4 * np.exp(-0.015 * r * T); k = k / k[0]
        (h, a), _ = curve_fit(lambda l, h, a: (1 + h * l) ** -a, ELL, k, p0=[2, .6], bounds=([0, 0], [100, 10]))
        print(f"{lab:14s} k1 {k[1]:.3f} k5 {k[5]:.3f} k10 {k[10]:.3f} k20 {k[20]:.3f}; trial hyperbola h {h:.2f} a {a:.3f}")


if __name__ == "__main__":
    print("plays", len(SUBJ), "valid", int(VALID.sum()), flush=True)
    {"pooled": pooled, "age": age, "within": within, "null": null, "mixture": mixture}[sys.argv[1]]()
