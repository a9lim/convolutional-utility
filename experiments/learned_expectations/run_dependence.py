"""Inferred dependence against the identity oracle (dependence.py). Run:
python experiments/learned_expectations/run_dependence.py   (writes dependence_report.txt, dependence.png)

A bank of four causal networks (self-play with no dependence) is trained first and frozen; it plays every
stranger and forger, so all variants face the same independent opponents. Environments: "mirrors" (copies and
mirrors half and half: every non-copy plays the twin's own policy), "strangers" (copies and frozen strangers
half and half), "forgers" (copies 0.5, frozen strangers 0.25, frozen forgers 0.25: independent opponents with
copy-like signals). Signal noise 0.5. Twins at w = 1: the oracle, the bayes twin with the true model, a
learned dependence head, a naive bayes twin that counts forgers as copies, and a credulous one that assumes
90% of partners are copies, a universal one that treats every partner as a copy;
felt oracle and bayes at w = 0.5 under loss-averse news (X4) as a control. Four seeds each. Measured:
cooperation in prisoner's dilemmas and stag hunts by signal; the dependence estimate against the true
posterior; payoff against each partner type; and boundary gradient signs of the expected gradient."""
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from agents import Agent  # noqa: E402
from dependence import dependence_logit, posterior, signal, slope, train  # noqa: E402
from felt import EVENT, X4  # noqa: E402
from games import symmetric_family, views  # noqa: E402
from partners import LAYOUT, policy  # noqa: E402
from partners import train as train_partners  # noqa: E402

HERE = os.path.dirname(__file__)
ETA = 0.5
ENV = {"mirrors": {"copy": 0.5, "mirror": 0.5}, "strangers": {"copy": 0.5, "stranger": 0.5},
       "forgers": {"copy": 0.5, "stranger": 0.25, "forger": 0.25}}
CREDULOUS = ({"copy": 0.9, "stranger": 0.1}, ETA)
UNIVERSAL = ({"copy": 1.0}, ETA)
NAIVE = ({"copy": 0.75, "stranger": 0.25}, ETA)
VARIANTS = {}
for env in ENV:
    VARIANTS[f"causal, {env}"] = dict(mode="oracle", w=0.0, env=env)
    VARIANTS[f"oracle, {env}"] = dict(mode="oracle", env=env)
    VARIANTS[f"bayes, {env}"] = dict(mode="bayes", env=env)
    VARIANTS[f"learned, {env}"] = dict(mode="learned", env=env)
    VARIANTS[f"credulous, {env}"] = dict(mode="bayes", env=env, assume=CREDULOUS)
    VARIANTS[f"universal, {env}"] = dict(mode="bayes", env=env, assume=UNIVERSAL)
VARIANTS["naive, forgers"] = dict(mode="bayes", env="forgers", assume=NAIVE)
VARIANTS["felt oracle 0.5, X4, forgers"] = dict(mode="oracle", w=0.5, env="forgers", felt=True, feel=dict(EVENT, **X4))
VARIANTS["felt bayes 0.5, X4, forgers"] = dict(mode="bayes", w=0.5, env="forgers", felt=True, feel=dict(EVENT, **X4))
SEEDS, BANK = 4, 4
GRID = (-0.5, 0.0, 0.5, 1.0, 1.5)
D = 1e-3


def bank_member(seed):
    torch.set_num_threads(int(os.environ.get("THREADS", "1")))
    nets, _ = train_partners(K=1, sigma=1.0, signal=False, seed=100 + seed, steps=int(os.environ.get("STEPS", "4000")))
    return nets[0].state_dict()


def load_bank(states):
    bank = []
    for st in states:
        n = Agent(**LAYOUT)
        n.load_state_dict(st)
        n.requires_grad_(False)
        bank.append(n)
    return bank


def dhat(kw, agent, s):
    if kw["mode"] == "learned":
        with torch.no_grad():
            return float(torch.sigmoid(dependence_logit(agent, torch.tensor([s]))))
    a_shares, a_eta = kw.get("assume") or (ENV[kw["env"]], ETA)
    return float(posterior(s, a_shares, a_eta))


def payoff(pi, pj, m):
    return pi * pj * m[:, 0, 0] + pi * (1 - pj) * m[:, 0, 1] + (1 - pi) * pj * m[:, 1, 0] + (1 - pi) * (1 - pj) * m[:, 1, 1]


def one(job):
    name, seed, states = job
    torch.set_num_threads(int(os.environ.get("THREADS", "1")))
    kw = VARIANTS[name]
    bank = load_bank(states)
    shares = ENV[kw["env"]]
    net, F = train(mode=kw["mode"], w=kw.get("w", 1.0), shares=shares, eta=ETA, assume=kw.get("assume"),
                        bank=bank, felt=kw.get("felt", False), feel=kw.get("feel", EVENT), seed=seed,
                        steps=int(os.environ.get("STEPS", "4000")))
    gen = torch.Generator().manual_seed(99)
    out = {"d": [dhat(kw, net, s) for s in GRID], "fam": {}, "pay": {}}
    with torch.no_grad():
        for fam, A in {k: symmetric_family(k, 4000, torch.Generator().manual_seed(7))[0]
                       for k in ("PD", "stag hunt")}.items():
            (m, t), _ = views(A, A.transpose(1, 2))
            frozen = [policy(b, m, t, torch.zeros(len(A))) for b in bank]
            rows = []
            for s in GRID:
                coop = policy(net, m, t, torch.full((len(A),), s))
                with torch.enable_grad():
                    lo, hi = (slope(A, F, s, p, frozen, shares, ETA, kw["mode"], kw.get("w", 1.0), dhat(kw, net, s))
                              for p in (D, 1 - D))
                c, dd = hi > 0, lo < 0
                cls = {"C": c & ~dd, "D": dd & ~c, "both": c & dd, "neither": ~c & ~dd}
                rows.append(dict(coop=float(coop.mean()),
                                 cls={k: (float(v.double().mean()), float(coop[v].mean()) if v.any() else float("nan"))
                                      for k, v in cls.items()}))
            out["fam"][fam] = rows
        A = torch.rand(20000, 2, 2, generator=gen) * 2 - 1
        (m1, t1), (m2, t2) = views(A, A.transpose(1, 2))
        for typ in ("copy", "stranger", "forger"):          # a mirror's payoff is a copy's
            s = signal(typ, len(A), ETA, gen)
            pi = policy(net, m1, t1, s)
            if typ == "copy":
                out["pay"][typ] = float(payoff(pi, policy(net, m2, t2, s), m1).mean())
            else:
                out["pay"][typ] = float(np.mean([float(payoff(pi, policy(b, m2, t2, torch.zeros(len(A))), m1).mean())
                                                 for b in bank]))
    return name, seed, out


if __name__ == "__main__":
    t0, lines = time.time(), []
    say = lambda s: (print(s, flush=True), lines.append(s))
    procs = int(os.environ.get("PROCS", "16"))
    with ProcessPoolExecutor(procs) as ex:
        states = list(ex.map(bank_member, range(BANK)))
        bank = load_bank(states)
        A = symmetric_family("PD", 4000, torch.Generator().manual_seed(7))[0]
        (m, t), _ = views(A, A.transpose(1, 2))
        with torch.no_grad():
            say("frozen bank (causal self-play), P(cooperate) in prisoner's dilemmas: "
                + " ".join(f"{float(policy(b, m, t, torch.zeros(len(A))).mean()):.3f}" for b in bank))
        jobs = [(n, s, states) for n in VARIANTS for s in range(SEEDS)]
        out = list(ex.map(one, jobs))
    say(f"Signal grid s = {GRID}. Means over {SEEDS} seeds. Cooperation (move 0) by signal; in brackets, under the "
        "variant's expected gradient (entropy-free, one policy per game), the share of games whose boundary gradient "
        "signs point to all-cooperate only / all-defect only / both / neither, and learned cooperation there.")
    for env, shares in ENV.items():
        say(f"true P(copy | s), {env}: " + " ".join(f"{float(posterior(s, shares, ETA)):.2f}" for s in GRID))
    for name, kw in VARIANTS.items():
        rs = [o for n, _, o in out if n == name]
        say(f"[{name}] {dict((k, v) for k, v in kw.items() if k not in ('env', 'feel'))}")
        say("    dependence d(s): " + " ".join(f"{np.mean([o['d'][i] for o in rs]):.2f}" for i in range(len(GRID))))
        for fam in ("PD", "stag hunt"):
            cells = []
            for i in range(len(GRID)):
                cl = {k: (np.mean([o["fam"][fam][i]["cls"][k][0] for o in rs]),
                          np.mean([o["fam"][fam][i]["cls"][k][1] for o in rs if o["fam"][fam][i]["cls"][k][0] > 0] or [np.nan]))
                      for k in ("C", "D", "both", "neither")}
                cells.append(f"{np.mean([o['fam'][fam][i]['coop'] for o in rs]):.2f} ["
                             + " ".join(f"{cl[k][0]:.2f}:{cl[k][1]:.2f}" for k in ("C", "D", "both", "neither")) + "]")
            say(f"    {fam:9s}: " + " | ".join(cells))
        shares = ENV[kw["env"]]
        pay = {"copy": [o["pay"]["copy"] for o in rs], "stranger": [o["pay"]["stranger"] for o in rs],
               "forger": [o["pay"]["forger"] for o in rs]}
        val = lambda o: sum(sh * o["pay"]["copy" if typ == "mirror" else typ] for typ, sh in shares.items())  # noqa: E731
        total = [val(o) for o in rs]
        say("    payoff vs copy/mirror {:+.3f}, frozen stranger {:+.3f}, frozen forger {:+.3f} | in its environment {:+.4f} [{}]"
            .format(np.mean(pay["copy"]), np.mean(pay["stranger"]), np.mean(pay["forger"]), np.mean(total),
                    " ".join(f"{x:+.4f}" for x in total)))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 4, figsize=(17, 3.8))
    for ax, env in zip(axes[:3], ENV):
        for name in [n for n in VARIANTS if n.endswith(env) and "felt" not in n]:
            rs = [o for n, _, o in out if n == name]
            ax.plot(GRID, [np.mean([o["fam"]["PD"][i]["coop"] for o in rs]) for i in range(len(GRID))], "o-",
                    label=name.split(",")[0])
        ax.set_title(f"{env}: PD cooperation", fontsize=10)
        ax.set_xlabel("similarity signal s")
        ax.legend(frameon=False, fontsize=8)
    for name in [n for n in VARIANTS if n.endswith("forgers") and n.split(",")[0] in ("learned", "naive", "credulous")]:
        rs = [o for n, _, o in out if n == name]
        axes[3].plot(GRID, [np.mean([o["d"][i] for o in rs]) for i in range(len(GRID))], "o-", label=name.split(",")[0])
    axes[3].plot(GRID, [float(posterior(s, ENV["forgers"], ETA)) for s in GRID], "k--", label="true P(copy | s)")
    axes[3].set_title("forgers: the twin's dependence estimate", fontsize=10)
    axes[3].set_xlabel("similarity signal s")
    axes[3].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "dependence.png"), dpi=120)
    say(f"done in {time.time() - t0:.0f}s")
    open(os.path.join(HERE, "dependence_report.txt"), "w").write("\n".join(lines) + "\n")
