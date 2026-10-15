"""Momentary happiness in the Great Brain Experiment risk task (Rutledge et al. 2014; data: Zenodo 4421847,
CC0), fitted by the direct and recursive echo models.

Each play: 30 trials of a safe option against a 50/50 gamble, and 12 ratings of "How happy are you right
now?" (one before trial 1, then after every 2-3 trials). Per trial, as in Rutledge et al.: the certain reward
CR (if safe), the gamble's expected value EV and the prediction error RPE = outcome - EV (if gambled).

Read as felt utility: a gamble's outcome is base utility EV + RPE, its EV is also anticipated before the
spin, and its RPE is also felt as news, so the trial's felt contribution is
  s [CR + (1 + a) EV + (1 + n) RPE+ + (1 + n lam) RPE-]
(a: anticipation, n: news, lam: loss aversion in news). A rating reads the current felt state: the trial's
contribution plus echoes of earlier ones, through a memory kernel k(lag). Rutledge's kernel is gamma^lag. The
recursive model (memory over felt states, e_t = f_t + m sum_j mu^j e_{t-j}) has resolvent kernel 1 at lag 0
and m mu (mu (1 + m))^(lag - 1) after: geometric after a jump at lag 0, k = (1, kappa, kappa gamma, ...),
with gamma = mu (1 + m) and kappa = m mu < gamma. Rutledge's kernel is the case kappa = gamma.
"""
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MAT = os.path.join(HERE, "..", "..", "data", "gbe", "extracted", "Rutledge_GBE_risk_data_TOD.mat")
TIDY = os.path.join(HERE, "..", "..", "data", "gbe", "tidy.npz")


def tidy(mat=MAT, out=TIDY):
    """Flatten subjData into per-play arrays (plays x 30): certain, win, lose, gambled, outcome, happiness."""
    import scipy.io
    S = scipy.io.loadmat(mat, struct_as_record=False, squeeze_me=True)["subjData"]
    plays, subj, version = [], [], []
    for i, s in enumerate(S):
        d = s.data
        mats = [d] if isinstance(d, np.ndarray) and d.dtype != object else list(np.atleast_1d(d))
        vers = np.atleast_1d(s.designVersion)
        for j, X in enumerate(mats):
            X = np.asarray(X, dtype=float)
            if X.shape != (30, 15):
                continue
            plays.append(X[:, [2, 3, 4, 6, 7, 9]])
            subj.append(i)
            version.append(vers[min(j, len(vers) - 1)])
    P = np.stack(plays)
    np.savez_compressed(out, c=P[..., 0], w=P[..., 1], l=P[..., 2], g=P[..., 3], o=P[..., 4], h=P[..., 5],
                        subj=np.array(subj), version=np.array(version))
    return out


def load(path=TIDY):
    if not os.path.exists(path):
        tidy(out=path)
    return dict(np.load(path))


def features(D, split="rpe"):
    """Per-trial regressors (plays x 30 x k), in hundreds of points.
    split: "none" (CR, EV, RPE: Rutledge 2014), "rpe" (RPE by sign), or "structural": what the trial paid
    (base utility, by sign, the same for certain and risky payoffs), plus a gamble's EV (anticipation) and
    RPE by sign (news). Base utility is pinned by safe choices; mixed trials, where EV and RPE vary
    independently, then identify anticipation and news by sign (in gain-only or loss-only trials EV equals
    the size of RPE)."""
    g = D["g"]
    ev = (D["w"] + D["l"]) / 2
    CR, EV, RPE = (1 - g) * D["c"], g * ev, g * (D["o"] - ev)
    pos, neg = lambda x: np.maximum(x, 0), lambda x: np.minimum(x, 0)
    out = (1 - g) * D["c"] + g * D["o"]                      # what the trial paid
    cols = {"none": [CR, EV, RPE], "rpe": [CR, EV, pos(RPE), neg(RPE)],
            "structural": [pos(out), neg(out), EV, pos(RPE), neg(RPE)]}[split]
    names = {"none": ["CR", "EV", "RPE"], "rpe": ["CR", "EV", "RPE+", "RPE-"],
             "structural": ["paid+", "paid-", "EV", "RPE+", "RPE-"]}[split]
    return np.stack(cols, -1) / 100.0, names


def echoes(F, gamma):
    """G_t = sum_{lag >= 1} gamma^(lag - 1) F_{t - lag}, by recursion along trials."""
    G = np.zeros_like(F)
    for t in range(1, F.shape[1]):
        G[:, t] = F[:, t - 1] + gamma * G[:, t - 1]
    return G


def filtered(F, gamma, kappa, G=None):
    """sum_{j <= t} k(t - j) F_j with k = (1, kappa, kappa gamma, kappa gamma^2, ...)."""
    return F + kappa * (echoes(F, gamma) if G is None else G)


def design(F, gamma, kappa):
    """Predictors for the rating stored on each trial's row: the filtered regressors, except that the first
    rating is made before trial 1 and sees no outcome."""
    X = filtered(F, gamma, kappa)
    X[:, 0] = 0.0
    return X


def ratings(D, keep):
    """z-scored happiness (within subject, over all its ratings) and the rating mask. The first rating is made
    before trial 1 (design() gives it no outcome), so it anchors the play's intercept."""
    h = D["h"][keep]
    subj = D["subj"][keep]
    z = np.full_like(h, np.nan)
    order = np.argsort(subj, kind="stable")
    bounds = np.flatnonzero(np.diff(subj[order])) + 1
    for idx in np.split(order, bounds):
        x = h[idx]
        sd = np.nanstd(x)
        if sd > 0:
            z[idx] = (x - np.nanmean(x)) / sd
    return z, ~np.isnan(z)


def fit(Ff, z, mask):
    """Least squares of z on filtered regressors with a fixed effect per play (within-play demeaning).
    Returns weights and the residual sum of squares and count."""
    cnt = mask.sum(1, keepdims=True)
    ok = cnt[:, 0] > 1
    Ff, z, mask, cnt = Ff[ok], z[ok], mask[ok], cnt[ok]
    zm = np.where(mask, z, 0).sum(1, keepdims=True) / cnt
    Fm = np.where(mask[..., None], Ff, 0).sum(1, keepdims=True) / cnt[..., None]
    y = (z - zm)[mask]
    X = (Ff - Fm)[mask]
    w, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ w
    return w, float(r @ r), len(y), X, y
