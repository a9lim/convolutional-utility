"""Step changes in luck: the open-loop up-down-up task of Keren et al. (2021, eLife; OSF vw7sz, "Structured
experiment data", the open-loop fixed version) and Jangraw et al. (2023, Nat. Hum. Behav. 7: 596; OSF km69z,
cohorts Weekly-Rest-02 and -03, folders COVID02 and COVID03; NIMH public domain).

Each trial offers a certain amount or a 50/50 gamble whose expected value equals it. Three blocks (27 trials
each in Keren's version, 22 in Jangraw's, after a rest period): in a "happy" block a gamble wins on congruent
trials (70%; win minus lose 5 points, so the prediction error is +2.5) and loses on incongruent ones (-0.75);
in the "unhappy" block the reverse. Blocks run happy, unhappy, happy, unsignalled. Ratings of "How happy are you
right now?" follow every 2-3 trials, plus one at the start of each block.

So luck is a sustained step: about 7 minutes of mostly good outcomes, then bad, then good. An impulse is nearly
blind to slow adaptation (audit/impulse_detectability.py); a step lets its negative lobe accumulate. Per trial,
as in gbe.py: the certain reward CR (if safe), the gamble's expected value EV and prediction error RPE (if
gambled), in points.
"""
import glob
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "data")
SOURCES = {"keren": os.path.join(DATA, "keren", "structured", "*.xlsx"),
           "covid02": os.path.join(DATA, "jangraw", "extracted", "PassageOfTimeDysphoria_Data", "PilotData",
                                   "COVID02", "*_MmiRecoveryOpen-*.csv"),
           "covid03": os.path.join(DATA, "jangraw", "extracted", "PassageOfTimeDysphoria_Data", "PilotData",
                                   "COVID03", "*_MmiRecoveryOpen-*.csv")}
CHECKS = os.path.join(DATA, "jangraw", "extracted", "PassageOfTimeDysphoria_Data", "DataChecks")


def read_one(path):
    """Trials (rows with a choice) and ratings. A rating's position tau: it sees trials 0..tau (tau = t for the
    rating after trial t, t - 1 for the one at the start of the block holding trial t)."""
    d = pd.read_excel(path) if path.endswith(".xlsx") else pd.read_csv(path)
    if "choice" not in d.columns:                           # one empty Keren file
        return None
    tr = d[d["choice"].isin(["gamble", "certain"])].reset_index(drop=True)
    g = (tr["choice"] == "gamble").to_numpy()
    cert = tr["certainAmount"].to_numpy(float)
    out = tr["outcomeAmount"].to_numpy(float)
    F = np.stack([np.where(g, 0.0, cert), np.where(g, cert, 0.0), np.where(g, out - cert, 0.0)], -1)
    blk = tr["isHappyBlock"].astype(float).to_numpy()
    start = np.r_[True, blk[1:] != blk[:-1]]
    block = np.cumsum(start) - 1
    taus, hs, kind = [], [], []
    for t in range(len(tr)):
        b = tr.loc[t, "blockHappySlider.response"]
        if pd.notna(b):
            taus.append(t - 1); hs.append(float(b)); kind.append(0)
        h = tr.loc[t, "happySlider.response"]
        if pd.notna(h):
            taus.append(t); hs.append(float(h)); kind.append(1)
    return dict(F=F, happy=np.where(blk == 1, 1.0, -1.0), block=block, tau=np.array(taus),
                h=np.array(hs), kind=np.array(kind), gamble=g)


def load(name):
    """All sessions of one source with a complete run (Jangraw's data checks for the cohorts), the design
    shape the majority has, and ratings that vary. Each run carries "person": the hashed MTurk id for
    Jangraw's weekly cohorts (most people did both weeks), the file for Keren's."""
    files = sorted(glob.glob(SOURCES[name]))
    who = {}
    if name != "keren":
        chk = pd.read_csv(os.path.join(CHECKS, f"{name.upper()}_DataCheck.csv"))
        chk = chk[chk["isComplete"] == True]  # noqa: E712
        who = dict(zip(chk["taskFile"].map(os.path.basename), chk["MTurkID"]))
        files = [f for f in files if os.path.basename(f) in who]
    runs = []
    for f in files:
        r = read_one(f)
        if r is not None:
            r["person"] = who.get(os.path.basename(f), os.path.basename(f))
            runs.append(r)
    T = pd.Series([len(r["F"]) for r in runs]).mode()[0]
    runs = [r for r in runs if len(r["F"]) == T and np.nanstd(r["h"]) > 0]
    return runs, int(T)


def zscore(runs):
    for r in runs:
        r["z"] = (r["h"] - r["h"].mean()) / r["h"].std()
    return runs


def kernel_matrix(k, T):
    """K[tau + 1, j] = k(tau - j) for j <= tau; row 0 is tau = -1 (sees nothing)."""
    K = np.zeros((T + 1, T))
    for tau in range(T):
        K[tau + 1, :tau + 1] = k[:tau + 1][::-1]
    return K


def stack(runs, T):
    """Arrays for least squares: features (people x T x 3), rating positions, ratings, person ids."""
    F = np.stack([r["F"] for r in runs])
    tau = np.concatenate([r["tau"] for r in runs])
    z = np.concatenate([r["z"] for r in runs])
    pid = np.concatenate([np.full(len(r["tau"]), i) for i, r in enumerate(runs)])
    return F, tau, z, pid


def design(F, tau, pid, k, T, extra=None):
    """Filtered inputs at each rating, a linear drift in position, optional extra columns (ratings x m)."""
    K = kernel_matrix(k, T)
    Xall = np.einsum("st,ptk->psk", K, F)                   # people x (T + 1) x 3
    X = Xall[pid, tau + 1]
    cols = [X, ((tau + 1) / T)[:, None]]
    if extra is not None:
        cols.append(extra)
    return np.concatenate(cols, 1)


def demean(X, y, pid):
    """Within-person demeaning (a fixed effect per person)."""
    n = pid.max() + 1
    cnt = np.bincount(pid, minlength=n)
    Xm = np.stack([np.bincount(pid, X[:, j], n) for j in range(X.shape[1])], 1) / cnt[:, None]
    ym = np.bincount(pid, y, n) / cnt
    return X - Xm[pid], y - ym[pid]


def lsq(X, y, pid, sel, w=None):
    """Least squares with a fixed effect per person on ratings of persons in sel; residuals per rating."""
    m = sel[pid]
    Xd, yd = demean(X[m], y[m], np.unique(pid[m], return_inverse=True)[1])
    if w is None:
        w = np.linalg.lstsq(Xd, yd, rcond=None)[0]
    return w, yd - Xd @ w


def running_mean(F, tau, pid):
    """Mean of all inputs before the rating's trial window: mean_{j <= tau - 1} F_j (Keren's primacy
    reference: the expectation is the average of everything so far). Zero before two trials."""
    cs = np.cumsum(F, 1)
    out = np.zeros((len(tau), F.shape[2]))
    ok = tau >= 1
    out[ok] = cs[pid[ok], tau[ok] - 1] / tau[ok][:, None]
    return out


ELL = None


def kernels(T):
    ell = np.arange(T, dtype=float)

    def jump(p):
        g, kap = p
        return np.r_[1.0, kap * g ** np.arange(T - 1)]

    def hyper(p):
        return (1 + p[0] * ell) ** -p[1]

    def biph(p):
        m, mu, c, g = p
        k = m * mu ** ell - c * g ** ell
        k[0] = 1.0
        return k

    def hypx(p):
        h, om, c, g = p
        k = (1 + h * ell) ** -om - c * g ** ell
        k[0] = 1.0
        return k

    return [("jump", jump, [[0.88, 0.45], [0.6, 0.6]], ([0, 0], [0.999, 2])),
            ("hyperbola", hyper, [[1.0, 0.7], [3.0, 0.5]], ([0, 0], [50, 10])),
            ("biphasic", biph, [[0.5, 0.88, 0.05, 0.98], [0.5, 0.88, 0.2, 0.95], [0.5, 0.7, 0.3, 0.97]],
             ([0, 0, 0, 0], [5, 0.999, 5, 0.9999])),
            ("hyperbola - exp", hypx, [[1.0, 0.7, 0.05, 0.98], [1.0, 0.7, 0.2, 0.95]],
             ([0, 0, 0, 0], [50, 10, 5, 0.9999]))]


def rest_after_wins():
    """Jangraw's RestAfterWins (folder Return1, complete runs): the block-start rating before a closed-loop
    winning block (its prediction errors rise to keep mood climbing), the last rating in it, then 30 ratings
    at rest 15 s apart. Returns pre (n), last (n), rest (n x 30) and the share of rest ratings exactly at the
    slider's 0.5."""
    root = os.path.join(DATA, "jangraw", "extracted", "PassageOfTimeDysphoria_Data")
    chk = pd.read_csv(os.path.join(CHECKS, "Return1_DataCheck.csv"))
    ok = set(chk.loc[chk["isComplete"] == True, "taskFile"].map(os.path.basename))  # noqa: E712
    pre, last, rest = [], [], []
    for f in sorted(glob.glob(os.path.join(root, "PilotData", "Return1", "*_Mmi_Return_*.csv"))):
        if os.path.basename(f) not in ok:
            continue
        d = pd.read_csv(f)
        tr = d[d["choice"].isin(["gamble", "certain"])]
        r = d.loc[d.index > tr.index.max(), "happySlider.response"].dropna().to_numpy(float)
        b = tr["blockHappySlider.response"].dropna()
        if len(b) == 0 or len(r) < 30:
            continue
        pre.append(b.iloc[0]); last.append(tr["happySlider.response"].dropna().iloc[-1]); rest.append(r[:30])
    rest = np.array(rest)
    return np.array(pre), np.array(last), rest, np.isclose(rest, 0.5).mean(1)


def rest_drift(name):
    """The rest period opening a Weekly-Rest cohort (18 ratings, no outcomes yet): ratings and spacing (s)."""
    files = sorted(glob.glob(SOURCES[name]))
    chk = pd.read_csv(os.path.join(CHECKS, f"{name.upper()}_DataCheck.csv"))
    ok = set(chk.loc[chk["isComplete"] == True, "taskFile"].map(os.path.basename))  # noqa: E712
    R, gap = [], None
    for f in files:
        if os.path.basename(f) not in ok:
            continue
        d = pd.read_csv(f)
        r = d.loc[d["returnLoop.thisN"].notna(), "happySlider.response"].to_numpy(float)
        if len(r) >= 18:
            R.append(r[:18])
        gap = float(d["iriDur"].dropna().iloc[0])
    return np.array(R), gap
