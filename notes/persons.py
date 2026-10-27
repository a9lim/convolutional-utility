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
