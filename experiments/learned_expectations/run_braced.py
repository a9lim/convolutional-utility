"""What the critic's level does to the hidden-game agent. Run:
python experiments/learned_expectations/run_braced.py   (writes braced_report.txt, braced.png; runs in parallel)

Learning first finds a complacent policy (switch only after quite bad payoffs; about 0.20 per round late),
then may escape to win-stay, lose-shift at zero, which explores the game (about 0.31). The policy ascends
payoffs throughout, so the critic acts only through the state it shares with the policy. Critics differ in
level: rosy or braced (felt objective, offsets, expectiles), forecasting felt utility (canonical), or honest
about rewards shifted by a constant that the state does not see and the policy's baseline removes (so only
the critic's level moves). Per critic: how many seeds escape and when, the play that separates the basins,
and the critic's level against realized payoffs, overall and just after bad or good news."""
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from repeated import FEEL, rollout, train  # noqa: E402

HERE = os.path.dirname(__file__)
K = 10
BRACED, ROSY = dict(FEEL, a=0.05), dict(FEEL, a=0.3)


def offsets(bias):
    """Per-round TD offsets that hold the critic at a given bias profile (b_k = o_k + nu b_{k+1})."""
    return [b - FEEL["nu"] * (bias[k + 1] if k + 1 < len(bias) else 0.0) for k, b in enumerate(bias)]


ROSY_PROFILE = offsets([-0.09, 1.81, 2.19, 2.19, 2.09, 1.96, 1.74, 1.43, 1.08, 0.63])
CRITICS = {                                                       # name: (training keywords, seeds)
    "honest": (dict(critic="honest"), 8),
    "motivated, braced (a = 0.05)": (dict(critic="motivated", feel=BRACED), 8),
    "motivated, braced, lam = 1": (dict(critic="motivated", feel=dict(BRACED, lam=1.0)), 4),
    "motivated, rosy (a = 0.3)": (dict(critic="motivated", feel=ROSY), 8),
    "offset, braced profile": (dict(critic="offset", offset=offsets(
        [-2.43, -1.16, -0.63, -0.45, -0.40, -0.34, -0.31, -0.27, -0.24, -0.17])), 4),
    "offset, deep (-0.5 a round)": (dict(critic="offset", offset=[-1.5] + [-0.5] * 9), 4),
    "offset, mild (+0.1 a round)": (dict(critic="offset", offset=[-1.5] + [0.1] * 9), 4),
    "offset, rosy profile": (dict(critic="offset", offset=ROSY_PROFILE), 4),
    "expectile 0.1": (dict(critic="expectile", expectile=0.1), 4),
    "expectile 0.9": (dict(critic="expectile", expectile=0.9), 4),
    "canonical (a = 0.05)": (dict(critic="canonical", feel=BRACED), 8),
    "canonical, lam = 1": (dict(critic="canonical", feel=dict(BRACED, lam=1.0)), 4),
    "honest, rewards +0.5": (dict(critic="honest", reward_shift=0.5), 6),
    "honest, rewards -0.5": (dict(critic="honest", reward_shift=-0.5), 6),
    "honest, detached": (dict(critic="honest", detach=True), 4),
    "offset, rosy profile, detached": (dict(critic="offset", offset=ROSY_PROFILE, detach=True), 4),
}


def games(G, seed):
    gen = torch.Generator().manual_seed(seed)
    return torch.rand(G, 2, 2, generator=gen) * 2 - 1, torch.rand(G, 2, 2, generator=gen) * 2 - 1


def evaluate(agent, nu=FEEL["nu"]):
    G = 20000
    A, Bm = games(G, 4242)
    with torch.no_grad():
        rec = rollout(agent, A, Bm, K, torch.Generator().manual_seed(1))
    R = rec[0]
    r, C, pi = R["r"], R["C"], R["pi"]
    move = (R["logp"] - torch.log(pi.clamp_min(1e-12))).abs() > 1e-9                    # True: played move 1
    disc, acc = torch.zeros_like(r), torch.zeros(G)
    for k in reversed(range(K)):
        acc = r[:, k] + nu * acc
        disc[:, k] = acc
    bias = C - disc
    delta = r + nu * torch.cat([C[:, 1:], torch.zeros(G, 1)], 1) - C
    bad = delta[:, :-1] < 0
    sw = move[:, 1] != move[:, 0]
    return dict(late=float(r[:, -3:].mean()), shift_bad=float(sw[r[:, 0] < 0].float().mean()),
                shift_good=float(sw[r[:, 0] >= 0].float().mean()), bias=float(bias[:, 1:].mean()),
                after_bad=float(bias[:, 1:][bad].mean()), after_good=float(bias[:, 1:][~bad].mean()))


def one(job):
    name, seed = job
    torch.set_num_threads(int(os.environ.get("THREADS", "3")))
    A, Bm = games(4096, 4242)
    curve = []

    def monitor(it, agent):
        with torch.no_grad():
            curve.append(float(rollout(agent, A, Bm, K, torch.Generator().manual_seed(1))[0]["r"][:, -3:].mean()))

    agent = train("payoff", seed=seed, monitor=monitor, **CRITICS[name][0])
    monitor(3000, agent)
    return name, seed, dict(evaluate(agent), curve=curve)


if __name__ == "__main__":
    t0, lines = time.time(), []
    say = lambda s: (print(s, flush=True), lines.append(s))
    jobs = [(name, s) for name, (_, n) in CRITICS.items() for s in range(n)]
    with ProcessPoolExecutor(int(os.environ.get("PROCS", "6"))) as ex:
        out = list(ex.map(one, jobs))
    res = {name: [o for n, _, o in out if n == name] for name in CRITICS}
    steps = np.arange(0, 3001, 250)
    say("Policy ascends payoffs. Escaped: late payoff above 0.26; escape step: first evaluation (every 250 steps)")
    say("above 0.25. Shift after round 1: switch rate after a negative / positive payoff. Bias: critic minus")
    say("realized discounted payoff-to-go, rounds 2-10, overall and just after a negative / positive TD error.")
    say(f"{'critic':31s} escaped  escape step   late (escaped/not)   shift bad/good   bias   after bad/good")
    for name, rs in res.items():
        esc = [o for o in rs if o["late"] > 0.26]
        stay = [o for o in rs if o["late"] <= 0.26]
        when = [int(steps[np.argmax(np.array(o["curve"]) > 0.25)]) for o in rs if max(o["curve"]) > 0.25]
        m = lambda xs, k: f"{np.mean([o[k] for o in xs]):.3f}" if xs else "  -  "
        say(f"{name:31s} {len(esc):2d}/{len(rs):<2d}   {f'{int(np.median(when))}' if when else '-':>6s} "
            f"({min(when) if when else '-'}-{max(when) if when else '-'})   {m(esc, 'late')} / {m(stay, 'late')}"
            f"      {np.mean([o['shift_bad'] for o in rs]):.2f} / {np.mean([o['shift_good'] for o in rs]):.2f}"
            f"    {np.mean([o['bias'] for o in rs]):+.2f}   "
            f"{np.mean([o['after_bad'] for o in rs]):+.2f} / {np.mean([o['after_good'] for o in rs]):+.2f}")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
    for j, (name, rs) in enumerate(res.items()):
        col = plt.cm.tab20(j / len(res))
        for i, o in enumerate(rs):
            axes[0].plot(steps, o["curve"], color=col, lw=0.8, alpha=0.7, label=name if i == 0 else None)
        axes[1].scatter([o["bias"] for o in rs], [o["late"] for o in rs], s=22, alpha=0.8, color=col, label=name)
    axes[0].set_xlabel("training step")
    axes[0].set_ylabel("late-round payoff (held-out games)")
    axes[0].set_title("Escaping the complacent plateau", fontsize=10)
    axes[1].axvline(0, color="#aaa", lw=0.8)
    axes[1].set_xlabel("critic level, forecast minus realized payoff-to-go (rounds 2-10)")
    axes[1].set_ylabel("late-round payoff")
    axes[1].set_title("A high critic keeps the agent on the plateau, biased or not", fontsize=10)
    axes[1].legend(fontsize=6, frameon=False, loc="lower left")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "braced.png"), dpi=130)
    say(f"done in {time.time() - t0:.0f}s")
    open(os.path.join(HERE, "braced_report.txt"), "w").write("\n".join(lines) + "\n")
