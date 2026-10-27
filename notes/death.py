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


def foreseen(u, a, al, m, mu, **_):
    """The felt path of a foreseen life with base path u (no uncertainty, so no news)."""
    i, j = np.meshgrid(np.arange(len(u)), np.arange(len(u)), indexing="ij")
    K = np.where(j > i, a * al ** np.abs(j - i), 0) + np.where(j < i, m * mu ** np.abs(j - i), 0)
    return np.linalg.solve(np.eye(len(u)) - K, u)


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
e1, e2 = foreseen(np.ones(200), **LIFE), foreseen(np.ones(201), **LIFE)
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
e2 = foreseen(np.ones(201), **LIFE)
print(f"      a period added to a constant life: new first moment {e2[0]:.4f}, new last {e2[-1]:.4f}")


# 12. The exact decision case: three moments, 0 and 1 certain, 2 alive with probability
#     s + a delta; paying (a = 1) costs c at 1. Commitment (plan foreseen at 0) against a fixed
#     past (plan ap foreseen at 0, the choice news at 1) and the momentary self. WTP per unit of
#     survival by the weight formula, channel by channel; loss-averse news gives a band of
#     credible plans.
def three_commit(a, s, d, c, a_, al, m, mu, n, nu, u=(1.0, 1.0, 1.0)):
    A1, A2, B1, B2 = a_ * al, a_ * al ** 2, m * mu, m * mu ** 2
    sa = s + a * d
    M = np.array([[1, -A1, -A2 * sa], [-B1, 1, -A1 * sa], [-B2, -B1, 1 - n * (1 - sa)]])
    e = np.linalg.solve(M, [u[0], u[1] - c * a, u[2]])
    if e[2] < 0:
        raise ValueError("terminal felt state negative: relief would be a loss branch")
    return e, e[0] + e[1] + sa * e[2]


def three_fixed(a, ap, s, d, c, a_, al, m, mu, n, nu, lam=1.0, u=(1.0, 1.0, 1.0)):
    """Returns (e1, e2, R = e1 + s_a e2). News at 1 is phi per horizon against the t = 0 forecast."""
    A1, B1, B2 = a_ * al, m * mu, m * mu ** 2
    (p0, p1, p2), _ = three_commit(ap, s, d, c, a_, al, m, mu, n, nu, u)
    sp_, sa = s + ap * d, s + a * d
    sols = []
    for k0 in ((1.0, lam) if lam != 1.0 else (1.0,)):
        for k1 in ((1.0, lam) if lam != 1.0 else (1.0,)):
            M = np.array([[1 - k0 * n, -(A1 + k1 * n * nu) * sa], [-B1, 1 - n * (1 - sa)]])
            rhs = [u[1] - c * a + B1 * p0 - k0 * n * p1 - k1 * n * nu * sp_ * p2, u[2] + B2 * p0]
            e1, e2 = np.linalg.solve(M, rhs)
            if (lam == 1.0 or ((e1 - p1 >= -1e-12) == (k0 == 1.0)
                               and (sa * e2 - sp_ * p2 >= -1e-12) == (k1 == 1.0))) and e2 >= 0:
                if not any(abs(e1 - x) < 1e-10 and abs(e2 - y) < 1e-10 for x, y in sols):
                    sols.append((e1, e2))
    if len(sols) != 1:
        raise RuntimeError(f"{len(sols)} consistent branches")      # Codex: never pick one silently
    e1, e2 = sols[0]
    return e1, e2, e1 + sa * e2


def three_channels(s, a_, al, m, mu, n, nu):
    """WTP per unit survival (delta -> 0, linear news): occupancy, anticipation, news of the
    choice, lost relief; for commitment, fixed past and the momentary self."""
    A1, A2, B1, B2 = a_ * al, a_ * al ** 2, m * mu, m * mu ** 2
    e, _ = three_commit(0, s, 0, 0, a_, al, m, mu, n, nu)
    K = np.array([[0, A1, A2 * s], [B1, 0, A1 * s], [B2, B1, n * (1 - s)]])
    w = np.linalg.solve(np.eye(3) - K.T, [1, 1, s])
    KF = np.array([[n, (A1 + n * nu) * s], [B1, n * (1 - s)]])
    wF, R = np.linalg.solve(np.eye(2) - KF.T, [1, s]), np.linalg.inv(np.eye(2) - KF)
    return {"commitment": (e[2] / w[1], e[2] * (w[0] * A2 + w[1] * A1) / w[1], 0.0, -e[2] * w[2] * n / w[1]),
            "fixed past": (e[2] / wF[0], e[2] * A1, e[2] * n * nu, -e[2] * n * wF[1] / wF[0]),
            "momentary": (0.0, e[2] * A1, e[2] * n * nu, -e[2] * n * R[0, 1] / R[0, 0])}


def three_band(s, lam, a_, al, m, mu, n, nu):
    """Fixed past, loss-averse news: deviating from 'no' pays iff c < lower; 'yes' is kept iff
    c < upper (per unit survival, delta -> 0)."""
    A1, B1 = a_ * al, m * mu
    e, _ = three_commit(0, s, 0, 0, a_, al, m, mu, n, nu)
    out = []
    for k0, k1 in ((lam, 1.0), (1.0, lam)):
        KF = np.array([[k0 * n, (A1 + k1 * n * nu) * s], [B1, n * (1 - s)]])
        w = np.linalg.solve(np.eye(2) - KF.T, [1, s])
        out.append(e[2] * (1 + w[0] * (A1 + k1 * n * nu) - w[1] * n) / w[0])
    return out


def threshold(f, lo=-5.0, hi=5.0, tol=1e-14):
    while hi - lo > tol:
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) > 0 else (lo, mid)
    return (lo + hi) / 2


par3 = dict(LIFE, a_=LIFE["a"])
del par3["a"]
s3, d3 = 0.9, 0.1
err = 0.0
for a in (0, 1):                                     # against the general solvers
    e3, w3 = three_commit(a, s3, d3, 0.2, **par3)
    e, surv = sudden_line(np.array([1.0, 1.0 - 0.2 * a, 1.0]), np.array([0.0, 1 - s3 - a * d3, 1.0]), **LIFE)
    err = max(err, np.max(np.abs(e - e3)), abs(surv @ e - w3))
x0, rem, _, _ = deviate(np.ones(3), np.array([0.0, 1 - s3, 1.0]), 1, -d3, **LIFE)
e1, e2, r = three_fixed(1, 0, s3, d3, 0.0, **par3)
report("three moments: commitment = sudden_line, fixed past = deviate", max(err, abs(x0 - e1), abs(rem - r)),
       tol=1e-12)
dd, err = 1e-7, 0.0
for s3 in (0.9, 0.5):
    ch = three_channels(s3, **par3)
    fd = [threshold(lambda c: three_commit(1, s3, dd, c, **par3)[1] - three_commit(0, s3, dd, c, **par3)[1]),
          threshold(lambda c: three_fixed(1, 0, s3, dd, c, **par3)[2] - three_fixed(0, 0, s3, dd, c, **par3)[2]),
          threshold(lambda c: three_fixed(1, 0, s3, dd, c, **par3)[0] - three_fixed(0, 0, s3, dd, c, **par3)[0])]
    err = max(err, max(abs(sum(v) - f / dd) for v, f in zip(ch.values(), fd)))
    for k, v in ch.items():
        print(f"      s = {s3}, {k:10s}: WTP {sum(v):.3f} = occupancy {v[0]:+.3f}, anticipation {v[1]:+.3f}, "
              f"news {v[2]:+.3f}, lost relief {v[3]:+.3f}")
report("three moments: channel WTPs = finite-difference thresholds", err, tol=1e-5)
err = 0.0
for lam in (2.0, 3.0):
    lo_, hi_ = three_band(0.9, lam, **par3)
    num = [threshold(lambda c: three_fixed(1, ap, 0.9, dd, c, **par3, lam=lam)[2]
                     - three_fixed(0, ap, 0.9, dd, c, **par3, lam=lam)[2]) / dd for ap in (0, 1)]
    err = max(err, abs(lo_ - num[0]), abs(hi_ - num[1]))
    print(f"      lam = {lam}: credible band [{lo_:.3f}, {hi_:.3f}] around commitment "
          f"{sum(three_channels(0.9, **par3)['commitment']):.3f}")
report("three moments: closed-form band edges = solver", err, tol=1e-5)


# 13. How death comes changes what safety is worth: commitment WTP per unit survival when the
#     averted death would be sudden (L = 0), warned a period ahead (L = 1), or foreseen from birth.
def tree_wtp(T, k, s, d, L, lam, par, t_pay=1):
    """Death before moment k with probability 1 - (s + a d), else at T; paying c at t_pay."""
    def W(a, c):
        P = np.zeros(T)
        P[k - 1], P[T - 1] = 1 - (s + a * d), s + a * d
        u = np.ones(T)
        u[t_pay] -= c * a
        return tree(u, P, L, **par, lam=lam)[1]
    W0 = W(0, 0.0)
    return threshold(lambda c: W(1, c) - W0, tol=1e-11) / d


v3 = sum(three_channels(0.9, **par3)["commitment"])
report("tree, sudden, three moments = the closed-form commitment WTP",
       abs(tree_wtp(3, 2, 0.9, 1e-4, 0, 1.0, LIFE) - v3), tol=2e-4)
for T, k in ((3, 2), (8, 5)):
    vals = {(lam, L): tree_wtp(T, k, 0.9, 1e-3, L, lam, LIFE) for lam in (1.0, 2.0) for L in (0, 1, T)}
    print(f"      {T} moments, risk before {k}: " + "  ".join(
        f"lam {lam:g} {'sudden' if L == 0 else 'warned' if L == 1 else 'foreseen'} {v:.3f}"
        for (lam, L), v in vals.items()))


# 14. The fixed past when the averted death would be warned: four moments, 0-2 certain, 3 alive
#     with probability s + a delta; choice at 1; with L = 1 the self at 2 knows whether 3 exists.
def four_plan(ap, s, d, c, L, lam, par):
    P = np.zeros(4)
    P[2], P[3] = 1 - (s + ap * d), s + ap * d
    u = np.ones(4)
    u[1] -= c * ap
    e, W, _, F = tree(u, P, L, **par, lam=lam)
    return e, W, F


def four_fixed(a, ap, s, d, c, L, lam, par, it=20000):
    """Remaining expected life-sum of the self at 1 choosing a against the plan ap."""
    kf, kb, kn = kernels(4, **par)
    e_p, _, F = four_plan(ap, s, d, c, L, lam, par)
    p0, F0, sa = e_p[1, 0], F[1, 1], s + a * d
    phi = lambda x: x if x >= 0 else lam * x
    x = np.ones(4)                                     # e1, e2 (survive), e2 (die), e3
    for _ in range(it):
        e1, e2S, e2D, e3 = x
        Fe2, Fe3 = sa * e2S + (1 - sa) * e2D, sa * e3
        n1 = kn[0] * phi(e1 - F0[1]) + kn[1] * phi(Fe2 - F0[2]) + kn[2] * phi(Fe3 - F0[3])
        E1 = 1 - c * a + kf[1] * Fe2 + kf[2] * Fe3 + kb[1] * p0 + n1
        if L >= 1:
            E2S = 1 + kf[1] * e3 + kb[1] * e1 + kb[2] * p0 + kn[0] * phi(e2S - Fe2) + kn[1] * phi(e3 - Fe3)
            E2D = 1 + kb[1] * e1 + kb[2] * p0 + kn[0] * phi(e2D - Fe2) + kn[1] * phi(-Fe3)
            E3 = 1 + kb[1] * e2S + kb[2] * e1 + kb[3] * p0
        else:
            E2S = E2D = 1 + kf[1] * sa * e3 + kb[1] * e1 + kb[2] * p0 + kn[0] * phi(e2S - Fe2) \
                + kn[1] * phi(sa * e3 - Fe3)
            E3 = 1 + kb[1] * e2S + kb[2] * e1 + kb[3] * p0 + kn[0] * phi((1 - sa) * e3)
        new = np.array([E1, E2S, E2D, E3])
        if np.max(np.abs(new - x)) < 1e-13:
            break
        x = 0.5 * new + 0.5 * x
    e1, e2S, e2D, e3 = x
    return e1 + sa * e2S + (1 - sa) * e2D + sa * e3


err = 0.0
for L in (0, 1):
    for lam in (1.0, 2.0):
        e_p, _, _ = four_plan(1, 0.9, 0.05, 0.2, L, lam, LIFE)
        R = e_p[1, 1] + 0.95 * e_p[1, 2] + 0.05 * e_p[0, 2] + 0.95 * e_p[1, 3]
        err = max(err, abs(four_fixed(1, 1, 0.9, 0.05, 0.2, L, lam, LIFE) - R))
report("four moments: the off-plan solver on plan = the tree", err, tol=1e-9)
d4 = 1e-3
for L in (0, 1):
    for lam in (1.0, 2.0):
        lo4, hi4 = (threshold(lambda c: four_fixed(1, ap, 0.9, d4, c, L, lam, LIFE)
                              - four_fixed(0, ap, 0.9, d4, c, L, lam, LIFE), tol=1e-11) / d4 for ap in (0, 1))
        cm4 = threshold(lambda c: four_plan(1, 0.9, d4, c, L, lam, LIFE)[1]
                        - four_plan(0, 0.9, d4, 0.0, L, lam, LIFE)[1], tol=1e-11) / d4
        print(f"      {'warned' if L else 'sudden'}, lam {lam:g}: commitment {cm4:.3f}, fixed-past band "
              f"[{lo4:.3f}, {hi4:.3f}]")


# 15. Codex's closed forms (cu-death): r = 1 - n + n s, q = A1 + n nu,
#     v_F = e2 (1-n)(1-n+q)/(r + s B1), v_M = e2 (1-n) q / r, v_C = e2 (1-n) G / Q,
#     G = 1 + A1 + A1^2 + A2 + B1 A2 - A1 B1, Q = (1+A1) r + s [B1 (1+A2) + B2 (A1 - A2)];
#     band edges F (1 + A1 - lam n + n nu), F (1 + A1 - n + lam n nu), F = e2 (1-n)/(r + s B1);
#     lost relief is -n s/(1-n) of every evaluator's WTP. Containment of the commitment
#     threshold in the band is an inequality, which fails at small news reach or weak news.
err, share = 0.0, 0.0
for _ in range(300):
    pr = dict(a_=rng.uniform(.01, .5), al=rng.uniform(.1, .9), m=rng.uniform(.01, .5), mu=rng.uniform(.1, .9),
              n=rng.uniform(.01, .4), nu=rng.uniform(.1, .95))
    s4 = rng.uniform(.3, .99)
    A1, A2, B1, B2 = pr["a_"] * pr["al"], pr["a_"] * pr["al"] ** 2, pr["m"] * pr["mu"], pr["m"] * pr["mu"] ** 2
    n4, nu4 = pr["n"], pr["nu"]
    r4, q4 = 1 - n4 + n4 * s4, A1 + n4 * nu4
    e4, _ = three_commit(0, s4, 0, 0, **pr)
    ch = three_channels(s4, **pr)
    G = 1 + A1 + A1 ** 2 + A2 + B1 * A2 - A1 * B1
    Q = (1 + A1) * r4 + s4 * (B1 * (1 + A2) + B2 * (A1 - A2))
    F4 = e4[2] * (1 - n4) / (r4 + s4 * B1)
    lo4, hi4 = three_band(s4, 2.0, **pr)
    err = max(err, abs(sum(ch["commitment"]) - e4[2] * (1 - n4) * G / Q),
              abs(sum(ch["fixed past"]) - F4 * (1 - n4 + q4)), abs(sum(ch["momentary"]) - e4[2] * (1 - n4) * q4 / r4),
              abs(lo4 - F4 * (1 + A1 - 2 * n4 + n4 * nu4)), abs(hi4 - F4 * (1 + A1 - n4 + 2 * n4 * nu4)))
    share = max(share, max(abs(v[3] / sum(v) + n4 * s4 / (1 - n4)) for v in ch.values()))
report("three moments: Codex's closed forms for the WTPs and band edges", err, tol=1e-12)
report("three moments: lost relief is -n s/(1-n) of each WTP", share, tol=1e-12)
cx3 = dict(par3, nu=0.1)                                 # Codex's counterexample: LIFE with nu = 0.1
cC3 = threshold(lambda c: three_commit(1, 0.9, 0.05, c, **cx3)[1] - three_commit(0, 0.9, 0.05, c, **cx3)[1])
lo3, hi3 = (threshold(lambda c: three_fixed(1, ap, 0.9, 0.05, c, **cx3, lam=2.0)[2]
                      - three_fixed(0, ap, 0.9, 0.05, c, **cx3, lam=2.0)[2]) for ap in (0, 1))
report("lam = 2, nu = 0.1: commitment (0.900) above the whole band [0.580, 0.773] (Codex)",
       float(not (hi3 < cC3)) + abs(cC3 / 0.05 - 0.900339) + abs(lo3 / 0.05 - 0.580350) + abs(hi3 / 0.05 - 0.772947),
       tol=1e-5)


# 16. Chosen death dates. (a) Appending a moment to a foreseen life changes the life-sum by that
#     moment's own felt state times 1 + 1'R_D k_f, the earlier selves' anticipation of it, echoed: a
#     planner extends iff the moment it adds would feel good, its memories of the life included.
def Kfore(D, a, al, m, mu, **_):
    i, j = np.meshgrid(np.arange(D), np.arange(D), indexing="ij")
    return np.where(j > i, a * al ** np.abs(j - i), 0) + np.where(j < i, m * mu ** np.abs(j - i), 0)


def last_gain(D, pr):
    """1 + 1'R_D k_f: what a unit of the appended moment's felt state adds to the life-sum."""
    return 1 + np.linalg.solve((np.eye(D) - Kfore(D, **pr)).T, np.ones(D)) @ (pr["a"] * pr["al"] ** np.arange(D, 0, -1))


err = 0.0
for _ in range(300):
    pr = dict(a=rng.uniform(0, .5), al=rng.uniform(.1, .9), m=rng.uniform(0, .5), mu=rng.uniform(.1, .9))
    if pr["a"] * pr["al"] / (1 - pr["al"]) + pr["m"] * pr["mu"] / (1 - pr["mu"]) > 0.9:
        continue
    D = int(rng.integers(2, 40))
    u = rng.normal(0, 1, D + 1)
    eD, eD1 = foreseen(u[:D], **pr), foreseen(u, **pr)
    err = max(err, abs(eD1.sum() - eD.sum() - eD1[-1] * last_gain(D, pr)))
report("chosen date: W(D+1) - W(D) = the appended moment's felt state x (1 + 1'R_D k_f)", err, tol=1e-10)
print(f"      life calibration, D = 200: 1 + 1'R_D k_f = {last_gain(200, LIFE):.4f}")
Wc = [foreseen(np.array([1.0, -2.0, 10.0])[:D], **LIFE).sum() for D in (1, 2, 3)]
report("first failure is not the optimum: u = (1, -2, 10), W = 1, -0.974841, 9.714593 (Codex)",
       float(not (Wc[1] < Wc[0] < Wc[2])) + abs(Wc[1] + 0.974841) + abs(Wc[2] - 9.714593), tol=1e-6)
# 16a'. Single crossing (Codex): geometric memory and a nonincreasing, nonpositive base tail keep every
#       appended felt state negative once one is.
bad = 0
for _ in range(100):
    pr = dict(a=rng.uniform(0, .4), al=rng.uniform(.1, .9), m=rng.uniform(0, .5), mu=rng.uniform(.1, .95))
    if pr["a"] * pr["al"] / (1 - pr["al"]) + pr["m"] * pr["mu"] / (1 - pr["mu"]) > 0.9:
        continue
    tail = -np.cumsum(rng.exponential(0.02, 80)) * rng.uniform(0, 1)
    u = np.r_[rng.uniform(0.5, 2, 30), tail]
    last = np.array([foreseen(u[:D + 1], **pr)[-1] for D in range(30, 110)])
    neg = np.flatnonzero(last <= 0)
    bad += len(neg) > 0 and bool(np.any(last[neg[0]:] > 0))
report("single crossing: after the first non-positive appended state, all are negative (Codex)", bad, tol=0.5)

# 16b. Living on memories: base utility 1 for 100 periods, then -c; the planner's chosen date
#      past the zero crossing, by memory reach (printed). The argmax is where the appended
#      moment's felt state first turns negative.
mB = lambda B, mu: B * (1 - mu) / mu
bad = 0
for label, pr in (("life calibration (mu 0.3, B 0.17)", LIFE), ("mu 0.9, same B", dict(LIFE, m=mB(0.4 * 0.3 / 0.7, 0.9), mu=0.9)),
                  ("mu 0.95, B 0.5", dict(LIFE, m=mB(0.5, 0.95), mu=0.95))):
    row = []
    for c in (0.02, 0.05, 0.1, 0.3):
        last = [foreseen(np.r_[np.ones(100), -c * np.ones(D - 99)], **pr)[-1] for D in range(100, 300)]
        Ws = [foreseen(np.r_[np.ones(100), -c * np.ones(D - 100)], **pr).sum() for D in range(100, 300)]
        row.append(int(np.argmax(Ws)))
        bad += row[-1] != int(np.argmax(np.array(last) < 0))
    print(f"      {label:34s} c = 0.02, 0.05, 0.1, 0.3: lives on {row} periods past the crossing")
report("chosen date: the argmax is where the appended moment first feels bad", bad, tol=0.5)


# 16c. The momentary self at t0, its past fixed on the plan, choosing death at t0 + 1 (the plan
#      foreseen, so the choice is news). Its felt state falls by S/(1 - lam n) if S > 0, S/(1 - n)
#      if not, S = sum_{j>=1} [a al^j e_{t0+j} + n nu^j psi(e_{t0+j})], psi of slope lam on
#      positive e (losing a good moment is a loss). It chooses by the sign of S, a kernel-weighted
#      forecast of its own felt states; its present base utility does not enter.
def exit_now(u, e, t0, lam, a, al, m, mu, n, nu):
    """Felt state at t0 on plan, choosing death at t0 + 1, the remaining life-sum on plan, and S."""
    T = len(u)
    kf, kb, kn = kernels(T, a, al, m, mu, n, nu)
    fut = e[t0 + 1:]
    X = u[t0] + kb[1:t0 + 1][::-1] @ e[:t0] + kn[1:T - t0] @ np.where(fut > 0, -lam * fut, -fut)
    up, dn = (X - n * e[t0]) / (1 - n), (X - lam * n * e[t0]) / (1 - lam * n)
    ed = up if up >= e[t0] else dn
    S = kf[1:T - t0] @ fut + kn[1:T - t0] @ np.where(fut > 0, lam * fut, fut)
    return e[t0], ed, e[t0:].sum(), S


err = 0.0
for _ in range(300):
    pr = dict(a=rng.uniform(0, .4), al=rng.uniform(.1, .9), m=rng.uniform(0, .4), mu=rng.uniform(.1, .9),
              n=rng.uniform(0, .4), nu=rng.uniform(.1, .9))
    lam = rng.choice([1.0, 2.0])
    if pr["a"] * pr["al"] / (1 - pr["al"]) + pr["m"] * pr["mu"] / (1 - pr["mu"]) > 0.9:
        continue
    u = rng.normal(0.3, 1, 40)
    ec, ed, _, S = exit_now(u, foreseen(u, **pr), 20, lam, **pr)
    err = max(err, abs(ec - ed - S / (1 - (lam if S > 0 else 1) * pr["n"])))
report("momentary exit: its felt state falls by S/(1 - lam n) or S/(1 - n), S the weighted forecast", err, tol=1e-10)
u = np.ones(150)
u[51] = -100.0
e = foreseen(u, **LIFE)
Ss = [exit_now(u, e, t, 1.0, **LIFE)[3] for t in (50, 51, 52, 53)]
report("a wait outlasting the patch does not filter it: S = -20.46, -2.49, -0.53, +0.30 at 50..53 (Codex)",
       max(abs(x - y) for x, y in zip(Ss, (-20.458522, -2.493839, -0.532714, 0.297476))), tol=1e-6)


# 16d. A foreseen bad patch of k periods at base level x in a long good life (u = 1): the level x*
#      below which each self prefers death at t0 + 1. The momentary threshold does not depend on
#      the length of the life left; the remaining-life self's falls with it (printed).
def patch_thresholds(k, lam, rem, pr, t0=300):
    T = t0 + 1 + rem
    one, pat = np.ones(T), np.zeros(T)
    pat[t0 + 1:t0 + 1 + k] = 1
    e1, ep = foreseen(one, **pr), foreseen(pat, **pr)
    out = []
    for which in ("momentary", "remaining"):
        lo, hi = 0.0, 1e4
        for _ in range(100):
            b = (lo + hi) / 2
            ec, ed, rem_sum, S = exit_now(one - b * pat, e1 - b * ep, t0, lam, **pr)
            lo, hi = (b, hi) if (S if which == "momentary" else rem_sum - ed) > 0 else (lo, b)
        out.append(lo)
    return [1 - b for b in out]


print("      bad patch of k periods at level x in a good life; x* for momentary / remaining-life self:")
for lam in (1.0, 2.0):
    for rem in (500, 2000):
        cells_ = [patch_thresholds(k, lam, rem, LIFE) for k in (1, 4, 13, 52)]
        print(f"        lam {lam:g}, {rem} periods left: " + "  ".join(f"k={k}: {m_:.3f} / {r_:.1f}" for k, (m_, r_)
                                                                    in zip((1, 4, 13, 52), cells_)))

# 16e. A hidden lottery against a chosen date: death uniform on a window, unannounced (sudden), against
#      a known date at the window's mean, life calibration (printed).
for lo_, T_ in ((16, 30), (46, 90)):
    Ds_ = np.arange(1, T_ + 1)
    P_ = ((Ds_ >= lo_) & (Ds_ <= T_)).astype(float)
    P_ /= P_.sum()
    Wk = foreseen(np.ones((lo_ + T_) // 2), **LIFE).sum()
    for lam in (1.0, 2.0):
        Wh, Wf = tree(np.ones(T_), P_, 0, **LIFE, lam=lam)[1], tree(np.ones(T_), P_, T_, **LIFE, lam=lam)[1]
        print(f"      death on {lo_}..{T_}, lam {lam:g}: hidden - known mean date {Wh - Wk:+.3f} "
              f"(hidden - foreseen from birth {Wh - Wf:+.3f}); W {Wk:.1f}")
# 16f. Codex's bound: with felt states in [0, E_max] for both lives, |E W_hidden - W_known| <=
#      E_max (N + J)/(1 - M), N = sum_j k_n(j), J = sum_j j (k_f(j) + k_b(j)): bounded in the mean
#      lifespan under uniform stability.
kf_, kb_, kn_ = kernels(400, **LIFE)
jj = np.arange(400)
Nm, Jm, Mm = kn_.sum(), jj @ (kf_ + kb_), kf_.sum() + kb_.sum()
bad = 0
for lo_, T_ in ((16, 30), (46, 90)):
    Ds_ = np.arange(1, T_ + 1)
    P_ = ((Ds_ >= lo_) & (Ds_ <= T_)).astype(float)
    P_ /= P_.sum()
    eh, Wh, _, _ = tree(np.ones(T_), P_, 0, **LIFE)
    ek = foreseen(np.ones((lo_ + T_) // 2), **LIFE)
    Emax = max(eh.max(), ek.max())
    bad += not (min(eh.min(), ek.min()) >= 0 and abs(Wh - ek.sum()) <= Emax * (Nm + Jm) / (1 - Mm))
report(f"the hidden lottery's gain within E_max (N + J)/(1 - M) = {Emax * (Nm + Jm) / (1 - Mm):.2f} (Codex)", bad, tol=0.5)


# 17. The momentary exit in personal equilibrium. (a) Plans: a foreseen bad patch of k periods at
#     level x in a good life (T = 160, patch after 60). A plan to exit at tau is a personal
#     equilibrium if no self before tau prefers exiting (S >= 0 on the plan's path) and self tau
#     prefers exiting to continuing, its continuation never exiting again (itself checked to be
#     one). Continuing against a planned exit revises forecasts up from zero: good moments are
#     gains, bad ones losses at lam, the mirror of exiting against a planned continuation.
def continue_from(u, P, tau, lam, a, al, m, mu, n, nu):
    """Self tau planned to exit (plan path P on 0..tau) and continues; later selves never exit.
    Returns the felt path from tau on."""
    T = len(u)
    kf, kb, kn = kernels(T, a, al, m, mu, n, nu)
    r = T - tau
    K, b = np.zeros((r, r)), u[tau:].copy()
    for k in range(r):
        K[k, k + 1:] += kf[1:r - k]
        K[k, :k] += kb[1:k + 1][::-1]
        b[k] += kb[tau + k - np.arange(tau)] @ P[:tau]
    c = np.ones(r)
    for _ in range(50):
        Kn, bn = K.copy(), b.copy()
        Kn[0, 0] += n * c[0]
        bn[0] -= n * c[0] * P[tau]
        Kn[0, 1:] += kn[1:r] * c[1:]
        x = np.linalg.solve(np.eye(r) - Kn, bn)
        cn = np.where(np.r_[x[0] - P[tau], x[1:]] >= 0, 1.0, lam)
        if np.all(cn == c):
            return x
        c = cn
    raise RuntimeError("sign iteration")


def plan_equilibria(xp, k, lam, pr=LIFE, T=160, t0=60):
    """Whether never exiting is an equilibrium, and the exit dates near the patch that are."""
    u = np.ones(T)
    u[t0 + 1:t0 + 1 + k] = xp
    e = foreseen(u, **pr)
    never = all(exit_now(u, e, t, lam, **pr)[3] >= 0 for t in range(T - 1))
    exits = []
    for tau in range(t0 - 2, t0 + 4):
        P = foreseen(u[:tau + 1], **pr)
        if not all(exit_now(u[:tau + 1], P, t, lam, **pr)[3] >= 0 for t in range(tau)):
            continue
        x = continue_from(u, P, tau, lam, **pr)
        full = np.r_[P[:tau], x]
        if x[0] <= P[tau] and all(exit_now(u, full, s, lam, **pr)[3] >= 0 for s in range(tau + 1, T - 1)):
            exits.append(tau)
    return never, exits


def edge(f, lo, hi, steps=14):
    """The x where f flips from False (below) to True (above)."""
    for _ in range(steps):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if f(mid) else (mid, hi)
    return (lo + hi) / 2


# Above x_lo the never-exit continuation is itself an equilibrium, so the exit plans' upper edge
# x_hi is searched there; below x_lo a deviation's continuation would need its own exit date.
print("      plans: never exiting is an equilibrium above x_lo; exiting before the patch too, up to x_hi")
bad = 0
for k, lo_, hi_ in ((1, -7.0, 0.0), (4, -1.5, 0.0)):
    for lam in (1.0, 1.2, 2.0):
        x_lo = edge(lambda xp: plan_equilibria(xp, k, lam)[0], lo_, hi_)
        x_hi = edge(lambda xp: not plan_equilibria(xp, k, lam)[1], x_lo + 1e-9, hi_)
        band = x_hi - x_lo
        print(f"        k = {k}, lam {lam:g}: x_lo {x_lo:+.3f}, x_hi {x_hi:+.3f}, band {band:.3f}")
        if lam == 1.0:
            bad += band > 1e-3
        else:
            nv, ex = plan_equilibria((x_lo + x_hi) / 2, k, lam)
            bad += not (band > 1e-3 and nv and ex)
report("plans, LIFE (alpha = nu): a band where both are equilibria opens at lam > 1, closes at lam = 1", bad, tol=0.5)
nv, ex = plan_equilibria(-2.1858, 1, 1.0, pr=dict(LIFE, nu=0.5))
report("unmatched kernels (nu = 0.5), lam = 1, x = -2.1858: both plans are equilibria (Codex)",
       float(not (nv and ex)), tol=0.5)


# 17b. Which equilibrium do expectations select? Foreseen plans carry no news, so the preferred
#      equilibrium of a self at t_f compares lam-free foreseen paths (selves at the same date in two
#      foreseen lives, not a choice with one past held fixed). Every prefix self ranks two plans by the
#      sign of Z = sum_j al^j e_{tau+j} (Codex), so formation time does not matter; with al = nu that
#      sign is the lam = 1 exit criterion, hence the switch at the lam = 1 edge. The life-sum prefers
#      never exiting throughout. (The Markov exit is in exit.py.)
def preferred(xp, k, lam, tf, pr=LIFE, T=160, t0=60):
    """Among the equilibria (never exit, and exits near the patch), the momentary choice at t_f and the
    life-sum's; None if the two kinds do not coexist."""
    never, exits = plan_equilibria(xp, k, lam, pr, T, t0)
    if not (never and exits):
        return None
    u = np.ones(T)
    u[t0 + 1:t0 + 1 + k] = xp
    paths = {T - 1: foreseen(u, **pr)} | {p: foreseen(u[:p + 1], **pr) for p in exits}
    tf = min(tf, min(exits))
    return (max(paths, key=lambda p: paths[p][tf]) == T - 1, max(paths, key=lambda p: paths[p].sum()) == T - 1)


bad = 0
for k, edge1 in ((1, -3.287), (4, -0.566)):
    for lam in (1.2, 2.0):
        for xp in (edge1 - 0.03, edge1 + 0.03):
            for tf in (0, 40, 55, 60):
                res = preferred(xp, k, lam, tf)
                if res is not None:
                    bad += res != (xp > edge1, True)
report("selection: the momentary preferred equilibrium switches at the lam = 1 edge; the life-sum never exits",
       bad, tol=0.5)
