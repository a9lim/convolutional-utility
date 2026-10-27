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


def grief_tree(P, L, S, V, R, a, al, m, mu, n, nu, lam=1.0, tol=1e-12, damp=0.5, it=100000, src=None, h=0.0, g=0.9):
    """Person 0 dies at D ~ P, warned L ahead; the others live to T and learn what person 0 learns, and
    the death when it happens. Returns (e[person, branch, t], expected welfare per person, felt news).
    src replaces base utility and the social and news terms with a fixed source (echoes only)."""
    T = len(P)
    kf, kb, kn = kernels(T, a, al, m, mu, n, nu)
    kc = np.where(np.arange(T) > 0, h * (1 - g) / g * g ** np.arange(T), 0.0)       # biphasic: adaptation, own only
    s, t = np.meshgrid(np.arange(T), np.arange(T))
    KF = np.where(s > t, kf[np.clip(s - t, 0, T - 1)], 0.0)
    KB = np.where(s < t, kb[np.clip(t - s, 0, T - 1)], 0.0)
    KC = np.where(s < t, kc[np.clip(t - s, 0, T - 1)], 0.0)
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
        mem = e @ KB.T                                   # afterglow, the channel vicarious memory reads
        own = mem - e @ KC.T                             # own memory, adaptation included (h for everyone)
        if src is None:
            new = (U + ant + own + N + soc(S, e) + soc(V, ant) + soc(R, mem)) * alive
        else:
            new = (src + ant + own) * alive
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


# 4. Budgeted attention: PageRank. If person i feels others with a fixed share sigma_i of attention
#    spread by a row-stochastic P (S = diag(sigma) P), interior welfare weights solve
#    w = 1 + M w + P' diag(sigma) w: with sigma uniform, w = N/((1 - M)(1 - d)) PR, PageRank with
#    damping d = sigma/(1 - M) and uniform teleport, and every felt level is 1/(1 - M - sigma).
#    Additive feeling (each tie its own weight, no budget) gives Katz instead.
def pagerank(P, d, it=10000):
    N = len(P)
    r = np.ones(N) / N
    for _ in range(it):
        r_new = (1 - d) / N + d * P.T @ r
        if np.max(np.abs(r_new - r)) < 1e-15:
            break
        r = r_new
    return r_new


Mlife = A + B
err = 0.0
for _ in range(50):
    N_ = int(rng.integers(3, 12))
    P = rng.uniform(0, 1, (N_, N_)) * (rng.uniform(0, 1, (N_, N_)) < 0.5) * (1 - np.eye(N_))
    P[np.arange(N_), (np.arange(N_) + 1) % N_] += 0.1             # no one feels nobody
    P /= P.sum(1, keepdims=True)
    sig = rng.uniform(0.05, 0.6)
    w = np.linalg.solve((1 - Mlife) * np.eye(N_) - sig * P.T, np.ones(N_))
    d = sig / (1 - Mlife)
    err = max(err, np.max(np.abs(w - N_ / ((1 - Mlife) * (1 - d)) * pagerank(P, d))),
              np.max(np.abs(np.linalg.solve((1 - Mlife) * np.eye(N_) - sig * P, np.ones(N_)) - 1 / (1 - Mlife - sig))))
report("budgeted attention: welfare weights are PageRank at damping sigma/(1 - M); felt levels all 1/(1 - M - sigma)",
       err, tol=1e-9)
Pd = np.array([[0.0, 1.0], [0.0, 0.0]])                          # the second person feels no one
lv = np.linalg.solve(np.eye(2) - 0.5 * Pd, np.ones(2))
wd = np.linalg.solve(np.eye(2) - 0.5 * Pd.T, np.ones(2))
report("a sink breaks it: M = 0, sigma = 1/2, levels (1.5, 1), weights (1, 1.5), not 2 (Codex)",
       np.max(np.abs(lv - [1.5, 1])) + np.max(np.abs(wd - [1, 1.5])), tol=1e-12)

# 4b. A celebrity and fans (printed). 1000 fans, each feeling a ring of friends and the celebrity, with
#     a social share 0.3; the celebrity feels its own circle of 10 at the same share. Fans who
#     follow K celebrities split the share K ways under a budget; additively each tie keeps its weight.
def celebrity(K, budget, fans=1000, share=0.3, to_celeb=0.2, circle=10):
    """Weights of a unit to one celebrity and to a fan; the fans' total echo share."""
    N_ = 1 + circle + fans                  # 0: the celebrity, 1..circle: its circle, then fans
    S = np.zeros((N_, N_))
    S[0, 1:1 + circle] = share / circle
    for c in range(1, 1 + circle):
        S[c, 0] = S[c, 1 + (c % circle)] = share / 2
    f0 = 1 + circle
    for f in range(f0, N_):
        friend = f0 + (f - f0 + 1) % fans
        each = share * to_celeb / K if budget else share * to_celeb
        S[f, friend] = share * (1 - to_celeb)
        S[f, 0] = each                          # the other K - 1 celebrities are outside the graph:
    row = Mlife + S.sum(1)                      # under a budget they take the rest of the share
    if not budget:
        row[f0:] += share * to_celeb * (K - 1)
    w = np.linalg.solve((1 - Mlife) * np.eye(N_) - S.T, np.ones(N_))
    return w[0], w[-1], row.max()


for K in (1, 10, 100):
    wb = celebrity(K, True)
    wa = celebrity(K, False)
    print(f"      fans following {K:3d} celebrities: budget, celebrity {wb[0]:7.1f} against a fan {wb[1]:.3f} "
          f"(max echo share {wb[2]:.2f}); additive, celebrity {wa[0]:7.1f} (max echo share {wa[2]:.2f})")


# 4c. The additive graph completed (Codex): K celebrities, each with its own circle, all felt by the
#     fans at full weight. Block triangular (no path from fans back to celebrities), so rho(S) stays
#     the circles' 0.3 at any K and the community is well-founded although a fan's row passes one;
#     what grows with K is a fan's felt level.
def completed(K, fans=300, share=0.3, to_celeb=0.2, circle=10):
    blk = 1 + circle
    N_ = K * blk + fans
    S = np.zeros((N_, N_))
    for c in range(K):
        h = c * blk
        S[h, h + 1:h + blk] = share / circle
        for i in range(1, blk):
            S[h + i, h] = S[h + i, h + 1 + (i % circle)] = share / 2
    f0 = K * blk
    for f in range(f0, N_):
        S[f, f0 + (f - f0 + 1) % fans] = share * (1 - to_celeb)
        S[f, [c * blk for c in range(K)]] = share * to_celeb
    return S, f0


lv_ = []
bad = 0
for K in (1, 10, 40):
    S, f0 = completed(K)
    bad += abs(max(abs(np.linalg.eigvals(S))) - 0.3) > 1e-9
    lv_.append(np.linalg.solve((1 - Mlife) * np.eye(len(S)) - S, np.ones(len(S)))[f0])
report("completed additive graph: rho(S) = 0.3 at K = 1, 10, 40 celebrities (Codex)", bad, tol=0.5)
print("      additively, a fan's felt level: " + ", ".join(f"{x:.3f}" for x in lv_) + " at K = 1, 10, 40; "
      f"under the budget 1/(1 - M - 0.3) = {1 / (1 - Mlife - 0.3):.3f}")


# 5. News across people (Codex, cu-vicarious). On a remaining life, a unit forcing felt now by k moves
#    i's forecasts at horizon j by G_j[i, k], a column of the community's resolvent; the felt news
#    solves s = b + K s with K = sum_j n nu^j G_j. Stable for every revision iff rho(K) < 1 (linear)
#    and rho(lam K) < 1 (loss averse, per person-horizon kinks).
def news_gain(S, V, R, pr, T=70):
    P_ = len(S)
    G = np.linalg.inv(np.eye(P_ * T) - community(T, S, V, R, pr))
    w = pr["n"] * pr["nu"] ** np.arange(T)
    cols = G[:, ::T].reshape(P_, T, P_)                # [i, j, k] = G_{(i, j), (k, 0)}
    return np.einsum("j,ijk->ik", w, cols), G


def kappa_mode(s, v, r, a, al, m, mu, n, nu):
    """Codex's half-line gain for one eigenmode: (a, m, n) rescaled by (1 + v, 1 + r, 1)/(1 - s)."""
    c = 1 - s
    a_, m_ = a * (1 + v) / c, m * (1 + r) / c
    C = 1 + (1 + a_ + m_) * al * mu
    H = (C + np.sqrt(C ** 2 - 4 * (1 + a_) * (1 + m_) * al * mu)) / 2
    q = (1 + m_) * mu / H
    return n / (c * H) * (1 - nu * mu) / (1 - nu * q)


K1, _ = news_gain(np.zeros((1, 1)), np.zeros((1, 1)), np.zeros((1, 1)), LIFE)
err = abs(K1[0, 0] - kappa_mode(0, 0, 0, **LIFE))
for _ in range(5):                                   # commuting symmetric S, V, R: per-mode gains
    P_ = 3
    Q, _ = np.linalg.qr(rng.normal(size=(P_, P_)))
    th = rng.uniform(-0.15, 0.25, (3, P_))
    S, V, R = (Q @ np.diag(t) @ Q.T for t in th)
    K, _ = news_gain(S, V, R, LIFE)
    err = max(err, np.max(np.abs(K - Q @ np.diag([kappa_mode(*th[:, i], **LIFE) for i in range(P_)]) @ Q.T)))
report("news gain: K from the resolvent = Codex's per-mode half-line kappa (one person: N4's)", err, tol=1e-9)

err = 0.0
for _ in range(10):                                  # pure contagion: rho(K) = f(rho(S))
    P_ = int(rng.integers(2, 5))
    S = rng.uniform(0, 1, (P_, P_)) * (1 - np.eye(P_))
    S *= rng.uniform(0.1, 0.5) / max(abs(np.linalg.eigvals(S)))
    K, _ = news_gain(S, np.zeros((P_, P_)), np.zeros((P_, P_)), LIFE)
    err = max(err, abs(max(abs(np.linalg.eigvals(K))) - kappa_mode(max(abs(np.linalg.eigvals(S))), 0, 0, **LIFE)))
report("pure contagion: rho(K) = f(rho(S)), whatever the graph", err, tol=1e-9)


def star(fans, s_hf, s_fh):
    S = np.zeros((fans + 1, fans + 1))
    S[0, 1:], S[1:, 0] = s_hf, s_fh
    return S


r11, r12 = (max(abs(np.linalg.eigvals(news_gain(star(f, 0.05, 0.4), np.zeros((f + 1, f + 1)),
                                                 np.zeros((f + 1, f + 1)), LIFE)[0]))) for f in (11, 12))
budget = [max(abs(np.linalg.eigvals(news_gain(star(f, 0.3 / f, 0.3), np.zeros((f + 1, f + 1)),
                                              np.zeros((f + 1, f + 1)), LIFE)[0]))) for f in (1, 3, 8)]
report("reciprocal star at lam = 2: 11 fans stable, 12 not (Codex); with budgets the radius is size-free",
       float(not (2 * r11 < 1 < 2 * r12)) + abs(r11 - 0.4971782252) + abs(r12 - 0.5262534514)
       + max(abs(x - 0.34582649374496) for x in budget), tol=1e-8)
print(f"      reciprocal star (0.05 hub to each fan, 0.4 back): lam rho(K) = {2 * r11:.4f} at 11 fans, "
      f"{2 * r12:.4f} at 12; echo M + rho(S) = {A + B + np.sqrt(12 * 0.05 * 0.4):.3f} at 12. "
      f"Budget 0.3: rho(K) = {budget[0]:.4f} at 1, 3, 8 fans")


# 5b. Public reaction (printed): a hardship revealed now for the hub, a unit base drop at horizon 4,
#     linear news. Felt news now: the hub's, and the fans' total; one-way fans against a hub that also
#     feels its fans (budgeted at 0.3), 20 fans feeling the hub at 0.1.
def reaction(S, h=4, T=70, pr=LIFE):
    K, G = news_gain(S, np.zeros_like(S), np.zeros_like(S), pr, T)
    P_ = len(S)
    w = pr["n"] * pr["nu"] ** np.arange(T)
    d = -G[:, h].reshape(P_, T)                        # revision of each person's forecasts, [i, j]
    s = np.linalg.solve(np.eye(P_) - K, d @ w)
    return s[0], s[1:].sum()


fans = 20
one_way = np.zeros((fans + 1, fans + 1))
one_way[1:, 0] = 0.1
recip = one_way.copy()
recip[0, 1:] = 0.3 / fans
for label, S in (("fans feel the hub", one_way), ("and the hub feels its fans", recip)):
    hub, crowd = reaction(S)
    print(f"      {label:27s}: felt news now, hub {hub:+.4f}, the fans together {crowd:+.4f}")


# 6. Grief under biphasic memory (notes/adaptation.md: afterglow minus adaptation c g^j, mass h). A survivor feels
#    the dying person by contagion; once they are gone the survivor's reference, built on the shared level, sits
#    above its new level, so its felt state undershoots and recovers as the reference adapts down. Without
#    adaptation it steps down and stays.
def pair_foreseen_bi(D, T, s_, pr, h, g):
    """Person 0 dies after D - 1 (foreseen), the survivor lives to T, contagion s_ one way; signed memory."""
    c = h * (1 - g) / g
    r = np.subtract.outer(np.arange(T), np.arange(T))
    K = np.where(r < 0, pr["a"] * pr["al"] ** (-r), 0.0) + np.where(r > 0, pr["m"] * pr["mu"] ** np.abs(r)
                                                                   - c * g ** np.abs(r), 0.0)
    J = np.zeros((2 * T, 2 * T))
    J[:T, :T] = J[T:, T:] = K
    J[T + np.arange(T), np.arange(T)] = s_
    keep = np.r_[np.arange(D), T + np.arange(T)]
    return np.linalg.solve(np.eye(len(keep)) - J[np.ix_(keep, keep)], np.ones(len(keep)))[D:]


gy = 1 - 1 / 52
out, bad = [], 0
for s_ in (0.2, 0.5):
    for h in (0.0, 0.5):
        e = pair_foreseen_bi(400, 1100, s_, LIFE, h, gy)
        before, after = e[300:390].mean(), e[750:850].mean()
        trough, tmin = e[400:750].min(), int(np.argmin(e[400:750]))
        rec = int(np.flatnonzero(np.abs(e[400:750] - after) < 0.1 * (before - after))[0])
        out.append((s_, h, before, after, trough, tmin, rec))
        bad += (h == 0.0 and trough < after - 1e-9) or (h == 0.5 and trough > after - 0.05)
report("grief, foreseen death: an undershoot below the new level with adaptation, none without", bad, tol=0.5)
for s_, h, before, after, trough, tmin, rec in out:
    print(f"      contagion {s_}, h {h}: before {before:.3f}, after {after:.3f}, lowest {trough:.3f} at +{tmin} weeks, "
          f"within 10% of the step after {rec} weeks")

# 6b. Sudden death, against the same death foreseen from birth (the tree, death on 41..50 of 100, a survivor to
#     100; contagion 0.5; adaptation over about 15 periods). The survivor's felt state in the branch dying at 45.
Ds6 = np.arange(1, 101)
P6 = ((Ds6 >= 41) & (Ds6 <= 50)).astype(float)
P6 /= P6.sum()
br = int(np.flatnonzero(Ds6[P6 > 0] == 45)[0])
print("      sudden death at 45 (death uniform on 41..50 of 100), survivor's felt state at 40, 44, 45, 48, 60, 90:")
paths6 = {}
for lam in (1.0, 2.0):
    for h in (0.0, 0.5):
        cells_ = []
        for L, label in ((0, "sudden"), (100, "foreseen")):
            e, W, N = grief_tree(P6, L, np.array([[0, 0], [0.5, 0]]), Z, Z, **LIFE, lam=lam, h=h, g=1 - 1 / 15)
            paths6[(lam, h, L)] = e[1, br]
            cells_.append(f"{label} " + ", ".join(f"{e[1, br, t]:+.2f}" for t in (40, 44, 45, 48, 60, 90))
                          + f" (W {W[1]:.1f})")
        print(f"        lam {lam:g}, h {h}: " + " | ".join(cells_))
p0, p5 = paths6[(1.0, 0.0, 0)], paths6[(1.0, 0.5, 0)]
report("grief, sudden death: a shock then a flat new level without adaptation, a shock then recovery with it",
       float(not (abs(p0[48] - p0[60]) < 0.02 and p5[48] < p5[60] - 0.05 < p5[90] - 0.05)), tol=0.5)

