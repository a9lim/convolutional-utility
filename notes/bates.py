"""Checks for notes/bates.md: the felt display's band in both readings, and price moves through
the news loop. Run: python notes/bates.py

Band DP. The gap d = q - M (terminal reading) or q - X (flow reading) moves by a Gaussian step
of variance sig^2 dt; the self then moves q at cost c|dq| and pays h(d) dt. Relative value
iteration on a grid gives the average cost rate and the no-push band, against the continuous
forms (the DP is discretely monitored, so edges sit inside by about 0.583 sig sqrt(dt)).
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "formalism"))
import pathwise as pw  # noqa: E402


def band_dp(h, sig, c, width, dt=4e-3, per_step=16, span=2.5, tol=1e-12):
    """h: running cost of the gap. width: the continuous band's half-width scale, sizing the grid.
    Returns (cost rate, upper edge, lower edge as a positive number)."""
    s = sig * np.sqrt(dt)
    dl = s / per_step
    N = int(span * width / dl)
    d = dl * np.arange(-N, N + 1)
    k = np.arange(-5 * per_step, 5 * per_step + 1)
    w = np.exp(-0.5 * (k / per_step) ** 2)
    w /= w.sum()
    K = len(k) // 2
    hd = h(d) * dt

    def push(V):                                       # min_z V(z) + c|z - y|
        lo = c * d + np.minimum.accumulate(V - c * d)
        hi = -c * d + np.minimum.accumulate((V + c * d)[::-1])[::-1]
        return np.minimum(lo, hi)

    pad = c * dl * np.arange(1, K + 1)                 # beyond the grid: push back to its edge
    V, rho_old = np.zeros_like(d), np.inf
    for it in range(200000):
        W = push(V)
        Wp = np.concatenate([W[0] + pad[::-1], W, W[-1] + pad])
        Vn = hd + np.convolve(Wp, w, mode="valid")
        rho = Vn[N]
        Vn -= rho
        if it % 500 == 0:
            if abs(rho - rho_old) < tol * dt and np.max(np.abs(Vn - V)) < 1e-9:
                V = Vn
                break
            rho_old = rho
        V = Vn
    inside = d[np.isclose(push(V), V, atol=1e-12, rtol=0)]
    return rho / dt, inside.max(), -inside.min()


BGK = 0.5826                                           # -zeta(1/2)/sqrt(2 pi)
DT = 4e-3
SIGS = (0.5, 1.0, 2.0)


def report(name, err, tol):
    print(f"{'PASS' if err < tol else 'FAIL'}  {name}  (max err {err:.2e})")


# Terminal reading: tether (eta/2) d^2, half-width b* = (3 c sig^2 / (2 eta))^{1/3}.
c, eta = 1.0, 1.0
costs, cost_err, shifts = [], [], []
for sig in SIGS:
    b = (3 * c * sig ** 2 / (2 * eta)) ** (1 / 3)
    J, up, dn = band_dp(lambda x: 0.5 * eta * x ** 2, sig, c, b, dt=DT)
    costs.append(J)
    cost_err.append(abs(J / (c * sig ** 2 / (2 * b) + eta * b ** 2 / 6) - 1))
    shifts += [(b - up) / (sig * np.sqrt(DT)), (b - dn) / (sig * np.sqrt(DT))]
    print(f"      terminal, sig = {sig}: edges +-{up:.4f} against b* = {b:.4f}, cost {J:.4f}")
slope = np.polyfit(np.log(SIGS), np.log(costs), 1)[0]
print(f"      edges inside by {min(shifts):.3f}-{max(shifts):.3f} sig sqrt(dt); cost slope in sig {slope:.3f}")
report("terminal band: cost against cs^2/(2b) + eta b^2/6 at b*, relative", max(cost_err), tol=3e-3)
report("terminal band: edges inside b* by about 0.583 sig sqrt(dt)", max(abs(x - BGK) for x in shifts), tol=0.06)
report("terminal band: cost slope 4/3 in sig", abs(slope - 4 / 3), tol=5e-3)

# Flow reading: the arrival kink is the tether, h = kp d+ + km d-, n0 = 1, lam = 2, c = 1.
edges = {}
for A in (1.3, 1.7):
    kp, km = 2.0 - A, A - 1.0                          # kp = lam n0 - A, km = A - n0
    kbar = kp * km / (kp + km)
    costs, cost_err, shifts = [], [], []
    for sig in SIGS:
        L = sig * np.sqrt(2 * c / kbar)
        al, be = km / (kp + km) * L, kp / (kp + km) * L
        J, up, dn = band_dp(lambda x: kp * np.maximum(x, 0) + km * np.maximum(-x, 0), sig, c, L, dt=DT)
        costs.append(J)
        cost_err.append(abs(J / (sig * np.sqrt(2 * c * kbar)) - 1))
        shifts += [(al - up) / (sig * np.sqrt(DT)), (be - dn) / (sig * np.sqrt(DT))]
        edges[A, sig] = (up, dn)
        print(f"      flow, A = {A}, sig = {sig}: optimistic edge {up:.4f} (continuous {al:.4f}), "
              f"pessimistic {dn:.4f} ({be:.4f}), cost {J:.4f}")
    slope = np.polyfit(np.log(SIGS), np.log(costs), 1)[0]
    report(f"flow band, A = {A}: cost against sig sqrt(2 c kbar), relative", max(cost_err), tol=1e-3)
    report(f"flow band, A = {A}: edges at km:kp of L*, inside by about 0.583 sig sqrt(dt)",
           max(abs(x - BGK) for x in shifts), tol=0.03)
    report(f"flow band, A = {A}: cost slope 1 in sig", abs(slope - 1), tol=1e-3)
report("flow band: A = 1.3 and 1.7 mirror each other",
       max(abs(edges[1.3, s][0] - edges[1.7, s][1]) + abs(edges[1.3, s][1] - edges[1.7, s][0]) for s in SIGS),
       tol=1e-12)

# Flow reading, honest self: price moves through the news loop at pathwise's defaults. A random
# walk as pathwise announcements: the move at t is news about every moment s >= t.
T = 40
eps = np.random.default_rng(0).normal(0, 1, T)
eps[0] = 0.0
events = [(t, s, eps[t], None) for t in range(1, T) for s in range(t, T)]
KF, KB = pw.kernels(T, 0.1, 0.85, 0.1, 0.75)
KN = 0.3 * 0.7 ** np.arange(T)
Kt = np.array([KN[:T - t].sum() for t in range(T)])


def resolvent(t):
    n = T - t
    i, j = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    A = np.where(j > i, KF[np.clip(j - i, 0, T - 1)], 0) + np.where(j < i, KB[np.clip(i - j, 0, T - 1)], 0)
    R = np.linalg.inv(np.eye(n) - A)
    return KN[:n] @ R.sum(1), KN[:n] @ R[:, 0]          # k_n . R 1, kappa = k_n . R e_0


for lam in (1.0, 2.0):
    phi = np.where(eps >= 0, eps, lam * eps)
    _, cu, _ = pw.run(T, 0.0, events, KF, KB, KN, lam, "u")
    _, ce, _ = pw.run(T, 0.0, events, KF, KB, KN, lam, "e")
    pred = np.zeros(T)
    for t in range(T):
        kd, kap = resolvent(t)
        pred[t] = eps[t] * kd / (1 - kap) if eps[t] >= 0 else lam * eps[t] * kd / (1 - lam * kap)
    kd, kap = resolvent(1)
    print(f"      lam = {lam}, t = 1: K = {Kt[1]:.3f}; felt per unit move, gain {kd / (1 - kap):.3f}, "
          f"loss {lam * kd / (1 - lam * kap):.3f} (kappa {kap:.3f})")
    report(f"loop, lam = {lam}: news over u is K_t phi(eps)", np.max(np.abs(cu["news"] - Kt * phi)), tol=1e-12)
    report(f"loop, lam = {lam}: news over e is gain/(1-kappa), lam loss/(1-lam kappa)",
           np.max(np.abs(ce["news"] - pred)), tol=1e-11)
