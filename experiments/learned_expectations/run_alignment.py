"""Why a rosy critic keeps the hidden-game agent complacent: value and staying share a direction. Run:
python experiments/learned_expectations/run_alignment.py   (writes alignment_report.txt)

For honest agents at early checkpoints, on the same rollouts: the cosine between the GRU-parameter gradients of
the mean stay logit (repeat my previous move) and of the mean critic value, rounds 2-10; and the change in the
round-2 stay logit after one normalized step that raises the critic's value (the push a critic held above its
targets puts on the shared state), split by the sign of the round-1 payoff."""
import os
import sys

import torch

sys.path.insert(0, os.path.dirname(__file__))
from rounds import Hidden, rollout, train  # noqa: E402


def stay_logit(rec):
    pi = rec["pi"].clamp(1e-12, 1 - 1e-12)
    logit = torch.log(pi) - torch.log(1 - pi)                                            # logit of move 0
    prev1 = (rec["logp"][:, :-1] - torch.log(pi[:, :-1])).abs() > 1e-9                   # previous move was 1
    return torch.where(prev1, -logit[:, 1:], logit[:, 1:])


if __name__ == "__main__":
    lines = []
    say = lambda s: (print(s, flush=True), lines.append(s))
    gen = torch.Generator().manual_seed(99)
    G = 4096
    A, Bm = torch.rand(G, 2, 2, generator=gen) * 2 - 1, torch.rand(G, 2, 2, generator=gen) * 2 - 1
    say("seed  step   cos(grad stay, grad value)   raise value -> round-2 stay logit, after loss / after gain")
    for seed in range(4):
        for steps in (0, 150, 300, 500):
            agent = train("payoff", "honest", steps=steps, seed=seed)
            gru = list(agent.trunks["state"].parameters())
            rec = rollout(agent, Hidden(A, Bm), 10, torch.Generator().manual_seed(5))[0]
            stay = stay_logit(rec)
            gs = torch.autograd.grad(stay.mean(), gru, retain_graph=True)
            gc = torch.autograd.grad(rec["C"][:, 1:].mean(), gru)
            norm = lambda g: torch.sqrt(sum((x * x).sum() for x in g))
            cos = sum((a * b).sum() for a, b in zip(gs, gc)) / (norm(gs) * norm(gc))
            with torch.no_grad():
                for p, g in zip(gru, gc):
                    p += 0.05 * g / norm(gc)
                d = (stay_logit(rollout(agent, Hidden(A, Bm), 10, torch.Generator().manual_seed(5))[0]) - stay)[:, 0]
            r0 = rec["r"][:, 0]
            say(f"{seed:4d}  {steps:4d}   {float(cos):+.3f}                        "
                f"{float(d[r0 < 0].mean()):+.4f} / {float(d[r0 >= 0].mean()):+.4f}")
    open(os.path.join(os.path.dirname(__file__), "alignment_report.txt"), "w").write("\n".join(lines) + "\n")
