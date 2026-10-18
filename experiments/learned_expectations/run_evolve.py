"""Which ways of feeling survive? Evolution of heritable felt parameters in learning agents. Run:
python experiments/learned_expectations/run_evolve.py   (writes evolve_report.txt, evolve.png; runs in parallel)

Each generation, a population of hidden-game agents (rounds.py) is born untrained, with heritable felt
parameters, and learns for one lifetime of LIFE steps playing random 2x2 games against randomly paired members,
each from its own seat. The genome: strengths of anticipation a and news n, and the three sign asymmetries the
rounds engine carries (felt.rounds_direct; core X1, X2, X4), each a loss/gain ratio that is 1 in the canonical
model: dread (a-/a+), rumination (m-/m+) and the news loss/gain ratio lam. Echoes otherwise as felt.ROUNDS. Fitness is
lifetime payoff, which rewards learning fast. The top half each leave two offspring with log-normally mutated
parameters; weights are not inherited. Variants:
- "felt critic":  the policy ascends payoffs; the critic is motivated (affect shapes forecasts only), so the
                  memory of payoffs, and with it rumination, does nothing (a drift control within the variant);
- "felt agents":  the policy ascends felt utility and the critic is motivated;
- "neutral":      the policy ascends payoffs, the critic is honest, so the parameters do nothing (drift control).
Selection gradients: within each generation, lifetime payoff regressed on the standardized log genome, pooled
over generations and runs; and per run, the spread of those slopes across runs, the primary summary (shared games
and ancestry make pooled OLS errors optimistic). This is exploratory coevolution: founders range widely and the
genes are linked in small populations, so it measures associations, not the local selection gradient at the
canonical model (run_invasion.py; Codex). Raw histories go to evolve_runs.json.
"""
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from agents import Agent  # noqa: E402
from felt import ROUNDS, rounds_direct  # noqa: E402
from rounds import Hidden, hidden_layout, rollout, td_loss, to_go  # noqa: E402

P, G, K = 8, 2048, 10
LIFE = int(os.environ.get("LIFE", "1200"))
GENS = int(os.environ.get("GENS", "10"))
VARIANTS = ["felt critic", "felt agents", "neutral"]
GENES = ("a", "n", "lam", "dread", "rumination")
FOUNDERS = np.log([[0.02, 0.5], [0.02, 0.5], [1 / 3, 3], [1 / 3, 3], [1 / 3, 3]])   # log-uniform ranges
LO, HI = np.log([0.005, 0.005, 0.2, 0.2, 0.2]), np.log([0.8, 0.8, 5.0, 5.0, 5.0])


def unpack(g):
    return {k: float(np.exp(x)) for k, x in zip(GENES, g)}


def loss_of(R, f, variant):
    """A member's loss under its feel f. Beyond the genes, f may carry `h`, the felt reference's strength (the
    motivated critic ascends welfare, weighing its push by 1 / (1 + h); the reference's level in felt rewards
    cancels against the batch baseline), and `meanfield`: the critic's felt push replaced by its batch mean at each
    round, the per-round level of the forcing without its dependence on the history (the signs of forecasts and
    TD errors that the sign ratios read). At the canonical model the push is the same for every episode, so
    meanfield changes nothing there."""
    reward = rounds_direct(R["r"], R["C"].detach(), f) if variant == "felt agents" else R["r"]
    ret = to_go(reward)
    loss = -(R["logp"] * (ret - ret.mean(0, keepdim=True))).mean() + td_loss(R, f)
    if variant != "neutral":
        felt = rounds_direct(R["r"], R["C"], f)
        if f.get("meanfield"):
            g = torch.autograd.grad(felt.sum(), R["C"], retain_graph=True)[0]          # each episode's push on C
            push = (g.mean(0) * R["C"]).sum(1).mean()
        else:
            push = felt.sum(1).mean()
        loss = loss - push / (1 + f.get("h", 0.0))
    return loss


def lifetime(feels, variant, rng, gen):
    """Train a fresh population, one member per feel, for one lifetime. Returns each member's mean payoff over it,
    its critic's mean level (forecast minus realized nu-discounted payoff-to-go, rounds 2-10) and, for members whose
    feel carries `probe`, the within-round spread of the felt push on its critic (s.d. over episodes over |mean|,
    averaged over rounds and steps; zero when the push is the same for every episode)."""
    agents = [Agent(**hidden_layout()) for _ in feels]
    opts = [torch.optim.Adam(ag.parameters(), lr=3e-3) for ag in agents]
    total, level, spread, g = np.zeros(P), np.zeros(P), np.zeros(P), G // (P // 2)
    for _ in range(LIFE):
        A, Bm = torch.rand(G, 2, 2, generator=gen) * 2 - 1, torch.rand(G, 2, 2, generator=gen) * 2 - 1
        order, loss = rng.permutation(P), 0.0
        for p in range(P // 2):
            i, j = order[2 * p], order[2 * p + 1]
            rec = rollout(agents[i], Hidden(A[p * g:(p + 1) * g], Bm[p * g:(p + 1) * g]), K, gen, other=agents[j])
            for seat, k in ((0, i), (1, j)):
                R = rec[seat]
                loss = loss + loss_of(R, feels[k], variant)
                total[k] += float(R["r"].mean())
                with torch.no_grad():
                    disc, acc = torch.zeros_like(R["r"]), torch.zeros(len(R["r"]))
                    for t in reversed(range(K)):
                        acc = R["r"][:, t] + feels[k]["nu"] * acc
                        disc[:, t] = acc
                    level[k] += float((R["C"] - disc)[:, 1:].mean())
                if feels[k].get("probe"):                      # how much the felt push on C varies within a round
                    C = R["C"].detach().requires_grad_()
                    push = torch.autograd.grad(rounds_direct(R["r"], C, feels[k]).sum(), C)[0]
                    spread[k] += float((push.std(0) / push.mean(0).abs().clamp_min(1e-12)).mean())
        for o in opts:
            o.zero_grad()
        loss.backward()
        for ag, o in zip(agents, opts):
            torch.nn.utils.clip_grad_norm_(ag.parameters(), 5.0)
            o.step()
    return total / LIFE, level / LIFE, spread / LIFE


def evolve(job):
    variant, seed = job
    torch.set_num_threads(int(os.environ.get("THREADS", "2")))
    rng = np.random.default_rng(seed)
    gen = torch.Generator().manual_seed(seed)
    torch.manual_seed(seed)
    genomes = np.column_stack([rng.uniform(lo, hi, P) for lo, hi in FOUNDERS])
    hist = []
    for _ in range(GENS):
        fit = lifetime([dict(ROUNDS, **unpack(g)) for g in genomes], variant, rng, gen)[0]
        hist.append(dict(genomes=genomes.tolist(), fit=fit.tolist()))
        parents = genomes[np.argsort(fit)[-(P // 2):]]
        genomes = np.clip(np.repeat(parents, 2, axis=0) + 0.2 * rng.normal(size=(P, len(GENES))), LO, HI)
    return variant, seed, hist


def gradients(runs):
    """Lifetime payoff (x1000) on the standardized log genome within generation: pooled slopes with OLS standard
    errors (one intercept per run-generation), and the slopes run by run."""
    def fit(hs):
        X, y = [], []
        for h in hs:
            for gen_ in h:
                Z = np.array(gen_["genomes"])
                X.append((Z - Z.mean(0)) / (Z.std(0) + 1e-9))
                y.append(np.array(gen_["fit"]) - np.mean(gen_["fit"]))
        groups = len(X)
        X, y = np.vstack(X), np.concatenate(y) * 1000
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        r = y - X @ beta
        s2 = float(r @ r) / (len(y) - groups - X.shape[1])
        return beta, np.sqrt(np.diag(np.linalg.pinv(X.T @ X)) * s2)
    beta, se = fit(runs)
    return beta, se, np.array([fit([h])[0] for h in runs])


if __name__ == "__main__":
    t0, lines = time.time(), []
    say = lambda s: (print(s, flush=True), lines.append(s))  # noqa: E731
    seeds = range(int(os.environ.get("SEEDS", "6")))
    with ProcessPoolExecutor(int(os.environ.get("PROCS", "9"))) as ex:
        out = list(ex.map(evolve, [(v, s) for v in VARIANTS for s in seeds]))
    json.dump(dict(config=dict(P=P, G=G, K=K, LIFE=LIFE, GENS=GENS, GENES=GENES, FOUNDERS=FOUNDERS.tolist(),
                               LO=LO.tolist(), HI=HI.tolist()),
                   runs=[dict(variant=v, seed=sd, history=h) for v, sd, h in out]),
              open(os.path.join(os.path.dirname(__file__), "evolve_runs.json"), "w"))
    say(f"Population {P}, lifetime {LIFE} steps, {GENS} generations, {len(seeds)} runs per variant. Founders: a, n "
        "log-uniform on [0.02, 0.5]; lam, dread (a-/a+) and rumination (m-/m+) log-uniform on [1/3, 3], centred on the")
    say("canonical 1. Final: the last generation's members over all runs, median [IQR]. Selection gradient: lifetime")
    say("payoff (x1000) per s.d. of each log gene within generation: the mean and s.e. of the per-run slopes (primary),")
    say("then pooled (OLS s.e., learners treated as independent: optimistic). lam is the news loss/gain ratio.")
    for v in VARIANTS:
        runs = [h for v_, _, h in out if v_ == v]
        last = np.array([[u[k] for k in GENES] for h in runs for u in map(unpack, h[-1]["genomes"])])
        q = lambda c: f"{np.median(last[:, c]):.3f} [{np.quantile(last[:, c], .25):.3f}, {np.quantile(last[:, c], .75):.3f}]"  # noqa: E731
        beta, se, per = gradients(runs)
        fit0 = np.mean([np.mean(h[0]["fit"]) for h in runs])
        fit1 = np.mean([np.mean(h[-1]["fit"]) for h in runs])
        say(f"[{v}] lifetime payoff {fit0:.3f} -> {fit1:.3f}; final " + "  ".join(f"{k} {q(c)}" for c, k in enumerate(GENES)))
        say("    selection gradient, per run, mean (s.e.): " + ", ".join(
            f"{k} {per[:, c].mean():+.2f} ({per[:, c].std(ddof=1) / np.sqrt(len(per)):.2f})" for c, k in enumerate(GENES)))
        say("    pooled:                                   " + ", ".join(
            f"{k} {beta[c]:+.2f} ({se[c]:.2f})" for c, k in enumerate(GENES)))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, len(GENES), figsize=(4 * len(GENES), 3.6))
    cols = {"felt critic": "#2a9d8f", "felt agents": "#e76f51", "neutral": "#7f7f7f"}
    for v in VARIANTS:
        for i, h in enumerate([h for v_, _, h in out if v_ == v]):
            med = np.exp(np.array([np.median(np.array(x["genomes"]), 0) for x in h]))
            for c in range(len(GENES)):
                axes[c].plot(np.arange(1, GENS + 1), med[:, c], color=cols[v], alpha=0.6, label=v if i == 0 else None)
    titles = ("anticipation a", "news n", "news loss/gain lam", "dread a-/a+", "rumination m-/m+")
    for c, name in enumerate(titles):
        axes[c].set_title(f"population median: {name}", fontsize=10)
        axes[c].set_xlabel("generation")
        axes[c].set_yscale("log")
        if c >= 2:
            axes[c].axhline(1.0, color="#333", lw=0.8, ls=":")
    axes[0].legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(__file__), "evolve.png"), dpi=120)
    say(f"done in {time.time() - t0:.0f}s")
    open(os.path.join(os.path.dirname(__file__), "evolve_report.txt"), "w").write("\n".join(lines) + "\n")
