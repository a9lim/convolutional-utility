"""Twins, altruists and felt empathizers with a similarity signal. Run:
python experiments/learned_expectations/run_partners.py   (writes partners_report.txt, partners.png; parallel)

Each variant trains a population of 4 networks (2 populations per variant) on random symmetric games, half
the objective against copies and half against other networks (sigma = 0.5 unless stated), or against
"snapshot strangers": a detached copy of the network itself, which plays its policy exactly but carries no
dependence, so the bit carries no information about how the partner plays. The noisy bit gates the gradient
on true identity, a selection experiment rather than inferred dependence. Evaluated on
prisoner's dilemmas and stag hunts (run_twin.py's families): cooperation (move 0) when the bit says copy and
when it says other, against the local stability of all-cooperate and all-defect computed from the same
objective (partners.slopes)."""
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from partners import slopes, train  # noqa: E402
from run_twin import symmetric_family  # noqa: E402

HERE = os.path.dirname(__file__)
VARIANTS = {
    "causal": dict(),
    "twin 1": dict(wT=1.0),
    "twin 0.5": dict(wT=0.5),
    "altruist 1": dict(wE=1.0),
    "altruist 0.5": dict(wE=0.5),
    "twin 1, no signal": dict(wT=1.0, signal=False),
    "altruist 0.5, no signal": dict(wE=0.5, signal=False),
    "twin 1, no signal, sigma 0.25": dict(wT=1.0, signal=False, sigma=0.25),
    "altruist 0.25, no signal": dict(wE=0.25, signal=False),
    "twin 1, noisy bit (eps 0.2)": dict(wT=1.0, eps=0.2),
    "twin 1, snapshot strangers": dict(wT=1.0, strangers="self"),
    "altruist 1, snapshot strangers": dict(wE=1.0, strangers="self"),
    "twin 1, no signal, snapshot strangers": dict(wT=1.0, signal=False, strangers="self"),
    "felt": dict(felt=True),
    "felt twin 0.5": dict(felt=True, wT=0.5),
    "felt empathy 0.5, J 0": dict(felt=True, wE=0.5, J=0.0),
    "felt empathy 0.5, J 1": dict(felt=True, wE=0.5, J=1.0),
    "felt empathy 0.25, J 0": dict(felt=True, wE=0.25, J=0.0),
    "felt empathy 0.25, J 1": dict(felt=True, wE=0.25, J=1.0),
    "felt twin 0.5, snapshot strangers": dict(felt=True, wT=0.5, strangers="self"),
    "felt empathy 0.5, J 1, snapshot strangers": dict(felt=True, wE=0.5, J=1.0, strangers="self"),
}
SEEDS = 2
DIALS = ("wT", "wE", "J")
D = 1e-3


def families():
    gen = torch.Generator().manual_seed(7)
    return {k: symmetric_family(k, 4000, gen)[0] for k in ("PD", "stag hunt")}


def classes(sl):
    """Local stability: all-cooperate stable if the slope at p = 1 is positive, all-defect if negative at 0."""
    c, d = sl[1] > 0, sl[0] < 0
    return {"C only": c & ~d, "D only": d & ~c, "both": c & d, "neither": ~c & ~d}


def one(job):
    name, seed = job
    torch.set_num_threads(int(os.environ.get("THREADS", "2")))
    kw = dict(VARIANTS[name])
    nets, F = train(seed=seed, steps=int(os.environ.get("STEPS", "4000")), **kw)
    sigma, signal = kw.get("sigma", 0.5), kw.get("signal", True)
    dials = {k: kw[k] for k in DIALS if k in kw}
    out = {}
    for fam, A in families().items():
        (m, t) = (A, A.transpose(1, 2))
        sl = {at: slopes(A, F, sigma, dials, at) for at in (D, 1 - D)}
        res = {}
        for bit, key in ((1.0, "copy"), (0.0, "other")):
            if not signal and bit == 1.0:
                continue
            with torch.no_grad():
                pc = torch.stack([n(m, t, torch.full((len(A),), bit if signal else 0.0)) for n in nets])  # (K, G)
            ref = key if signal else "mixed"
            cl = classes({0: sl[D][ref], 1: sl[1 - D][ref]})
            res["copy" if bit == 1.0 and signal else ("other" if signal else "no signal")] = dict(
                coop=[float(x) for x in pc.mean(1)],
                cls={k: (float(v.double().mean()), float(pc[:, v].mean()) if v.any() else float("nan"))
                     for k, v in cl.items()})
        out[fam] = res
    return name, seed, out


if __name__ == "__main__":
    t0, lines = time.time(), []
    say = lambda s: (print(s, flush=True), lines.append(s))
    jobs = [(n, s) for n in VARIANTS for s in range(SEEDS)]
    with ProcessPoolExecutor(int(os.environ.get("PROCS", "8"))) as ex:
        out = list(ex.map(one, jobs))
    say("P(cooperate) by what the bit says, mean over 2 populations x 4 networks [per-population means]. Local "
        "stability classes from the objective's slope at all-cooperate / all-defect: share of games, learned "
        "P(cooperate) in them.")
    for name in VARIANTS:
        rs = [o for n, _, o in out if n == name]
        say(f"[{name}] {VARIANTS[name]}")
        for fam in ("PD", "stag hunt"):
            for cond in rs[0][fam]:
                per = [np.mean(o[fam][cond]["coop"]) for o in rs]
                cl = "  ".join(f"{k} {np.mean([o[fam][cond]['cls'][k][0] for o in rs]):.2f}:"
                               f"{np.nanmean([o[fam][cond]['cls'][k][1] for o in rs]):.2f}"
                               for k in ("C only", "D only", "both", "neither"))
                say(f"    {fam:9s} {cond:9s}: cooperate {np.mean(per):.2f} [{' '.join(f'{x:.2f}' for x in per)}]   {cl}")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    names = [n for n in VARIANTS if VARIANTS[n].get("signal", True)]
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.2), sharey=True)
    for ax, fam in zip(axes, ("PD", "stag hunt")):
        x = np.arange(len(names))
        for j, (cond, col) in enumerate((("copy", "tab:blue"), ("other", "tab:orange"))):
            vals = [np.mean([np.mean(o[fam][cond]["coop"]) for n, _, o in out if n == name]) for name in names]
            ax.bar(x + (j - 0.5) * 0.38, vals, 0.38, color=col, label=f"bit says {cond}")
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=50, ha="right", fontsize=8)
        ax.set_title(f"{fam}: P(cooperate / stag)", fontsize=10)
    axes[0].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "partners.png"), dpi=120)
    say(f"done in {time.time() - t0:.0f}s")
    open(os.path.join(HERE, "partners_report.txt"), "w").write("\n".join(lines) + "\n")
