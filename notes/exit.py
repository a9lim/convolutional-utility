"""Checks for notes/death.md, chosen dates: the momentary exit under a Markov mood.
Run: python notes/exit.py (several minutes: the memory solves)

A mood follows an AR(1) on a Tauchen grid with mean 1; the self at t exits (dies after t) or continues.
markov_exit(): no memory, state (previous mood, mood); memory_exit(): geometric memory, state
(previous mood, mood, memory stock H_t = sum_j mu^j e_{t-j}) with H on a grid, interpolated. References are
the previous self's forecasts given it continued; news is kinked per horizon (core X4).
"""
import numpy as np

LIFE = dict(a=0.064, al=0.7, m=0.4, mu=0.3, n=0.2, nu=0.7)     # calibration.md, a week


def report(name, err, tol):
    print(f"{'PASS' if err < tol else 'FAIL'}  {name}  (max err {err:.2e})")


# 1. No memory (m = 0): the exit policy over (previous, current) moods as a fixed point, and the
#    expected lifespan from the stationary mood, a first-passage time.
def tauchen(N, rho, sd, mean=1.0, width=3.0):
    from scipy.special import ndtr
    grid = np.linspace(-width * sd, width * sd, N)
    se, h = sd * np.sqrt(1 - rho ** 2), grid[1] - grid[0]
    z = grid[None, :] - rho * grid[:, None]
    up = np.where(np.arange(N) < N - 1, ndtr((z + h / 2) / se), 1.0)
    lo = np.where(np.arange(N) > 0, ndtr((z - h / 2) / se), 0.0)
    return mean + grid, up - lo


def markov_exit(u, Pi, lam, a, al, n, nu, J=90, X0=None, damp=0.5, **_):
    """Returns (felt states e[sp, s], exit policy X[sp, s], forecasts F[j-1, s] given continuing)."""
    N = len(u)
    ka, kn = a * al ** np.arange(1, J + 1), n * nu ** np.arange(0, J + 1)
    phi = lambda x: np.where(x >= 0, x, lam * x)
    h0 = lambda Xv, Rv: np.where((Xv - n * Rv) / (1 - n) >= Rv, (Xv - n * Rv) / (1 - n),
                                 (Xv - lam * n * Rv) / (1 - lam * n))   # e = Xv + n phi(e - Rv)
    X = np.zeros((N, N), bool) if X0 is None else X0.copy()
    e = np.tile(u, (N, 1)).astype(float)
    for _ in range(200):
        for _ in range(4000):
            F = np.zeros((J + 1, N))
            F[0] = (Pi * e).sum(1)
            for j in range(1, J + 1):
                F[j] = (Pi * ~X) @ F[j - 1]
            ec = h0(u[None, :] + (ka @ F[:J])[None, :]
                    + (kn[1:, None, None] * phi(F[:J, None, :] - F[1:, :, None])).sum(0), F[0][:, None])
            ee = h0(u[None, :] + (kn[1:, None, None] * phi(-F[1:, :, None])).sum(0), F[0][:, None])
            new = np.where(X, ee, ec)
            err = np.max(np.abs(new - e))
            e = damp * new + (1 - damp) * e
            if err < 1e-11:
                break
        else:
            raise RuntimeError(f"felt states did not converge, err {err:.1e}")
        Xn = ee > ec + 1e-12
        if np.array_equal(Xn, X):
            return e, X, F, ee - ec
        X = Xn
    raise RuntimeError("policy cycle")


def lifespan(Pi, X):
    """Expected periods lived from the stationary mood: absorbing chain over pairs."""
    N = len(Pi)
    if not X.any():
        return np.inf
    w, v = np.linalg.eig(Pi.T)
    pi = np.real(v[:, np.argmin(abs(w - 1))])
    pi /= pi.sum()
    A = np.eye(N * N)
    for sp in range(N):
        for s in range(N):
            if not X[sp, s]:
                A[sp * N + s, s * N:(s + 1) * N] -= Pi[s]
    return (pi[:, None] * Pi).ravel() @ np.linalg.solve(A, np.ones(N * N))


MOOD = dict(a=LIFE["a"], al=LIFE["al"], n=LIFE["n"], nu=LIFE["nu"])
J_ = 90
ka_, kn_ = MOOD["a"] * MOOD["al"] ** np.arange(1, J_ + 1), MOOD["n"] * MOOD["nu"] ** np.arange(1, J_ + 1)


def matched_policy(u, Pi, a, al, it=100000, **_):
    """Codex's reduction for m = 0, lam = 1, al = nu: v = Pi u + beta Pi v_+, beta = al (1 + a), a
    contraction; exit iff v(s) < 0, whatever n."""
    v = Pi @ u
    for _ in range(it):
        v_new = Pi @ u + al * (1 + a) * Pi @ np.maximum(v, 0)
        if np.max(np.abs(v_new - v)) < 1e-13:
            return v_new < 0
        v = v_new
    raise RuntimeError("no convergence")


def state_lifespan(Pi, exit_s):
    """Expected periods lived from the stationary mood when the policy depends on the current mood."""
    if not exit_s.any():
        return np.inf
    w, vec = np.linalg.eig(Pi.T)
    pi = np.real(vec[:, np.argmin(abs(w - 1))])
    pi /= pi.sum()
    return pi @ np.linalg.solve(np.eye(len(Pi)) - Pi * ~exit_s[:, None], np.ones(len(Pi)))


bad = 0
for rho, sd in ((0.9, 1.0), (0.95, 0.75), (0.8, 1.5)):
    u, Pi = tauchen(31, rho, sd)
    pols = [markov_exit(u, Pi, 1.0, **dict(MOOD, n=n_))[1] for n_ in (0.05, 0.2, 0.3)]
    F = markov_exit(u, Pi, 1.0, **MOOD)[2]
    bad += not (np.all(pols[1] == pols[1][:1]) and np.array_equal(pols[1][0], (ka_ + kn_) @ F[:J_] < 0))
    bad += not all(np.array_equal(P_[0], matched_policy(u, Pi, **MOOD)) for P_ in pols)
report("Markov, lam = 1, alpha = nu: exit iff S(s) < 0, = Codex's contraction v = Pi u + beta Pi v+, any n", bad,
       tol=0.5)

# Multiplicity under loss-averse news (Codex): a two-state mood and a Tauchen case, two strict equilibria each.
u2, Pi2 = np.array([-1.4, 1.4]), np.array([[0.7, 0.3], [0.05, 0.95]])
_, Xa, _, ma = markov_exit(u2, Pi2, 2.0, **MOOD)
_, Xb, _, mb = markov_exit(u2, Pi2, 2.0, X0=np.array([[True, False], [False, False]]), **MOOD)
u3, Pi3 = tauchen(31, 0.55, 1.5)
_, Xc, _, mc = markov_exit(u3, Pi3, 2.0, **MOOD)
_, Xd, _, md = markov_exit(u3, Pi3, 2.0, X0=np.tile(u3 < 0, (31, 1)), **MOOD)
strict = min(np.min(np.abs(x)) for x in (ma, mb, mc, md))
report(f"lam = 2: two strict equilibria in a two-state mood (never exit; exit after two lows, lives "
       f"{lifespan(Pi2, Xb):.2f}) and at rho 0.55, sd 1.5 (Codex)",
       float(not (not Xa.any() and Xb[0, 0] and not np.array_equal(Xc, Xd) and strict > 1e-3)), tol=0.5)

# The lifespan table at lam = 1, by the contraction on a fine grid (601 points, 6 sd) against the
# coarse one (31 points, 3 sd); the coarse grid misses stops in the tails.
print("      Markov mood, lam = 1: expected weeks from the stationary mood, fine grid (coarse grid)")
print("        persistence \\ sd   0.5               0.75              1                 1.5")
for rho in (0.5, 0.8, 0.9, 0.95, 0.98):
    cells_ = []
    for sd in (0.5, 0.75, 1.0, 1.5):
        uf, Pf = tauchen(601, rho, sd, width=6.0)
        uc, Pc = tauchen(31, rho, sd)
        Lf, Lc = state_lifespan(Pf, matched_policy(uf, Pf, **MOOD)), state_lifespan(Pc, matched_policy(uc, Pc, **MOOD))
        cells_.append(f"{Lf:9.3g} ({Lc:6.3g})")
    print(f"        {rho:<11}" + "  ".join(cells_))


# 2. Which equilibrium would a momentary self pick? In the two-state example, compare each self's felt
#    state under the two equilibria (expectations equal to each): selves in good moods prefer the one
#    with exits, through its felt news (their anticipation falls slightly, Codex); selves in bad moods
#    prefer never exiting. Means are over the stationary mood pairs, not over living selves.
eA, XA, _, _ = markov_exit(u2, Pi2, 2.0, **MOOD)
eB, XB, _, _ = markov_exit(u2, Pi2, 2.0, X0=np.array([[True, False], [False, False]]), **MOOD)
w2, v2 = np.linalg.eig(Pi2.T)
pi2 = np.real(v2[:, np.argmin(abs(w2 - 1))])
pi2 /= pi2.sum()
start2 = pi2[:, None] * Pi2
prefers_never = eA > eB
report("two-state selection: bad moods prefer never exiting, good moods the exit equilibrium",
       float(not (prefers_never[:, 0].all() and not prefers_never[:, 1].any())), tol=0.5)
print("      felt state, never exit / exit after two lows, by (previous, current) mood: " + "  ".join(
    f"({'LH'[a_]},{'LH'[b_]}) {eA[a_, b_]:+.4f} / {eB[a_, b_]:+.4f}" for a_ in range(2) for b_ in range(2))
      + f"; means over stationary mood pairs {np.sum(start2 * eA):+.4f} / {np.sum(start2 * eB):+.4f}")


# 3. Memory. The stock H_{t+1} = mu (H_t + e_t) enters as m H_t; a self's own felt state is remembered,
#    so its continuation forecasts depend on it (and, through its news, on the previous mood even at
#    lam = 1). Lifespans by simulation after a forced-continuation start: 300 periods in which every
#    self continues, with forecasts of equilibrium play after it (Codex), then exits allowed.
def interp(F, s_idx, h, H0, dH, NH):
    """F[..., s, iH] linearly interpolated at (s_idx, h), clamped to the grid."""
    pos = np.clip((h - H0) / dH, 0, NH - 1 - 1e-12)
    i0 = np.floor(pos).astype(int)
    w = pos - i0
    return F[..., s_idx, i0] * (1 - w) + F[..., s_idx, i0 + 1] * w


def memory_exit(u, Pi, lam, a, al, m, mu, n, nu, Hlim=(-6.0, 6.0), NH=41, J=60, C0=None, damp=0.5, tol=1e-10):
    """Returns felt states continuing (ec) and exiting (ed) and the policy C (continue) on (sp, s, H)."""
    Ns = len(u)
    Hg = np.linspace(*Hlim, NH)
    H0, dH = Hg[0], Hg[1] - Hg[0]
    ka, kn = a * al ** np.arange(1, J + 1), n * nu ** np.arange(0, J + 1)
    phi = lambda x: np.where(x >= 0, x, lam * x)
    h0 = lambda X, Rv: np.where((X - n * Rv) / (1 - n) >= Rv, (X - n * Rv) / (1 - n),
                                (X - lam * n * Rv) / (1 - lam * n))
    sp_, s_, iH_ = np.meshgrid(np.arange(Ns), np.arange(Ns), np.arange(NH), indexing="ij")
    nxt = np.arange(Ns)[None, :, None]
    C = np.ones((Ns, Ns, NH), bool) if C0 is None else C0.copy()
    e = (u[s_] + m * Hg[iH_]).astype(float)
    ec = e.copy()
    for _ in range(100):
        for _ in range(20000):
            F = np.zeros((J + 1, Ns, NH))                 # F[j-1, s, h]: E[e_{t+j} alive | s_t, H_{t+1} = h]
            F[0] = np.einsum("sx,sxh->sh", Pi, e)
            hnext = mu * (Hg[None, None, :] + e)
            for j in range(1, J + 1):
                F[j] = np.einsum("sx,sxh->sh", Pi, C * interp(F[j - 1], nxt, hnext, H0, dH, NH))
            R = F[:, sp_, iH_]                             # the previous self's forecasts
            own = interp(F[:J], s_, mu * (Hg[None, None, :] + ec), H0, dH, NH)
            base = u[s_] + m * Hg[iH_]
            ec_new = h0(base + np.tensordot(ka, own, 1) + (kn[1:, None, None, None] * phi(own - R[1:])).sum(0), R[0])
            ed = h0(base + (kn[1:, None, None, None] * phi(-R[1:])).sum(0), R[0])
            e_new = np.where(C, ec_new, ed)
            err = max(np.max(np.abs(e_new - e)), np.max(np.abs(ec_new - ec)))
            e, ec = damp * e_new + (1 - damp) * e, damp * ec_new + (1 - damp) * ec
            if err < tol:
                break
        else:
            raise RuntimeError(f"felt states did not converge, err {err:.1e}")
        Cn = ec >= ed - 1e-12
        if np.array_equal(Cn, C):
            return dict(e=e, ec=ec, ed=ed, C=C, Hg=Hg)
        C = Cn
    raise RuntimeError("policy cycle")


def simulate(sol, u, Pi, mu, paths=20000, steps=20000, burn=300, seed=0):
    """Mean remaining periods lived after the forced-continuation start, and the share still alive at
    the end (censored)."""
    rng = np.random.default_rng(seed)
    Hg = sol["Hg"]
    H0, dH, NH, Ns = Hg[0], Hg[1] - Hg[0], len(Hg), len(u)
    cum = np.cumsum(Pi, 1)
    s = rng.integers(0, Ns, paths)
    sp, H = s.copy(), np.zeros(paths)
    margin = sol["ec"] - sol["ed"]
    alive, life = np.ones(paths, bool), np.zeros(paths)
    for t in range(burn + steps):
        pos = np.clip((H - H0) / dH, 0, NH - 1 - 1e-12)
        i0 = pos.astype(int)
        w = pos - i0
        e = sol["ec"][sp, s, i0] * (1 - w) + sol["ec"][sp, s, i0 + 1] * w
        if t >= burn:
            life += alive
            alive &= (margin[sp, s, i0] * (1 - w) + margin[sp, s, i0 + 1] * w) >= 0
            if not alive.any():
                break
        sp, s, H = s, np.minimum((rng.random(paths)[:, None] > cum[s]).sum(1), Ns - 1), mu * (H + e)
    return life.mean(), alive.mean()


u15, Pi15 = tauchen(15, 0.9, 1.0)
s0 = memory_exit(u15, Pi15, 1.0, **dict(MOOD, m=0.0, mu=0.3), Hlim=(-1, 1), NH=5)
e0, X0_, _, _ = markov_exit(u15, Pi15, 1.0, **MOOD)
report("memory solver at m = 0 reproduces the memoryless one", np.max(np.abs(s0["e"] - e0[:, :, None]))
       + float(not np.array_equal(~s0["C"][:, :, 0], X0_)), tol=1e-8)
u31, Pi31 = tauchen(31, 0.9, 1.0)
s1 = memory_exit(u31, Pi31, 1.0, **dict(MOOD, m=0.4, mu=0.3), Hlim=(-4, 6), NH=41)
top = [u31[(~s1["C"][:, :, ih]).any(0)].max() for ih in range(41)]
report("worse memories, exits at better moods: the highest exiting mood falls as the stock rises",
       float(np.any(np.diff(top) > 1e-12)), tol=0.5)
print(f"      highest exiting mood: {top[0]:+.1f} at H = {s1['Hg'][0]:+.1f}, {top[20]:+.1f} at {s1['Hg'][20]:+.1f}, "
      f"{top[-1]:+.1f} at {s1['Hg'][-1]:+.1f}")

B17 = 0.4 * 0.3 / 0.7
CASES = (("no memory", dict(m=0.0, mu=0.3), (-1, 1), 3),
         ("mu 0.3, B 0.17 (life)", dict(m=0.4, mu=0.3), (-4, 6), 41),
         ("mu 0.9, B 0.17", dict(m=B17 * 0.1 / 0.9, mu=0.9), (-30, 50), 81),
         ("mu 0.9, B 0.5", dict(m=0.5 * 0.1 / 0.9, mu=0.9), (-40, 80), 121))
print("      expected remaining weeks, 31 moods (coarse): " + " / ".join(c[0] for c in CASES))
for lam in (1.0, 2.0):
    for rho, sd in ((0.9, 1.0), (0.95, 0.75)):
        u, Pi = tauchen(31, rho, sd)
        Ls = [simulate(memory_exit(u, Pi, lam, **dict(MOOD, **kw), Hlim=Hl, NH=NH), u, Pi, kw["mu"])
              for _, kw, Hl, NH in CASES]
        print(f"        lam {lam:g}, persistence {rho}, sd {sd}: " + " / ".join(f"{x:.0f}" for x, _ in Ls)
              + f" (censored at most {max(c_ for _, c_ in Ls):.4f})")
# Short memory can hasten exit under linear news too (Codex): 15 moods, persistence 0.9, sd 0.9.
u, Pi = tauchen(15, 0.9, 0.9)
L0 = simulate(memory_exit(u, Pi, 1.0, **dict(MOOD, m=0.0, mu=0.3), Hlim=(-1, 1), NH=3), u, Pi, 0.3)[0]
L1 = simulate(memory_exit(u, Pi, 1.0, **dict(MOOD, m=0.4, mu=0.3), Hlim=(-5, 8), NH=53), u, Pi, 0.3)[0]
report(f"lam = 1, 15 moods, persistence 0.9, sd 0.9: short memory {L1:.1f} weeks against none {L0:.1f} (Codex)",
       float(not L1 < 0.6 * L0), tol=0.5)


# 4. Adaptation (biphasic memory's slow lobe, notes/adaptation.md, no afterglow): the one-stock solver with the
#    stock as the adaptation sum, m = -c and mu = g (a year, g = 1 - 1/52), h = c g/(1 - g). Expected remaining
#    weeks at persistence 0.9, sd 1, for mean moods 1 and 2, and with the mean raised so that the stationary
#    felt mean of the never-exit life, E[u]/(1 - A + h), matches the unadapted one (Codex: exact for that
#    counterfactual, not the mean among living selves; it does not isolate a single channel).
ga = 1 - 1 / 52
Aa = MOOD["a"] * MOOD["al"] / (1 - MOOD["al"])


def adapted_life(rho, sd, mean, h, seed=0):
    u, Pi = tauchen(31, rho, sd, mean=mean)
    if h == 0:
        sol = memory_exit(u, Pi, 1.0, **dict(MOOD, m=0.0, mu=0.3), Hlim=(-1, 1), NH=3)
        return simulate(sol, u, Pi, 0.3, seed=seed)
    c = h * (1 - ga) / ga
    sol = memory_exit(u, Pi, 1.0, **dict(MOOD, m=-c, mu=ga), Hlim=(-60, 60 + 60 * mean), NH=121)
    return simulate(sol, u, Pi, ga, burn=600, seed=seed)


ad = {(mean, h): adapted_life(0.9, 1.0, mean, h)[0] for mean in (1.0, 2.0) for h in (0.0, 0.5, 2.0)}
matched = {h: adapted_life(0.9, 1.0, (1 - Aa + h) / (1 - Aa), h)[0] for h in (0.5, 2.0)}
ratios = [ad[(2.0, h)] / ad[(1.0, h)] for h in (0.0, 0.5, 2.0)]
report("adaptation flattens the lifespan's dependence on the mean mood (ratio of mean 2 to mean 1 falls with h)",
       float(not ratios[0] > ratios[1] > ratios[2]), tol=0.5)
print("      expected remaining weeks, persistence 0.9, sd 1, mean mood 1 / 2 / felt mean matched: " + "  ".join(
    f"h {h}: {ad[(1.0, h)]:.0f} / {ad[(2.0, h)]:.0f}" + (f" / {matched[h]:.0f}" if h else "") for h in (0.0, 0.5, 2.0)))
