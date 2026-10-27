"""Checks for notes/vicarious.md: felt echoes between people, additive reading.
Run: python notes/vicarious.py

People share one time axis. Person i's felt state adds, to its own canonical echoes, contagion
S[i, k] e_k,t (feeling what k feels now), vicarious anticipation V[i, k] times i's anticipation
kernel over k's forecast felt states, and vicarious memory R[i, k] times i's memory kernel over
k's past felt states. Welfare is the sum over people and moments.

grief_tree(): person 0 dies at D ~ P, warned L ahead; the others live to T and learn what person 0
learns, and of the death once it happens. Each feels news over its own felt states (which carry
the vicarious terms), so grief is the survivor's revision of its own forecasts.
"""
import numpy as np

LIFE = dict(a=0.064, al=0.7, m=0.4, mu=0.3, n=0.2, nu=0.7)     # calibration.md, a week
rng = np.random.default_rng(0)


def report(name, err, tol):
    print(f"{'PASS' if err < tol else 'FAIL'}  {name}  (max err {err:.2e})")


def kernels(T, a, al, m, mu, n, nu):
    j = np.arange(T)
    return np.where(j > 0, a * al ** j, 0.0), np.where(j > 0, m * mu ** j, 0.0), n * nu ** j


def Kfore(T, a, al, m, mu, **_):
    """Own echoes on a foreseen life: anticipation above the diagonal, memory below."""
    i, j = np.meshgrid(np.arange(T), np.arange(T), indexing="ij")
    return np.where(j > i, a * al ** np.abs(j - i), 0) + np.where(j < i, m * mu ** np.abs(j - i), 0)


def community(T, S, V, R, pr):
    """The joint operator on (person, time), person-major, for foreseen lives."""
    K = Kfore(T, **pr)
    up, lo = np.triu(K, 1), np.tril(K, -1)
    I_P = np.eye(len(S))
    return np.kron(I_P, K) + np.kron(S, np.eye(T)) + np.kron(V, up) + np.kron(R, lo)


# 1. Joint well-foundedness. Contagion alone is a Kronecker sum, rho(K + S) = rho(K) + rho(S); a
#    person's total echo share (own M plus its row of social mass) below one in every row suffices,
#    as P1's row-sum bound. Two people well-founded alone (M = 0.6) are not jointly at s = 0.45.
strong = {k: v * 0.6 / 0.32 if k in ("a", "m") else v for k, v in LIFE.items()}   # M = 0.6
err = 0.0
for T in (10, 40, 120):
    K = Kfore(T, **strong)
    S = rng.uniform(0, 0.3, (3, 3))
    np.fill_diagonal(S, 0)
    J = np.kron(np.eye(3), K) + np.kron(S, np.eye(T))
    rho = lambda X: max(abs(np.linalg.eigvals(X)))
    err = max(err, abs(rho(J) - rho(K) - rho(S)))
report("contagion: rho(K (+) S) = rho(K) + rho(S)", err, tol=1e-9)
bad = 0
for _ in range(200):
    P_ = int(rng.integers(2, 5))
    pr = dict(a=rng.uniform(0, .3), al=rng.uniform(.1, .9), m=rng.uniform(0, .3), mu=rng.uniform(.1, .9))
    A, B = pr["a"] * pr["al"] / (1 - pr["al"]), pr["m"] * pr["mu"] / (1 - pr["mu"])
    S, V, R = (rng.uniform(0, 1, (P_, P_)) * (1 - np.eye(P_)) for _ in range(3))
    share = A + B + S.sum(1) + A * V.sum(1) + B * R.sum(1)
    scale = rng.uniform(0.5, 0.99) / share.max()
    if A + B > 0.99 * share.max():
        continue
    S, V, R = S * scale, V * scale, R * scale       # own share kept, social mass scaled into the bound
    share = A + B + S.sum(1) + A * V.sum(1) + B * R.sum(1)
    if share.max() >= 1:
        continue
    bad += max(abs(np.linalg.eigvals(community(60, S, V, R, pr)))) >= 1
report("every row's total echo share < 1 => the community's echoes are well-founded (random draws)", bad, tol=0.5)
Sx, nx = np.array([[0, 0.9], [0.9, 0]]), 0.2
report("echo radius 0.9 and news gain 0.2, yet the revision loop S + n I has radius 1.1 (Codex)",
       abs(max(abs(np.linalg.eigvals(Sx + nx * np.eye(2)))) - 1.1), tol=1e-12)
pair = np.array([[0, 0.45], [0.45, 0]])
print("      M = 0.6 each, contagion 0.45 each way: rho alone / jointly, interior felt state jointly")
for T in (5, 20, 80, 320):
    J = community(T, pair, np.zeros((2, 2)), np.zeros((2, 2)), strong)
    rK, rJ = max(abs(np.linalg.eigvals(Kfore(T, **strong)))), max(abs(np.linalg.eigvals(J)))
    e = np.linalg.solve(np.eye(2 * T) - J, np.ones(2 * T))
    print(f"        T = {T:3d}: {rK:.3f} / {rJ:.3f}, e_mid = {e[T // 2]:+.2f}")

# 2. Whose base utility counts: in a long life's interior a unit of k's base utility adds
#    1'(I - G)^{-1} e_k to welfare, G = M I + S + A V + B R in person space (column sums). A star:
#    ten fans feel the hub at s each; the hub's moments weigh more, the fans feel more.
T = 400
A, B = LIFE["a"] * LIFE["al"] / (1 - LIFE["al"]), LIFE["m"] * LIFE["mu"] / (1 - LIFE["mu"])
err = 0.0
for fans, s, back in ((10, 0.1, 0.0), (10, 0.05, 0.01), (3, 0.2, 0.05)):
    P_ = fans + 1
    S = np.zeros((P_, P_))
    S[1:, 0], S[0, 1:] = s, back
    V, R = 0.5 * S, 0.5 * S                         # vicarious anticipation and memory at half own strength
    G = (A + B) * np.eye(P_) + S + A * V + B * R
    w = np.linalg.solve((np.eye(P_) - G).T, np.ones(P_))
    Rinv = np.linalg.inv(np.eye(P_ * T) - community(T, S, V, R, LIFE))
    col = lambda k: Rinv[:, k * T + T // 2].sum()
    lvl = np.linalg.solve(np.eye(P_) - G, np.ones(P_))
    err = max(err, abs(col(0) - w[0]), abs(col(1) - w[1]))
    print(f"      {fans} fans at s = {s}, hub back {back}: weight of a unit to the hub {w[0]:.3f}, to a fan "
          f"{w[1]:.3f}; felt level of the hub {lvl[0]:.3f}, of a fan {lvl[1]:.3f} (alone {1 / (1 - A - B):.3f})")
report("interior weights: column sums = 1'(I - M I - S - A V - B R)^-1", err, tol=1e-6)


# 3. Grief: one mortal (person 0, death uniform on 16..30 of a 30-period life) and survivors who live to
#    30, life calibration, u = 1 for all. "Foreseen from birth" is revelation at 0 against the prior;
#    a death at D = T falls outside the survivors' scored interval.
def cells(P, L):
    """W[t+1, i, k]: weight on branch Ds[k] in the forecast held at t in branch Ds[i]. Before the death
    as in death.py; at or after it the death is known."""
    T = len(P)
    Ds, P = np.arange(1, T + 1)[P > 0], P[P > 0]
    W = np.zeros((T + 1, len(Ds), len(Ds)))
    for t in range(-1, T):
        for i, D in enumerate(Ds):
            mask = (np.ones(len(Ds), bool) if t < 0 else Ds == D if D <= t + L else Ds > t + L)
            W[t + 1, i] = P * mask / (P * mask).sum()
    return W


def grief_tree(P, L, S, V, R, a, al, m, mu, n, nu, lam=1.0, tol=1e-12, damp=0.5, it=100000, src=None):
    """Person 0 dies at D ~ P, warned L ahead; the others live to T and learn what person 0 learns, and
    the death when it happens. Returns (e[person, branch, t], expected welfare per person, felt news).
    src replaces base utility and the social and news terms with a fixed source (echoes only)."""
    T = len(P)
    kf, kb, kn = kernels(T, a, al, m, mu, n, nu)
    s, t = np.meshgrid(np.arange(T), np.arange(T))
    KF = np.where(s > t, kf[np.clip(s - t, 0, T - 1)], 0.0)
    KB = np.where(s < t, kb[np.clip(t - s, 0, T - 1)], 0.0)
    KN = np.where(s >= t, kn[np.clip(s - t, 0, T - 1)], 0.0)
    Ds, Pp = np.arange(1, T + 1)[P > 0], P[P > 0]
    alive = np.stack([(np.arange(T)[None, :] < Ds[:, None]).astype(float)] + [np.ones((len(Ds), T))] * (len(S) - 1))
    U = alive.copy()
    W = cells(P, L)
    phi = lambda x: np.where(x >= 0, x, lam * x)
    soc = lambda X, Y: np.einsum("ik,kdt->idt", X, Y)
    e = U.copy()
    for _ in range(it):
        F = np.einsum("tdk,iks->itds", W, e)
        N = np.einsum("ts,itds->idt", KN, phi(F[:, 1:] - F[:, :-1])) * alive
        ant = np.einsum("ts,itds->idt", KF, F[:, 1:])
        mem = e @ KB.T
        if src is None:
            new = (U + ant + mem + N + soc(S, e) + soc(V, ant) + soc(R, mem)) * alive
        else:
            new = (src + ant + mem) * alive
        err = np.max(np.abs(new - e))
        e = damp * new + (1 - damp) * e
        if err < tol:
            return e, e.sum(2) @ Pp, N
    raise RuntimeError(f"no convergence, err {err:.2e}")


T = 30
Ds = np.arange(1, T + 1)
P_late = np.where(Ds >= 16, 1.0, 0.0) / 15
Z = np.zeros((2, 2))
one_way = lambda x: np.array([[0, 0], [x, 0]])
_, W0, _ = grief_tree(P_late, 0, Z, Z, Z, **LIFE)
_, WT, _ = grief_tree(P_late, T, Z, Z, Z, **LIFE)
surv_alone = np.linalg.solve(np.eye(T) - Kfore(T, **LIFE), np.ones(T)).sum()
report("uncoupled: death.py's tree (sudden - foreseen 0.68198...), and the survivor's foreseen life",
       max(abs(W0[0] - WT[0] - 0.6819807679228447), abs(W0[1] - surv_alone)), tol=1e-9)

SETTINGS = (("contagion 0.2", one_way(0.2), Z, Z),
            ("+ vicarious anticipation", one_way(0.2), one_way(1.0), Z),
            ("+ vicarious memory", one_way(0.2), Z, one_way(1.0)),
            ("contagion 0.2 both ways", np.array([[0, 0.2], [0.2, 0]]), Z, Z))
err = 0.0
for label, S, V, R in SETTINGS:
    for L in (0, 1, 4, T):
        _, _, N = grief_tree(P_late, L, S, V, R, **LIFE)
        err = max(err, abs(N[1].sum(1) @ P_late[P_late > 0]))
report("lam = 1: the survivor's expected felt news is zero at every warning (its realization is felt)",
       err, tol=1e-9)

Pl = P_late[P_late > 0]
for lam in (1.0, 2.0):
    Ns = {L: grief_tree(P_late, L, one_way(0.2), Z, Z, **LIFE, lam=lam)[2] for L in (0, 1, 4, T)}
    print(f"      lam {lam:g}, contagion 0.2: expected felt news, dying / survivor: " + "  ".join(
        f"L={L}: {Ns[L][0].sum(1) @ Pl:+.3f} / {Ns[L][1].sum(1) @ Pl:+.3f}" for L in (0, 1, 4, T)))
print("      W(L) - W(foreseen from birth), dying / survivor / pair:")
for lam in (1.0, 2.0):
    for label, S, V, R in SETTINGS:
        Ws = {L: grief_tree(P_late, L, S, V, R, **LIFE, lam=lam)[1] for L in (0, 1, 4, T)}
        print(f"        lam {lam:g}, {label:25s}" + "  ".join(
            f"L={L}: {Ws[L][0] - Ws[T][0]:+.3f} / {Ws[L][1] - Ws[T][1]:+.3f} / {Ws[L].sum() - Ws[T].sum():+.3f}"
            for L in (0, 1, 4)))

# 3b. Where a foreseen extra period lands with a survivor: person 0's death from 100 to 101, person 1
#     lives to 200 (printed). Without coupling, 83% is the new moment's own felt state (death.md).
def pair_foreseen(D, T, S, V, R, pr):
    keep = np.r_[np.arange(D), T + np.arange(T)]
    J = community(T, S, V, R, pr)[np.ix_(keep, keep)]
    return np.linalg.solve(np.eye(len(keep)) - J, np.ones(len(keep))), D


print("      one more foreseen period for person 0 (100 -> 101, survivor to 200): dW = new moment / "
      "person 0's raise / survivor's raise")
for label, S, V, R in (("uncoupled", Z, Z, Z),) + SETTINGS:
    (e1, D1), (e2, D2) = pair_foreseen(100, 200, S, V, R, LIFE), pair_foreseen(101, 200, S, V, R, LIFE)
    dW = e2.sum() - e1.sum()
    new, raise0, raise1 = e2[D2 - 1], e2[:D2 - 1].sum() - e1[:D1].sum(), e2[D2:].sum() - e1[D1:].sum()
    print(f"        {label:25s} dW {dW:.3f} = {new:.3f} ({new / dW:.0%}) / {raise0:.3f} ({raise0 / dW:.0%}) / "
          f"{raise1:.3f} ({raise1 / dW:.0%})")


# 3c. One-way contagion s from survivors who do not feel each other: the survivor's deterministic
#     baseline and the kink's positive homogeneity make each survivor's response s times a fixed one,
#     so the pair's sudden - foreseen gap is linear in s, and survivors add (Codex).
gap = lambda S, lam: (lambda W0, WT: W0.sum() - WT.sum())(grief_tree(P_late, 0, S, np.zeros_like(S), np.zeros_like(S),
                                                                    **LIFE, lam=lam)[1],
                                                         grief_tree(P_late, T, S, np.zeros_like(S), np.zeros_like(S),
                                                                    **LIFE, lam=lam)[1])
g0, g1 = gap(np.zeros((2, 2)), 2.0), gap(one_way(1.0), 2.0)
err = max(abs(gap(one_way(x), 2.0) - (g0 + x * (g1 - g0))) for x in (0.2, 0.5, 2.0))
eight = np.zeros((9, 9))
eight[1:, 0] = 0.2
err = max(err, abs(gap(eight, 2.0) - (g0 + 8 * 0.2 * (g1 - g0))), abs(g0 - 0.684306899), abs(g1 - g0 + 0.485772161))
report("lam = 2: the sudden - foreseen gap is 0.6843 - 0.4858 x (total one-way contagion), survivors add (Codex)",
       err, tol=1e-6)
l0, l1 = gap(np.zeros((2, 2)), 1.0), gap(one_way(1.0), 1.0)
print(f"      lam 2: foreknowledge wins once total contagion toward the dying exceeds {g0 / (g0 - g1):.3f}; "
      f"eight survivors at 0.2: {gap(eight, 2.0):+.4f}")
print(f"      lam 1: gap {l0:.4f} + {l1 - l0:.4f} x (total one-way contagion)")
Ws = {L: grief_tree(P_late, L, one_way(2.0), Z, Z, **LIFE, lam=2.0)[1] for L in (0, 13, 16, T)}
print("      lam 2, contagion 2: pair " + "  ".join(f"L={L}: {Ws[L].sum():.4f}" for L in (0, 13, 16, T)))

# 3d. The survivor's welfare split by source (contagion 0.2, lam = 2), each through the survivor's own
#     echoes: what it feels of the dying, s e_0, against its own felt news (Codex's decomposition).
S2 = one_way(0.2)
parts = {}
for L in (0, 1, 4, T):
    e, W, N = grief_tree(P_late, L, S2, Z, Z, **LIFE, lam=2.0)
    caught = np.stack([np.zeros_like(e[0]), 0.2 * e[0]])
    W_caught = grief_tree(P_late, L, S2, Z, Z, **LIFE, src=caught)[1][1]
    W_news = grief_tree(P_late, L, S2, Z, Z, **LIFE, src=np.stack([np.zeros_like(N[1]), N[1]]))[1][1]
    W_base = grief_tree(P_late, L, S2, Z, Z, **LIFE, src=np.stack([np.zeros_like(N[1]), np.ones_like(N[1])]))[1][1]
    parts[L] = (W_caught, W_news, W[1], W_base)
err = max(abs(sum(parts[L][:2]) + parts[L][3] - parts[L][2]) for L in parts)
report("the survivor's welfare = base + caught + own news, each echoed", err, tol=1e-8)
print("      survivor against foreseen from birth, caught / own news / total: " + "  ".join(
    f"L={L}: {parts[L][0] - parts[T][0]:+.3f} / {parts[L][1] - parts[T][1]:+.3f} / {parts[L][2] - parts[T][2]:+.3f}"
    for L in (0, 1, 4)))
