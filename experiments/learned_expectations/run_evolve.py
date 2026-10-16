"""Which ways of feeling survive? Evolution of heritable felt parameters in learning agents. Run:
python experiments/learned_expectations/run_evolve.py   (writes evolve_report.txt, evolve.png; runs in parallel)

Each generation, a population of hidden-game agents (rounds.py) is born untrained, with heritable felt
parameters (anticipation a, news n, loss aversion lam; echoes otherwise as felt.ROUNDS), and learns for one lifetime
of LIFE steps playing random 2x2 games against randomly paired members, each from its own seat. Fitness is
lifetime payoff, which rewards learning fast. The top half each leave two offspring with log-normally
mutated parameters (a, n and lam - 1); weights are not inherited. Variants:
- "felt critic":  the policy ascends payoffs; the critic is motivated (affect shapes forecasts only);
- "felt agents":  the policy ascends felt utility and the critic is motivated;
- "neutral":      the policy ascends payoffs, the critic is honest, so the parameters do nothing (drift control).
Selection gradients: within each generation, lifetime payoff regressed on standardized log a, log n and
log(lam - 1), pooled over generations and runs.
"""
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from agents import Agent  # noqa: E402
from felt import ROUNDS, rounds_direct  # noqa: E402
from rounds import Hidden, hidden_layout, rollout, td_loss  # noqa: E402

P, G, K = 8, 2048, 10
LIFE = int(os.environ.get("LIFE", "1500"))
GENS = int(os.environ.get("GENS", "12"))
VARIANTS = ["felt critic", "felt agents", "neutral"]
LO, HI = np.log([0.005, 0.005, 0.01]), np.log([0.8, 0.8, 5.0])            # bounds on log a, log n, log(lam - 1)


def unpack(g):
    return dict(a=float(np.exp(g[0])), n=float(np.exp(g[1])), lam=float(1 + np.exp(g[2])))


def loss_of(R, f, variant):
    reward = rounds_direct(R["r"], R["C"].detach(), f) if variant == "felt agents" else R["r"]
    ret = torch.flip(torch.cumsum(torch.flip(reward.detach(), [1]), 1), [1])
    loss = -(R["logp"] * (ret - ret.mean(0, keepdim=True))).mean() + td_loss(R, f)
    if variant != "neutral":
        loss = loss - rounds_direct(R["r"], R["C"], f).sum(1).mean()
    return loss


def lifetime(genomes, variant, rng, gen):
    """Train a fresh population for one lifetime; returns each member's mean payoff over it."""
    agents = [Agent(**hidden_layout()) for _ in genomes]
    opts = [torch.optim.Adam(ag.parameters(), lr=3e-3) for ag in agents]
    feels = [dict(ROUNDS, **unpack(g)) for g in genomes]
    total, g = np.zeros(P), G // (P // 2)
    for _ in range(LIFE):
        A, Bm = torch.rand(G, 2, 2, generator=gen) * 2 - 1, torch.rand(G, 2, 2, generator=gen) * 2 - 1
        order, loss = rng.permutation(P), 0.0
        for p in range(P // 2):
            i, j = order[2 * p], order[2 * p + 1]
            rec = rollout(agents[i], Hidden(A[p * g:(p + 1) * g], Bm[p * g:(p + 1) * g]), K, gen, other=agents[j])
            for seat, k in ((0, i), (1, j)):
                loss = loss + loss_of(rec[seat], feels[k], variant)
                total[k] += float(rec[seat]["r"].mean())
        for o in opts:
            o.zero_grad()
        loss.backward()
        for ag, o in zip(agents, opts):
            torch.nn.utils.clip_grad_norm_(ag.parameters(), 5.0)
            o.step()
    return total / LIFE


def evolve(job):
    variant, seed = job
    torch.set_num_threads(int(os.environ.get("THREADS", "3")))
    rng = np.random.default_rng(seed)
    gen = torch.Generator().manual_seed(seed)
    torch.manual_seed(seed)
    genomes = np.column_stack([rng.uniform(np.log(0.02), np.log(0.5), P), rng.uniform(np.log(0.02), np.log(0.5), P),
                               rng.uniform(np.log(0.05), np.log(3.0), P)])
    hist = []
    for _ in range(GENS):
        fit = lifetime(genomes, variant, rng, gen)
        hist.append(dict(genomes=genomes.tolist(), fit=fit.tolist()))
        parents = genomes[np.argsort(fit)[-(P // 2):]]
        genomes = np.clip(np.repeat(parents, 2, axis=0) + 0.2 * rng.normal(size=(P, 3)), LO, HI)
    return variant, seed, hist


if __name__ == "__main__":
    t0, lines = time.time(), []
    say = lambda s: (print(s, flush=True), lines.append(s))
    seeds = range(int(os.environ.get("SEEDS", "4")))
    with ProcessPoolExecutor(int(os.environ.get("PROCS", "6"))) as ex:
        out = list(ex.map(evolve, [(v, s) for v in VARIANTS for s in seeds]))
    say(f"Population {P}, lifetime {LIFE} steps, {GENS} generations, {len(seeds)} runs per variant. Founders:")
    say("a, n log-uniform on [0.02, 0.5], lam - 1 log-uniform on [0.05, 3]. Final: the last generation's")
    say("members over all runs, median [IQR]. Selection gradient: lifetime payoff (x1000) on standardized log a,")
    say("log n, log(lam - 1) within generation, pooled, with standard errors.")
    for v in VARIANTS:
        runs = [h for v_, _, h in out if v_ == v]
        last = np.array([[u["a"], u["n"], u["lam"]] for h in runs for u in map(unpack, h[-1]["genomes"])])
        q = lambda c: f"{np.median(last[:, c]):.3f} [{np.quantile(last[:, c], .25):.3f}, {np.quantile(last[:, c], .75):.3f}]"
        X, y = [], []
        for h in runs:
            for gen_ in h:
                Z = np.array(gen_["genomes"])
                X.append((Z - Z.mean(0)) / (Z.std(0) + 1e-9))
                y.append(np.array(gen_["fit"]) - np.mean(gen_["fit"]))
        X, y = np.vstack(X), np.concatenate(y) * 1000
        beta, res = np.linalg.lstsq(X, y, rcond=None)[:2]
        se = np.sqrt(np.diag(np.linalg.inv(X.T @ X)) * float(res[0]) / (len(y) - 3))
        fit0 = np.mean([np.mean(h[0]["fit"]) for h in runs])
        fit1 = np.mean([np.mean(h[-1]["fit"]) for h in runs])
        say(f"[{v}] final a {q(0)}  n {q(1)}  lam {q(2)}; lifetime payoff {fit0:.3f} -> {fit1:.3f}; "
            "selection gradient a {:+.2f} ({:.2f}), n {:+.2f} ({:.2f}), lam {:+.2f} ({:.2f})".format(
                beta[0], se[0], beta[1], se[1], beta[2], se[2]))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))
    cols = {"felt critic": "#2a9d8f", "felt agents": "#e76f51", "neutral": "#7f7f7f"}
    for v in VARIANTS:
        for i, h in enumerate([h for v_, _, h in out if v_ == v]):
            med = np.array([np.median(np.array(x["genomes"]), 0) for x in h])
            for c, (name, f) in enumerate([("a", np.exp), ("n", np.exp), ("lam", lambda z: 1 + np.exp(z))]):
                axes[c].plot(np.arange(1, GENS + 1), f(med[:, c]), color=cols[v], alpha=0.7,
                             label=v if i == 0 else None)
    for c, name in enumerate(("anticipation a", "news n", "loss aversion lam")):
        axes[c].set_title(f"population median: {name}", fontsize=10)
        axes[c].set_xlabel("generation")
        axes[c].set_yscale("log")
    axes[0].legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(__file__), "evolve.png"), dpi=120)
    say(f"done in {time.time() - t0:.0f}s")
    open(os.path.join(os.path.dirname(__file__), "evolve_report.txt"), "w").write("\n".join(lines) + "\n")
