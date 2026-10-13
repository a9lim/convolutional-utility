"""Numerical checks for formalism/core.md. Run: python formalism/checks.py

Conventions: K[t, s] is the weight of e(s) (recursive model R) or u(s) (direct model D)
in e(t). Geometric family: forward a*b**(s-t) for s > t, backward m*al**(t-s) for s < t.
"""
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

# A1: recursive memory-only kernel, mirror of P3: r(-j) = (m/(1+m))((1+m)al)^j
m, al = 1.0, 0.3
r = resolvent_line(0.0, 0.5, m, al)
report("A1 memory-only resolvent", max(abs(r[-j] - (m / (1 + m)) * ((1 + m) * al) ** j) for j in range(1, 6)))
print(f"A1  b=2, m=1, al=0.3: per-observer M = {m * al / (1 - al):.3f} (< 1); copy-counted "
      f"total ratio b(1+m)al = {2 * (1 + m) * al:.2f} (>= 1 diverges); measure-weighted ratio "
      f"(1+m)al = {(1 + m) * al:.2f}")
