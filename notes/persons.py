"""Checks for notes/persons.md: persons as soft clusters in the echo graph, additive reading.
Run: python notes/persons.py

Moments are nodes; anticipation, memory and the vicarious kernels are weighted edges; e = R u with
R = (I - J)^-1. A moment's row of R is what its felt state is made of (whose base utility, when);
its column is where its base utility is felt.
"""
import numpy as np

LIFE = dict(a=0.064, al=0.7, m=0.4, mu=0.3, n=0.2, nu=0.7)     # calibration.md, a week
A = LIFE["a"] * LIFE["al"] / (1 - LIFE["al"])
B = LIFE["m"] * LIFE["mu"] / (1 - LIFE["mu"])


def report(name, err, tol):
    print(f"{'PASS' if err < tol else 'FAIL'}  {name}  (max err {err:.2e})")


def Kfore(T, a, al, m, mu, **_):
    i, j = np.meshgrid(np.arange(T), np.arange(T), indexing="ij")
    return np.where(j > i, a * al ** np.abs(j - i), 0) + np.where(j < i, m * mu ** np.abs(j - i), 0)


def community(T, S, V, R, pr):
    K = Kfore(T, **pr)
    return (np.kron(np.eye(len(S)), K) + np.kron(S, np.eye(T)) + np.kron(V, np.triu(K, 1))
            + np.kron(R, np.tril(K, -1)))


# 1. Experiential overlap. In a long life's interior, the share of a moment's felt state made of its
#    own body's base utility is the diagonal of (I - G)^-1 over its row sum, G = M I + S + A V + B R.
#    Two people coupled symmetrically at total c = s + A v + B r: (1 - M)/(1 - M + c).
T = 300
err = 0.0
print("      a couple, contagion s each way (vicarious anticipation and memory v = r = s):")
for s in (0.05, 0.1, 0.2, 0.4):
    S = np.array([[0, s], [s, 0]])
    Rr = np.linalg.inv(np.eye(2 * T) - community(T, S, S, S, LIFE))
    row = Rr[T // 2]
    own, other = row[:T].sum(), row[T:].sum()
    c = s * (1 + A + B)
    err = max(err, abs(own / (own + other) - (1 - A - B) / (1 - A - B + c)))
    print(f"        s = {s}: own body {own / (own + other):.1%}, the other {other / (own + other):.1%}")
report("couple: own share of a moment's felt state = (1 - M)/(1 - M + c)", err, tol=1e-6)
print("      a moment's felt state by source: its own base utility / the rest of its life / the other person:")
for s in (0.0, 0.1, 0.2):
    S = np.array([[0, s], [s, 0]])
    row = np.linalg.inv(np.eye(2 * T) - community(T, S, S, S, LIFE))[T // 2]
    tot = row.sum()
    print(f"        s = {s}: {row[T // 2] / tot:.1%} / {(row[:T].sum() - row[T // 2]) / tot:.1%} / {row[T:].sum() / tot:.1%}")


# 2. A fork. A trunk of 40 moments, then two branches of 40 that each remember the whole trunk;
#    trunk moments anticipate both branches at half weight (measure-weighted, A1), and no edge
#    joins the branches. Yet a branch moment's felt state carries its sibling's base utility, through
#    remembered anticipation of it (printed by time since the fork).
def fork(T0=40, T1=40, pr=LIFE, weight=0.5):
    a, al, m, mu = pr["a"], pr["al"], pr["m"], pr["mu"]
    N = T0 + 2 * T1
    time = np.r_[np.arange(T0), T0 + np.arange(T1), T0 + np.arange(T1)]
    branch = np.r_[np.zeros(T0, int), np.ones(T1, int), 2 * np.ones(T1, int)]
    J = np.zeros((N, N))
    for x in range(N):
        for y in range(N):
            lag = time[y] - time[x]
            if lag > 0 and (branch[x] == branch[y] or branch[x] == 0):
                J[x, y] = a * al ** lag * (weight if branch[x] == 0 and branch[y] > 0 else 1.0)
            if lag < 0 and (branch[x] == branch[y] or branch[y] == 0):
                J[x, y] = m * mu ** (-lag)
    return np.linalg.inv(np.eye(N) - J), branch, time


Rf, br, tm = fork()
shares = []
for tau in (0, 1, 2, 5, 10):
    x = 40 + tau                                        # branch A, tau periods after the fork
    row = Rf[x]
    shares.append((tau, row[br == 1].sum(), row[br == 0].sum(), row[br == 2].sum()))
last = Rf[39]
report("the trunk's last moment weighs both branches equally (measure-weighting)",
       abs(last[br == 1].sum() - last[br == 2].sum()), tol=1e-12)
report("a branch moment carries its sibling's base utility, with no edge between them",
       float(not all(sh[3] > 0 for sh in shares)), tol=0.5)
print("      branch A's felt state by source (own branch / shared trunk / sibling B), periods after the fork:")
for tau, own, trunk, sib in shares:
    tot = own + trunk + sib
    print(f"        {tau:2d}: {own / tot:.2%} / {trunk / tot:.2%} / {sib / tot:.4%}")
Rc, _, _ = fork(weight=1.0)
print(f"      copy-counted anticipation (weight 1 per branch): sibling share at the fork "
      f"{Rc[40][br == 2].sum() / Rc[40].sum():.4%}")
print(f"      copy-counted / measure-weighted sibling share at the fork: {Rc[40][br == 2].sum() / Rc[40].sum() / shares[0][3] * (shares[0][1] + shares[0][2] + shares[0][3]):.3f}")
# Long memory, M < 1 kept (near-total recall with B 0.9 would put M past 1): shares depend on the
# trunk's and branches' lengths, so both are stated.
for label, pr in (("mu 0.95, B 0.5", dict(LIFE, m=0.5 * 0.05 / 0.95, mu=0.95)),
                  ("mu 0.99, B 0.8", dict(LIFE, m=0.8 * 0.01 / 0.99, mu=0.99))):
    for L_ in (40, 100):
        Rl, bl, _ = fork(T0=L_, T1=L_, pr=pr)
        out = []
        for tau in (0, 10, 39):
            row = Rl[L_ + tau]
            out.append(f"{tau}: {row[bl == 0].sum() / row.sum():.1%} / {row[bl == 2].sum() / row.sum():.2%}")
        print(f"      {label}, trunk and branches of {L_}: trunk / sibling share at " + ", ".join(out))


# 3. Are persons the clusters? Two people as chains of T moments (the life calibration's kernels, no
#    news), coupled by contagion c each way, symmetrized: W = [[B, 2cI], [2cI, B]], B_ij =
#    a al^|i-j| + m mu^|i-j|. (Codex, cu-persons.)
from scipy.linalg import eigh


def chains(T, c, a=LIFE["a"], al=LIFE["al"], m=LIFE["m"], mu=LIFE["mu"]):
    r = np.abs(np.subtract.outer(np.arange(T), np.arange(T)))
    Bm = np.where(r > 0, a * al ** r + m * mu ** r, 0.0)
    return Bm, np.block([[Bm, 2 * c * np.eye(T)], [2 * c * np.eye(T), Bm]])


def ncut(W, side):
    cut = W[np.ix_(side, ~side)].sum()
    return cut / W[side].sum() + cut / W[~side].sum()


aa, al_, mm, mu_ = LIFE["a"], LIFE["al"], LIFE["m"], LIFE["mu"]
F1 = aa * al_ / (1 - al_) ** 2 + mm * mu_ / (1 - mu_) ** 2
F2 = aa * al_ * (1 + al_) / (1 - al_) ** 3 + mm * mu_ * (1 + mu_) / (1 - mu_) ** 3

# 3a. Candidate cuts: by person (2cT) against each chain at its midpoint (2 C_T, C_T in closed form),
#     equal volumes, so the person split wins iff c < C_T/T ~ F1/T.
err, bad = 0.0, 0
for T in (8, 12, 14, 40):
    n_ = T // 2
    Bm, W = chains(T, 0.05)
    CT = aa * al_ * (1 - al_ ** n_) ** 2 / (1 - al_) ** 2 + mm * mu_ * (1 - mu_ ** n_) ** 2 / (1 - mu_) ** 2
    err = max(err, abs(Bm[:n_, n_:].sum() - CT))
    person = np.r_[np.ones(T, bool), np.zeros(T, bool)]
    time_ = np.r_[np.arange(T) < n_, np.arange(T) < n_]
    bad += (ncut(W, person) < ncut(W, time_)) != (0.05 < CT / T)
report("cuts: the midpoint cut C_T in closed form; person beats time iff c < C_T/T (c = 0.05: T <= 12)",
       err + bad, tol=1e-12)

# 3b. Spectra: person-symmetric modes are L0's, antisymmetric ones L0's + 4c, so the Fiedler value is
#     min(lambda_2(L0), 4c) and the Fiedler vector is (1, -1) below c = lambda_2(L0)/4 ~ F2 pi^2/(4T^2).
lap = lambda W: np.diag(W.sum(1)) - W
err = 0.0
rows = []
for T in (20, 40, 100, 300):
    Bm, _ = chains(T, 0.0)
    l2 = eigh(lap(Bm), eigvals_only=True)[1]
    for c in (0.5 * l2 / 4, 2 * l2 / 4):
        _, W = chains(T, c)
        w_, v_ = eigh(lap(W))
        err = max(err, abs(w_[1] - min(l2, 4 * c)))
        if c < l2 / 4:
            fv = v_[:, 1] * np.sign(v_[0, 1])
            err = max(err, np.max(np.abs(fv - np.r_[np.ones(T), -np.ones(T)] / np.sqrt(2 * T))))
    rows.append((T, F1 / T, l2 / 4, F2 * np.pi ** 2 / (4 * T ** 2)))
report("spectra: Fiedler value min(lambda_2(L0), 4c), Fiedler vector (1, -1) below lambda_2(L0)/4", err, tol=1e-9)
print("      whole-person thresholds on c: cut ~F1/T, spectral lambda_2(L0)/4 (asymptotic F2 pi^2/(4T^2)):")
for T, cut_, sp, asy in rows:
    print(f"        T = {T:3d}: cut {cut_:.5f}, spectral {sp:.3g} ({asy:.3g})")
print(f"        a life of 4000 weeks: cut {F1 / 4000:.2e}, spectral ~{F2 * np.pi ** 2 / (4 * 4000 ** 2):.1e}")

# 3c. Uniform recall over a whole context (memory B/L to every earlier moment, L = T - 1): each person
#     is a complete graph and the threshold is B T/(4L) -> B/4 at every length (Codex).
for T, B_ in ((20, 0.4), (100, 0.4)):
    Bm = np.where(np.subtract.outer(np.arange(T), np.arange(T)) != 0, B_ / (T - 1), 0.0)
    l2 = eigh(lap(Bm), eigvals_only=True)[1]
    err = max(err, abs(l2 / 4 - B_ * T / (4 * (T - 1))))
report("uniform recall: whole-person threshold B T/(4(T - 1)), 0.1053 at T = 20, 0.1010 at 100", err, tol=1e-9)

# 3d. Markov stability (continuous-time walk with generator -L, uniform stationary measure): the person
#     partition's autocovariance is e^{-4ct}/2, the midpoint split's a mix of temporal modes; between the
#     two thresholds persons win first and lose after one crossover (T = 100; Codex: 264.9 at c = 0.001,
#     12.21 at c = 0.003).
T = 100
Bm, _ = chains(T, 0.0)
lam_, vec_ = eigh(lap(Bm))
q = np.r_[np.ones(T // 2), -np.ones(T // 2)]
ak = (vec_.T @ q) ** 2 / T
r_time = lambda t: 0.5 * np.sum(ak[1:] * np.exp(-lam_[1:] * t))
cross = []
for c in (0.001, 0.003):
    f = lambda t: 0.5 * np.exp(-4 * c * t) - r_time(t)
    lo, hi = 1e-6, 1e5
    for _ in range(200):
        mid = np.sqrt(lo * hi)
        lo, hi = (mid, hi) if f(mid) > 0 else (lo, mid)
    cross.append(lo)
report("Markov stability, T = 100: persons first, slices after t* = 264.9 (c 0.001), 12.21 (c 0.003)",
       abs(cross[0] - 264.901) + abs(cross[1] - 12.2108), tol=1e-2)
