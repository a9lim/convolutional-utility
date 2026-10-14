"""The J dial in games: symmetric games played by one network against itself.
Run: python experiments/learned_expectations/run_twin.py
w = 0 holds the other's policy fixed (causal reasoning: Nash); w = 1 lets the gradient through it, and in a
symmetric game the other is a copy of one's own policy (the twin: evidential or functional reasoning).
Evaluated on prisoner's dilemmas and stag hunts."""
import os
import sys

import torch

sys.path.insert(0, os.path.dirname(__file__))
from games import objectives, train  # noqa: E402


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


if __name__ == "__main__":
    gen = torch.Generator().manual_seed(7)
    fam = {k: symmetric_family(k, 4000, gen) for k in ("PD", "stag hunt")}
    for variant in ("payoff", "calibrated", "free"):
        for w in (0.0, 1.0):
            net, felt = train(variant, steps=4000, batch=1024, w=w, symmetric=True)
            row = []
            with torch.no_grad():
                for k, (A, Bm) in fam.items():
                    _, (pi1, q1, pi2, q2) = objectives(net, felt, A, Bm, variant, w=w)
                    row.append(f"{k}: P(cooperate / stag) {float(pi1.mean()):.2f}")
            print(f"[{variant}, w = {w:g}] " + "; ".join(row), flush=True)

    # the graded dial on prisoner's dilemmas: with weight w on the twin's dependence, all-cooperate is
    # stable iff w >= (T - R)/(R - S), all-defect iff w <= (P - S)/(T - P)
    A, Bm = fam["PD"]
    R, S, T_, P = A[:, 0, 0], A[:, 0, 1], A[:, 1, 0], A[:, 1, 1]
    wc, wd = (T_ - R) / (R - S), (P - S) / (T_ - P)
    for w in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        net, felt = train("payoff", steps=4000, batch=1024, w=w, symmetric=True)
        with torch.no_grad():
            _, (pi1, _, _, _) = objectives(net, felt, A, Bm, "payoff", w=w)
        coop = pi1 > 0.5
        only_c, only_d, both = (w >= wc) & (w > wd), (w < wc) & (w <= wd), (w >= wc) & (w <= wd)
        print(f"PD dial w = {w:.1f}: learned cooperation {float(coop.float().mean()):.2f}; cooperation the only stable "
              f"profile in {float(only_c.float().mean()):.2f} of games (learned there {float(coop[only_c].float().mean()) if only_c.any() else float('nan'):.2f}), "
              f"defection the only one in {float(only_d.float().mean()):.2f} (learned cooperation there "
              f"{float(coop[only_d].float().mean()) if only_d.any() else float('nan'):.2f}), both in {float(both.float().mean()):.2f}",
              flush=True)
