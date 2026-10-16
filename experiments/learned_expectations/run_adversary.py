"""Unknown adversaries (adversary.py). Run:
python experiments/learned_expectations/run_adversary.py   (writes adversary_report.txt, adversary.png; parallel)

Variants: selfish, twin and altruist (w = 1) on the fixed and geometric horizons; selfish on the uniform horizon;
on the geometric horizon, rosy and braced motivated critics, and the batch baseline in place of groups. Four
seeds each. Per agent and partner: payoff per live round, cooperation by family, prisoner's-dilemma cooperation by
round and by rounds to go; a probe for the partner's identity on the state; then cross-play among the final agents
of each horizon (each against frozen agents of other seeds)."""
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from adversary import CAPS, HELD_OUT, POOL, crossplay, episodes, evaluate, train  # noqa: E402
from agents import Agent  # noqa: E402
from rounds import iterated_layout  # noqa: E402

HERE = os.path.dirname(__file__)
SEEDS = range(int(os.environ.get("SEEDS", "4")))
STEPS = int(os.environ.get("STEPS", "3000"))
VARIANTS = {f"{o}, {h}": dict(objective=o, horizon=h) for h in ("fixed", "geometric") for o in ("selfish", "twin", "altruist")}
VARIANTS.update({"selfish, uniform": dict(objective="selfish", horizon="uniform"),
                 "selfish, geometric, rosy critic": dict(objective="selfish", horizon="geometric", critic="rosy"),
                 "selfish, geometric, braced critic": dict(objective="selfish", horizon="geometric", critic="braced"),
                 "selfish, geometric, batch baseline": dict(objective="selfish", horizon="geometric", estimator="batch")})
CURVE = ("copy", "always defect", "tit for tat", "latest past self")


def one(job):
    name, seed = job
    torch.set_num_threads(int(os.environ.get("THREADS", "1")))
    kw = VARIANTS[name]
    curve = []

    def monitor(it, agent, league):
        g, row = torch.Generator().manual_seed(5), []
        with torch.no_grad():
            for p in (None, POOL["always defect"], POOL["tit for tat"], league[-1]):
                R = episodes(agent, p, 1024, kw["horizon"], g)[0]
                pd = (R["fam"] == 0).double() * R["mask"]
                row.append(float((R["coop"] * pd).sum() / pd.sum()))
        curve.append(row)

    agent, league = train(seed=seed, steps=STEPS, monitor=monitor, **kw)
    return name, seed, dict(evaluate(agent, league, kw["horizon"], STEPS), curve=curve, state=agent.state_dict())


def rebuild(state, horizon):
    agent = Agent(**iterated_layout())
    agent.register_buffer("level", torch.zeros(CAPS[horizon]))
    agent.load_state_dict(state)
    return agent


if __name__ == "__main__":
    t0, lines = time.time(), []
    say = lambda s: (print(s, flush=True), lines.append(s))  # noqa: E731
    jobs = [(n, s) for n in VARIANTS for s in SEEDS]
    with ProcessPoolExecutor(int(os.environ.get("PROCS", "16"))) as ex:
        out = list(ex.map(one, jobs))
    res = {n: [o for n_, _, o in out if n_ == n] for n in VARIANTS}
    names = res[next(iter(VARIANTS))][0]["names"]
    say(f"{len(SEEDS)} seeds, {STEPS} steps. Cooperation = the prosocial move; PD = prisoner's dilemmas. Means over seeds, "
        "per-seed values in brackets where shown. Pool partners in training: copy, past self, "
        f"{', '.join(POOL)}; held out: {', '.join(HELD_OUT)}.")
    for n, rs in res.items():
        m = lambda f: np.mean([f(o) for o in rs], 0)  # noqa: E731
        say(f"[{n}]")
        for p in names:
            pd = [o["partners"][p]["coop"][0] for o in rs]
            say(f"    vs {p:30s} PD {np.mean(pd):.2f} [{' '.join(f'{x:.2f}' for x in pd)}]  stag "
                f"{m(lambda o: o['partners'][p]['coop'][2]):.2f}  chicken {m(lambda o: o['partners'][p]['coop'][1]):.2f}  "
                f"payoff {m(lambda o: o['partners'][p]['pay']):+.3f}")
        for p in ("copy", "always defect", "tit for tat", "past self, 500 steps back"):
            say(f"    PD by round vs {p:26s} " + " ".join(f"{x:.2f}" for x in m(lambda o: o["partners"][p]["pd_round"]))
                + " | by rounds to go 4..0: " + " ".join(f"{x:.2f}" for x in m(lambda o: o["partners"][p]["pd_togo"])[::-1]))
        say("    partner identity from the state after 1/2/3/5 rounds (balanced accuracy, chance 0.10): "
            + " ".join(f"{m(lambda o: o['probe'][k]):.2f}" for k in (1, 2, 3, 5)))
    for horizon in ("fixed", "geometric"):
        objs = ("selfish", "twin", "altruist")
        agents = {o: [rebuild(r["state"], horizon) for r in res[f"{o}, {horizon}"]] for o in objs}
        say(f"cross-play, {horizon} horizon: row agent against a frozen column agent of another seed; PD cooperation / "
            "payoff of the row agent (self-play: against its own copy)")
        for a in objs:
            cells = []
            for b in objs:
                pairs = [crossplay(x, y, horizon) for i, x in enumerate(agents[a]) for j, y in enumerate(agents[b]) if i != j]
                cells.append(f"{b} {np.mean([c for _, c in pairs]):.2f} / {np.mean([p for p, _ in pairs]):+.3f}")
            own = [res[f"{a}, {horizon}"][i]["partners"]["copy"] for i in range(len(agents[a]))]
            say(f"    {a:9s} " + "   ".join(cells) + f"   self-play {np.mean([o['coop'][0] for o in own]):.2f} / "
                f"{np.mean([o['pay'] for o in own]):+.3f}")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(17, 4.4))
    show = ["copy", "past self, 500 steps back", "past self, 1500 steps back"] + list(POOL) + list(HELD_OUT)
    x = np.arange(len(show))
    for j, o in enumerate(("selfish", "twin", "altruist")):
        rs = res[f"{o}, geometric"]
        axes[0].bar(x + (j - 1) * 0.27, [np.mean([r["partners"][p]["coop"][0] for r in rs]) for p in show], 0.27, label=o)
        c = np.mean([r["curve"] for r in rs], 0)
        steps = 250 * np.arange(len(c))
        axes[1].plot(steps, c[:, 0], "-", color=f"C{j}", label=f"{o}: copy")
        axes[1].plot(steps, c[:, 3], "--", color=f"C{j}", label=f"{o}: latest past self")
    axes[0].set_xticks(x, show, rotation=60, ha="right", fontsize=7)
    axes[0].set_ylabel("PD cooperation")
    axes[0].set_title("Geometric horizon: PD cooperation by partner", fontsize=10)
    axes[0].legend(fontsize=8, frameon=False)
    axes[1].set_xlabel("training step")
    axes[1].set_title("PD cooperation with copies and past selves in training", fontsize=10)
    axes[1].legend(fontsize=7, frameon=False)
    for h, col in (("fixed", "C0"), ("geometric", "C1"), ("uniform", "C2")):
        rs = res[f"selfish, {h}"]
        axes[2].plot(range(5), np.mean([r["partners"]["tit for tat"]["pd_togo"] for r in rs], 0), "o-", color=col, label=h)
    axes[2].invert_xaxis()
    axes[2].set_xlabel("rounds to go (0 = the episode's last)")
    axes[2].set_ylabel("PD cooperation against tit for tat")
    axes[2].set_title("The end game by horizon (selfish)", fontsize=10)
    axes[2].legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "adversary.png"), dpi=120)
    say(f"done in {time.time() - t0:.0f}s")
    open(os.path.join(HERE, "adversary_report.txt"), "w").write("\n".join(lines) + "\n")
