"""Two channels for a critic's optimism in the hidden-game agent. Run:
python experiments/learned_expectations/run_channels.py   (writes channels_report.txt; runs in parallel)

The critic's level can reach the policy through the state they share (run_braced.py: a critic above its
targets keeps the agent complacent) or through the decision rule, when the critic is the policy's baseline:
an advantage computed against a high baseline marks every sampled move as worse than expected. Here the
critic forecasts undiscounted payoffs-to-go, the quantity the policy's returns use, held at a constant bias
(0, +1.5 or -1.5) by a TD offset. Channels: shared state only (batch-mean baseline), decision rule only
(critic baseline, critic detached from the state), and both."""
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from repeated import FEEL, rollout, train  # noqa: E402
from run_braced import evaluate, games  # noqa: E402

SEEDS = range(int(os.environ.get("SEEDS", "6")))
UNDISCOUNTED = dict(FEEL, nu=1.0)
LEVELS = {"honest": 0.0, "rosy (+1.5)": 1.5, "braced (-1.5)": -1.5}
CHANNELS = {"shared state": dict(baseline="batch"), "decision rule": dict(baseline="critic", detach=True),
            "both": dict(baseline="critic")}


def one(job):
    channel, level, seed = job
    torch.set_num_threads(int(os.environ.get("THREADS", "3")))
    A, Bm = games(4096, 4242)
    curve = []

    def monitor(it, agent):
        with torch.no_grad():
            curve.append(float(rollout(agent, A, Bm, 10, torch.Generator().manual_seed(1))[0]["r"][:, -3:].mean()))

    off = [0.0] * 9 + [LEVELS[level]]                     # b_k = o_k + b_{k+1}: a constant bias at every round
    agent = train("payoff", "offset", seed=seed, feel=UNDISCOUNTED, offset=off, monitor=monitor, **CHANNELS[channel])
    monitor(3000, agent)
    return channel, level, dict(evaluate(agent, nu=1.0), curve=curve)


if __name__ == "__main__":
    t0, lines = time.time(), []
    say = lambda s: (print(s, flush=True), lines.append(s))
    jobs = [(c, lv, s) for s in SEEDS for c in CHANNELS for lv in LEVELS]
    with ProcessPoolExecutor(int(os.environ.get("PROCS", "6"))) as ex:
        out = list(ex.map(one, jobs))
    steps = np.arange(0, 3001, 250)
    say(f"Policy ascends payoffs; critic on undiscounted payoffs-to-go; {len(SEEDS)} seeds. Escaped: late payoff")
    say("above 0.26; escape step: first evaluation above 0.25. Shift: switch rate after a round-1 loss / gain.")
    say(f"{'channel':15s} {'critic':15s} escaped  escape step      late (escaped/not)   shift bad/good   bias")
    for c in CHANNELS:
        for lv in LEVELS:
            rs = [o for c_, l_, o in out if c_ == c and l_ == lv]
            esc, stay = [o for o in rs if o["late"] > 0.26], [o for o in rs if o["late"] <= 0.26]
            when = [int(steps[np.argmax(np.array(o["curve"]) > 0.25)]) for o in rs if max(o["curve"]) > 0.25]
            m = lambda xs, k: f"{np.mean([o[k] for o in xs]):.3f}" if xs else "  -  "
            span = f"{int(np.median(when))} ({min(when)}-{max(when)})" if when else "-"
            say(f"{c:15s} {lv:15s} {len(esc):2d}/{len(rs):<2d}   {span:15s}  {m(esc, 'late')} / {m(stay, 'late')}"
                f"      {np.mean([o['shift_bad'] for o in rs]):.2f} / {np.mean([o['shift_good'] for o in rs]):.2f}"
                f"    {np.mean([o['bias'] for o in rs]):+.2f}")
    say(f"done in {time.time() - t0:.0f}s")
    open(os.path.join(os.path.dirname(__file__), "channels_report.txt"), "w").write("\n".join(lines) + "\n")
