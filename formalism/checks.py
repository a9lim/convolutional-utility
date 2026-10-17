"""Numerical checks for the formalism: core, decision, calibration, selves and learning.
Run: python formalism/checks.py

Conventions: K[t, s] is the weight of e(s) (recursive model R) or u(s) (direct model D)
in e(t). Geometric family: forward a*al**(s-t) for s > t, backward m*mu**(t-s) for s < t
(docs: a·α^j, m·μ^j; news n·ν^j).
"""
import importlib.util
import math
import os

import numpy as np

rng = np.random.default_rng(0)


def K_matrix(T, a, al, m, mu):
    d = np.arange(T)[None, :] - np.arange(T)[:, None]  # s - t
    fwd = np.where(d > 0, a * al ** np.clip(d, 0, None), 0.0)
    bwd = np.where(d < 0, m * mu ** np.clip(-d, 0, None), 0.0)
    return fwd + bwd


def resolvent_line(a, al, m, mu, N=4096):
    """Laurent coefficients r[n] (weight on u(t+n) in e(t)) of 1/(1 - K(z)) on the unit circle."""
    z = np.exp(2j * np.pi * np.arange(N) / N)
    K = a * al * z / (1 - al * z) + m * mu / (z - mu)
    return np.real(np.fft.fft(1 / (1 - K)) / N)


def mass(a, al, m, mu):
    return a * al / (1 - al) + m * mu / (1 - mu)


def geometric_closed_form(a, al, m, mu):
    A, B = (1 + a) * al, (1 + m) * mu
    C = 1 + (1 + a + m) * al * mu
    D = np.sqrt(C * C - 4 * A * B)
    H = (C + D) / 2
    p, q = A / H, B / H
    r0 = (1 + al * mu - al * q - mu * p) / D
    return p, q, r0


def stable_draws(n, amp=(0.05, 2.0), rate=(0.02, 0.9), cap=0.95):
    out = []
    while len(out) < n:
        a, m = rng.uniform(*amp, 2)
        al, mu = rng.uniform(*rate, 2)
        if mass(a, al, m, mu) < cap:
            out.append((a, al, m, mu))
    return out


def report(name, err, tol=1e-8):
    print(f"{'PASS' if err < tol else 'FAIL'}  {name}  (max err {err:.2e})")


# P1(al): constant u on the line -> e = u/(1-M); echo share = M
a, al, m, mu = 1, 0.3, 1, 0.2
T = 400
e = np.linalg.solve(np.eye(T) - K_matrix(T, a, al, m, mu), np.ones(T))
M = mass(a, al, m, mu)
report("P1b echo share = M (interior)", abs((e[T // 2] - 1) / e[T // 2] - M))

# P1(c): M > 1 yet positive on every finite life, with explosive growth
a, al, m, mu = 1, 0.6, 1, 0.05
print(f"P1c  M = {mass(a, al, m, mu):.3f}, predicted sup rho(K_T) = "
      f"{2 * np.sqrt(al * mu) / (1 - np.sqrt(al * mu)):.4f}")
for T in [20, 100, 400]:
    R = np.linalg.inv(np.eye(T) - K_matrix(T, a, al, m, mu))
    print(f"     T={T:3d}: min resolvent entry {R.min():.2e} (>= 0), e_mid for u=1: {(R @ np.ones(T))[T // 2]:.2e}")

# P3: one-sided recursion -> quasi-hyperbolic 1, (a/(1+a))((1+a)al)^n
a, al = 1.0, 0.3
r = resolvent_line(a, al, 0.0, 0.5)
pred = np.array([1] + [(a / (1 + a)) * ((1 + a) * al) ** n for n in range(1, 6)])
report("P3 one-sided resolvent", np.max(np.abs(r[:6] - pred)))

# P4: two-sided geometric closed form and beta_L = 1 - 1/((1+a) r0)
err_cf, err_bl, max_bl = 0.0, 0.0, 0.0
for a, al, m, mu in stable_draws(300):
    p, q, r0 = geometric_closed_form(a, al, m, mu)
    r = resolvent_line(a, al, m, mu)
    err_cf = max(err_cf, abs(r0 - r[0]), abs((r0 - 1 / (1 + a)) * p ** 3 - r[3]),
                 abs((r0 - 1 / (1 + m)) * q ** 2 - r[-2]))
    bl = r[1] / (r[0] * r[3] / r[2])
    err_bl = max(err_bl, abs(bl - (1 - 1 / ((1 + a) * r0))))
    max_bl = max(max_bl, bl)
report("P4 closed-form resolvent", err_cf)
report("P4 beta_L formula", err_bl)
print(f"     max beta_L over draws: {max_bl:.4f} (< 1)")

# P5 + P6: finite-life weights and ramp, closed forms for R; exact formula for D
err_w, err_E, err_D = 0.0, 0.0, 0.0
for a, al, m, mu in stable_draws(100):
    p, q, r0 = geometric_closed_form(a, al, m, mu)
    W = 1 / (1 - mass(a, al, m, mu))
    Linf, Uinf = W * (p - al) / (1 - al), W * (q - mu) / (1 - mu)
    for T in [2, 7, 40]:
        cT = (p - al) * q ** T / (1 - al * q)
        dT = (q - mu) * p ** T / (1 - mu * p)
        LT = (Linf - cT * Uinf) / (1 - cT * dT)
        UT = (Uinf - dT * Linf) / (1 - cT * dT)
        s = np.arange(T)
        K = K_matrix(T, a, al, m, mu)
        w = np.linalg.solve(np.eye(T) - K.T, np.ones(T))
        err_w = max(err_w, np.max(np.abs(W - LT * p ** s - UT * q ** (T - 1 - s) - w)))
        J = lambda x: np.sum(((T - 1) / 2 - s) * x ** s)
        err_E = max(err_E, abs(LT * J(p) - UT * J(q) - w @ (s - (T - 1) / 2)))
        wD = 1 + K.sum(axis=0)
        taus = np.arange(-(T - 1), T)
        kt = np.where(taus > 0, a * al ** np.clip(taus, 0, None), 0) \
            + np.where(taus < 0, m * mu ** np.clip(-taus, 0, None), 0)
        err_D = max(err_D, abs(wD @ (s - (T - 1) / 2) - 0.5 * np.sum(kt * (T - np.abs(taus)) * taus)))
report("P5 finite-life weight closed form (R)", err_w)
report("P6 ramp closed form (R)", err_E)
report("P6 ramp exact formula (D)", err_D)

# P6: finite-T sign flip despite negative first moment
a, al, m, mu = 1, 0.1, 0.1, 0.5
signs = []
for T in [2, 3, 5, 10, 40]:
    w = np.linalg.solve(np.eye(T) - K_matrix(T, a, al, m, mu).T, np.ones(T))
    signs.append(f"T={T}:{w @ (np.arange(T) - (T - 1) / 2):+.3f}")
print("P6  sign flip (M1 < 0):", "  ".join(signs))

# P6: asymptotic slope M1 / (2 (1-M)^2)
a, al, m, mu = 1, 0.3, 1, 0.2
M1 = a * al / (1 - al) ** 2 - m * mu / (1 - mu) ** 2
M = mass(a, al, m, mu)
T1, T2 = 400, 800
E = [np.linalg.solve(np.eye(T) - K_matrix(T, a, al, m, mu).T, np.ones(T)) @ (np.arange(T) - (T - 1) / 2)
     for T in (T1, T2)]
report("P6 asymptotic slope", abs((E[1] - E[0]) / (T2 - T1) - M1 / (2 * (1 - M) ** 2)), tol=1e-6)

# P6: size of the shape preference relative to the base utility rearranged, 4 M1 / T (D),
# 4 M1 / ((1-M)^2 T) (R)
a, al, m, mu = 0.15, 0.8, 0.1, 0.5
M1, M = a * al / (1 - al) ** 2 - m * mu / (1 - mu) ** 2, mass(a, al, m, mu)
rows = []
for T in [100, 1000, 3000]:
    K, u = K_matrix(T, a, al, m, mu), np.arange(T) - (T - 1) / 2
    gD = 2 * (1 + K.sum(axis=0)) @ u / np.abs(u).sum()
    gR = 2 * np.linalg.solve(np.eye(T) - K.T, np.ones(T)) @ u / np.abs(u).sum()
    rows.append(f"T={T}: D {gD:.4f} vs {4 * M1 / T:.4f}, R {gR:.4f} vs {4 * M1 / ((1 - M) ** 2 * T):.4f}")
print("P6  relative gap:", "; ".join(rows))

# P6 is about ramps: an end pulse against a start pulse compares echo masses, w(T-1) against w(0),
# not first moments. M1 < 0 (the decreasing ramp wins) while the end pulse beats the start pulse.
a, al, m, mu = 2, 0.2, 0.05, 0.8
M1 = a * al / (1 - al) ** 2 - m * mu / (1 - mu) ** 2
rows, ok = [], M1 < 0
for T in (200, 1000):
    K, u = K_matrix(T, a, al, m, mu), np.arange(T) - (T - 1) / 2
    for name, w in (("D", 1 + K.sum(axis=0)), ("R", np.linalg.solve(np.eye(T) - K.T, np.ones(T)))):
        pulse, ramp = w[-1] - w[0], w @ u - w @ u[::-1]
        ok = ok and pulse > 0 > ramp
        rows.append(f"T={T} {name}: end-minus-start pulse {pulse:+.3f}, ramp {ramp:+.1f}")
print(f"{'PASS' if ok else 'FAIL'}  P6 ramps only (M1 = {M1:.3f}): " + "; ".join(rows))

# P6 finite-T signs: R can differ from D; at equal amplitudes a = m the sign is sign(al - mu), D and R.
def ramp_gap(T, a, al, m, mu, rec):
    K, u = K_matrix(T, a, al, m, mu), np.arange(T) - (T - 1) / 2
    w = np.linalg.solve(np.eye(T) - K.T, np.ones(T)) if rec else 1 + K.sum(axis=0)
    return w @ u


bad, rng_p6 = 0, np.random.default_rng(6)  # own stream, so later draws are unchanged
for _ in range(500):
    a_, al_, mu_ = rng_p6.uniform(0.05, 1.0), rng_p6.uniform(0.02, 0.9), rng_p6.uniform(0.02, 0.9)
    if mass(a_, al_, a_, mu_) >= 0.95 or abs(al_ - mu_) < 1e-3:
        continue
    for T in (2, 3, 6, 20):
        bad += any(np.sign(ramp_gap(T, a_, al_, a_, mu_, rec)) != np.sign(al_ - mu_) for rec in (False, True))
flip = ramp_gap(6, 0.2, 0.7, 1, 0.3, False) > 0 > ramp_gap(6, 0.2, 0.7, 1, 0.3, True)
print(f"{'PASS' if bad == 0 and flip else 'FAIL'}  P6 signs: T = 6 example E_D > 0 > E_R; "
      f"a = m gives sign(al - mu) in D and R ({bad} violations)")

# P2: two-sided one-step R has exponential twin (beta_L = 1)
f, g = 0.3, 0.25
z = np.exp(2j * np.pi * np.arange(4096) / 4096)
r = np.real(np.fft.fft(1 / (1 - f * z - g / z)) / 4096)
report("P2 one-step R -> exponential", np.ptp([r[n + 1] / r[n] for n in range(5)]))

# P9: causal semantics -- decision weights are the first row on the remaining life
a, al, m, mu = 1, 0.3, 1, 0.2
for L in [60, 5, 3]:
    R = np.linalg.inv(np.eye(L) - K_matrix(L, a, al, m, mu))
    f = R[0]
    bl = f[1] / (f[0] * f[2] / f[1])
    print(f"P9  remaining life {L:2d}: r0={f[0]:.4f}  beta_L={bl:.4f}  "
          f"formula 1-1/((1+a)r0)={1 - 1 / ((1 + a) * f[0]):.4f}")


# ---- decision.md -----------------------------------------------------------------------

def weights_cdt(K, t, recursive=True):
    """Life-sum weight of u(s), s >= t, counting e(r) for r >= t only (felt past fixed)."""
    Ks = K[t:, t:]
    n = len(Ks)
    if recursive:
        return np.linalg.solve(np.eye(n) - Ks.T, np.ones(n))
    return 1 + Ks.sum(axis=0)


def weights_commit(K, recursive=True):
    return weights_cdt(K, 0, recursive)


def schedule(K, sign=+1, recursive=True):
    """One indivisible event (value sign*1) available from t = 0. Returns (CDT time, commitment time,
    full-life weights). CDT: sophisticated backward induction over selves sharing the
    life-sum objective. Commitment: the schedule maximizing the full-life weight."""
    T = len(K)
    tau = [0] * T
    tau[T - 1] = T - 1
    for t in range(T - 2, -1, -1):
        c = weights_cdt(K, t, recursive)
        tau[t] = t if sign * c[0] >= sign * c[tau[t + 1] - t] else tau[t + 1]
    w = weights_commit(K, recursive)
    return tau[0], int(np.argmax(sign * w)), w


# D3: savoring trap
T, n, pl, pa, losses = 40, 0, 0, 0, []
for _ in range(1500):
    rec = rng.random() < 0.5
    a, m = rng.uniform(0.05, 1.5, 2)
    al, mu = rng.uniform(0.1, 0.9, 2)
    if rec and mass(a, al, m, mu) >= 0.9:
        continue
    K = K_matrix(T, a, al, m, mu)
    n += 1
    c1, f1, w1 = schedule(K, +1, rec)
    c2, f2, w2 = schedule(K, -1, rec)
    pl += (c1 >= f1) or abs(w1[c1] - w1[f1]) < 1e-9
    pa += (c2 <= f2) or abs(w2[c2] - w2[f2]) < 1e-9
    losses.append(1 - w1[c1] / w1[f1])
print(f"D3  {n} draws: pleasure CDT not earlier than commitment {pl / n:.3f}; pain CDT not later than "
      f"commitment {pa / n:.3f}; pleasure loss median {np.median(losses):.3f}, max {max(losses):.3f}")

# D4: momentary hedonist, bilateral interior row vs fixed-past (remaining-life) first row
a, al, m, mu = 1, 0.3, 1, 0.2
for name, L, row in [("bilateral", 600, 300), ("fixed-past", 300, 0)]:
    R = np.linalg.inv(np.eye(L) - K_matrix(L, a, al, m, mu))
    f = R[row, row:row + 3]
    print(f"D4  {name}: r0={f[0]:.4f}  beta_L={f[1] / (f[0] * f[2] / f[1]):.4f}")

# D3 analytic (direct geometric model): stopping conditions for the CDT equilibrium
bad, n = 0, 0
for _ in range(1500):
    T = int(rng.integers(2, 40))
    N = T - 1
    a, m = rng.uniform(0.02, 2, 2)
    al, mu = rng.uniform(0.05, 0.95, 2)
    K = K_matrix(T, a, al, m, mu)
    A = lambda h: sum(a * al ** j for j in range(1, h + 1))
    B = lambda h: sum(m * mu ** j for j in range(1, h + 1))
    t = int(rng.integers(0, T))
    h = N - t
    c = weights_cdt(K, t, False)
    bad += any(abs((c[d] - c[0]) - (A(d) - mu ** (h - d) * B(d))) > 1e-9 for d in range(h + 1))
    cp, _, _ = schedule(K, +1, False)
    cq, fq, w = schedule(K, -1, False)
    if N >= 1:
        bad += (cp == N) != all(A(k) > B(k) for k in range(1, N + 1))
        bad += (cq == N) != all(A(k) < B(k) for k in range(1, N + 1))
        if al >= mu:
            hs = max([0] + [k for k in range(1, N + 1) if m * mu ** k >= a * al])
            bad += cp != N - hs
    bad += cq not in (0, N)
    bad += (cq > fq) and abs(w[cq] - w[fq]) > 1e-9
    n += 1
print(f"{'PASS' if bad == 0 else 'FAIL'}  D3 analytic stopping conditions ({n} draws, {bad} violations)")
for rec in (False, True):
    cp, fp, w = schedule(K_matrix(40, 0.0465, 0.896, 0.0196, 0.964), +1, rec)
    print(f"D3  long-memory exception ({'R' if rec else 'D'}): CDT {cp}, commitment {fp}, "
          f"loss {1 - w[cp] / w[fp]:.3f}")

# D3: the exception is preemption. Continuation times and each self's own optimum (D)
a, al, m, mu, T = 0.0465, 0.896, 0.0196, 0.964, 40
K = K_matrix(T, a, al, m, mu)
tau = [0] * T
tau[T - 1] = T - 1
for t in range(T - 2, -1, -1):
    c = weights_cdt(K, t, False)
    tau[t] = t if c[0] >= c[tau[t + 1] - t] else tau[t + 1]
own = [t + int(np.argmax(weights_cdt(K, t, False))) for t in range(T)]
A = lambda h: a * al * (1 - al ** h) / (1 - al)
B = lambda h: m * mu * (1 - mu ** h) / (1 - mu)
print(f"D3  preemption: tau[0..5] = {tau[:6]}, own optima[0..5] = {own[:6]}, "
      f"first h with B_h >= A_h: {min(h for h in range(1, T) if B(h) >= A(h))}")

# D4: half-line (fixed past) row: R+_00 = 1/H, beta_L = 1 - H/(1+a)
err = 0.0
for a, al, m, mu in stable_draws(100):
    A_, B_ = (1 + a) * al, (1 + m) * mu
    C = 1 + (1 + a + m) * al * mu
    H = (C + np.sqrt(C * C - 4 * A_ * B_)) / 2
    R = np.linalg.inv(np.eye(400) - K_matrix(400, a, al, m, mu))
    f = R[0, :4]
    err = max(err, abs(f[0] - 1 / H), abs(f[1] / (f[0] * f[2] / f[1]) - (1 - H / (1 + a))))
report("D4 half-line row closed form", err, tol=1e-8)


# D5: timing of information. Causal form with state-contingent paths and sign-dependent
# kernels; two equiprobable states differ in the last period's u, revealed at time r.
def info_welfare(r, rec, kp, km, T=6, al=0.7, mp=0.15, mm=0.15, mu=0.6):
    u = np.full((2, T), 0.3)
    u[0, -1], u[1, -1] = 1.0, -1.0
    e = u.copy()
    for _ in range(2000):
        X = e if rec else u
        new = u.copy()
        for t in range(T):
            for j in range(1, T - t):
                v = np.where(X[:, t + j] >= 0, kp, km) * al ** j * X[:, t + j]
                new[:, t] += v if t >= r else v.mean()
            for j in range(1, t + 1):
                new[:, t] += np.where(X[:, t - j] >= 0, mp, mm) * mu ** j * X[:, t - j]
        if np.max(np.abs(new - e)) < 1e-13:
            break
        e = new
    return e.sum(axis=1).mean()


spread = {}
for name, kp, km in [("symmetric", 0.2, 0.2), ("dread > savoring", 0.1, 0.35)]:
    for rec in (False, True):
        W = [info_welfare(r, rec, kp, km) for r in range(6)]
        spread[(name, rec)] = np.ptp(W)
        print(f"D5  {name}, {'R' if rec else 'D'}: welfare by reveal time 0..5: "
              + " ".join(f"{w:.5f}" for w in W))
report("D5 timing-neutral unless R with dread asymmetry",
       max(spread[("symmetric", False)], spread[("symmetric", True)], spread[("dread > savoring", False)]))
print(f"     R with dread asymmetry: later revelation is better, spread {spread[('dread > savoring', True)]:.5f}")


# N (core extension): felt news N_t = sum_j kn(j) phi(E[u_{t+j}|G_t] - E[u_{t+j}|G_{t-1}]), f = u + n
def cond(Y, cells, p):
    out = np.empty(len(Y))
    for c in np.unique(cells):
        out[cells == c] = p[cells == c] @ Y[cells == c] / p[cells == c].sum()
    return out


def news_welfare(u, G, p, kn, lam, kf, kb, rec):
    """Expected life-sum with felt news. u: (T, S) base utility by state; G: (T, S) felt-information
    cell labels (realized u_t is felt at t). Returns (welfare, expected news by period)."""
    T, S = u.shape
    fc = lambda t, s: u[s] if s <= t else cond(u[s], np.zeros(S, int) if t < 0 else G[t], p)
    phi = lambda x: np.where(x >= 0, x, lam * x)
    n = np.array([sum(kn(s - t) * phi(fc(t, s) - fc(t - 1, s)) for s in range(t, T)) for t in range(T)])
    f = u + n
    e = f.copy()
    for _ in range(5000):
        X = e if rec else f
        new = f.copy()
        for t in range(T):
            for j in range(1, T - t):
                new[t] += kf(j) * cond(X[t + j], G[t], p)
            for j in range(1, t + 1):
                new[t] += kb(j) * X[t - j]
        if not rec or np.max(np.abs(new - e)) < 1e-13:
            return p @ new.sum(axis=0), n @ p
        e = new


T = 8
Y = np.array([[.5, .5], [.5, -.5], [-.5, .5], [-.5, -.5]])  # u_7 = Y1 + Y2
p = np.full(4, .25)
u = np.full((T, 4), 0.2)
u[T - 1] = Y.sum(axis=1)
sched = lambda r1, r2: np.array([2 * (Y[:, 0] > 0) * (t >= r1) + (Y[:, 1] > 0) * (t >= r2) for t in range(T)])
schedules = {"clumped at 2": sched(2, 2), "piecemeal 2,5": sched(2, 5), "clumped at 5": sched(5, 5),
             "at realization": sched(7, 7)}
kf, kb = (lambda j: 0.25 * 0.7 ** j), (lambda j: 0.2 * 0.6 ** j)
Kn = np.array([[kf(s - t) if s > t else kb(t - s) if t > s else 0 for s in range(T)] for t in range(T)])
wts = {False: 1 + Kn.sum(axis=0), True: np.linalg.solve(np.eye(T) - Kn.T, np.ones(T))}
err_neutral, err_id, rows = 0.0, 0.0, []
for rec in (False, True):
    base = news_welfare(u, schedules["at realization"], p, lambda j: 0.5, 1.0, kf, kb, rec)[0]
    for kn_name, kn in [("flat", lambda j: 0.5), ("decaying", lambda j: 0.5 * 0.8 ** j)]:
        Ws = {}
        for name, G in schedules.items():
            err_neutral = max(err_neutral, abs(news_welfare(u, G, p, kn, 1.0, kf, kb, rec)[0] - base))
            Ws[name], En = news_welfare(u, G, p, kn, 2.5, kf, kb, rec)
            err_id = max(err_id, abs(Ws[name] - base - wts[rec] @ En))
        rows.append(f"{'R' if rec else 'D'} {kn_name} kn: " + ", ".join(f"{k} {v:.4f}" for k, v in Ws.items()))
report("N1 lam = 1: information timing neutral (D, R)", err_neutral)
report("N2 news cost = sum_r w(r) E[n_r] (D, R)", err_id)
for row in rows:
    print("     " + row)

# N3: optimism with felt disappointment (direct model). One event u_s = Z ~ N(0, 1), revealed at s.
Phi = np.vectorize(lambda x: 0.5 * (1 + math.erf(x / np.sqrt(2))))
T, s, lam = 12, 7, 2.5
z = np.linspace(-6, 6, 4001)
pz = np.exp(-z ** 2 / 2)
pz /= pz.sum()
kf, kb = (lambda j: 0.3 * 0.8 ** j), (lambda j: 0.25 * 0.6 ** j)
A, B = sum(kf(s - t) for t in range(s)), sum(kb(t - s) for t in range(s + 1, T))
phi = lambda x: np.where(x >= 0, x, lam * x)


def W_bias(bias, n0):
    """Event-related welfare when the felt forecast of u_s is biased by `bias` before s; the
    agent believes itself unbiased, so its anticipated news has the unbiased shape."""
    realized = pz @ (z + n0 * phi(z - bias))
    return A * (bias + pz @ (n0 * phi(z))) + (1 + B) * realized


err_slope, err_q = 0.0, 0.0
for n0 in (0.3, 0.5):
    h = 1e-5
    err_slope = max(err_slope, abs((W_bias(h, n0) - W_bias(-h, n0)) / (2 * h)
                                   - (A - n0 * (1 + B) * (1 + lam) / 2)))
    bs = np.linspace(-4, 4, 8001)
    b_star = bs[np.argmax([W_bias(x, n0) for x in bs])]
    err_q = max(err_q, abs(Phi(b_star) - (A / (n0 * (1 + B)) - 1) / (lam - 1)))
report("N3 optimism slope at bias 0: A - n0 (1+B)(1+lam)/2", err_slope)
report("N3 optimal bias at quantile (A/(n0(1+B)) - 1)/(lam - 1)", err_q, tol=1e-3)

# A1: recursive memory-only kernel, mirror of P3: r(-j) = (m/(1+m))((1+m)mu)^j
m, mu = 1.0, 0.3
r = resolvent_line(0.0, 0.5, m, mu)
report("A1 memory-only resolvent", max(abs(r[-j] - (m / (1 + m)) * ((1 + m) * mu) ** j) for j in range(1, 6)))
print(f"A1  b=2, m=1, mu=0.3: per-observer M = {m * mu / (1 - mu):.3f} (< 1); copy-counted "
      f"total ratio b(1+m)mu = {2 * (1 + m) * mu:.2f} (>= 1 diverges); measure-weighted ratio "
      f"(1+m)mu = {(1 + m) * mu:.2f}")
# A1 with anticipation: anticipation feeds back through memory, so the memory tail of the line
# resolvent is P4's q, longer than (1+m)mu; copy-counted totals need b q < 1.
a, al, m, mu, b = 0.3, 0.6, 0.6, 0.3, 2
q_tail = geometric_closed_form(a, al, m, mu)[1]
r = resolvent_line(a, al, m, mu)
report("A1 memory tail ratio with anticipation is q", max(abs(r[-j - 1] / r[-j] - q_tail) for j in range(1, 8)))
print(f"A1  b=2, a=0.3, al=0.6, m=0.6, mu=0.3: M = {mass(a, al, m, mu):.3f}; b(1+m)mu = "
      f"{b * (1 + m) * mu:.3f} (< 1) but b q = {b * q_tail:.4f} (>= 1 diverges)")


# N4: news over experienced utility. e_t = u_t + anticipation + memory
#     + sum_{j>=0} kn(j) phi(E[e_{t+j}|G_t] - E[e_{t+j}|G_{t-1}]), the j = 0 term being e_t itself.
def news_e_welfare(u, G, p, kn, lam, kf, kb, damp=0.5):
    T, S = u.shape
    phi = lambda x: np.where(x >= 0, x, lam * x)
    prior = np.zeros(S, int)
    e = u.copy()
    for _ in range(20000):
        new = u.copy()
        for t in range(T):
            for j in range(1, T - t):
                new[t] += kf(j) * cond(e[t + j], G[t], p)
            for j in range(1, t + 1):
                new[t] += kb(j) * e[t - j]
            for j in range(T - t):
                now = e[t] if j == 0 else cond(e[t + j], G[t], p)
                new[t] += kn(j) * phi(now - cond(e[t + j], G[t - 1] if t else prior, p))
        if np.max(np.abs(new - e)) < 1e-12:
            return p @ e.sum(axis=0)
        e = damp * new + (1 - damp) * e


T = 8
u = np.full((T, 4), 0.2)
u[T - 1] = Y.sum(axis=1)
schedules = {"clumped at 2": sched(2, 2), "piecemeal 2,5": sched(2, 5), "clumped at 5": sched(5, 5),
             "at realization": sched(7, 7)}
kf, kb = (lambda j: 0.25 * 0.7 ** j), (lambda j: 0.2 * 0.6 ** j)
base = news_welfare(u, schedules["at realization"], p, lambda j: 0.3, 1.0, kf, kb, True)[0]
err = max(abs(news_e_welfare(u, G, p, kn, 1.0, kf, kb) - base)
          for G in schedules.values() for kn in (lambda j: 0.3, lambda j: 0.3 * 0.7 ** j))
report("N4 news over e, lam = 1: neutral in expectation, equal to base R", err, tol=1e-9)
for kn_name, kn in [("flat", lambda j: 0.3), ("decaying", lambda j: 0.3 * 0.7 ** j)]:
    W = {k: news_e_welfare(u, G, p, kn, 2.0, kf, kb) for k, G in schedules.items()}
    print(f"     lam = 2, {kn_name} kn: " + ", ".join(f"{k} {v:.4f}" for k, v in W.items()))

# N4: well-foundedness. Felt news at a surprise solves h(s) = s - sum_j nu_j phi(x0_j + s g_j) = 0;
# unique and stable for every revision iff lam (kn . g) < 1. Between 1/lam and 1, a bad shock has no felt state.
T, t0 = 40, 20
j = np.arange(T)
kf_v, kb_v = np.where(j > 0, 0.1 * 0.85 ** j, 0), np.where(j > 0, 0.1 * 0.75 ** j, 0)
n = T - t0
A_ = np.array([[kf_v[c - r] if c > r else kb_v[r - c] if r > c else 0 for c in range(n)] for r in range(n)])
Rinv = np.linalg.inv(np.eye(n) - A_)
g = Rinv[:, 0]
grid = np.linspace(-200, 50, 5001)
rows = []
for n0, lam in [(0.3, 2.0), (0.45, 2.5)]:
    kn = np.array([n0] + [0.1 * 0.7 ** q for q in range(1, n)])
    phi = lambda x: np.where(x >= 0, x, lam * x)
    counts = []
    for shock in (-3.0, 3.0):
        hv = np.array([s - kn @ phi(g * shock + s * g) for s in grid])
        counts.append(int(np.sum(np.sign(hv[:-1]) != np.sign(hv[1:]))))
    rows.append(f"lam (kn.g) = {lam * kn @ g:.3f}: felt states after bad / good shock = {counts[0]} / {counts[1]}")
print("N4  " + "; ".join(rows))


# Canonical model, reduced form (core.md): effective coefficients and the echoed news kernel
spec_pw = importlib.util.spec_from_file_location("pathwise", os.path.join(os.path.dirname(__file__), "pathwise.py"))
pw = importlib.util.module_from_spec(spec_pw)
spec_pw.loader.exec_module(pw)
a, al, m, mu = 0.09, 0.88, 0.05, 0.75
p, q, r0 = geometric_closed_form(a, al, m, mu)
print(f"RF  r(0) = {r0:.3f}, p = {p:.3f}, q = {q:.3f}; reach fwd {1 / (1 - al):.1f} -> {1 / (1 - p):.1f}, "
      f"bwd {1 / (1 - mu):.1f} -> {1 / (1 - q):.1f}")
T, t0 = 120, 40
kf_r, kb_r = pw.kernels(T, a, al, m, mu)
kn_r = 0.3 * 0.8 ** np.arange(T)
eff, prim = [], []
for h in (1, 5, 20, 30, 50):
    ev = [(t0, t0 + h, 1.0, None)]
    eff.append(pw.run(T, 0.0, ev, kf_r, kb_r, kn_r, 1.0, "e")[1]["news"][t0])
    prim.append(pw.run(T, 0.0, ev, kf_r, kb_r, kn_r, 1.0, "u")[1]["news"][t0])
report("RF direct news equals the primitive kernel", max(abs(x - kn_r[h]) for x, h in zip(prim, (1, 5, 20, 30, 50))))
print("RF  echoed news kernel at h = 1, 5, 20, 30, 50: " + ", ".join(f"{x:.3f}" for x in eff))

# P1(d): non-summable tails. Simple-hyperbolic kernels with the same short-run rates
j = np.arange(1, 2000)
for T in (50, 2000):
    jj = j[: T - 1]
    M_T = (a / (1 - np.log(al) * jj)).sum() + (m / (1 - np.log(mu) * jj)).sum()
    print(f"P1d simple-hyperbolic tails: M_T = {M_T:.2f} at T = {T}")

# Calibration: invert present bias to one-sided primitives; the echo share it implies
err = 0.0
for bL, d in [(0.7, 0.96), (0.9, 0.96), (0.7, 0.9)]:
    a, al = bL / (1 - bL), d * (1 - bL)
    r = resolvent_line(a, al, 0.0, 0.5)
    M_pred = bL * d / (1 - d + bL * d)
    err = max(err, abs(r[1] / (r[0] * r[2] / r[1]) - bL), abs(r[2] / r[1] - d), abs(mass(a, al, 0.0, 0.5) - M_pred))
report("CAL inversion a = bL/(1-bL), beta = d(1-bL); M = bL d/(1-d+bL d)", err)

# ---- canonical-model audit -------------------------------------------------------------

# N4 threshold, closed form: on the half-line the felt-now column of the remaining-life
# resolvent is g_0 = 1/H, g_j = (q - mu) q^(j-1) / H, so kn . g = (n/H)(1 - nu mu)/(1 - nu q);
# finite remaining lives give a nondecreasing sequence below it.
err, mono = 0.0, True
for a, al, m, mu, n0, nu in [(0.09, 0.88, 0.05, 0.75, 0.3, 0.8), (0.1, 0.85, 0.1, 0.75, 0.3, 0.7),
                             (0.3, 0.5, 0.4, 0.6, 0.5, 0.9)]:
    A, B = (1 + a) * al, (1 + m) * mu
    C = 1 + (1 + a + m) * al * mu
    H = (C + np.sqrt(C * C - 4 * A * B)) / 2
    q = B / H
    kap = n0 / H * (1 - nu * mu) / (1 - nu * q)
    seq = [n0 * nu ** np.arange(L) @ np.linalg.inv(np.eye(L) - K_matrix(L, a, al, m, mu))[:, 0]
           for L in (2, 5, 20, 80, 400)]
    mono &= all(x <= y + 1e-12 for x, y in zip(seq, seq[1:]))
    err = max(err, abs(seq[-1] - kap))
report("N4 half-line kn.g = (n/H)(1 - nu mu)/(1 - nu q), nondecreasing in remaining life", err + (not mono))

# N4 regimes for a revision proportional to g (y = D + c phi(y)): unique below 1/lam; between
# 1/lam and 1 bad news has no root and good news two; above 1 one root again.
lam = 2.0
counts = {}
for c in (0.3, 0.7, 1.2):
    for D in (-1.0, 1.0):
        ys = np.linspace(-400, 400, 800001) + 1e-4 * np.pi   # offset: no root on a grid point
        hv = ys - D - c * np.where(ys >= 0, ys, lam * ys)
        counts[(c, D)] = int(np.sum(np.sign(hv[:-1]) != np.sign(hv[1:])))
print("N4  roots (bad / good news) at lam = 2: " + "; ".join(
    f"c = {c}: {counts[(c, -1.0)]} / {counts[(c, 1.0)]}" for c in (0.3, 0.7, 1.2)))
report("N4 regimes: 1/1 below 1/lam, 0/2 between, 1/1 above 1",
       float(counts != {(0.3, -1.0): 1, (0.3, 1.0): 1, (0.7, -1.0): 0, (0.7, 1.0): 2, (1.2, -1.0): 1, (1.2, 1.0): 1}))


# N3 in the canonical model (recursive echoes, news over e, Bayesian forecasts with anticipated news).
# One event u_s = Z ~ N(0,1); the self believes u_s ~ N(b, 1). Generic solver, then the closed form:
# dW/db|0 = Acal - (1'g) kt [1 + (lt - 1) P(Z < sbar)], with kappa = kn . g, kt = kappa/(1 - kappa),
# lt = lam (1 - kappa)/(1 - lam kappa), sbar = E[psi(Z' - sbar)] the anticipated news, and
# Acal = w_s - 1'g the life-weighted value of foreseeing the event. Optimum: P(Z < b* + sbar) = (Th - 1)/(lt - 1).
def n3_canonical(b, T, s, a, al, m, mu, n0, nu, lam, zs, w_obj):
    K = K_matrix(T, a, al, m, mu)
    P, F = np.arange(s), np.arange(s, T)
    RF = np.linalg.inv(np.eye(T - s) - K[np.ix_(F, F)])
    RP = np.linalg.inv(np.eye(s) - K[np.ix_(P, P)])
    g, kn = RF[:, 0], n0 * nu ** np.arange(T - s)
    phi = lambda x: np.where(x >= 0, x, lam * x)
    w_sub = np.exp(-(zs - b) ** 2 / 2)
    w_sub /= w_sub.sum()

    def felt(eP, xprev):
        uF = np.zeros((len(zs), T - s))
        uF[:, 0] = zs
        x0 = (uF + K[np.ix_(F, P)] @ eP) @ RF.T
        lo, hi = np.full(len(zs), -300.0), np.full(len(zs), 300.0)
        for _ in range(64):
            mid = (lo + hi) / 2
            neg = mid - phi(x0 - xprev + mid[:, None] * g) @ kn < 0
            lo, hi = np.where(neg, mid, lo), np.where(neg, hi, mid)
        return x0 + ((lo + hi) / 2)[:, None] * g

    eP, xprev = np.zeros(s), np.zeros(T - s)
    for _ in range(3000):
        xnew = 0.85 * xprev + 0.15 * (w_sub @ felt(eP, xprev))   # damped: the anticipated-news map is expansive
        eP_new = RP @ (K[np.ix_(P, F)] @ xnew)
        done = max(np.abs(xnew - xprev).max(), np.abs(eP_new - eP).max()) < 1e-12
        xprev, eP = xnew, eP_new
        if done:
            break
    return eP.sum() + w_obj @ felt(eP, xprev).sum(axis=1), K, g, kn


zs = np.linspace(-7, 7, 1001)
w_obj = np.exp(-zs ** 2 / 2)
w_obj /= w_obj.sum()
Phi = np.vectorize(lambda x: 0.5 * (1 + math.erf(x / np.sqrt(2))))
Phinv = lambda p: zs[np.argmin(np.abs(Phi(zs) - p))]
err_s, err_b = 0.0, 0.0
for T, s, a, al, m, mu, n0, nu, lam in [(12, 7, 0.15, 0.8, 0.1, 0.6, 0.3, 0.7, 2.5),
                                        (14, 9, 0.12, 0.7, 0.1, 0.6, 0.25, 0.6, 3.0)]:
    args = (T, s, a, al, m, mu, n0, nu, lam, zs, w_obj)
    _, K, g, kn = n3_canonical(0.0, *args)
    kap = kn @ g
    kt, lt = kap / (1 - kap), lam * (1 - kap) / (1 - lam * kap)
    psi = lambda y: np.where(y >= 0, kt * y, lt * kt * y)
    lo, hi = -50.0, 0.0
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if mid - w_obj @ psi(zs - mid) < 0 else (lo, mid)
    sbar = (lo + hi) / 2
    w = np.linalg.solve(np.eye(T) - K.T, np.ones(T))
    Acal, one_g = w[s] - g.sum(), g.sum()
    h = 1e-4
    slope = (n3_canonical(h, *args)[0] - n3_canonical(-h, *args)[0]) / (2 * h)
    err_s = max(err_s, abs(slope - (Acal - one_g * kt * (1 + (lt - 1) * Phi(sbar)))))
    Th = Acal / (one_g * kt)
    b_star = Phinv((Th - 1) / (lt - 1)) - sbar
    slope_at_star = (n3_canonical(b_star + h, *args)[0] - n3_canonical(b_star - h, *args)[0]) / (2 * h)
    err_b = max(err_b, abs(slope_at_star))
    print(f"N3c lam kappa = {lam * kap:.3f}, amplified loss aversion {lt:.2f}, anticipated news {sbar:.3f}, "
          f"P(loss | b = 0) = {Phi(sbar):.3f}, b* = {b_star:.3f}")
report("N3 canonical slope at bias 0 (closed form)", err_s, tol=5e-3)
report("N3 canonical optimum: slope vanishes at the predicted b*", err_b, tol=2e-2)

# N3 in the core (lam = 1): no anticipated news, and the slope Acal - (1'g) kt at every bias, so the
# hedonic optimum is a corner.
h, err1 = 1e-4, 0.0
for T, s, a, al, m, mu, n0, nu in [(12, 7, 0.15, 0.8, 0.1, 0.6, 0.3, 0.7), (14, 9, 0.12, 0.7, 0.1, 0.6, 0.25, 0.6)]:
    args = (T, s, a, al, m, mu, n0, nu, 1.0, zs, w_obj)
    _, K, g, kn = n3_canonical(0.0, *args)
    kt = (kn @ g) / (1 - kn @ g)
    w = np.linalg.solve(np.eye(T) - K.T, np.ones(T))
    pred = w[s] - g.sum() - g.sum() * kt
    for b0 in (-1.0, 0.0, 1.5):
        slope = (n3_canonical(b0 + h, *args)[0] - n3_canonical(b0 - h, *args)[0]) / (2 * h)
        err1 = max(err1, abs(slope - pred))
report("N3 canonical, lam = 1: slope Acal - (1'g) kt at every bias", err1, tol=5e-3)


# D5, exact: with sign-dependent strengths (kp, km forward; mp, mm backward) and Bayesian forecasts,
# E[W] = W_sym - sum_t w_t [(km - kp) sum_j al^j E[X_{t+j}^-] + (mm - mp) sum_j mu^j E[X_{t-j}^-]],
# w the life weights of the (kp, mp) kernel (D: 1 for these terms); no felt news. X = u in D:
# timing-free. X = e in R: information timing matters only if some felt state can land on either
# side of zero. Revelation times r <= s: realized base utility is felt when it happens.
def dread(r, rec, kp, km, mp, mm, T=8, s=5, al=0.7, mu=0.6, base=0.1):
    u = np.full((2, T), base)
    u[0, s] += 2.0
    u[1, s] -= 2.0
    e = u.copy()
    for _ in range(6000):
        X = e if rec else u
        new = u.copy()
        for t in range(T):
            for j in range(1, T - t):
                v = np.where(X[:, t + j] >= 0, kp, km) * al ** j * X[:, t + j]
                new[:, t] += v if t >= r else v.mean()
            for j in range(1, t + 1):
                new[:, t] += np.where(X[:, t - j] >= 0, mp, mm) * mu ** j * X[:, t - j]
        if np.max(np.abs(new - e)) < 1e-14:
            break
        e = 0.5 * e + 0.5 * new
    X = e if rec else u
    K = np.array([[kp * al ** (c - t) if c > t else mp * mu ** (t - c) if t > c else 0 for c in range(T)]
                  for t in range(T)])
    w = np.linalg.solve(np.eye(T) - K.T, np.ones(T)) if rec else np.ones(T)
    wu = np.linalg.solve(np.eye(T) - K.T, np.ones(T)) if rec else 1 + K.sum(axis=0)
    neg = np.maximum(-X, 0).mean(axis=0)
    dA = np.array([sum(al ** j * neg[t + j] for j in range(1, T - t)) for t in range(T)])
    dM = np.array([sum(mu ** j * neg[t - j] for j in range(1, t + 1)) for t in range(T)])
    return e.sum(axis=1).mean(), wu @ u.mean(axis=0) - w @ ((km - kp) * dA + (mm - mp) * dM), e.min()


err_id, spreads = 0.0, {}
for rec in (False, True):
    for name, ks in [("dread", (0.1, 0.35, 0.15, 0.15)), ("rumination", (0.2, 0.2, 0.1, 0.3))]:
        for base in (0.1, 3.0):
            out = [dread(r, rec, *ks, base=base) for r in range(6)]
            err_id = max(err_id, max(abs(W - pred) for W, pred, _ in out))
            spreads[(name, rec, base)] = (np.ptp([o[0] for o in out]), min(o[2] for o in out))
report("D5 identity: E[W] = W_sym - asymmetry x life-weighted E[X^-]", err_id, tol=1e-10)
for name in ("dread", "rumination"):
    print(f"D5  {name}: welfare spread over reveal times D {spreads[(name, False, 0.1)][0]:.1e}, "
          f"R {spreads[(name, True, 0.1)][0]:.3f} (min e {spreads[(name, True, 0.1)][1]:+.2f}); "
          f"R with e > 0 throughout {spreads[(name, True, 3.0)][0]:.1e} (min e {spreads[(name, True, 3.0)][1]:+.2f})")
report("D5 straddle: every felt state of fixed sign -> timing neutral in R",
       max(spreads[(n, True, 3.0)][0] for n in ("dread", "rumination"))
       + max(spreads[(n, False, b)][0] for n in ("dread", "rumination") for b in (0.1, 3.0)), tol=1e-10)


# D5 under death risk: moment 1 exists with probability 1 - p, learned at 0 or never. The recursive
# loop runs only in the surviving branch and its gain is convex in survival, so information is priced.
def mortality_info(u0, u1, a, m, p, rec):
    if not rec:
        return p * u0 + (1 - p) * (u0 + a * u1 + u1 + m * u0) - (u0 + a * (1 - p) * u1 + (1 - p) * (u1 + m * u0))
    e0 = (u0 + a * (1 - p) * u1) / (1 - a * (1 - p) * m)
    eB = (u0 + a * u1) / (1 - a * m)
    return p * u0 + (1 - p) * (eB + u1 + m * eB) - (e0 + (1 - p) * (u1 + m * e0))


got = [mortality_info(0, 1, .5, .5, .5, True), mortality_info(0, -1, .5, .5, .5, True),
       mortality_info(0, 1, .5, .5, .5, False), mortality_info(0, 1, .5, .5, 0, True),
       mortality_info(0, 1, .5, 0, .5, True), mortality_info(0, 1, 0, .5, .5, True)]
report("D5 death risk: value of knowing +-1/7 (R), 0 direct, 0 without risk, 0 with either kernel alone",
       max(abs(g - t) for g, t in zip(got, [1 / 7, -1 / 7, 0, 0, 0, 0])))

# Information boundary: a surprise reaches the present through the remaining-life column (1/H now),
# not the bilateral row r(0); the reduced form describes foreseen lives.
a, al, m, mu = 1.0, 0.3, 1.0, 0.2
p, q, r0 = geometric_closed_form(a, al, m, mu)
H = (1 + (1 + a + m) * al * mu + np.sqrt((1 + (1 + a + m) * al * mu) ** 2 - 4 * (1 + a) * al * (1 + m) * mu)) / 2
g = np.linalg.inv(np.eye(400) - K_matrix(400, a, al, m, mu))[:, 0]
report("RF surprise response g_0 = 1/H, g_j = (q - mu) q^(j-1)/H", max(abs(g[0] - 1 / H),
       max(abs(g[j] - (q - mu) * q ** (j - 1) / H) for j in range(1, 8))))
print(f"RF  unforeseen unit at 0: causal e_0 = 1/H = {1 / H:.6f}; bilateral reduced form r(0) = {r0:.6f}")


# P1(d): a genuine spectral crossing for the two-sided simple-hyperbolic example
a, al, m, mu = 0.09, 0.88, 0.05, 0.75
def K_hyp(T):
    d = np.arange(T)[None, :] - np.arange(T)[:, None]
    return np.where(d > 0, a / (1 - np.log(al) * np.abs(d)), 0.0) + np.where(d < 0, m / (1 - np.log(mu) * np.abs(d)), 0.0)
rho = {T: max(abs(np.linalg.eigvals(K_hyp(T)))) for T in (41, 42, 2000)}
print("P1d rho(K_T) = " + ", ".join(f"{v:.3f} at T = {T}" for T, v in rho.items()))
report("P1d hyperbolic tails cross rho(K_T) = 1 between T = 41 and 42", float(not (rho[41] < 1 <= rho[42])))


# Calibration: default parameter sets per horizon (calibration.md), derived quantities
for name, (A_, al, B_, mu, n0, nu) in {"waking day, hourly": (0.2, 0.8, 0.1, 0.5, 0.2, 0.8),
                                       "life, weekly": (0.15, 0.7, 0.17, 0.3, 0.2, 0.7)}.items():
    a, m = A_ * (1 - al) / al, B_ * (1 - mu) / mu
    p, q, r0 = geometric_closed_form(a, al, m, mu)
    C = 1 + (1 + a + m) * al * mu
    H = (C + np.sqrt(C * C - 4 * (1 + a) * al * (1 + m) * mu)) / 2
    kap = n0 / H * (1 - nu * mu) / (1 - nu * q)
    print(f"CAL {name}: a = {a:.3f}, m = {m:.3f}; M = {A_ + B_:.2f}; beta_L = {1 - 1 / ((1 + a) * r0):.3f} "
          f"(bilateral), {1 - H / (1 + a):.3f} (causal); "
          f"reach {1 / (1 - al):.1f} -> {1 / (1 - p):.1f} ahead, {1 / (1 - mu):.1f} -> {1 / (1 - q):.1f} back; "
          f"kappa = {kap:.3f}, loop amplification 1/(1 - kappa) = {1 / (1 - kap):.3f}")

# Calibration, the quoted numbers: life weights at the ends against the interior (life, P5), each
# default's loop gain kappa and amplification 1/(1 - kappa), and the threshold's memory multiplier and examples.
def kappa_half(a, al, m, mu, n0, nu):
    _, q_, _ = geometric_closed_form(a, al, m, mu)
    C_ = 1 + (1 + a + m) * al * mu
    H_ = (C_ + np.sqrt(C_ * C_ - 4 * (1 + a) * al * (1 + m) * mu)) / 2
    return n0 / H_ * (1 - nu * mu) / (1 - nu * q_), (1 - nu * mu) / (H_ * (1 - nu * q_))


day, life = (0.05, 0.8, 0.1, 0.5), (0.15 * 0.3 / 0.7, 0.7, 0.17 * 0.7 / 0.3, 0.3)
w = np.linalg.solve(np.eye(400) - K_matrix(400, *life).T, np.ones(400))
kd, kl = kappa_half(*day, 0.2, 0.8)[0], kappa_half(*life, 0.2, 0.7)[0]
got = [w[0], w[-1], w[200], kd, kl, 1 / (1 - kd), 1 / (1 - kl),
       kappa_half(*life, 0.2, 0.7)[1], kappa_half(0.0, 0.7, 0.5, 0.6, 0.6, 0.9)[0],
       kappa_half(0.064, 0.7, 0.5, 0.6, 0.6, 0.9)[0]]
doc = [1.22, 1.21, 1.47, 0.22, 0.23, 1.27, 1.29, 1.13, 1.45, 1.90]
report("CAL quoted numbers: ends 1.22/1.21 vs 1.47; kappa 0.22/0.23, amplification 1.27/1.29; "
       "multiplier 1.13; kappa 1.45/1.90 at n = 0.6",
       max(abs(g - d) for g, d in zip(got, doc)), tol=0.006)

# N4 with saturating gain-loss, y = D + c clip(phi(y), -1, 1): bistable over a range of shocks only
# (Codex: c = 0.7, lam = 2 gives roots -0.6, -0.25, 1/3 at D = 0.1, one root at D = +-1).
def sat_roots(D, c=0.7, lam=2.0):
    ys = np.linspace(-5, 5, 1000001) + 1e-5 * np.pi
    hv = ys - D - c * np.clip(np.where(ys >= 0, ys, lam * ys), -1, 1)
    idx = np.nonzero(np.sign(hv[:-1]) != np.sign(hv[1:]))[0]
    return np.round(ys[idx], 3)
sat = {D: sat_roots(D) for D in (0.1, 1.0, -1.0)}
print("N4  saturating news: roots " + "; ".join(f"D = {D}: {[float(x) for x in r]}" for D, r in sat.items()))
report("N4 saturation: three roots at D = 0.1, one at D = +-1",
       float(not (len(sat[0.1]) == 3 and len(sat[1.0]) == 1 and len(sat[-1.0]) == 1)))

# pathwise.news_root: roots on a breakpoint or an interval end are found (Codex reproducers)
err = abs(pw.news_root(np.array([.75]), np.array([1.]), np.array([.25]), 2.) - 0.25)
err = max(err, abs(pw.news_root(np.array([-3.]), np.array([1.]), np.array([.499]), 2.) + 1497))
err = max(err, abs(pw.news_root(np.array([0.]), np.array([1.]), np.array([.3]), 2.)))
report("pathwise exact news root (endpoint, far root, zero revision)", err, tol=1e-9)

# ---- decision theory under the canonical model ---------------------------------------------

# D2 with linear news: a fixed-past self's weights on a deviation are c_t(s) + (1'g) kn'(s - t),
# kn' = kn'R_F/(1 - kappa) the local news kernel. Deviation = cancel the forecast, announce anew.
T, t = 30, 10
a, al, m, mu, n0, nu = 0.2, 0.7, 0.15, 0.6, 0.3, 0.7
KF_, KB_ = pw.kernels(T, a, al, m, mu)
KN_ = n0 * nu ** np.arange(T)
RF = np.linalg.inv(np.eye(T - t) - K_matrix(T - t, a, al, m, mu))
g = RF[:, 0]
pred = RF.sum(axis=0) + g.sum() * (KN_[:T - t] @ RF) / (1 - KN_[:T - t] @ g)
base = pw.run(T, 0.0, [], KF_, KB_, KN_, 1.0, "e")[0][t:].sum()
num = [(pw.run(T, 0.0, [(t, t + h, 1e-3, None)], KF_, KB_, KN_, 1.0, "e")[0][t:].sum() - base) / 1e-3
       for h in range(6)]
report("D2 deviation weights with linear news: c_t + (1'g) kn'", max(abs(x - y) for x, y in zip(num, pred)), tol=1e-6)


# D3 under the canonical model: one pleasure announced at 0, Kőszegi–Rabin-style credible replanning.
# Switching the planned date p to q at t changes remaining welfare by
# Delta_t(p->q) = v 1'R_t(d_q - d_p) + (1'g_t) N,  N = kn . phi(v R_t(d_q - d_p) + N g_t)  (independent
# of the past). C_{T-1} = {T-1}; A_t = {t} u C_{t+1}; C_t = {p in A_t: Delta_t(p->q) <= 0 for all q in A_t}.
# At 0 the plan is chosen against the no-event prior: the best of {0} u C_1.
def d3_credible(T, a, al, m, mu, n0, nu, lam, v=1.0):
    K = K_matrix(T, a, al, m, mu)
    R = [np.linalg.inv(np.eye(T - t) - K[t:, t:]) for t in range(T)]
    kn = n0 * nu ** np.arange(T)

    def delta(t, p, q):
        d = v * (R[t][:, q - t] - R[t][:, p - t])
        return d.sum() + R[t][:, 0].sum() * pw.news_root(d, R[t][:, 0], kn[:T - t], lam)

    C = [T - 1]
    for t in range(T - 2, 0, -1):
        A = sorted(set([t] + C))
        C = [p for p in A if all(delta(t, p, q) <= 1e-12 for q in A if q != p)]
        assert C, "no credible plan"
    W = [(v * R[0][:, x] + pw.news_root(v * R[0][:, x], R[0][:, 0], kn, lam) * R[0][:, 0]).sum() for x in range(T)]
    commit = int(np.argmax(W))
    return C, commit, max(sorted(set([0] + C)), key=lambda x: W[x])


C0, c0, p0 = d3_credible(20, 0.3, 0.7, 0.2, 0.6, 0.0, 0.7, 1.0)
C2, c2, p2 = d3_credible(20, 0.3, 0.7, 0.2, 0.6, 0.3, 0.7, 2.0)
Cs, cs, ps = d3_credible(20, 0.3, 0.7, 0.2, 0.6, 0.001, 0.7, 2.0)
print(f"D3c credible plans at 1: no news {C0} (commitment {c0}); n = 0.3, lam = 2: {C2} (commitment {c2}, "
      f"preferred {p2}); n = 0.001, lam = 2: {Cs} (commitment {cs})")
report("D3c trap without news and for weak news; loss-averse news makes the commitment plan credible",
       float(not (C0 == [19] and c0 == 15 and C2 == [12, 13, 14] and c2 == 14 == p2 and Cs == [19] and cs == 15)))


# D6 under the canonical model: pay c at d for v at s; c is high (cH) with probability p, revealed at d.
# Bayesian forecasts on a two-state tree; the high-cost self compares on-path with deviating.
def d6_tree(u, d, p, a, al, m, mu, n0, nu, lam):
    pr = np.array([1 - p, p])
    T = u.shape[1]
    phi = lambda x: np.where(x >= 0, x, lam * x)
    Ex = lambda X, t: X if t >= d else np.full(2, pr @ X)
    e = u.copy()
    for _ in range(20000):
        new = u.copy()
        for t in range(T):
            for j in range(1, T - t):
                new[:, t] += a * al ** j * Ex(e[:, t + j], t)
            for j in range(1, t + 1):
                new[:, t] += m * mu ** j * e[:, t - j]
            for j in range(T - t):
                now = e[:, t] if j == 0 else Ex(e[:, t + j], t)
                new[:, t] += n0 * nu ** j * phi(now - Ex(e[:, t + j], t - 1))
        if np.max(np.abs(new - e)) < 1e-12:
            return e
        e = 0.5 * new + 0.5 * e


def d6_margin(pay_high, T, d, s, p, v, cL, cH, a, al, m, mu, n0, nu, lam):
    """(E[W], on-path minus deviation value for the high-cost self at d)."""
    def u_of(pay):
        u = np.zeros((2, T))
        u[0, d] -= cL
        u[0, s] += v
        if pay:
            u[1, d] -= cH
            u[1, s] += v
        return u
    e = d6_tree(u_of(pay_high), d, p, a, al, m, mu, n0, nu, lam)
    K = K_matrix(T, a, al, m, mu)
    F, P = np.arange(d, T), np.arange(d)
    RF = np.linalg.inv(np.eye(T - d) - K[np.ix_(F, F)])
    x0 = RF @ (u_of(not pay_high)[1][d:] + K[np.ix_(F, P)] @ e[1, :d])
    sdev = pw.news_root(x0 - np.array([1 - p, p]) @ e[:, d:], RF[:, 0], n0 * nu ** np.arange(T - d), lam)
    return np.array([1 - p, p]) @ e.sum(axis=1), e[1, d:].sum() - (x0 + sdev * RF[:, 0]).sum()


args = (16, 3, 10, 0.3, 3.0, 0.5, 2.5, 0.1, 0.8, 0.15, 0.6)
rows = {}
for n0, lam in [(0.0, 1.0), (0.3, 1.0), (0.5, 1.0), (0.3, 2.0)]:
    rows[(n0, lam)] = [d6_margin(pay, *args, n0, 0.5, lam) for pay in (True, False)]
for (n0, lam), ((Wr, mr), (Wf, mf)) in rows.items():
    print(f"D6c n = {n0}, lam = {lam}: E[W] reliable {Wr:.3f}, flaky {Wf:.3f}; "
          f"reliable self-enforcing {mr >= 0} ({mr:+.3f}), flaky {mf >= 0} ({mf:+.3f})")
(Wr0, mr0), (Wf0, mf0) = rows[(0.0, 1.0)]
(Wr1, mr1), (Wf1, mf1) = rows[(0.5, 1.0)]
(Wr2, mr2), (Wf2, mf2) = rows[(0.3, 2.0)]
report("D6c felt news makes the high-cost self flaky against the planner (linear at n = 0.5; loss-averse at n = 0.3)",
       float(not (Wr0 > Wf0 and mr0 >= 0 > mf0 and abs(Wr1 - Wr0) < 1e-9 and mr1 < 0 <= mf1
                  and rows[(0.3, 1.0)][0][1] >= 0 and Wr2 > Wf2 and mr2 < 0 <= mf2)))

# RL reading: linear news over e is (n/nu) times the TD error e_{t-1} + nu V_t - V_{t-1}, with
# V_t = sum_j nu^j x_t(j) over the forecast path of e (x_t(0) = e_t); pathwise, lam = 1.
T = 40
KF_, KB_ = pw.kernels(T, 0.1, 0.85, 0.1, 0.75)
n0, nu = 0.3, 0.7
KN_ = n0 * nu ** np.arange(T)
EV = [(5, 20, 3.0, None), (12, 30, -2.0, None), (None, 25, 1.5, None)]
e, comp, _ = pw.run(T, 0.0, EV, KF_, KB_, KN_, 1.0, "e")


def forecast_path(t):
    nrem = T - t
    A_ = K_matrix(nrem, 0.1, 0.85, 0.1, 0.75)
    mem = np.array([e[:t][::-1] @ KB_[k + 1:k + 1 + t] for k in range(nrem)]) if t else np.zeros(nrem)
    R = np.linalg.inv(np.eye(nrem) - A_)
    return R @ (pw.forecast_u(T, 0.0, EV, t)[t:] + mem) + comp["news"][t] * R[:, 0]


V = [nu ** np.arange(T - t) @ forecast_path(t) for t in range(T)]
report("RL news = (n/nu) x TD error at discount nu (lam = 1)",
       max(abs(comp["news"][t] - (n0 / nu) * (e[t - 1] + nu * V[t] - V[t - 1])) for t in range(1, T)), tol=1e-10)

# N3 canonical at the felt calibrations: Theta = Acal/((1'g) kt) against the band (1, lt).
for name, (a, al, m, mu, n0, nu, lam) in {"day": (0.05, 0.8, 0.1, 0.5, 0.2, 0.8, 1.5),
                                         "life": (0.0643, 0.7, 0.3967, 0.3, 0.2, 0.7, 1.5),
                                         "life, n = 0.1": (0.0643, 0.7, 0.3967, 0.3, 0.1, 0.7, 1.5)}.items():
    T, s = 200, 100
    K = K_matrix(T, a, al, m, mu)
    w = np.linalg.solve(np.eye(T) - K.T, np.ones(T))
    g = np.linalg.inv(np.eye(T - s) - K_matrix(T - s, a, al, m, mu))[:, 0]
    kap = n0 * nu ** np.arange(T - s) @ g
    kt, lt = kap / (1 - kap), lam * (1 - kap) / (1 - lam * kap)
    Th = (w[s] - g.sum()) / (g.sum() * kt)
    print(f"N3c {name}: Theta = {Th:.2f}, band (1, {lt:.2f}) -> "
          + ("pessimism corner" if Th <= 1 else "optimism corner" if Th >= lt else "interior"))

# The local news kernel need not decay: with strong anticipation and nu near 1 it rises (Codex),
# so news at the deviation margin need not add present bias.
T, t0 = 200, 0
a, al, m, mu, n0, nu = 0.2, 0.8, 0.0, 0.5, 0.1, 0.99
Rp = np.linalg.inv(np.eye(T) - K_matrix(T, a, al, m, mu))
kn = n0 * nu ** np.arange(T)
knp = (kn @ Rp) / (1 - kn @ Rp[:, 0])
print("D4  rising local news kernel kn'(0..4): " + ", ".join(f"{x:.4f}" for x in knp[:5]))
report("D4 kn' can rise with distance", float(not np.all(np.diff(knp[:5]) > 0)))

# D7: actions leak into affect. Z = +-1 seen by the doer, a = Z w.p. q, u = sZ + r 1[a = Z] + eps eta at T
# (eta = +-1 revealed only at T); the feeler knows the policy and sees a at 1 (or not: an unobserved delegate);
# loss-averse news over u at unit weights.
def leak_welfare(q, s, r, eps, lam, observe=True):
    Eu, W = r * q, 0.0
    for Z in (1, -1):
        for act, pa in ((Z, q), (-Z, 1 - q)):
            for eta in (1, -1):
                u = s * Z + r * (act == Z) + eps * eta
                mid = s * (2 * q - 1) * act + r * q
                revs = [mid - Eu, u - mid] if observe else [u - Eu]
                W += 0.25 * pa * (u + (lam - 1) * sum(min(x, 0.0) for x in revs))
    return W


errs = []
for s_, r_, lam_ in [(2, 0.5, 2), (1, 1, 1.5), (3, 0.2, 2.5), (0.5, 2, 3)]:
    for q in np.linspace(0.5, 1, 11):
        closed = r_ * q - (lam_ - 1) * (s_ * (q - 0.5) + q * (1 - q) * max(r_, 2 * s_))
        errs.append(abs(leak_welfare(q, s_, r_, 0, lam_) - closed))
    errs.append(abs(leak_welfare(1, s_, r_, 0, lam_) - leak_welfare(1, s_, r_, 0, lam_, observe=False)))
report("D7 leakage, eps = 0: E[W] = rq - (lam-1)[s(q - 1/2) + q(1-q) max(r, 2s)]; a full leak is free", max(errs))
act, ign, dlg = (leak_welfare(1, 1, 0.3, 1, 2), leak_welfare(0.5, 1, 0.3, 1, 2),
                 leak_welfare(1, 1, 0.3, 1, 2, observe=False))
print(f"{'PASS' if dlg > ign > act else 'FAIL'}  D7 partial leak (s = 1, r = 0.3, eps = 1, lam = 2): act and observe "
      f"{act:.2f}, ignore {ign:.2f}, unobserved delegate {dlg:.2f}")


# D8: a shared state carries the critic's level. Two-layer linear model, heads frozen, critic fitted alone
# (W and its bias at equal rates): shifting fitted targets by f = mu + w.xi moves the stay logit by
# (s.v) [mu/(1 + |v|^2) + w.xi/|v|^2], the bias taking mu/(1 + |v|^2).
rng = np.random.default_rng(0)
N, d, H, mu0 = 2000, 5, 8, 0.7
xi = rng.normal(size=(N, d))
X = np.hstack([np.ones((N, 1)), xi - xi.mean(0)])
y = X @ rng.normal(size=d + 1)
W, v, s_ = rng.normal(size=(H, d + 1)) * 0.3, rng.normal(size=H), rng.normal(size=H)
wf = rng.normal(size=d) * 0.3


def d8_fit(W, c, target, steps=20000, eta=0.01):
    for _ in range(steps):
        res = X @ W.T @ v + c - target
        c, W = c - eta * 2 * res.mean(), W - eta * 2 * np.outer(v, res @ X / N)
    return W, c


W0, c0 = d8_fit(W.copy(), 0.0, y)
W1, c1 = d8_fit(W0.copy(), c0, y + mu0 + X[:, 1:] @ wf)
probe = np.hstack([np.ones((20, 1)), rng.normal(size=(20, d))])
dz = probe @ (W1 - W0).T @ s_
pred = (s_ @ v) * (mu0 / (1 + v @ v) + probe[:, 1:] @ wf / (v @ v))
report("D8b forcing: dz = (s.v)[mu/(1 + |v|^2) + f~/|v|^2]; the bias takes mu/(1 + |v|^2)",
       float(max(np.abs(dz - pred).max(), abs(c1 - c0 - mu0 / (1 + v @ v)))), tol=1e-9)
# (c) at a balanced rank-one zero-error factorization: s.v = alpha beta/sigma, |v|^2 = alpha^2/sigma ...
errs = []
for al, be in [(1.0, 0.6), (1.0, -0.6), (-0.5, -0.8)]:
    sg, u = np.hypot(al, be), rng.normal(size=H)
    u /= np.linalg.norm(u)
    W1_, W2_ = np.sqrt(sg) * np.outer(u, [1, 0, 0, 0]), np.vstack([al * u, be * u]) / np.sqrt(sg)
    errs += [np.abs(W2_ @ W1_[:, 0] - [al, be]).max(), abs(W2_[1] @ W2_[0] - al * be / sg),
             abs(W2_[0] @ W2_[0] - al ** 2 / sg)]
report("D8c balanced rank-one factorization: s.v = alpha beta/sigma, |v|^2 = alpha^2/sigma", max(errs), tol=1e-12)
# ... and small random initialization gets there (corroboration; not exactly balanced or whitened).
errs = []
for al, be in [(1.0, 0.6), (1.0, -0.6), (-0.5, -0.8)]:
    r = rng.normal(size=N)
    Xc = np.column_stack([(r - r.mean()) / r.std(), rng.normal(size=(N, 3))])
    Y = np.column_stack([al * Xc[:, 0], be * Xc[:, 0]])
    W1_, W2_ = rng.normal(size=(H, 4)) * 1e-3, rng.normal(size=(2, H)) * 1e-3
    for _ in range(40000):
        E = Xc @ W1_.T @ W2_.T - Y
        W2_, W1_ = W2_ - 0.01 * E.T @ (Xc @ W1_.T) / N, W1_ - 0.01 * W2_.T @ E.T @ Xc / N
    errs += [abs(W2_[1] @ W2_[0] - al * be / np.hypot(al, be)), abs(W2_[0] @ W2_[0] - al ** 2 / np.hypot(al, be))]
report("D8c small initialization reaches it", max(errs), tol=1e-3)
