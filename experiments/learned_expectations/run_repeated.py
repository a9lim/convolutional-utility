"""Train the hidden-game agent in each variant over several seeds and evaluate on held-out games.
Run: python experiments/learned_expectations/run_repeated.py   (writes repeated_report.txt, repeated.png; parallel)
Variants: payoff (policy on payoffs, honest critic), calibrated (policy on felt utility, honest critic),
motivated (policy on felt utility, critic also ascends it), at a = 0.3 and at weak anticipation a = 0.05."""
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from games import classify, pure_nash  # noqa: E402
from repeated import FEEL, rollout, train  # noqa: E402

HERE = os.path.dirname(__file__)
K, SEEDS = 10, range(4)
WEAK = dict(FEEL, a=0.05)
VARIANTS = {"payoff": ("payoff", "honest", FEEL), "calibrated": ("felt", "honest", FEEL),
            "motivated": ("felt", "motivated", FEEL), "calibrated, a = 0.05": ("felt", "honest", WEAK),
            "motivated, a = 0.05": ("felt", "motivated", WEAK)}


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


def one(job):
    v, seed = job
    torch.set_num_threads(int(os.environ.get("THREADS", "3")))
    policy, critic, feel = VARIANTS[v]
    agent = train(policy, critic, seed=seed, feel=feel)
    gen = torch.Generator().manual_seed(4242)
    G, n_tr = 20000, 15000
    A, Bm = torch.rand(G, 2, 2, generator=gen) * 2 - 1, torch.rand(G, 2, 2, generator=gen) * 2 - 1
    cls, ne = classify(A, Bm), pure_nash(A, Bm)
    with torch.no_grad():
        rec = rollout(agent, A, Bm, K, torch.Generator().manual_seed(1))
    R = rec[0]
    disc, acc = torch.zeros_like(R["r"]), torch.zeros(G)        # realized discounted payoff-to-go
    for k in reversed(range(K)):
        acc = R["r"][:, k] + FEEL["nu"] * acc
        disc[:, k] = acc
    last = [(rec[i]["pi"][:, -1] < 0.5).long() for i in range(2)]
    hit = ne[torch.arange(G), last[0], last[1]]
    return v, dict(pay=R["r"].mean(0).numpy(), bias=(R["C"] - disc).mean(0).numpy(),
                   probes=[balanced_probe(R["h"][:, k], cls, n_tr) for k in (0, 1, 2, 4, 9)],
                   eq=[float(hit[cls == c].float().mean()) for c in (1, 2, 3)], late=float(R["r"][:, -3:].mean()))


if __name__ == "__main__":
    t0, lines = time.time(), []
    say = lambda s: (print(s, flush=True), lines.append(s))
    with ProcessPoolExecutor(int(os.environ.get("PROCS", "6"))) as ex:
        out = list(ex.map(one, [(v, s) for v in VARIANTS for s in SEEDS]))
    say(f"{len(SEEDS)} seeds per variant; means over seeds. Escaped the complacent plateau: late payoff above 0.26.")
    res = {}
    for v in VARIANTS:
        rs = [o for n, o in out if n == v]
        m = {k: np.mean([o[k] for o in rs], 0) for k in ("pay", "bias", "probes", "eq")}
        res[v] = m
        say(f"[{v}] escaped {sum(o['late'] > 0.26 for o in rs)}/{len(rs)} (late payoffs "
            + " ".join(f"{o['late']:.3f}" for o in rs) + ")")
        say("    mean payoff by round: " + " ".join(f"{x:+.3f}" for x in m["pay"]))
        say(f"    last-round modal play is a pure equilibrium: unique-efficient {m['eq'][0]:.1%}, "
            f"PD-like {m['eq'][1]:.1%}, two-equilibrium {m['eq'][2]:.1%}")
        say("    critic bias (forecast minus realized) by round: " + " ".join(f"{x:+.3f}" for x in m["bias"]))
        say("    game-class probe (balanced accuracy, chance 25%) after rounds 1/2/3/5/10: "
            + " ".join(f"{p:.1%}" for p in m["probes"]))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    cols = {"payoff": "#7f7f7f", "calibrated": "#3182bd", "motivated": "#e76f51",
            "calibrated, a = 0.05": "#9ecae1", "motivated, a = 0.05": "#2a9d8f"}
    for v in VARIANTS:
        axes[0].plot(np.arange(1, K + 1), res[v]["pay"], "o-", color=cols[v], label=v)
        axes[1].plot(np.arange(1, K + 1), res[v]["bias"], "o-", color=cols[v], label=v)
        axes[2].plot([1, 2, 3, 5, 10], res[v]["probes"], "o-", color=cols[v], label=v)
    axes[0].set_title("Payoff by round", fontsize=10)
    axes[1].axhline(0, color="#aaa", lw=0.8)
    axes[1].set_title("Critic bias: felt forecast minus realized", fontsize=10)
    axes[2].axhline(0.25, color="#aaa", lw=0.8, ls="--")
    axes[2].set_title("Telling games apart: class probe on the state", fontsize=10)
    for ax in axes:
        ax.set_xlabel("round")
        ax.legend(fontsize=7, frameon=False)
    fig.suptitle(f"Hidden 2x2 games, 10 rounds of self-play, means over {len(SEEDS)} seeds", fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "repeated.png"), dpi=130)
    say(f"done in {time.time() - t0:.0f}s")
    open(os.path.join(HERE, "repeated_report.txt"), "w").write("\n".join(lines) + "\n")
