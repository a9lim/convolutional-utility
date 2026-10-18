"""Train the game-playing agent in each variant and evaluate on held-out random 2x2 games.
Run: python experiments/learned_expectations/run_games.py   (writes games_report.txt and games.png)

Variants in the canonical model (lam = 1) and under loss-averse news (X4). Equilibrium selection over seeds is a
four-way control: payoffs; payoffs at the calibrated felt agent's scale alpha + beta (the same temperature against
the entropy bonus); calibrated felt utility, canonical (the matched payoff agent up to rounding); and X4.
Also writes games_runs.json: per run, its held-out statistics, learning curves (every 250 steps) and its play on
the symmetric (S, T) plane; the free agent's hidden layer in two principal components; the sweep's shares."""
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))
from games import CLASSES, classify, pure_nash, risk_dominant, sample_games, views  # noqa: E402
from felt import EVENT, X4, Event  # noqa: E402
from oneshot import objectives, play, train  # noqa: E402

HERE = os.path.dirname(__file__)
X4_EVENT = dict(EVENT, **X4)
ALPHA, BETA = Event(**EVENT).weights()
RUNS = {                                                   # label: (variant, training keywords)
    "payoff": ("payoff", {}),
    "calibrated": ("calibrated", {}),
    "free": ("free", {}),
    "coupled": ("coupled", {}),
    "calibrated, X4": ("calibrated", dict(feel=X4_EVENT)),
    "free, X4": ("free", dict(feel=X4_EVENT)),
    "coupled, X4": ("coupled", dict(feel=X4_EVENT)),
}
SWEEP = {
    "payoff": ("payoff", {}),
    "payoff, matched": ("payoff", dict(scale=ALPHA + BETA)),
    "calibrated": ("calibrated", {}),
    "calibrated, X4": ("calibrated", dict(feel=X4_EVENT)),
}


def rd_share(i1, i2, ne, rd, sel):
    """Share of the risk-dominant equilibrium among equilibria chosen where risk and payoff dominance disagree."""
    chosen = torch.full_like(rd, -1)
    for b in torch.nonzero(sel)[:, 0].tolist():
        eqs = [(i, j) for i in (0, 1) for j in (0, 1) if ne[b, i, j]]
        if (int(i1[b]), int(i2[b])) in eqs:
            chosen[b] = eqs.index((int(i1[b]), int(i2[b])))
    return float((chosen[sel] == rd[sel]).float().sum() / (chosen[sel] >= 0).float().sum().clamp_min(1))


def tilt_good(A, pi1, q1, pi2):
    """Belief tilt toward the other's move that is better for me, given my likelier move."""
    i1 = (pi1 < 0.5).long()
    good = (A[torch.arange(len(A)), i1, 0] < A[torch.arange(len(A)), i1, 1]).long()   # 1: their move 1 better for me
    return torch.where(good == 0, q1, 1 - q1) - torch.where(good == 0, pi2, 1 - pi2)


def plane(n=41):
    """Symmetric games on the (S, T) plane at R = 0.5, P = -0.5, move 0 cooperating: harmony (S > P, T < R),
    chicken (S > P, T > R), stag hunt (S < P, T < R), prisoner's dilemma (S < P, T > R). Row-major in T."""
    g = torch.linspace(-1, 1, n)
    T_, S = torch.meshgrid(g, g, indexing="ij")
    S, T_ = S.flatten(), T_.flatten()
    A = torch.stack([torch.stack([torch.full_like(S, 0.5), S], 1), torch.stack([T_, torch.full_like(S, -0.5)], 1)], 1)
    return A, g


def tracker(curve, v, H, tau=3.0):
    """A training monitor: held-out pure-equilibrium play, risk-dominant share and cyclic optimism."""
    A, Bm, ne, cls, rd, sel = H
    idx = torch.arange(len(cls))

    def monitor(step, net, ev):
        with torch.no_grad():
            _, (pi1, q1, pi2, _) = objectives(net, ev, A, Bm, v, tau=tau)
        i1, i2 = (pi1 < 0.5).long(), (pi2 < 0.5).long()
        hit = ne[idx, i1, i2]
        row = dict(step=step, pure=float(hit[cls > 0].float().mean()), rd=rd_share(i1, i2, ne, rd, sel),
                   cyclic_dev=float((pi1[cls == 0] - 0.5).abs().mean()))
        if v in ("free", "coupled"):
            row["tilt_cyclic"] = float(tilt_good(A, pi1, q1, pi2)[cls == 0].mean())
        curve.append({k: round(x, 4) if isinstance(x, float) else x for k, x in row.items()})
    return monitor


def play_map(net, felt, v, tau=3.0):
    """P(cooperate) and the belief that the other cooperates on the (S, T) plane (self-play, symmetric)."""
    A, _ = plane()
    with torch.no_grad():
        _, (pi1, q1, _, _) = objectives(net, felt, A, A.transpose(1, 2), v, tau=tau)
    return dict(p=[round(float(x), 4) for x in pi1], q=[round(float(x), 4) for x in q1])


def selection_seed(job):
    """Equilibrium play and the risk-dominant share for one variant and seed (the seed sweep)."""
    label, seed = job
    v, kw = SWEEP[label]
    torch.set_num_threads(2)
    gen = torch.Generator().manual_seed(2026)
    A, Bm = sample_games(20000, gen)
    ne, cls = pure_nash(A, Bm), classify(A, Bm)
    rd, pd = risk_dominant(A, Bm, ne)
    sel = (rd >= 0) & (pd >= 0) & (rd != pd)
    net, felt = train(v, steps=6000, batch=1024, seed=seed, **kw)
    with torch.no_grad():
        _, (pi1, _, pi2, _) = objectives(net, felt, A, Bm, v)
    return label, seed, rd_share((pi1 < 0.5).long(), (pi2 < 0.5).long(), ne, rd, sel)


def probe(X, y, Xt, yt, steps=3000):
    """Multinomial logistic-regression probe accuracy."""
    mu, sd = X.mean(0), X.std(0) + 1e-9
    X, Xt = (X - mu) / sd, (Xt - mu) / sd
    W = torch.zeros(X.shape[1], 4, requires_grad=True)
    b = torch.zeros(4, requires_grad=True)
    opt = torch.optim.Adam([W, b], lr=0.05)
    for _ in range(steps):
        opt.zero_grad()
        torch.nn.functional.cross_entropy(X @ W + b, y).backward()
        opt.step()
    with torch.no_grad():
        return float(((Xt @ W + b).argmax(1) == yt).float().mean())


if __name__ == "__main__":
    t0 = time.time()
    lines = []
    say = lambda s: (print(s, flush=True), lines.append(s))
    gen = torch.Generator().manual_seed(2026)
    A, Bm = sample_games(20000, gen)
    ne, cls = pure_nash(A, Bm), classify(A, Bm)
    rd, pd = risk_dominant(A, Bm, ne)
    sel = (rd >= 0) & (pd >= 0) & (rd != pd)               # risk- and payoff-dominance disagree
    say(f"held-out games: " + ", ".join(f"{c} {int((cls == k).sum())}" for k, c in enumerate(CLASSES))
        + f"; two-equilibrium games where risk and payoff dominance disagree: {int(sel.sum())}")
    say(f"Canonical felt welfare alpha m(q) + beta m(p): alpha {ALPHA:.4f}, beta {BETA:.4f}, scale {ALPHA + BETA:.4f}; "
        f"X4: lam {X4['lam']}")
    H = (A, Bm, ne, cls, rd, sel)
    res, export = {}, dict(classes=CLASSES, plane=[round(float(x), 4) for x in plane()[1]], alpha=ALPHA, beta=BETA,
                           runs=[])
    for label, (v, kw) in RUNS.items():
        curve = []
        net, felt = train(v, steps=6000, batch=1024, monitor=tracker(curve, v, H), **kw)
        with torch.no_grad():
            (o1, o2), (pi1, q1, pi2, q2) = objectives(net, felt, A, Bm, v)
            (m1, t1), _ = views(A, Bm)
            _, _, h = play(net, m1, t1)
        res[label] = (net, felt, pi1, q1, pi2, q2, h)
        i1, i2 = (pi1 < 0.5).long(), (pi2 < 0.5).long()
        hit = ne[torch.arange(len(cls)), i1, i2]
        accs = [float(hit[cls == k].float().mean()) for k in (1, 2, 3)]
        # equilibrium selection where risk and payoff dominance disagree
        chosen = torch.full_like(rd, -1)
        for b in torch.nonzero(sel)[:, 0].tolist():
            eqs = [(i, j) for i in (0, 1) for j in (0, 1) if ne[b, i, j]]
            if (int(i1[b]), int(i2[b])) in eqs:
                chosen[b] = eqs.index((int(i1[b]), int(i2[b])))
        rd_sh = float((chosen[sel] == rd[sel]).float().sum() / (chosen[sel] >= 0).float().sum().clamp_min(1))
        say(f"[{label}] plays a pure equilibrium: unique-efficient {accs[0]:.1%}, PD-like {accs[1]:.1%}, "
            f"two-equilibrium {accs[2]:.1%}; where risk and payoff dominance disagree, picks the risk-dominant "
            f"one {rd_sh:.1%}; cyclic games: mean |P(move 0) - 1/2| {float((pi1[cls == 0] - 0.5).abs().mean()):.3f}")
        if v in ("free", "coupled"):
            # optimism: belief tilt toward the other's move that is better for me, given my likelier move
            mine = A
            good = (mine[torch.arange(len(cls)), i1, 0] < mine[torch.arange(len(cls)), i1, 1]).long()   # 1: their move 1 better for me
            q_good = torch.where(good == 0, q1, 1 - q1)
            p_good = torch.where(good == 0, pi2, 1 - pi2)
            tilt = q_good - p_good
            say(f"    belief tilt toward the outcome good for me (q - p): " + ", ".join(
                f"{CLASSES[k]} {float(tilt[cls == k].mean()):+.3f}" for k in range(4)))
        export["runs"].append(dict(
            label=label, variant=v, calibration="X4" if "X4" in label else "canonical", tau=3.0,
            pure={CLASSES[k]: accs[k - 1] for k in (1, 2, 3)}, rd=rd_sh,
            cyclic_dev=float((pi1[cls == 0] - 0.5).abs().mean()),
            tilt={CLASSES[k]: float(tilt_good(A, pi1, q1, pi2)[cls == k].mean()) for k in range(4)}
            if v in ("free", "coupled") else None,
            curve=curve, map=play_map(net, felt, v)))
    # a looser tether: motivated beliefs at tau = 30
    for label in ("free", "coupled", "free, X4", "coupled, X4"):
        v, kw = RUNS[label]
        curve = []
        net, felt = train(v, steps=6000, batch=1024, tau=30.0, monitor=tracker(curve, v, H, tau=30.0), **kw)
        with torch.no_grad():
            _, (pi1, q1, pi2, q2) = objectives(net, felt, A, Bm, v, tau=30.0)
        i1, i2 = (pi1 < 0.5).long(), (pi2 < 0.5).long()
        hit = ne[torch.arange(len(cls)), i1, i2]
        good = (A[torch.arange(len(cls)), i1, 0] < A[torch.arange(len(cls)), i1, 1]).long()
        tilt = torch.where(good == 0, q1, 1 - q1) - torch.where(good == 0, pi2, 1 - pi2)
        say(f"[{label}, tau = 30] pure equilibrium: unique-efficient {float(hit[cls == 1].float().mean()):.1%}, "
            f"PD-like {float(hit[cls == 2].float().mean()):.1%}, two-equilibrium {float(hit[cls == 3].float().mean()):.1%}; "
            "belief tilt toward the good outcome: " + ", ".join(f"{CLASSES[k]} {float(tilt[cls == k].mean()):+.3f}" for k in range(4)))
        export["runs"].append(dict(
            label=f"{label}, tau 30", variant=v, calibration="X4" if "X4" in label else "canonical", tau=30.0,
            pure={CLASSES[k]: float(hit[cls == k].float().mean()) for k in (1, 2, 3)},
            rd=rd_share(i1, i2, ne, rd, sel), cyclic_dev=float((pi1[cls == 0] - 0.5).abs().mean()),
            tilt={CLASSES[k]: float(tilt[cls == k].mean()) for k in range(4)},
            curve=curve, map=play_map(net, felt, v, tau=30.0)))
    # do they tell games apart? probe class from the hidden layer vs from raw payoffs
    X_raw = torch.cat([A.flatten(1), Bm.flatten(1)], 1)
    n_tr = 15000
    raw = probe(X_raw[:n_tr], cls[:n_tr], X_raw[n_tr:], cls[n_tr:])
    probes = {v: probe(res[v][6][:n_tr], cls[:n_tr], res[v][6][n_tr:], cls[n_tr:]) for v in RUNS}
    say(f"linear probe for game class: raw payoffs {raw:.1%}; " + ", ".join(
        f"{v} hidden layer {probes[v]:.1%}" for v in RUNS))
    export["probe"] = dict(raw=raw, **probes)
    # differences in play: felt variants against the payoff baseline
    base = (res["payoff"][2] < 0.5)
    for v in [x for x in RUNS if x != "payoff"]:
        diff = ((res[v][2] < 0.5) != base)
        next(r for r in export["runs"] if r["label"] == v)["differs"] = {
            CLASSES[k]: float(diff[cls == k].float().mean()) for k in range(4)}
        say(f"[{v}] modal move differs from the payoff agent in: " + ", ".join(
            f"{CLASSES[k]} {float(diff[cls == k].float().mean()):.1%}" for k in range(4)))
    # equilibrium selection over seeds: the four-way control
    with ProcessPoolExecutor(10) as ex:
        sweep = list(ex.map(selection_seed, [(v, s) for v in SWEEP for s in range(5)]))
    by = {v: [x for v_, _, x in sweep if v_ == v] for v in SWEEP}
    export["sweep"] = by
    say("risk-dominant share over 5 seeds: " + "; ".join(
        f"{v} " + " ".join(f"{x:.3f}" for x in by[v]) + f" (mean {np.mean(by[v]):.3f})" for v in SWEEP))
    pairs = (("calibrated, X4", "payoff, matched"), ("calibrated, X4", "payoff"), ("payoff, matched", "payoff"),
             ("calibrated", "payoff, matched"))
    say("    higher by seed: " + "; ".join(f"{a} over {b} {sum(x > y for x, y in zip(by[a], by[b]))}/5" for a, b in pairs)
        + f"; calibrated against payoff, matched, max |difference| {max(abs(x - y) for x, y in zip(by['calibrated'], by['payoff, matched'])):.1e}")
    # figure: PCA of the free agent's hidden layer, coloured by class; belief tilt by class
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    h = res["free"][6][:4000]
    hc = h - h.mean(0)
    U, S, Vt = torch.linalg.svd(hc, full_matrices=False)
    Z = hc @ Vt[:2].T
    export["pca"] = dict(x=[round(float(z), 3) for z in Z[:, 0]], y=[round(float(z), 3) for z in Z[:, 1]],
                         cls=[int(c) for c in cls[:4000]])
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    cols = ["#e76f51", "#2a9d8f", "#8e44ad", "#e9c46a"]
    for k in range(4):
        sel_k = cls[:4000] == k
        axes[0].scatter(Z[sel_k, 0], Z[sel_k, 1], s=4, alpha=0.5, color=cols[k], label=CLASSES[k])
    axes[0].set_title("Felt agent's hidden layer (PCA, free beliefs, canonical), by game class", fontsize=10)
    axes[0].legend(fontsize=8, markerscale=3, frameon=False)
    tilts = ("free", "coupled", "free, X4", "coupled, X4")
    for j, v in enumerate(tilts):
        pi1, q1, pi2 = res[v][2], res[v][3], res[v][4]
        i1 = (pi1 < 0.5).long()
        good = (A[torch.arange(len(cls)), i1, 0] < A[torch.arange(len(cls)), i1, 1]).long()
        tilt = torch.where(good == 0, q1, 1 - q1) - torch.where(good == 0, pi2, 1 - pi2)
        means = [float(tilt[cls == k].mean()) for k in range(4)]
        axes[1].bar(np.arange(4) + 0.2 * j, means, width=0.2, label=v,
                    color=["#3182bd", "#9ecae1", "#e6550d", "#fdae6b"][j])
    axes[1].axhline(0, color="#777", lw=0.8)
    axes[1].set_xticks(np.arange(4) + 0.3, ["cyclic", "unique\nefficient", "PD-like", "two eq."], fontsize=8)
    axes[1].set_ylabel("belief tilt toward the good outcome (q − p)")
    axes[1].set_title("Motivated beliefs about the other player", fontsize=10)
    axes[1].legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "games.png"), dpi=130)
    json.dump(export, open(os.path.join(HERE, "games_runs.json"), "w"))
    say(f"done in {time.time() - t0:.0f}s")
    open(os.path.join(HERE, "games_report.txt"), "w").write("\n".join(lines) + "\n")
