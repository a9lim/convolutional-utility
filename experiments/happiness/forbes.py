"""Momentary affect in Forbes & Bennett (2024, Emotion; data OSF m7dtw): two experiments, 150 people each, 4 blocks
of 53 trials, an affect rating (bipolar slider, 0-1) before each block and every 3-5 trials (56 per person).

Each trial a chosen two-outcome lottery (amounts -200..200, probabilities 0.25/0.5/0.75) pays an outcome o;
EV is the chosen lottery's expected value and RPE = o - EV. Unlike the GBE task there are no certain options,
and every payoff is a lottery's: o = EV + RPE always, so base utility, anticipation and news are identified
only as (base + anticipation) on o and (news - anticipation) on RPE. Asymmetric news is still testable: the
RPE weights differ by sign exactly when news does. Experiment 1 mixes free and forced choices; experiment 2
shows the unchosen option's outcome on half the trials.
"""
import csv
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "data", "forbes")
T = 53


def load(exp):
    """Per (person, block): trial arrays (blocks x 53) and ratings stored at 54 positions (0: before the block,
    t: after trial t)."""
    rows = list(csv.DictReader(open(os.path.join(DATA, exp, "behav_data.csv"))))
    mood = list(csv.DictReader(open(os.path.join(DATA, exp, "mood_data.csv"))))
    keys = sorted({(r["id"], int(r["block"])) for r in rows})
    index = {k: i for i, k in enumerate(keys)}
    n = len(keys)
    out = {k: np.full((n, T), np.nan) for k in ("o", "ev", "cf", "free", "both")}
    for r in rows:
        i, t = index[(r["id"], int(r["block"]))], int(r["trial"]) - 1
        a1, a2, p1, p2 = (float(r[k]) for k in ("chosen_amount_1", "chosen_amount_2", "chosen_prob_1", "chosen_prob_2"))
        out["o"][i, t] = float(r["outcome"])
        out["ev"][i, t] = a1 * p1 + a2 * p2
        kind = r["task_trial_type"]
        out["free"][i, t] = 1.0 if kind == "free" else 0.0
        out["both"][i, t] = 1.0 if kind == "both-feedback" else 0.0
        out["cf"][i, t] = float(r["cf_outcome"]) if kind == "both-feedback" else 0.0
    h = np.full((n, T + 1), np.nan)
    for r in mood:
        h[index[(r["id"], int(r["preceding_block_no"]))], int(r["preceding_trial_no"])] = float(r["valence"])
    out["h"] = h
    out["person"] = np.array([k[0] for k in keys])
    return out


def features(D, split="sign"):
    """Per-trial regressors (blocks x 53 x k), in hundreds of points.
    "rutledge": EV and RPE; "sign": what was paid by sign and RPE by sign; "choice": as "sign" with RPE by sign
    separately on free and forced trials; "counterfactual": as "sign" plus the unchosen option's outcome by sign
    (when shown)."""
    o, ev = D["o"], D["ev"]
    rpe = o - ev
    pos, neg = lambda x: np.maximum(x, 0), lambda x: np.minimum(x, 0)
    if split == "rutledge":
        cols, names = [ev, rpe], ["EV", "RPE"]
    else:
        cols, names = [pos(o), neg(o)], ["paid+", "paid-"]
        if split == "choice":
            f = D["free"]
            cols += [pos(rpe) * f, neg(rpe) * f, pos(rpe) * (1 - f), neg(rpe) * (1 - f)]
            names += ["RPE+ free", "RPE- free", "RPE+ forced", "RPE- forced"]
        else:
            cols += [pos(rpe), neg(rpe)]
            names += ["RPE+", "RPE-"]
        if split == "counterfactual":
            cols += [pos(D["cf"]) * D["both"], neg(D["cf"]) * D["both"]]
            names += ["unchosen+", "unchosen-"]
    return np.stack(cols, -1) / 100.0, names


def design(F, gamma, kappa):
    """Predictors at the 54 rating positions: none before the block, then the jump-kernel filtered regressors."""
    G = np.zeros_like(F)
    for t in range(1, F.shape[1]):
        G[:, t] = F[:, t - 1] + gamma * G[:, t - 1]
    X = np.zeros((F.shape[0], F.shape[1] + 1, F.shape[2]))
    X[:, 1:] = F + kappa * G
    return X


def ratings(D):
    """Valence z-scored within person (over its 56 ratings); mask of rated positions."""
    h, person = D["h"], D["person"]
    z = np.full_like(h, np.nan)
    for p in np.unique(person):
        idx = person == p
        x = h[idx]
        sd = np.nanstd(x)
        if sd > 0:
            z[idx] = (x - np.nanmean(x)) / sd
    return z, ~np.isnan(z)
