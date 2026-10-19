"""Checks for notes/death.md: random death dates in the canonical model, additive reading.
Run: python notes/death.py

Dead moments are hedonic zero and forecasts are Bayesian over the death date D (life = moments
0..D-1), so a forecast of e_{t+j} is E_t[e_{t+j} 1{alive}]. A diagnosis arrives L periods before
death: L = 0 is sudden, L >= T foreseen from birth. News at t = 0 is against the prior over D.

tree(): the exact fixed point over branches. The alive self at t in branch D knows D if
D <= t + L, else only that D > t + L. rec=True: echoes and news over e (canonical);
rec=False: echoes of f = u + N, news over u (the direct corner).
sudden_line(): sudden death under a hazard path, where the alive path is deterministic and
e = u + K_S e is one linear system.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "formalism"))
import pathwise as pw  # noqa: E402

LIFE = dict(a=0.064, al=0.7, m=0.4, mu=0.3, n=0.2, nu=0.7)     # calibration.md, a week
DAY = dict(a=0.05, al=0.8, m=0.1, mu=0.5, n=0.2, nu=0.8)       # calibration.md, an hour


def report(name, err, tol):
    print(f"{'PASS' if err < tol else 'FAIL'}  {name}  (max err {err:.2e})")


def kernels(T, a, al, m, mu, n, nu):
    j = np.arange(T)
    return np.where(j > 0, a * al ** j, 0.0), np.where(j > 0, m * mu ** j, 0.0), n * nu ** j


def cells(P, L):
    """W[t+1, i, k]: weight on branch Ds[k] in the forecast of the self at t in branch Ds[i], over
    the support of P. Row t = -1 is the prior."""
    T = len(P)
    Ds, P = np.arange(1, T + 1)[P > 0], P[P > 0]
    W = np.zeros((T + 1, len(Ds), len(Ds)))
    for t in range(-1, T):
        for i, D in enumerate(Ds):
            if t >= D:
                continue
            mask = (np.ones(len(Ds), bool) if t < 0 else Ds == D if D <= t + L else Ds > t + L)
            W[t + 1, i] = P * mask / (P * mask).sum()
    return W


def tree(u, P, L, a, al, m, mu, n, nu, lam=1.0, rec=True, tol=1e-13, damp=0.5, it=200000):
    """Returns (e[branch, t], expected welfare, felt news[branch, t], forecasts[t+1, branch, s])."""
    T = len(u)
    kf, kb, kn = kernels(T, a, al, m, mu, n, nu)
    s, t = np.meshgrid(np.arange(T), np.arange(T))
    KF = np.where(s > t, kf[np.clip(s - t, 0, T - 1)], 0.0)
    KB = np.where(s < t, kb[np.clip(t - s, 0, T - 1)], 0.0)
    KN = np.where(s >= t, kn[np.clip(s - t, 0, T - 1)], 0.0)
    Ds, Pp = np.arange(1, T + 1)[P > 0], P[P > 0]
    alive = (np.arange(T)[None, :] < Ds[:, None]).astype(float)
    U = alive * u[None, :]
    W = cells(P, L)
    phi = lambda x: np.where(x >= 0, x, lam * x)
    fc = lambda X: np.einsum("tdk,ks->tds", W, X)
    news = lambda F: np.einsum("ts,tds->dt", KN, phi(F[1:] - F[:-1])) * alive
    if not rec:
        N = news(fc(U))
        f = U + N
        e = (f + np.einsum("ts,tds->dt", KF, fc(f)[1:]) + f @ KB.T) * alive
        return e, Pp @ e.sum(1), N, fc(U)
    e = U.copy()
    for _ in range(it):
        F = fc(e)
        N = news(F)
        new = (U + np.einsum("ts,tds->dt", KF, F[1:]) + e @ KB.T + N) * alive
        err = np.max(np.abs(new - e))
        e = damp * new + (1 - damp) * e
        if err < tol:
            return e, Pp @ e.sum(1), N, F
    raise RuntimeError(f"no convergence, err {err:.2e}")


def sudden_line(u, h, a, al, m, mu, n, nu):
    """h[t] = P(die before t + 1 | alive at t). News at t is h[t-1] sum_j kn(j) S_t(j) e_{t+j}."""
    T = len(u)
    kf, kb, kn = kernels(T, a, al, m, mu, n, nu)
    surv = np.concatenate([[1.0], np.cumprod(1 - h[:-1])])
    K = np.zeros((T, T))
    for t in range(T):
        hp = h[t - 1] if t > 0 else 0.0
        K[t, t:] += (kf[:T - t] + hp * kn[:T - t]) * surv[t:] / surv[t]
        K[t, :t] += kb[1:t + 1][::-1]
    return np.linalg.solve(np.eye(T) - K, u), surv


def foreseen(D, a, al, m, mu, **_):
    i, j = np.meshgrid(np.arange(D), np.arange(D), indexing="ij")
    K = np.where(j > i, a * al ** np.abs(j - i), 0) + np.where(j < i, m * mu ** np.abs(j - i), 0)
    return np.linalg.solve(np.eye(D) - K, np.ones(D))


def stationary(h, a, al, m, mu, n, nu):
    """Interior felt state per unit base utility under constant hazard h, sudden death."""
    return 1 / (1 - a * al * (1 - h) / (1 - al * (1 - h)) - m * mu / (1 - mu) - h * n / (1 - nu * (1 - h)))


# 1. Reproduce D5's mortality check (checks.py): two moments, a = m = 1/2, p = 1/2, no news.
two = lambda u1, rec, L: tree(np.array([0.0, u1]), np.array([0.5, 0.5]), L, 0.5, 1.0, 0.5, 1.0, 0.0, 0.5,
                               rec=rec)[1]
report("D5 reproduced: knowing at once is worth +-1/7 (R), 0 (direct)",
       max(abs(two(1, True, 5) - two(1, True, 0) - 1 / 7), abs(two(-1, True, 5) - two(-1, True, 0) + 1 / 7),
           abs(two(1, False, 5) - two(1, False, 0))), tol=1e-10)

# 2. The news route in closed form, direct, no echoes: ignorance pays n p (1-p) u1 (1 + nu (lam - 1)).
err = 0.0
for lam in (1.0, 2.0):
    for nu in (0.5, 0.9):
        kw = dict(a=0, al=0.5, m=0, mu=0.5, n=0.3, nu=nu, lam=lam, rec=False)
        u, P = np.array([0.0, 1.0]), np.array([0.3, 0.7])
        err = max(err, abs(tree(u, P, 0, **kw)[1] - tree(u, P, 5, **kw)[1] - 0.3 * 0.21 * (1 + nu * (lam - 1))))
report("news route: ignorance pays n p (1-p) u1 (1 + nu (lam - 1))", err, tol=1e-12)

# 3. The two solvers agree on sudden death under a random hazard path.
rng = np.random.default_rng(0)
T = 12
h = rng.uniform(0.05, 0.3, T)
h[-1] = 1
surv = np.concatenate([[1.0], np.cumprod(1 - h[:-1])])
u = rng.normal(0.5, 1, T)
par = dict(a=0.3, al=0.7, m=0.3, mu=0.5, n=0.3, nu=0.7)
e_line, _ = sudden_line(u, h, **par)
e_tree, W_tree, _, _ = tree(u, surv * h, 0, **par)
report("sudden death: tree = linear system on the alive path", max(np.max(np.abs(e_tree[-1] - e_line)),
                                                                    abs(surv @ e_line - W_tree)), tol=1e-10)

# 4. The dead feel no news: E[felt news] = E[news-weighted forecast the dying self held of its
#    unlived future], sudden deaths only; zero once every death is warned.
T = 30
Ds = np.arange(1, T + 1)
P_late = np.where(Ds >= 16, 1.0, 0.0) / 15
kn = kernels(T, **LIFE)[2]
err = 0.0
for rec in (True, False):
    for L in (0, 1, 3):
        e, W, N, F = tree(np.ones(T), P_late, L, **LIFE, rec=rec)
        Pp, Dsup = P_late[P_late > 0], Ds[P_late > 0]
        lost = sum(Pp[i] * (kn[:T - D] @ F[D, i, D:]) for i, D in enumerate(Dsup) if D < T)
        err = max(err, abs(Pp @ N.sum(1) - (lost if L == 0 else 0.0)), abs(lost) if L > 0 else 0.0)
        if L == 0:
            print(f"      {'canonical' if rec else 'direct':9s}: expected felt news {Pp @ N.sum(1):+.4f}")
report("the dead feel no news: E[felt] = E[dying self's lost forecast], zero with warning", err, tol=1e-9)

# 5. Constant hazard: the stationary felt state, and its slope at h = 0 by N - M1+.
err = 0.0
for par in (LIFE, DAY):
    for h0 in (0.0, 0.01, 0.05, 0.2):
        h = np.full(800, h0)
        h[-1] = 1
        err = max(err, abs(sudden_line(np.ones(800), h, **par)[0][400] - stationary(h0, **par)))
report("constant hazard: e* = u / (1 - A_h - B - h n / (1 - nu (1 - h)))", err, tol=1e-9)
bad = 0
for _ in range(2000):
    a, m, n = rng.uniform(0.01, 0.3, 3)
    al, mu, nu = rng.uniform(0.1, 0.9, 3)
    if a * al / (1 - al) + m * mu / (1 - mu) > 0.9:
        continue
    slope = (stationary(1e-6, a, al, m, mu, n, nu) - stationary(0, a, al, m, mu, n, nu)) / 1e-6
    gap = n / (1 - nu) - a * al / (1 - al) ** 2
    bad += abs(gap) > 1e-3 and np.sign(slope) != np.sign(gap)
report("slope of e*(h) at 0 has the sign of N - M1+ (random draws)", bad, tol=0.5)
inv = max(abs(stationary(h0, **DAY) - stationary(0, **DAY)) for h0 in np.linspace(0, 0.9, 10))
report("day calibration (al = nu, n = A): hazard-invariant at every h", inv, tol=1e-12)
for name, par in (("life", LIFE), ("day", DAY)):
    print(f"      {name}: N = {par['n'] / (1 - par['nu']):.3f}, M1+ = {par['a'] * par['al'] / (1 - par['al']) ** 2:.3f}; "
          f"e*(0.02) / e*(0) = {stationary(0.02, **par) / stationary(0, **par):.5f}")

# 6. Survival optimism (forecasting no hazard) lives the h = 0 felt state: its disappointment is death.
#    The stationary comparison is the sign of M_h - M_0, not N - M1+ beyond small h (Codex's
#    counterexample); from birth a boundary term favours the optimist (no relief yet at t = 0).
def from_birth(par, h0, Tn=1500):
    h = np.full(Tn, h0)
    h[-1] = 1
    eb, s = sudden_line(np.ones(Tn), h, **par)
    eo, _ = sudden_line(np.ones(Tn), np.r_[np.zeros(Tn - 1), 1.0], **par)
    return s @ eb, s @ eo, eb, eo


_, _, bay, opt = from_birth(LIFE, 0.05)
report("survival optimism = the hazard-free felt state", abs(opt[400] - stationary(0, **LIFE)), tol=1e-9)
cx = dict(a=0.1, al=0.5, m=0.0, mu=0.5, n=0.03, nu=0.9)
report("finite h: N > M1+ yet optimism wins the stationary comparison at h = 0.2 (Codex)",
       float(not (stationary(0.01, **cx) > stationary(0, **cx) > stationary(0.2, **cx))), tol=0.5)
wb, wo, _, _ = from_birth(dict(a=0.1, al=0.5, m=0.0, mu=0.5, n=0.1, nu=0.5), 0.2)
report("equal stationary states, optimist ahead from birth by 1/27 (Codex)", abs(wo - wb - 1 / 27), tol=1e-12)
for name, par, h0 in (("life", LIFE, 0.05), ("life", LIFE, 0.01), ("day", DAY, 0.1), ("day", DAY, 0.01)):
    wb, wo, _, _ = from_birth(par, h0)
    print(f"      {name}, h = {h0}: from birth, optimist - Bayesian {wo - wb:+.3f} ({(wo - wb) / wb:+.2%}); "
          f"stationary {stationary(0, **par):.4f} against {stationary(h0, **par):.4f}")

# 6b. Mortality adds feedback: M_0 < 1 and kappa < 1 do not bound echo under hazard (Codex).
wf = dict(a=0.9, al=0.5, m=0.0, mu=0.5, n=0.3, nu=0.99)
Mh = 1 - 1 / stationary(0.05, **wf)
e0s = []
for Tn in (30, 80, 150):
    h = np.full(Tn, 0.05)
    h[-1] = 1
    e0s.append(sudden_line(np.ones(Tn), h, **wf)[0][0])
report("M_0 = 0.9, kappa = 0.3, but M_h = 1.066 at h = 0.05: e_0 grows with the horizon",
       float(not (Mh > 1 and e0s[0] < e0s[1] < e0s[2])), tol=0.5)
print(f"      M_h = {Mh:.4f}; e_0 = " + ", ".join(f"{x:.2f}" for x in e0s) + " at T = 30, 80, 150")

# 6c. Two periods exactly (Codex): c = a + n p (a + nu)/(1 - n), one-step weights a, m;
#     W_known = u0 + (1-p)(1+a)(u1 + m u0)/(1 - m c), W_sudden: denominator 1 - n p - a m (1-p);
#     knowing wins iff a m - n (1 - m nu) + n^2 > 0 when u1 + m u0 > 0.
err, bad, n_sign = 0.0, 0, 0
for _ in range(300):
    a, m, n = rng.uniform(0, 0.6, 3)
    nu, p = rng.uniform(0.1, 0.95), rng.uniform(0.05, 0.95)
    u0, u1 = rng.normal(0, 1, 2)
    c = a + n * p * (a + nu) / (1 - n)
    if 1 - m * c <= 0 or 1 - n * p - a * m * (1 - p) <= 0:
        continue
    kw = dict(a=a, al=1.0, m=m, mu=1.0, n=n, nu=nu)
    u, P = np.array([u0, u1]), np.array([p, 1 - p])
    try:
        Wk, Ws = tree(u, P, 5, **kw)[1], tree(u, P, 0, **kw)[1]
    except RuntimeError:
        continue
    err = max(err, abs(Wk - u0 - (1 - p) * (1 + a) * (u1 + m * u0) / (1 - m * c)),
              abs(Ws - u0 - (1 - p) * (1 + a) * (u1 + m * u0) / (1 - n * p - a * m * (1 - p))))
    if u1 + m * u0 > 0:
        n_sign += 1
        bad += (Wk > Ws) != (a * m - n * (1 - m * nu) + n ** 2 > 0)
report(f"two periods: Codex's closed forms, and the knowing criterion ({n_sign} draws)", max(err, bad), tol=1e-10)

# 7. Value of knowing, by lead time, life calibration, death uniform on 16..30 (printed).
for ulev in (1.0, -0.5):
    print(f"      u = {ulev:+.1f}: W(L) - W(foreseen from birth)")
    for label, kw in (("canonical", dict(rec=True, lam=1.0)), ("canonical lam 2", dict(rec=True, lam=2.0)),
                      ("direct", dict(rec=False, lam=1.0)), ("no news", dict(rec=True, lam=1.0))):
        p = dict(LIFE, n=0.0) if label == "no news" else LIFE
        Ws = {L: tree(np.full(T, ulev), P_late, L, **p, **kw)[1] for L in (0, 1, 2, 4, 8, T)}
        print(f"        {label:16s}" + "  ".join(f"L={L}: {Ws[L] - Ws[T]:+.3f}" for L in (0, 1, 2, 4, 8)))

Ds8 = np.arange(1, 9)
c3 = {L: tree(np.ones(8), np.ones(8) / 8, L, a=0.4, al=0.5, m=0.5, mu=0.5, n=0.01, nu=0.7, lam=2.0)[1] for L in (0, 1, 4, 8)}
report("lam = 2, weak news, strong echoes: sudden < short warning < long < foreseen (Codex)",
       float(not (c3[0] < c3[1] < c3[4] < c3[8])), tol=0.5)

# 8. Who wins: the Epicurean term against loop convexity, by echo scale, news, timing (printed).
print("      value of knowing (good future), echo scale x news strength:")
for win in ((2, 10), (21, 30)):
    P = ((Ds >= win[0]) & (Ds <= win[1])).astype(float)
    P /= P.sum()
    for c in (1.0, 2.0, 2.8):
        p = dict(LIFE, a=LIFE["a"] * c, m=LIFE["m"] * c)
        Mc = c * (LIFE["a"] * LIFE["al"] / (1 - LIFE["al"]) + LIFE["m"] * LIFE["mu"] / (1 - LIFE["mu"]))
        row = [tree(np.ones(T), P, T, **dict(p, n=n))[1] - tree(np.ones(T), P, 0, **dict(p, n=n))[1]
               for n in (0.05, 0.2, 0.5)]
        print(f"        death on {win}, M = {Mc:.2f}: " + "  ".join(f"n={n}: {v:+.3f}" for n, v in zip((0.05, 0.2, 0.5), row)))

# 9. Where a foreseen death's harm lands: one more period, D = 200 -> 201, life calibration.
e1, e2 = foreseen(200, **LIFE), foreseen(201, **LIFE)
dW, own = e2.sum() - e1.sum(), e2[-1]
report("a foreseen extra period adds the interior weight 1/(1-M)", abs(dW - 1 / (1 - 0.32)), tol=5e-3)
print(f"      dW {dW:.4f}: the new moment's own felt state {own:.4f} ({own / dW:.0%}), "
      f"the living's raise {dW - own:.4f}")


# 10. Decisions that move the death date: a risk d before t0 + 1, taken off plan (past e and past
#     forecasts fixed; the decision is news at t0) against foreseen from birth (commitment).
def deviate(u, h, t0, d, a, al, m, mu, n, nu, lam=1.0):
    """Returns the deviating self's felt state and its expected remaining life-sum, then the plan's."""
    T = len(u)
    kf, kb, kn = kernels(T, a, al, m, mu, n, nu)
    e0, surv = sudden_line(u, h, a, al, m, mu, n, nu)
    h2 = h.copy()
    h2[t0] += d
    surv2 = np.concatenate([[1.0], np.cumprod(1 - h2[:-1])])
    r = T - t0
    K, b = np.zeros((r, r)), u[t0:].copy()
    for i, t in enumerate(range(t0, T)):
        S = surv2[t:] / surv2[t]
        K[i, i:] += kf[:T - t] * S + (h2[t - 1] * kn[:T - t] * S if t > t0 else 0)
        K[i, :i] += kb[1:i + 1][::-1]
        b[i] += kb[t - t0 + 1:t + 1][::-1] @ e0[:t0]
    S0 = surv2[t0:] / surv2[t0]
    old = surv[t0:] / surv[t0 - 1] * e0[t0:]           # the self at t0 - 1's forecast
    R = np.linalg.inv(np.eye(r) - K)
    xb, g = R @ b, R[:, 0]                             # x = xb + s g, s the news felt at t0
    s = pw.news_root(S0 * xb - old, S0 * g, kn[:r], lam)
    x = xb + s * g
    return x[0], S0 @ x, e0[t0], surv[t0:] / surv[t0] @ e0[t0:]


T, t0 = 120, 40
h = np.full(T, 0.01)
h[-1] = 1
x0, rem, p0, rem0 = deviate(np.ones(T), h, t0, 0.0, **LIFE, lam=2.0)
report("off-plan solver at d = 0 reproduces the plan", max(abs(x0 - p0), abs(rem - rem0)), tol=1e-10)
e0, s0 = sudden_line(np.ones(T), h, **LIFE)
print(f"      per unit of extra death risk at t = {t0} (plan hazard 0.01; reaching t0 has probability {s0[t0]:.3f}):")
for d in (1e-4, 0.02):
    h2 = h.copy()
    h2[t0] += d
    eC, sC = sudden_line(np.ones(T), h2, **LIFE)
    for lam in (1.0, 2.0):
        x0, rem, p0, rem0 = deviate(np.ones(T), h, t0, d, **LIFE, lam=lam)
        print(f"        d = {d}, lam = {lam}: momentary self {(x0 - p0) / d:+.3f}, "
              f"fixed past {s0[t0] * (rem - rem0) / d:+.2f}, commitment {(sC @ eC - s0 @ e0) / d:+.2f}")

# 11. Loss-averse news splits exactly: E sum N = the dividend - (lam - 1) E sum k_n (-dF)_+, both on
#     the loss-averse fixed point (Codex). And translation: one period at either end of a constant
#     life adds the same total, allocated differently.
T = 30
e, W, N, F = tree(np.ones(T), P_late, 2, **LIFE, lam=2.0)
Pp, Dsup = P_late[P_late > 0], Ds[P_late > 0]
alive = (np.arange(T)[None, :] < Dsup[:, None]).astype(float)
s_, t_ = np.meshgrid(np.arange(T), np.arange(T))
KN = np.where(s_ >= t_, kn[np.clip(s_ - t_, 0, T - 1)], 0.0)
loss = np.einsum("ts,tds->dt", KN, np.maximum(-(F[1:] - F[:-1]), 0)) * alive
lin = np.einsum("ts,tds->dt", KN, F[1:] - F[:-1]) * alive
report("lam = 2, warned: E sum N = 0 (the dividend) - (lam - 1) E sum k_n (-dF)_+",
       max(abs(Pp @ N.sum(1) + Pp @ loss.sum(1)), abs(Pp @ lin.sum(1))), tol=1e-10)
e2 = foreseen(201, **LIFE)
print(f"      a period added to a constant life: new first moment {e2[0]:.4f}, new last {e2[-1]:.4f}")
