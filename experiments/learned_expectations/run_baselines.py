"""Policy-gradient noise in the mixed-partner iterated agent, by baseline. Run:
python experiments/learned_expectations/run_baselines.py   (writes baselines_report.txt)

Checkpoints of one training run (seed 0). At each, 24 estimates of the policy gradient per estimator, each
from 2048 episodes split as in training (half self-play, half over the scripted partners):
- batch:    rewards-to-go minus their per-round batch mean (what the trainer uses);
- rloo g:   episodes in groups of g that share the exogenous context (game sequence, label flips, partner
            type) and differ only in sampled moves, baseline the leave-one-out group mean per round
            (Dr. GRPO's group mean up to a (g - 1)/g scale, with no std or length normalization);
- grpo-std: the group mean, divided by the group's std (GRPO's normalization; biased).
cos is the mean cosine with a reference (the mean of all unbiased estimates); noise is the estimates'
spread about their own mean, over the reference's squared norm.
"""
import copy
import os
import sys

import torch

sys.path.insert(0, os.path.dirname(__file__))
import iterated as it  # noqa: E402

G, M = 2048, 24
EST = [("batch", 1), ("rloo", 2), ("rloo", 4), ("rloo", 8), ("rloo", 16), ("rloo", 64), ("grpo-std", 16)]
SAMPLE = it.sample_round


def grouped(g):
    def sample(n, gen, families=(0, 1, 2, 3)):
        Mx, fam, flips = SAMPLE(n // g, gen, families)
        rep = lambda x: x.repeat_interleave(g, 0)  # noqa: E731
        return rep(Mx), rep(fam), [rep(x) for x in flips]
    return sample


def learners(player, gen, g):
    it.sample_round = grouped(g) if g > 1 else SAMPLE
    try:
        rec = it.rollout(player, G // 2, gen)
        out = [rec[0], rec[1]]
        for p in it.PARTNERS.values():
            out.append(it.rollout(player, G // (2 * len(it.PARTNERS)), gen, partner=p)[0])
    finally:
        it.sample_round = SAMPLE
    return out


def grad(player, gen, kind, g):
    loss = 0.0
    for R in learners(player, gen, g):
        ret = torch.flip(torch.cumsum(torch.flip(R["r"], [1]), 1), [1])
        if kind == "batch":
            adv = ret - ret.mean(0, keepdim=True)
        else:
            x = ret.reshape(-1, g, ret.shape[1])
            if kind == "rloo":
                adv = (x - (x.sum(1, keepdim=True) - x) / (g - 1)).reshape(ret.shape)
            else:
                adv = ((x - x.mean(1, keepdim=True)) / (x.std(1, keepdim=True) + 1e-6)).reshape(ret.shape)
        loss = loss - (R["logp"] * adv).mean()
    return torch.cat([x.flatten() for x in torch.autograd.grad(loss, list(player.parameters()))])


if __name__ == "__main__":
    torch.set_num_threads(int(os.environ.get("THREADS", "4")))
    lines = []
    say = lambda s: (print(s, flush=True), lines.append(s))  # noqa: E731
    snaps = {}

    def monitor(step, player):
        if step in (0, 500, 1500):
            snaps[step] = copy.deepcopy(player.state_dict())

    player = it.train(seed=0, mixed=True, monitor=monitor)
    snaps[3000] = copy.deepcopy(player.state_dict())
    say(f"{G} episodes per estimate, {M} estimates per estimator. cos: mean cosine with the reference gradient; "
        "noise: spread about the estimator's mean over the reference's squared norm.")
    for step, sd in sorted(snaps.items()):
        player.load_state_dict(sd)
        est = {}
        for i, (kind, g) in enumerate(EST):
            gen = torch.Generator().manual_seed(1000 * i + step)
            est[(kind, g)] = torch.stack([grad(player, gen, kind, g) for _ in range(M)])
        ref = torch.cat([v for (k, _), v in est.items() if k != "grpo-std"]).mean(0)
        row = []
        for (kind, g), v in est.items():
            cos = torch.nn.functional.cosine_similarity(v, ref[None], dim=1).mean()
            noise = ((v - v.mean(0)) ** 2).sum(1).mean() / (ref ** 2).sum()
            row.append(f"{kind}{'' if g == 1 else f' {g}'} {float(cos):.2f}/{float(noise):.1f}")
        say(f"step {step:4d}  cos/noise: " + "  ".join(row))
    open(os.path.join(os.path.dirname(__file__), "baselines_report.txt"), "w").write("\n".join(lines) + "\n")
