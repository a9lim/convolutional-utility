"""Iterated randomized games: how does one network strategize when the game changes every round? Run:
python experiments/learned_expectations/run_iterated.py   (writes iterated_report.txt, iterated.png; parallel)

Variants: selfish learners over 10 rounds; the same over one round (no future); team learners (both players'
payoffs, the twin) over 10 rounds; selfish learners with mixed partners, trained for 3000 and for 9000 steps. Measured in self-play on fresh episodes: cooperation by family and round,
reciprocity across games (cooperation after the partner cooperated or defected in the previous round, when
that round was a different game), and play against scripted partners."""
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from iterated import FAMILIES, PARTNERS, rollout, train  # noqa: E402

HERE = os.path.dirname(__file__)
VARIANTS = {"selfish, 10 rounds": (dict(objective="selfish"), 4), "selfish, one round": (dict(objective="selfish", K=1), 2),
            "team, 10 rounds": (dict(objective="team"), 2),
            "selfish, mixed partners": (dict(objective="selfish", mixed=True), 4),
            "selfish, mixed partners, 9000 steps": (dict(objective="selfish", mixed=True, steps=9000), 4)}


def evaluate(player, K):
    gen = torch.Generator().manual_seed(77)
    G = 16384
    with torch.no_grad():
        R = rollout(player, G, gen, K=K)
    coop, fam, r = R[0]["coop"], R[0]["fam"], R[0]["r"]
    other = R[1]["coop"]
    out = dict(coop={f: float(coop[fam == f].mean()) for f in range(4)},
               joint={f: float(((r + R[1]["r"]) / 2)[fam == f].mean()) for f in range(4)},
               by_round=[float(coop[:, k].mean()) for k in range(K)],
               label0={f: float(R[0]["label0"][fam == f].mean()) for f in range(4)},
               agree={f: float((coop == other)[fam == f].float().mean()) for f in range(4)})
    if K > 1:
        prev_c, prev_f = other[:, :-1], fam[:, :-1]
        cur, cf = coop[:, 1:], fam[:, 1:]
        diff = cf != prev_f
        out["recip"] = {f: (float(cur[(cf == f) & diff & (prev_c == 1)].mean()),
                            float(cur[(cf == f) & diff & (prev_c == 0)].mean())) for f in range(4)}
        out["last"] = {f: (float(coop[:, :-1][fam[:, :-1] == f].mean()), float(coop[:, -1][fam[:, -1] == f].mean()))
                       for f in range(4)}
        out["partners"] = {}
        for name, partner in PARTNERS.items():
            with torch.no_grad():
                Rp = rollout(player, G, torch.Generator().manual_seed(78), partner=partner, K=K)
            pd = Rp[0]["fam"] == 0
            out["partners"][name] = ({f: float(Rp[0]["coop"][Rp[0]["fam"] == f].mean()) for f in range(4)},
                                     float(Rp[0]["r"].mean()),
                                     [float(Rp[0]["coop"][:, k][pd[:, k]].mean()) for k in range(K)])
    return out


def one(job):
    name, seed = job
    torch.set_num_threads(int(os.environ.get("THREADS", "3")))
    kw = VARIANTS[name][0]
    curve = []

    def monitor(it, player):
        with torch.no_grad():
            R = rollout(player, 4096, torch.Generator().manual_seed(5), K=kw.get("K", 10))
        curve.append([float(R[0]["coop"][R[0]["fam"] == f].mean()) for f in range(4)])

    player = train(seed=seed, monitor=monitor, **kw)
    monitor(kw.get("steps", 3000), player)
    return name, seed, dict(evaluate(player, kw.get("K", 10)), curve=curve)


if __name__ == "__main__":
    t0, lines = time.time(), []
    say = lambda s: (print(s, flush=True), lines.append(s))
    jobs = [(n, s) for n, (_, k) in VARIANTS.items() for s in range(k)]
    with ProcessPoolExecutor(int(os.environ.get("PROCS", "6"))) as ex:
        out = list(ex.map(one, jobs))
    fam_names = ["PD", "chicken", "stag hunt", "harmony"]
    say("Cooperation = the prosocial move (C, swerve, stag, C). Means over seeds; per-seed values in brackets.")
    for name in VARIANTS:
        rs = [o for n, _, o in out if n == name]
        m = lambda get: np.mean([get(o) for o in rs])
        say(f"[{name}] ({len(rs)} seeds)")
        say("    cooperation:   " + "  ".join(f"{fam_names[f]} {m(lambda o: o['coop'][f]):.2f} "
                                             f"[{' '.join(f'{o['coop'][f]:.2f}' for o in rs)}]" for f in range(4)))
        say("    payoff (each): " + "  ".join(f"{fam_names[f]} {m(lambda o: o['joint'][f]):+.3f}" for f in range(4)))
        say("    plays its label 0: " + "  ".join(f"{fam_names[f]} {m(lambda o: o['label0'][f]):.2f}" for f in range(4))
            + " | partners make the same move: " + "  ".join(f"{fam_names[f]} {m(lambda o: o['agree'][f]):.2f}" for f in range(4)))
        if "recip" in rs[0]:
            say("    cooperation by round: " + " ".join(f"{np.mean([o['by_round'][k] for o in rs]):.2f}" for k in range(10)))
            say("    rounds 1-9 / round 10: " + "  ".join(
                f"{fam_names[f]} {m(lambda o: o['last'][f][0]):.2f}/{m(lambda o: o['last'][f][1]):.2f}" for f in range(4)))
            say("    after the partner cooperated / defected in a different game: " + "  ".join(
                f"{fam_names[f]} {m(lambda o: o['recip'][f][0]):.2f}/{m(lambda o: o['recip'][f][1]):.2f}" for f in range(4)))
            for p in PARTNERS:
                say(f"    vs {p:16s}: cooperation " + "  ".join(
                    f"{fam_names[f]} {m(lambda o: o['partners'][p][0][f]):.2f}" for f in range(4))
                    + f"; payoff {m(lambda o: o['partners'][p][1]):+.3f}; PD cooperation by round "
                    + " ".join(f"{np.mean([o['partners'][p][2][k] for o in rs]):.2f}" for k in range(10)))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, len(VARIANTS), figsize=(16, 3.6), sharey=True)
    for ax, name in zip(axes, VARIANTS):
        for o in [o for n, _, o in out if n == name]:
            c = np.array(o["curve"])
            steps = 250 * np.arange(len(c))
            for f in range(4):
                ax.plot(steps, c[:, f], color=plt.cm.tab10(f), alpha=0.7, label=fam_names[f] if o is not None else None)
        ax.set_title(name, fontsize=10)
        ax.set_xlabel("training step")
    axes[0].set_ylabel("cooperation")
    handles, labels = axes[0].get_legend_handles_labels()
    axes[0].legend(handles[:4], labels[:4], fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "iterated.png"), dpi=120)
    say(f"done in {time.time() - t0:.0f}s")
    open(os.path.join(HERE, "iterated_report.txt"), "w").write("\n".join(lines) + "\n")
