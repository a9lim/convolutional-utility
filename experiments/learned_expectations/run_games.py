"""Train the game-playing agent in each variant and evaluate on held-out random 2x2 games.
Run: python experiments/learned_expectations/run_games.py   (writes games_report.txt and games.png)"""
import os
import sys
import time

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from games import CLASSES, classify, objectives, pure_nash, sample_games, train, views  # noqa: E402

VARIANTS = ["payoff", "calibrated", "free", "coupled"]
HERE = os.path.dirname(__file__)


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


def probe(X, y, Xt, yt, steps=3000):
    """Multinomial logistic-regression probe accuracy."""
    mu, sd = X.mean(0), X.std(0) + 1e-9
    X, Xt = (X - mu) / sd, (Xt - mu) / sd
    W = torch.zeros(X.shape[1], 4, requires_grad=True)
    b = torch.zeros(4, requires_grad=True)
    opt = torch.optim.Adam([W, b], lr=0.05)
    for _ in range(steps):
        opt.zero_grad()
        torch.nn.functional.cross_entropy(X @ W + b, y).backward()
        opt.step()
    with torch.no_grad():
        return float(((Xt @ W + b).argmax(1) == yt).float().mean())


if __name__ == "__main__":
    t0 = time.time()
    lines = []
    say = lambda s: (print(s, flush=True), lines.append(s))
    gen = torch.Generator().manual_seed(2026)
    A, Bm = sample_games(20000, gen)
    ne, cls = pure_nash(A, Bm), classify(A, Bm)
    rd, pd = risk_dominant(A, Bm, ne)
    sel = (rd >= 0) & (pd >= 0) & (rd != pd)               # risk- and payoff-dominance disagree
    say(f"held-out games: " + ", ".join(f"{c} {int((cls == k).sum())}" for k, c in enumerate(CLASSES))
        + f"; two-equilibrium games where risk and payoff dominance disagree: {int(sel.sum())}")
    res = {}
    for v in VARIANTS:
        net, felt = train(v, steps=6000, batch=1024)
        with torch.no_grad():
            (o1, o2), (pi1, q1, pi2, q2) = objectives(net, felt, A, Bm, v)
            (m1, t1), _ = views(A, Bm)
            _, _, h = net(m1, t1)
        res[v] = (net, felt, pi1, q1, pi2, q2, h)
        i1, i2 = (pi1 < 0.5).long(), (pi2 < 0.5).long()
        hit = ne[torch.arange(len(cls)), i1, i2]
        accs = [float(hit[cls == k].float().mean()) for k in (1, 2, 3)]
        # equilibrium selection where risk and payoff dominance disagree
        chosen = torch.full_like(rd, -1)
        for b in torch.nonzero(sel)[:, 0].tolist():
            eqs = [(i, j) for i in (0, 1) for j in (0, 1) if ne[b, i, j]]
            if (int(i1[b]), int(i2[b])) in eqs:
                chosen[b] = eqs.index((int(i1[b]), int(i2[b])))
        rd_share = float((chosen[sel] == rd[sel]).float().sum() / (chosen[sel] >= 0).float().sum().clamp_min(1))
        say(f"[{v}] plays a pure equilibrium: unique-efficient {accs[0]:.1%}, PD-like {accs[1]:.1%}, "
            f"two-equilibrium {accs[2]:.1%}; where risk and payoff dominance disagree, picks the risk-dominant "
            f"one {rd_share:.1%}; cyclic games: mean |P(move 0) - 1/2| {float((pi1[cls == 0] - 0.5).abs().mean()):.3f}")
        if v in ("free", "coupled"):
            # optimism: belief tilt toward the other's move that is better for me, given my likelier move
            mine = A
            good = (mine[torch.arange(len(cls)), i1, 0] < mine[torch.arange(len(cls)), i1, 1]).long()   # 1: their move 1 better for me
            q_good = torch.where(good == 0, q1, 1 - q1)
            p_good = torch.where(good == 0, pi2, 1 - pi2)
            tilt = q_good - p_good
            say(f"    belief tilt toward the outcome good for me (q - p): " + ", ".join(
                f"{CLASSES[k]} {float(tilt[cls == k].mean()):+.3f}" for k in range(4)))
    # a looser tether: motivated beliefs at tau = 30
    for v in ("free", "coupled"):
        net, felt = train(v, steps=6000, batch=1024, tau=30.0)
        with torch.no_grad():
            _, (pi1, q1, pi2, q2) = objectives(net, felt, A, Bm, v, tau=30.0)
        i1, i2 = (pi1 < 0.5).long(), (pi2 < 0.5).long()
        hit = ne[torch.arange(len(cls)), i1, i2]
        good = (A[torch.arange(len(cls)), i1, 0] < A[torch.arange(len(cls)), i1, 1]).long()
        tilt = torch.where(good == 0, q1, 1 - q1) - torch.where(good == 0, pi2, 1 - pi2)
        say(f"[{v}, tau = 30] pure equilibrium: unique-efficient {float(hit[cls == 1].float().mean()):.1%}, "
            f"PD-like {float(hit[cls == 2].float().mean()):.1%}, two-equilibrium {float(hit[cls == 3].float().mean()):.1%}; "
            "belief tilt toward the good outcome: " + ", ".join(f"{CLASSES[k]} {float(tilt[cls == k].mean()):+.3f}" for k in range(4)))
    # do they tell games apart? probe class from the hidden layer vs from raw payoffs
    X_raw = torch.cat([A.flatten(1), Bm.flatten(1)], 1)
    n_tr = 15000
    raw = probe(X_raw[:n_tr], cls[:n_tr], X_raw[n_tr:], cls[n_tr:])
    say(f"linear probe for game class: raw payoffs {raw:.1%}; " + ", ".join(
        f"{v} hidden layer {probe(res[v][6][:n_tr], cls[:n_tr], res[v][6][n_tr:], cls[n_tr:]):.1%}" for v in VARIANTS))
    # differences in play: felt variants against the payoff baseline
    base = (res["payoff"][2] < 0.5)
    for v in ("calibrated", "free", "coupled"):
        diff = ((res[v][2] < 0.5) != base)
        say(f"[{v}] modal move differs from the payoff agent in: " + ", ".join(
            f"{CLASSES[k]} {float(diff[cls == k].float().mean()):.1%}" for k in range(4)))
    # figure: PCA of the free agent's hidden layer, coloured by class; belief tilt by class
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    h = res["free"][6][:4000]
    hc = h - h.mean(0)
    U, S, Vt = torch.linalg.svd(hc, full_matrices=False)
    Z = hc @ Vt[:2].T
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    cols = ["#e76f51", "#2a9d8f", "#8e44ad", "#e9c46a"]
    for k in range(4):
        sel_k = cls[:4000] == k
        axes[0].scatter(Z[sel_k, 0], Z[sel_k, 1], s=4, alpha=0.5, color=cols[k], label=CLASSES[k])
    axes[0].set_title("Felt agent's hidden layer (PCA), by game class", fontsize=10)
    axes[0].legend(fontsize=8, markerscale=3, frameon=False)
    for j, v in enumerate(("free", "coupled")):
        pi1, q1, pi2 = res[v][2], res[v][3], res[v][4]
        i1 = (pi1 < 0.5).long()
        good = (A[torch.arange(len(cls)), i1, 0] < A[torch.arange(len(cls)), i1, 1]).long()
        tilt = torch.where(good == 0, q1, 1 - q1) - torch.where(good == 0, pi2, 1 - pi2)
        means = [float(tilt[cls == k].mean()) for k in range(4)]
        axes[1].bar(np.arange(4) + 0.38 * j, means, width=0.38, label=v, color=["#3182bd", "#9ecae1"][j])
    axes[1].axhline(0, color="#777", lw=0.8)
    axes[1].set_xticks(np.arange(4) + 0.19, ["cyclic", "unique\nefficient", "PD-like", "two eq."], fontsize=8)
    axes[1].set_ylabel("belief tilt toward the good outcome (q − p)")
    axes[1].set_title("Motivated beliefs about the other player", fontsize=10)
    axes[1].legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "games.png"), dpi=130)
    say(f"done in {time.time() - t0:.0f}s")
    open(os.path.join(HERE, "games_report.txt"), "w").write("\n".join(lines) + "\n")
