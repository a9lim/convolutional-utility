"""Numerical checks for formalism/core.md. Run: python formalism/checks.py

Conventions: K[t, s] is the weight of e(s) (recursive model R) or u(s) (direct model D)
in e(t). Geometric family: forward a*b**(s-t) for s > t, backward m*al**(t-s) for s < t.
"""
import importlib.util
import math
import os

import numpy as np

rng = np.random.default_rng(0)


def K_matrix(T, a, b, m, al):
    d = np.arange(T)[None, :] - np.arange(T)[:, None]  # s - t
    fwd = np.where(d > 0, a * b ** np.clip(d, 0, None), 0.0)
    bwd = np.where(d < 0, m * al ** np.clip(-d, 0, None), 0.0)
    return fwd + bwd


def resolvent_line(a, b, m, al, N=4096):
    """Laurent coefficients r[n] (weight on u(t+n) in e(t)) of 1/(1 - K(z)) on the unit circle."""
    z = np.exp(2j * np.pi * np.arange(N) / N)
    K = a * b * z / (1 - b * z) + m * al / (z - al)
    return np.real(np.fft.fft(1 / (1 - K)) / N)


def mass(a, b, m, al):
    return a * b / (1 - b) + m * al / (1 - al)


def geometric_closed_form(a, b, m, al):
    A, B = (1 + a) * b, (1 + m) * al
    C = 1 + (1 + a + m) * b * al
    D = np.sqrt(C * C - 4 * A * B)
    H = (C + D) / 2
    p, q = A / H, B / H
    r0 = (1 + b * al - b * q - al * p) / D
    return p, q, r0


def stable_draws(n, amp=(0.05, 2.0), rate=(0.02, 0.9), cap=0.95):
    out = []
    while len(out) < n:
        a, m = rng.uniform(*amp, 2)
        b, al = rng.uniform(*rate, 2)
        if mass(a, b, m, al) < cap:
            out.append((a, b, m, al))
    return out


def report(name, err, tol=1e-8):
    print(f"{'PASS' if err < tol else 'FAIL'}  {name}  (max err {err:.2e})")


# P1(b): constant u on the line -> e = u/(1-M); echo share = M
a, b, m, al = 1, 0.3, 1, 0.2
T = 400
e = np.linalg.solve(np.eye(T) - K_matrix(T, a, b, m, al), np.ones(T))
M = mass(a, b, m, al)
report("P1b echo share = M (interior)", abs((e[T // 2] - 1) / e[T // 2] - M))

# P1(c): M > 1 yet positive on every finite life, with explosive growth
a, b, m, al = 1, 0.6, 1, 0.05
print(f"P1c  M = {mass(a, b, m, al):.3f}, predicted sup rho(K_T) = "
      f"{2 * np.sqrt(b * al) / (1 - np.sqrt(b * al)):.4f}")
for T in [20, 100, 400]:
    R = np.linalg.inv(np.eye(T) - K_matrix(T, a, b, m, al))
    print(f"     T={T:3d}: min resolvent entry {R.min():.2e} (>= 0), e_mid for u=1: {(R @ np.ones(T))[T // 2]:.2e}")

# P3: one-sided recursion -> quasi-hyperbolic 1, (a/(1+a))((1+a)b)^n
a, b = 1.0, 0.3
r = resolvent_line(a, b, 0.0, 0.5)
pred = np.array([1] + [(a / (1 + a)) * ((1 + a) * b) ** n for n in range(1, 6)])
report("P3 one-sided resolvent", np.max(np.abs(r[:6] - pred)))

# P4: two-sided geometric closed form and beta_L = 1 - 1/((1+a) r0)
err_cf, err_bl, max_bl = 0.0, 0.0, 0.0
for a, b, m, al in stable_draws(300):
    p, q, r0 = geometric_closed_form(a, b, m, al)
    r = resolvent_line(a, b, m, al)
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
for a, b, m, al in stable_draws(100):
    p, q, r0 = geometric_closed_form(a, b, m, al)
    W = 1 / (1 - mass(a, b, m, al))
    Linf, Uinf = W * (p - b) / (1 - b), W * (q - al) / (1 - al)
    for T in [2, 7, 40]:
        cT = (p - b) * q ** T / (1 - b * q)
        dT = (q - al) * p ** T / (1 - al * p)
        LT = (Linf - cT * Uinf) / (1 - cT * dT)
        UT = (Uinf - dT * Linf) / (1 - cT * dT)
        s = np.arange(T)
        K = K_matrix(T, a, b, m, al)
        w = np.linalg.solve(np.eye(T) - K.T, np.ones(T))
        err_w = max(err_w, np.max(np.abs(W - LT * p ** s - UT * q ** (T - 1 - s) - w)))
        J = lambda x: np.sum(((T - 1) / 2 - s) * x ** s)
        err_E = max(err_E, abs(LT * J(p) - UT * J(q) - w @ (s - (T - 1) / 2)))
        wD = 1 + K.sum(axis=0)
        taus = np.arange(-(T - 1), T)
        kt = np.where(taus > 0, a * b ** np.clip(taus, 0, None), 0) \
            + np.where(taus < 0, m * al ** np.clip(-taus, 0, None), 0)
        err_D = max(err_D, abs(wD @ (s - (T - 1) / 2) - 0.5 * np.sum(kt * (T - np.abs(taus)) * taus)))
report("P5 finite-life weight closed form (R)", err_w)
report("P6 ramp closed form (R)", err_E)
report("P6 ramp exact formula (D)", err_D)

# P6: finite-T sign flip despite negative first moment
a, b, m, al = 1, 0.1, 0.1, 0.5
signs = []
for T in [2, 3, 5, 10, 40]:
    w = np.linalg.solve(np.eye(T) - K_matrix(T, a, b, m, al).T, np.ones(T))
    signs.append(f"T={T}:{w @ (np.arange(T) - (T - 1) / 2):+.3f}")
print("P6  sign flip (mu1 < 0):", "  ".join(signs))

# P6: asymptotic slope mu1 / (2 (1-M)^2)
a, b, m, al = 1, 0.3, 1, 0.2
mu1 = a * b / (1 - b) ** 2 - m * al / (1 - al) ** 2
M = mass(a, b, m, al)
T1, T2 = 400, 800
E = [np.linalg.solve(np.eye(T) - K_matrix(T, a, b, m, al).T, np.ones(T)) @ (np.arange(T) - (T - 1) / 2)
     for T in (T1, T2)]
report("P6 asymptotic slope", abs((E[1] - E[0]) / (T2 - T1) - mu1 / (2 * (1 - M) ** 2)), tol=1e-6)

# P6: size of the shape preference relative to the base utility rearranged, 4 mu1 / T (D),
# 4 mu1 / ((1-M)^2 T) (R)
a, b, m, al = 0.15, 0.8, 0.1, 0.5
mu1, M = a * b / (1 - b) ** 2 - m * al / (1 - al) ** 2, mass(a, b, m, al)
rows = []
for T in [100, 1000, 3000]:
    K, u = K_matrix(T, a, b, m, al), np.arange(T) - (T - 1) / 2
    gD = 2 * (1 + K.sum(axis=0)) @ u / np.abs(u).sum()
    gR = 2 * np.linalg.solve(np.eye(T) - K.T, np.ones(T)) @ u / np.abs(u).sum()
    rows.append(f"T={T}: D {gD:.4f} vs {4 * mu1 / T:.4f}, R {gR:.4f} vs {4 * mu1 / ((1 - M) ** 2 * T):.4f}")
print("P6  relative gap:", "; ".join(rows))

# P2: two-sided one-step R has exponential twin (beta_L = 1)
f, g = 0.3, 0.25
z = np.exp(2j * np.pi * np.arange(4096) / 4096)
r = np.real(np.fft.fft(1 / (1 - f * z - g / z)) / 4096)
report("P2 one-step R -> exponential", np.ptp([r[n + 1] / r[n] for n in range(5)]))

# P9: causal semantics -- decision weights are the first row on the remaining life
a, b, m, al = 1, 0.3, 1, 0.2
for L in [60, 5, 3]:
    R = np.linalg.inv(np.eye(L) - K_matrix(L, a, b, m, al))
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
    b, al = rng.uniform(0.1, 0.9, 2)
    if rec and mass(a, b, m, al) >= 0.9:
        continue
    K = K_matrix(T, a, b, m, al)
    n += 1
    c1, f1, w1 = schedule(K, +1, rec)
    c2, f2, w2 = schedule(K, -1, rec)
    pl += (c1 >= f1) or abs(w1[c1] - w1[f1]) < 1e-9
    pa += (c2 <= f2) or abs(w2[c2] - w2[f2]) < 1e-9
    losses.append(1 - w1[c1] / w1[f1])
print(f"D3  {n} draws: pleasure CDT not earlier than commitment {pl / n:.3f}; pain CDT not later than "
      f"commitment {pa / n:.3f}; pleasure loss median {np.median(losses):.3f}, max {max(losses):.3f}")

# D4: momentary hedonist, bilateral interior row vs fixed-past (remaining-life) first row
a, b, m, al = 1, 0.3, 1, 0.2
for name, L, row in [("bilateral", 600, 300), ("fixed-past", 300, 0)]:
    R = np.linalg.inv(np.eye(L) - K_matrix(L, a, b, m, al))
    f = R[row, row:row + 3]
    print(f"D4  {name}: r0={f[0]:.4f}  beta_L={f[1] / (f[0] * f[2] / f[1]):.4f}")

# D3 analytic (direct geometric model): stopping conditions for the CDT equilibrium
bad, n = 0, 0
for _ in range(1500):
    T = int(rng.integers(2, 40))
    N = T - 1
    a, m = rng.uniform(0.02, 2, 2)
    b, al = rng.uniform(0.05, 0.95, 2)
    K = K_matrix(T, a, b, m, al)
    A = lambda h: sum(a * b ** j for j in range(1, h + 1))
    B = lambda h: sum(m * al ** j for j in range(1, h + 1))
    t = int(rng.integers(0, T))
    h = N - t
    c = weights_cdt(K, t, False)
    bad += any(abs((c[d] - c[0]) - (A(d) - al ** (h - d) * B(d))) > 1e-9 for d in range(h + 1))
    cp, _, _ = schedule(K, +1, False)
    cq, fq, w = schedule(K, -1, False)
    if N >= 1:
        bad += (cp == N) != all(A(k) > B(k) for k in range(1, N + 1))
        bad += (cq == N) != all(A(k) < B(k) for k in range(1, N + 1))
        if b >= al:
            hs = max([0] + [k for k in range(1, N + 1) if m * al ** k >= a * b])
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
a, b, m, al, T = 0.0465, 0.896, 0.0196, 0.964, 40
K = K_matrix(T, a, b, m, al)
tau = [0] * T
tau[T - 1] = T - 1
for t in range(T - 2, -1, -1):
    c = weights_cdt(K, t, False)
    tau[t] = t if c[0] >= c[tau[t + 1] - t] else tau[t + 1]
own = [t + int(np.argmax(weights_cdt(K, t, False))) for t in range(T)]
A = lambda h: a * b * (1 - b ** h) / (1 - b)
B = lambda h: m * al * (1 - al ** h) / (1 - al)
print(f"D3  preemption: tau[0..5] = {tau[:6]}, own optima[0..5] = {own[:6]}, "
      f"first h with B_h >= A_h: {min(h for h in range(1, T) if B(h) >= A(h))}")

# D4: half-line (fixed past) row: R+_00 = 1/H, beta_L = 1 - H/(1+a)
err = 0.0
for a, b, m, al in stable_draws(100):
    A_, B_ = (1 + a) * b, (1 + m) * al
    C = 1 + (1 + a + m) * b * al
    H = (C + np.sqrt(C * C - 4 * A_ * B_)) / 2
    R = np.linalg.inv(np.eye(400) - K_matrix(400, a, b, m, al))
    f = R[0, :4]
    err = max(err, abs(f[0] - 1 / H), abs(f[1] / (f[0] * f[2] / f[1]) - (1 - H / (1 + a))))
report("D4 half-line row closed form", err, tol=1e-8)


# D5: timing of information. Causal form with state-contingent paths and sign-dependent
# kernels; two equiprobable states differ in the last period's u, revealed at time r.
def info_welfare(r, rec, kp, km, T=6, b=0.7, mp=0.15, mm=0.15, al=0.6):
    u = np.full((2, T), 0.3)
    u[0, -1], u[1, -1] = 1.0, -1.0
    e = u.copy()
    for _ in range(2000):
        X = e if rec else u
        new = u.copy()
        for t in range(T):
            for j in range(1, T - t):
                v = np.where(X[:, t + j] >= 0, kp, km) * b ** j * X[:, t + j]
                new[:, t] += v if t >= r else v.mean()
            for j in range(1, t + 1):
                new[:, t] += np.where(X[:, t - j] >= 0, mp, mm) * al ** j * X[:, t - j]
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


# N (core extension): felt news n_t = sum_j nu(j) mu(E[u_{t+j}|G_t] - E[u_{t+j}|G_{t-1}]), f = u + n
def cond(Y, cells, p):
    out = np.empty(len(Y))
    for c in np.unique(cells):
        out[cells == c] = p[cells == c] @ Y[cells == c] / p[cells == c].sum()
    return out


def news_welfare(u, G, p, nu, lam, kf, kb, rec):
    """Expected life-sum with felt news. u: (T, S) base utility by state; G: (T, S) felt-information
    cell labels (realized u_t is felt at t). Returns (welfare, expected news by period)."""
    T, S = u.shape
    fc = lambda t, s: u[s] if s <= t else cond(u[s], np.zeros(S, int) if t < 0 else G[t], p)
    mu = lambda x: np.where(x >= 0, x, lam * x)
    n = np.array([sum(nu(s - t) * mu(fc(t, s) - fc(t - 1, s)) for s in range(t, T)) for t in range(T)])
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
    for nu_name, nu in [("flat", lambda j: 0.5), ("decaying", lambda j: 0.5 * 0.8 ** j)]:
        Ws = {}
        for name, G in schedules.items():
            err_neutral = max(err_neutral, abs(news_welfare(u, G, p, nu, 1.0, kf, kb, rec)[0] - base))
            Ws[name], En = news_welfare(u, G, p, nu, 2.5, kf, kb, rec)
            err_id = max(err_id, abs(Ws[name] - base - wts[rec] @ En))
        rows.append(f"{'R' if rec else 'D'} {nu_name} nu: " + ", ".join(f"{k} {v:.4f}" for k, v in Ws.items()))
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
mu = lambda x: np.where(x >= 0, x, lam * x)


def W_bias(b, nu0):
    """Event-related welfare when the felt forecast of u_s is biased by b before s; the agent
    believes itself unbiased, so its anticipated news has the unbiased shape."""
    realized = pz @ (z + nu0 * mu(z - b))
    return A * (b + pz @ (nu0 * mu(z))) + (1 + B) * realized


err_slope, err_q = 0.0, 0.0
for nu0 in (0.3, 0.5):
    h = 1e-5
    err_slope = max(err_slope, abs((W_bias(h, nu0) - W_bias(-h, nu0)) / (2 * h)
                                   - (A - nu0 * (1 + B) * (1 + lam) / 2)))
    bs = np.linspace(-4, 4, 8001)
    b_star = bs[np.argmax([W_bias(b, nu0) for b in bs])]
    err_q = max(err_q, abs(Phi(b_star) - (A / (nu0 * (1 + B)) - 1) / (lam - 1)))
report("N3 optimism slope at b = 0: A - nu0 (1+B)(1+lam)/2", err_slope)
report("N3 optimal bias at quantile (A/(nu0(1+B)) - 1)/(lam - 1)", err_q, tol=1e-3)

# A1: recursive memory-only kernel, mirror of P3: r(-j) = (m/(1+m))((1+m)al)^j
m, al = 1.0, 0.3
r = resolvent_line(0.0, 0.5, m, al)
report("A1 memory-only resolvent", max(abs(r[-j] - (m / (1 + m)) * ((1 + m) * al) ** j) for j in range(1, 6)))
print(f"A1  b=2, m=1, al=0.3: per-observer M = {m * al / (1 - al):.3f} (< 1); copy-counted "
      f"total ratio b(1+m)al = {2 * (1 + m) * al:.2f} (>= 1 diverges); measure-weighted ratio "
      f"(1+m)al = {(1 + m) * al:.2f}")


# N4: news over experienced utility. e_t = u_t + anticipation + memory
#     + sum_{j>=0} nu(j) mu(E[e_{t+j}|G_t] - E[e_{t+j}|G_{t-1}]), the j = 0 term being e_t itself.
def news_e_welfare(u, G, p, nu, lam, kf, kb, damp=0.5):
    T, S = u.shape
    mu = lambda x: np.where(x >= 0, x, lam * x)
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
                new[t] += nu(j) * mu(now - cond(e[t + j], G[t - 1] if t else prior, p))
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
err = max(abs(news_e_welfare(u, G, p, nu, 1.0, kf, kb) - base)
          for G in schedules.values() for nu in (lambda j: 0.3, lambda j: 0.3 * 0.7 ** j))
report("N4 news over e, lam = 1: neutral in expectation, equal to base R", err, tol=1e-9)
for nu_name, nu in [("flat", lambda j: 0.3), ("decaying", lambda j: 0.3 * 0.7 ** j)]:
    W = {k: news_e_welfare(u, G, p, nu, 2.0, kf, kb) for k, G in schedules.items()}
    print(f"     lam = 2, {nu_name} nu: " + ", ".join(f"{k} {v:.4f}" for k, v in W.items()))

# N4: well-foundedness. Felt news at a surprise solves h(s) = s - sum_j nu_j mu(x0_j + s g_j) = 0;
# unique iff lam (nu . g) < 1. Beyond it a bad shock has no felt state.
T, t0 = 40, 20
j = np.arange(T)
kf_v, kb_v = np.where(j > 0, 0.1 * 0.85 ** j, 0), np.where(j > 0, 0.1 * 0.75 ** j, 0)
n = T - t0
A_ = np.array([[kf_v[c - r] if c > r else kb_v[r - c] if r > c else 0 for c in range(n)] for r in range(n)])
Rinv = np.linalg.inv(np.eye(n) - A_)
g = Rinv[:, 0]
grid = np.linspace(-200, 50, 5001)
rows = []
for nu0, lam in [(0.3, 2.0), (0.45, 2.5)]:
    nu = np.array([nu0] + [0.1 * 0.7 ** q for q in range(1, n)])
    mu = lambda x: np.where(x >= 0, x, lam * x)
    counts = []
    for shock in (-3.0, 3.0):
        hv = np.array([s - nu @ mu(g * shock + s * g) for s in grid])
        counts.append(int(np.sum(np.sign(hv[:-1]) != np.sign(hv[1:]))))
    rows.append(f"lam (nu.g) = {lam * nu @ g:.3f}: felt states after bad / good shock = {counts[0]} / {counts[1]}")
print("N4  " + "; ".join(rows))


# Canonical model, reduced form (core.md): effective coefficients and the echoed news kernel
spec_pw = importlib.util.spec_from_file_location("pathwise", os.path.join(os.path.dirname(__file__), "pathwise.py"))
pw = importlib.util.module_from_spec(spec_pw)
spec_pw.loader.exec_module(pw)
a, b, m, al = 0.09, 0.88, 0.05, 0.75
p, q, r0 = geometric_closed_form(a, b, m, al)
print(f"RF  r(0) = {r0:.3f}, p = {p:.3f}, q = {q:.3f}; reach fwd {1 / (1 - b):.1f} -> {1 / (1 - p):.1f}, "
      f"bwd {1 / (1 - al):.1f} -> {1 / (1 - q):.1f}")
T, t0 = 120, 40
kf_r, kb_r = pw.kernels(T, a, b, m, al)
nu_r = 0.3 * 0.8 ** np.arange(T)
eff, prim = [], []
for h in (1, 5, 20, 30, 50):
    ev = [(t0, t0 + h, 1.0, None)]
    eff.append(pw.run(T, 0.0, ev, kf_r, kb_r, nu_r, 1.0, "e")[1]["news"][t0])
    prim.append(pw.run(T, 0.0, ev, kf_r, kb_r, nu_r, 1.0, "u")[1]["news"][t0])
report("RF direct news equals the primitive kernel", max(abs(x - nu_r[h]) for x, h in zip(prim, (1, 5, 20, 30, 50))))
print("RF  echoed news kernel at h = 1, 5, 20, 30, 50: " + ", ".join(f"{x:.3f}" for x in eff))

# P1(d): non-summable tails. Simple-hyperbolic kernels with the same short-run rates
j = np.arange(1, 2000)
for T in (50, 2000):
    jj = j[: T - 1]
    M_T = (a / (1 - np.log(b) * jj)).sum() + (m / (1 - np.log(al) * jj)).sum()
    print(f"P1d simple-hyperbolic tails: M_T = {M_T:.2f} at T = {T}")

# Calibration: invert present bias to one-sided primitives; the echo share it implies
err = 0.0
for bL, d in [(0.7, 0.96), (0.9, 0.96), (0.7, 0.9)]:
    a, b = bL / (1 - bL), d * (1 - bL)
    r = resolvent_line(a, b, 0.0, 0.5)
    M_pred = bL * d / (1 - d + bL * d)
    err = max(err, abs(r[1] / (r[0] * r[2] / r[1]) - bL), abs(r[2] / r[1] - d), abs(mass(a, b, 0.0, 0.5) - M_pred))
report("CAL inversion a = bL/(1-bL), beta = d(1-bL); M = bL d/(1-d+bL d)", err)
