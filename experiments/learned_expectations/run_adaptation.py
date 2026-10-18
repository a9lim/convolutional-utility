"""The level of what reinforces, three ways: a felt reference, learning from memory, and score centering. Run:
python experiments/learned_expectations/run_adaptation.py   (writes adaptation_report.txt, adaptation_runs.json; parallel;
runs only the arms and seeds missing from adaptation_runs.json at the same configuration, FRESH=1 for all)

The hidden-game agent (run_braced.py) first finds a complacent policy, then may escape to win-stay, lose-shift.
A critic above realized payoffs keeps it complacent through the state they share (D8); that is a level effect.
- Adaptation (rounds.py `adapt`, notes/adaptation.md): a felt reference across episodes, steady level 1 / (1 + h)
  of the unadapted one (1 / (1 + d h) in the canonical solve, d about 2.07). The motivated critic ascends welfare,
  so its push is weighed by 1 / (1 + h), exactly a TD offset profile; the canonical critic forecasts adapted felt
  utility, so its level falls with h. Prediction: both escape as h grows.
- Replay (rounds.py `replay`): the policy learns from episodes 100 steps old, each once, without importance
  weights, as a mind replaying memories would; it starts learning at step 100 (the critic, and through the shared
  state the policy, trains before that), so against on-policy arms the schedule differs too. Off-policy the advantage's level
  enters the expected update times a pull toward the old policy (Marek & Ryabinin 2026): a positive level should
  drag the policy toward its past self, a negative one push it away (a prediction, not a consequence: the weights
  are levels conditional on each history). The critic is honest with its level outside the network, and shifts of
  +-0.5 go to the policy's rewards only, so the critic's objective is the same in every arm (the level kept outside
  is a mitigation of the state channel, not an exact knockout).
  Controls: the batch baseline (removes a constant shift, not the level's variation across histories), score
  centering (removes the pull, keeps the covariance under the stale sampler), and the anchor: unshifted replay plus
  only the analytic pull a shift of +-0.5 would add, c (K - k) grad sum_v q_v log p_v, without its sampling noise
  (Codex). If the anchor reproduces the shift, the pull toward the past self is sufficient.
- Felt replay: a policy reinforced by felt utility itself, no baseline (the hedonic learner), learning from
  memory; adaptation as its only centering.
Policy ascends payoffs unless marked felt; canonical model (lam = 1) throughout. Per arm: seeds escaped and when,
late payoff, the critic's level against realized payoffs, and for replay the replayed advantage level, the RMS gap
between the old and current move probabilities, and the drift part's share of the move-logit update."""
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from felt import ROUNDS  # noqa: E402
from rounds import Hidden, rollout, train  # noqa: E402
from run_braced import evaluate, games  # noqa: E402

HERE = os.path.dirname(__file__)
K, LAG = 10, 100
ROSY, CANON = dict(ROUNDS, a=0.3), dict(ROUNDS, a=0.05)
OUT = dict(critic="honest", center=True)                                     # level outside: no state channel
REPLAY = dict(replay=dict(lag=LAG))
CENTERED = dict(replay=dict(lag=LAG, center=True))


ARMS = {                                                              # name: (group, training keywords, seeds)
    "motivated, rosy": ("adaptation", dict(critic="motivated", feel=ROSY), 6),
    "motivated, rosy, h = 1": ("adaptation", dict(critic="motivated", feel=ROSY, adapt=dict(h=1.0)), 6),
    "motivated, rosy, h = 3": ("adaptation", dict(critic="motivated", feel=ROSY, adapt=dict(h=3.0)), 6),
    "motivated, rosy, h = 9": ("adaptation", dict(critic="motivated", feel=ROSY, adapt=dict(h=9.0)), 6),
    "canonical": ("adaptation", dict(critic="canonical", feel=CANON), 6),
    "canonical, h = 1": ("adaptation", dict(critic="canonical", feel=CANON, adapt=dict(h=1.0)), 6),
    "canonical, h = 3": ("adaptation", dict(critic="canonical", feel=CANON, adapt=dict(h=3.0)), 6),
    "canonical, no memory": ("adaptation", dict(critic="canonical", feel=dict(CANON, m=0.0)), 6),
    "canonical, no memory, h = 3": ("adaptation", dict(critic="canonical", feel=dict(CANON, m=0.0), adapt=dict(h=3.0)), 6),
    "canonical, no news": ("adaptation", dict(critic="canonical", feel=dict(CANON, n=0.0)), 6),
    "canonical, no news, h = 3": ("adaptation", dict(critic="canonical", feel=dict(CANON, n=0.0), adapt=dict(h=3.0)), 6),
    "on-policy, no baseline": ("replay", dict(OUT, baseline="none"), 4),
    "on-policy, no baseline, actor +0.5": ("replay", dict(OUT, baseline="none", actor_shift=0.5), 4),
    "on-policy, no baseline, actor -0.5": ("replay", dict(OUT, baseline="none", actor_shift=-0.5), 4),
    "replay, batch baseline": ("replay", dict(OUT, **REPLAY), 4),
    "replay, no baseline": ("replay", dict(OUT, baseline="none", **REPLAY), 4),
    "replay, no baseline, centered": ("replay", dict(OUT, baseline="none", **CENTERED), 4),
    "replay, actor +0.5": ("replay", dict(OUT, baseline="none", actor_shift=0.5, **REPLAY), 4),
    "replay, actor +0.5, centered": ("replay", dict(OUT, baseline="none", actor_shift=0.5, **CENTERED), 4),
    "replay, actor -0.5": ("replay", dict(OUT, baseline="none", actor_shift=-0.5, **REPLAY), 4),
    "replay, actor -0.5, centered": ("replay", dict(OUT, baseline="none", actor_shift=-0.5, **CENTERED), 4),
    "replay, anchor +0.5": ("replay", dict(OUT, baseline="none", replay=dict(lag=LAG, anchor=0.5)), 4),
    "replay, anchor -0.5": ("replay", dict(OUT, baseline="none", replay=dict(lag=LAG, anchor=-0.5)), 4),
    "felt, on-policy, no baseline": ("felt", dict(OUT, reward="felt", baseline="none"), 4),
    "felt, replay, no baseline": ("felt", dict(OUT, reward="felt", baseline="none", **REPLAY), 4),
    "felt, replay, no baseline, h = 3": ("felt", dict(OUT, reward="felt", baseline="none", adapt=dict(h=3.0), **REPLAY), 4),
    "felt, replay, no baseline, centered": ("felt", dict(OUT, reward="felt", baseline="none", **CENTERED), 4),
}


STEPS = int(os.environ.get("STEPS", "3000"))


def one(job):
    name, seed = job
    torch.set_num_threads(int(os.environ.get("THREADS", "2")))
    A, Bm = games(4096, 4242)
    curve, log = [], {}

    def monitor(it, agent):
        with torch.no_grad():
            curve.append(float(rollout(agent, Hidden(A, Bm), K, torch.Generator().manual_seed(1))[0]["r"][:, -3:].mean()))

    kw = dict(ARMS[name][1])
    reward = kw.pop("reward", "payoff")
    agent = train(reward, seed=seed, monitor=monitor, log=log if "replay" in kw else None, steps=STEPS, **kw)
    monitor(STEPS, agent)
    steps = log.get("steps", [])
    windows = [[*np.mean(steps[i:i + 250], 0).tolist(), len(steps[i:i + 250])] for i in range(0, len(steps), 250)]
    return name, seed, dict(evaluate(agent, kw.get("feel", ROUNDS)["nu"]), curve=curve, replay=windows,
                            checks=log.get("checks", []), ref=float(agent.ref))


if __name__ == "__main__":
    t0, lines = time.time(), []
    say = lambda s: (print(s, flush=True), lines.append(s))  # noqa: E731
    path = os.path.join(HERE, "adaptation_runs.json")
    config = dict(LAG=LAG, STEPS=STEPS, ROSY=ROSY, CANON=CANON)
    done = {}                                    # runs kept from an earlier invocation of this same configuration
    if os.path.exists(path) and not os.environ.get("FRESH"):
        old = json.load(open(path))
        if old["config"] == json.loads(json.dumps(config)):
            done = {(n, i): o for n, a in old["arms"].items() if n in ARMS for i, o in enumerate(a["seeds"])}
    jobs = [(name, s) for name, (_, _, n) in ARMS.items() for s in range(n) if (name, s) not in done]
    jobs.sort(key=lambda j: "replay" not in ARMS[j[0]][1])                     # the slow ones first
    with ProcessPoolExecutor(int(os.environ.get("PROCS", "9"))) as ex:
        done.update({(n, s): o for n, s, o in ex.map(one, jobs)})
    res = {name: [done[(name, s)] for s in range(n)] for name, (_, _, n) in ARMS.items()}
    json.dump(dict(config=config, arms={n: dict(group=g, seeds=res[n]) for n, (g, _, _) in ARMS.items()}),
              open(path, "w"))
    evals = np.array(list(range(0, STEPS, 250)) + [STEPS])
    say(f"{STEPS} steps. Escaped: late payoff above 0.26; escape step: first evaluation (every 250 steps) above 0.25.")
    say("Level: critic minus realized payoff-to-go at its own discount, rounds 2-10. Adaptation: the reference r at")
    say(f"the end. Replay (lag {LAG}, learning from step {LAG}), means over learning: the replayed advantage's mean,")
    say("the RMS gap |q - p| between old and current move probabilities, and the sample logit-correction RMS over")
    say("the raw-score RMS, |A (q - p)| / |A (y - p)| (first 500 steps of learning in brackets). Parameter space, at")
    say("checkpoints every 250 steps, over the weights the policy reads: the correction score centering removes,")
    say("mean[A grad sum_v q_v log p_v], as a share of the raw ascent direction's norm, and its cosine with the way back")
    say("to the weights that played the batch (positive: that component pulls toward the past self). On-policy arms")
    say(f"learn from step 0; replay arms from step {LAG} (the critic trains alone before), each batch once.")
    group = None
    for name, rs in res.items():
        if ARMS[name][0] != group:
            group = ARMS[name][0]
            say(f"\n[{group}]")
            say(f"{'arm':38s} escaped  escape step    late (escaped/not)  level  " + (
                " A mean        |q - p|       correction RMS   |corr|/|raw|  cos back" if group != "adaptation"
                else "reference r"))
        esc = [o for o in rs if o["late"] > 0.26]
        stay = [o for o in rs if o["late"] <= 0.26]
        when = [int(evals[np.argmax(np.array(o["curve"]) > 0.25)]) for o in rs if max(o["curve"]) > 0.25]
        m = lambda xs, k: f"{np.mean([o[k] for o in xs]):.3f}" if xs else "  -  "  # noqa: E731
        row = (f"{name:38s} {len(esc):2d}/{len(rs):<2d}   {f'{int(np.median(when))}' if when else '-':>5s} "
               f"({min(when) if when else '-'}-{max(when) if when else '-'})").ljust(67) + (
               f"{m(esc, 'late')} / {m(stay, 'late')}  {np.mean([o['bias'] for o in rs]):+.2f}  ")
        if rs[0]["replay"]:
            w = np.array([o["replay"] for o in rs])                        # seeds x windows x (mean, gap, share, n)
            c = [ch for o in rs for ch in o["checks"]]
            avg = lambda j, s: float((w[:, s, j] * w[:, s, 3]).sum() / w[:, s, 3].sum())  # noqa: E731
            row += "  ".join(f"{avg(j, slice(None)):+.3f} [{avg(j, slice(0, 2)):+.3f}]" for j in range(3)) + (
                f"   {np.mean([ch['correction'] / ch['raw'] for ch in c]):.2f}       {np.mean([ch['cos_back'] for ch in c]):+.2f}")
        elif group == "adaptation":
            row += f"{np.mean([o['ref'] for o in rs]):+.3f}"
        say(row)
    say(f"done in {time.time() - t0:.0f}s ({len(jobs)} runs this invocation)")
    open(os.path.join(HERE, "adaptation_report.txt"), "w").write("\n".join(lines) + "\n")
