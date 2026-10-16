"""Games: the distributions the learners play and the analysis of them.

- One-shot bimatrix games: `sample_games` (every payoff uniform on [-1, 1]), `views` (each player's view),
  `pure_nash`, `classify` and `CLASSES`, `risk_dominant`.
- `symmetric_family`: symmetric prisoner's dilemmas (with 2R > T + S) and stag hunts (hare risk-dominant), by
  rejection; the one-shot agents' evaluation families.
- `FAMILIES`, `family_round`, `relabeled`: the iterated agent's rounds, one of four symmetric families per game
  with payoffs assigned by rank alone (no 2R > T + S), each player seeing its own random action labels.
"""
import torch

torch.set_default_dtype(torch.float64)


def sample_games(B, gen):
    """Bimatrix games: A[b, i, j] row player's payoff, Bm[b, i, j] column player's (i row move, j column)."""
    return torch.rand(B, 2, 2, generator=gen) * 2 - 1, torch.rand(B, 2, 2, generator=gen) * 2 - 1


def views(A, Bm):
    """Each player's view: (my payoffs, their payoffs), indexed [my move, their move]."""
    return (A, Bm), (Bm.transpose(1, 2), A.transpose(1, 2))


def pure_nash(A, Bm):
    """Boolean (B, 2, 2): which pure profiles are Nash equilibria of the payoff game."""
    row_best = A >= A.max(1, keepdim=True).values
    col_best = Bm >= Bm.max(2, keepdim=True).values
    return row_best & col_best


def classify(A, Bm):
    """0: no pure equilibrium (cyclic); 1: one, Pareto-efficient; 2: one, Pareto-dominated (PD-like);
    3: two (coordination or anti-coordination)."""
    ne = pure_nash(A, Bm)
    k = ne.flatten(1).sum(1)
    cls = torch.where(k == 0, 0, torch.where(k >= 2, 3, 1))
    idx = ne.flatten(1).float().argmax(1)
    a_ne, b_ne = A.flatten(1).gather(1, idx[:, None])[:, 0], Bm.flatten(1).gather(1, idx[:, None])[:, 0]
    dominated = ((A.flatten(1) > a_ne[:, None]) & (Bm.flatten(1) > b_ne[:, None])).any(1)
    return torch.where((cls == 1) & dominated, 2, cls)


CLASSES = ["cyclic", "unique, efficient", "unique, dominated (PD-like)", "two equilibria"]


def risk_dominant(A, Bm, ne):
    """For games with two pure equilibria on a diagonal or anti-diagonal: index (0/1) of the
    risk-dominant one by the Harsanyi-Selten product of deviation losses, and of the payoff-dominant
    one if one Pareto-dominates (else -1)."""
    rd, pd = torch.full((A.shape[0],), -1), torch.full((A.shape[0],), -1)
    for b in range(A.shape[0]):
        eqs = [(i, j) for i in (0, 1) for j in (0, 1) if ne[b, i, j]]
        if len(eqs) != 2 or eqs[0][0] == eqs[1][0] or eqs[0][1] == eqs[1][1]:
            continue
        loss = []
        for (i, j) in eqs:
            loss.append((A[b, i, j] - A[b, 1 - i, j]) * (Bm[b, i, j] - Bm[b, i, 1 - j]))
        rd[b] = 0 if loss[0] > loss[1] else 1
        (i0, j0), (i1, j1) = eqs
        if A[b, i0, j0] > A[b, i1, j1] and Bm[b, i0, j0] > Bm[b, i1, j1]:
            pd[b] = 0
        elif A[b, i1, j1] > A[b, i0, j0] and Bm[b, i1, j1] > Bm[b, i0, j0]:
            pd[b] = 1
    return rd, pd


def symmetric_family(kind, B, gen):
    """Symmetric 2x2 games A[i, j] (row payoff, move 0 = cooperate / stag), B = A^T.
    PD: T > R > P > S and 2R > T + S. Stag hunt: R > T >= P > S, risk-dominant hare (R + S < T + P)."""
    u = torch.rand(B, 4, generator=gen)
    if kind == "PD":
        S, P, R, T_ = (torch.sort(u * 2 - 1, 1).values).unbind(1)
        ok = 2 * R > T_ + S
    else:
        S, P, T_, R = (torch.sort(u * 2 - 1, 1).values).unbind(1)
        ok = R + S < T_ + P
    A = torch.stack([torch.stack([R, S], 1), torch.stack([T_, P], 1)], 1)[ok]
    return A, A.transpose(1, 2)


FAMILIES = ["prisoner's dilemma", "chicken", "stag hunt", "harmony"]
# rank (0 = largest of the four draws) of R, S, T, P in each family
RANKS = torch.tensor([[1, 3, 0, 2],      # PD:        T > R > P > S
                      [1, 2, 0, 3],      # chicken:   T > R > S > P
                      [0, 3, 1, 2],      # stag hunt: R > T > P > S
                      [0, 2, 1, 3]])     # harmony:   R > T > S > P


def family_round(G, gen, families=(0, 1, 2, 3)):
    """Canonical payoff matrices M (G, 2, 2) for the row player ([[R, S], [T, P]], C = 0, four sorted draws from
    U[-1, 1] assigned by the family's order), the family index, and each player's label flip."""
    fam = torch.tensor(families)[torch.randint(len(families), (G,), generator=gen)]
    v = torch.sort(torch.rand(G, 4, generator=gen) * 2 - 1, dim=1, descending=True).values
    RSTP = v.gather(1, RANKS[fam])
    M = torch.stack([torch.stack([RSTP[:, 0], RSTP[:, 1]], 1), torch.stack([RSTP[:, 2], RSTP[:, 3]], 1)], 1)
    flips = [torch.rand(G, generator=gen) < 0.5 for _ in range(2)]
    return M, fam, flips


def relabeled(M, f_me, f_them):
    """(my payoffs, their payoffs) of a symmetric game M, indexed [my label, their label], flattened to 8 numbers."""
    def relabel(X, fr, fc):
        X = torch.where(fr[:, None, None], X.flip(1), X)
        return torch.where(fc[:, None, None], X.flip(2), X)
    mine = relabel(M, f_me, f_them)
    theirs = relabel(M.transpose(1, 2), f_me, f_them)
    return torch.cat([mine.flatten(1), theirs.flatten(1)], 1)
