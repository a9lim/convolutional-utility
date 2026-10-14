"""Train the hidden-game agent in each variant and evaluate on held-out games.
Run: python experiments/learned_expectations/run_repeated.py   (writes repeated_report.txt, repeated.png)"""
import os
import sys
import time

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from games import CLASSES, classify, pure_nash  # noqa: E402
from repeated import FEEL, rollout, train  # noqa: E402

HERE = os.path.dirname(__file__)
VARIANTS = ["payoff", "calibrated", "motivated"]
K = 10


def balanced_probe(X, y, n_tr, steps=2000):
    """Balanced accuracy of a linear probe for game class (class-weighted training)."""
    mu, sd = X[:n_tr].mean(0), X[:n_tr].std(0) + 1e-9
    X = (X - mu) / sd
    w = torch.bincount(y[:n_tr], minlength=4).double()
    w = (w.sum() / (4 * w.clamp_min(1)))
    W, b = torch.zeros(X.shape[1], 4, requires_grad=True), torch.zeros(4, requires_grad=True)
    opt = torch.optim.Adam([W, b], lr=0.05)
    for _ in range(steps):
        opt.zero_grad()
        torch.nn.functional.cross_entropy(X[:n_tr] @ W + b, y[:n_tr], weight=w).backward()
        opt.step()
    with torch.no_grad():
        pred = (X[n_tr:] @ W + b).argmax(1)
        yt = y[n_tr:]
        return float(np.mean([float((pred[yt == k] == k).float().mean()) for k in range(4)]))


if __name__ == "__main__":
    t0 = time.time()
    lines = []
    say = lambda s: (print(s, flush=True), lines.append(s))
    gen = torch.Generator().manual_seed(4242)
    G = 20000
    A, Bm = torch.rand(G, 2, 2, generator=gen) * 2 - 1, torch.rand(G, 2, 2, generator=gen) * 2 - 1
    cls, ne = classify(A, Bm), pure_nash(A, Bm)
    n_tr = 15000
    res = {}
    for v in VARIANTS:
        agent = train(v, steps=3000)
        with torch.no_grad():
            rec = rollout(agent, A, Bm, K, torch.Generator().manual_seed(1))
        R = rec[0]
        # realized discounted payoff-to-go, the critic's target
        disc = torch.zeros_like(R["r"])
        acc = torch.zeros(G)
        for k in reversed(range(K)):
            acc = R["r"][:, k] + FEEL["nu"] * acc
            disc[:, k] = acc
        bias = (R["C"] - disc).mean(0)
        probes = [balanced_probe(R["h"][:, k], cls, n_tr) for k in (0, 1, 2, 4, 9)]
        last = [(rec[i]["pi"][:, -1] < 0.5).long() for i in range(2)]
        hit = ne[torch.arange(G), last[0], last[1]]
        res[v] = dict(pay=R["r"].mean(0), bias=bias, probes=probes)
        say(f"[{v}] mean payoff by round: " + " ".join(f"{float(x):+.3f}" for x in R["r"].mean(0)))
        say(f"    last-round modal play is a pure equilibrium: unique-efficient {float(hit[cls == 1].float().mean()):.1%}, "
            f"PD-like {float(hit[cls == 2].float().mean()):.1%}, two-equilibrium {float(hit[cls == 3].float().mean()):.1%}")
        say(f"    critic bias (forecast minus realized) by round: " + " ".join(f"{float(x):+.3f}" for x in bias))
        say(f"    game-class probe (balanced accuracy, chance 25%) after rounds 1/2/3/5/10: "
            + " ".join(f"{p:.1%}" for p in probes))
    # weak anticipation (felt calibration): a nu below the chronic-disappointment rate n lam (1 - nu)
    import repeated
    repeated.FEEL["a"] = 0.05
    for v in ("calibrated", "motivated"):
        for seed in (0, 1):
            agent = train(v, steps=3000, seed=seed)
            with torch.no_grad():
                rec = rollout(agent, A, Bm, K, torch.Generator().manual_seed(1))
            R = rec[0]
            disc, acc = torch.zeros_like(R["r"]), torch.zeros(G)
            for k in reversed(range(K)):
                acc = R["r"][:, k] + FEEL["nu"] * acc
                disc[:, k] = acc
            say(f"[{v}, a = 0.05, seed {seed}] critic bias by round: "
                + " ".join(f"{float(x):+.3f}" for x in (R["C"] - disc).mean(0))
                + f"; last-round payoff {float(R['r'][:, -1].mean()):+.3f}")
    # ablation at a = 0.05: is the payoff gain from the felt reward or from the motivated critic?
    for pr, cm in [("payoff", True), ("felt", False), ("felt", True), ("payoff", False)]:
        agent = repeated.train_mix(pr, cm)
        with torch.no_grad():
            rec = rollout(agent, A, Bm, K, torch.Generator().manual_seed(1))
        say(f"[ablation, a = 0.05] policy reward {pr}, critic {'motivated' if cm else 'honest'}: "
            f"late-round payoff {float(rec[0]['r'][:, -3:].mean()):+.3f}")
    repeated.FEEL["a"] = 0.3
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    cols = {"payoff": "#7f7f7f", "calibrated": "#3182bd", "motivated": "#e76f51"}
    for v in VARIANTS:
        axes[0].plot(np.arange(1, K + 1), res[v]["pay"].numpy(), "o-", color=cols[v], label=v)
        axes[1].plot(np.arange(1, K + 1), res[v]["bias"].numpy(), "o-", color=cols[v], label=v)
        axes[2].plot([1, 2, 3, 5, 10], res[v]["probes"], "o-", color=cols[v], label=v)
    axes[0].set_title("Payoff by round", fontsize=10)
    axes[1].axhline(0, color="#aaa", lw=0.8)
    axes[1].set_title("Critic bias: felt forecast minus realized", fontsize=10)
    axes[2].axhline(0.25, color="#aaa", lw=0.8, ls="--")
    axes[2].set_title("Telling games apart: class probe on the state", fontsize=10)
    for ax in axes:
        ax.set_xlabel("round")
        ax.legend(fontsize=8, frameon=False)
    fig.suptitle("Hidden 2x2 games, 10 rounds of self-play: does felt utility change what it learns?", fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "repeated.png"), dpi=130)
    say(f"done in {time.time() - t0:.0f}s")
    open(os.path.join(HERE, "repeated_report.txt"), "w").write("\n".join(lines) + "\n")
