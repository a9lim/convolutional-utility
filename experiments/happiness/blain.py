"""News about later trials in Blain & Rutledge's car-race bandit (2020, eLife 9: e57977; data: GitHub
BastienBlain/MSWB_LearningNotReward, PublicCode/Blain_MoodTracksLearning_data.mat, no license stated).

75 participants, two 80-trial blocks each (stable: the better car wins 80%; volatile: the better car switches
every 20 trials), order counterbalanced. Each trial shows both cars' reward magnitudes (10-80 points, random);
one car wins the race; "How happy are you right now?" after every 3-4 trials (46 ratings).

Unlike the Great Brain Experiment, an outcome here is news about later trials: it moves the belief q about
which car wins, and with it the value of every remaining trial. The felt contribution of trial t, read in the
canonical model's channels:
  magnitude:  EVm = p M (anticipated at choice), RPEm = M (win - p)   (base utility win * M = EVm + RPEm)
  win itself: P = p (anticipated),  PPE = win - p                      (if winning per se is felt)
  later:      Vnext = V(q_{t+1}) (anticipation of the remaining trials, a level),
              dV = V(q_{t+1}) - [q V(q+) + (1 - q) V(q-)] (news about later trials: the next trial's value
              after the outcome minus its forecast before it, which averages over the outcome),
              and Wnext, dW the same for the probability of winning a later trial
with p the believed win probability of the chosen car, M its magnitude / 80, and V(q) the expected reward of
a future trial under the participant's own choice rule at belief q (W(q) its probability of a win). PPE and
dV, dW can differ in sign: a win on the car believed worse usually makes the race less predictable later, so
it pays now and is bad news about later trials (not always: a large update can overshoot past 1/2).
"""
import os

import numpy as np
import scipy.io
from scipy.optimize import minimize
from scipy.special import expit

HERE = os.path.dirname(os.path.abspath(__file__))
MAT = os.path.join(HERE, "..", "..", "data", "blain", "Blain_MoodTracksLearning_data.mat")
TIDY = os.path.join(HERE, "..", "..", "data", "blain", "tidy.npz")
PAIRS = np.array([[10, 10], [10, 60], [10, 40], [10, 80], [60, 10], [20, 40], [40, 10], [40, 20], [40, 40],
                  [80, 10]], float) / 80.0
B = 80  # trials per block
BETA_MAX = 50.0  # the paper's bound on the inverse temperature


def tidy(mat=MAT, out=TIDY):
    """Per participant x 160 trials: magnitude of car 1 and car 2 (/80), car chosen (0/1), car 1 won,
    reward (/80), happiness (0-1, NaN unrated); block environment (1 volatile) per participant x 2."""
    M = scipy.io.loadmat(mat, struct_as_record=False, squeeze_me=True)
    rows = {k: [] for k in ("m1", "m2", "ch", "w1", "rew", "h", "vol", "group")}
    for gi, key in enumerate(("stable2volatile_data", "volatile2stable_data")):
        for s in M[key]:
            d = s.main
            X = np.asarray(d.maintask, float)
            lp = np.asarray(d.list_pair) - 1                    # lp[side, t] = car on that side
            side = X[:, 4].astype(int) - 1
            car = lp[side, np.arange(160)]
            mag_side = X[:, 2:4] / 80.0
            m = np.zeros((160, 2))
            for sd in (0, 1):
                m[np.arange(160), lp[sd]] = mag_side[:, sd]
            win = X[:, 14] > 0
            w1 = np.where(car == 0, win, ~win)
            assert np.allclose(np.where(win, m[np.arange(160), car], 0), X[:, 16] / 80.0)
            mu = np.asarray(d.task_mu)
            vol = [int((np.diff(mu[0, b * B:(b + 1) * B]) != 0).sum() > 0) for b in (0, 1)]
            rows["m1"].append(m[:, 0]); rows["m2"].append(m[:, 1]); rows["ch"].append(car)
            rows["w1"].append(w1.astype(float)); rows["rew"].append(X[:, 16] / 80.0)
            rows["h"].append(X[:, 7]); rows["vol"].append(vol); rows["group"].append(gi)
    np.savez_compressed(out, **{k: np.array(v) for k, v in rows.items()})
    return out


def load(path=TIDY):
    if not os.path.exists(path):
        tidy(out=path)
    return dict(np.load(path))


# --- the learner: a delta rule on q = P(car 1 wins), fitted to choices in each environment separately by
# Blain & Rutledge's additive rule, P(car 1) = sigmoid(beta [phi (2q - 1) + (1 - phi)(M1 - M2)])

def beliefs(w1, vol, lr):
    """q before each trial (reset to 1/2 at each block's start)."""
    q = np.empty(160)
    for b in (0, 1):
        x, a = 0.5, lr[vol[b]]
        for t in range(b * B, (b + 1) * B):
            q[t] = x
            x += a * (w1[t] - x)
    return q


def choice_nll(p, D, i):
    """p = (logit lr, log beta, logit phi) for one environment; the other block's trials are not scored."""
    env = p[3]
    lr = np.array([0.5, 0.5]); lr[int(env)] = 1 / (1 + np.exp(-p[0]))
    beta, phi = min(np.exp(p[1]), BETA_MAX), 1 / (1 + np.exp(-p[2]))
    q = beliefs(D["w1"][i], D["vol"][i], lr)
    v = beta * (phi * (2 * q - 1) + (1 - phi) * (D["m1"][i] - D["m2"][i]))
    c = D["ch"][i] == 0
    ll = np.logaddexp(0, -v) * c + np.logaddexp(0, v) * ~c
    blk = np.repeat(D["vol"][i], B) == env
    return float(ll[blk].sum())


def fit_learner(D, i):
    """Per environment: learning rate, softmax beta (at most 50) and probability weight phi (as Blain &
    Rutledge fit each environment separately). Returns arrays indexed by environment (0 stable, 1 volatile)."""
    out = dict(lr=np.zeros(2), beta=np.zeros(2), phi=np.zeros(2), nll=0.0)
    for env in (0, 1):
        best = None
        for lr0 in (-1.5, 0.0):
            for ph0 in (-0.5, 0.5):
                r = minimize(lambda x: choice_nll(np.r_[x, env], D, i), [lr0, np.log(5.0), ph0],
                             method="Nelder-Mead", options=dict(maxiter=4000, xatol=1e-4, fatol=1e-6))
                if best is None or r.fun < best.fun:
                    best = r
        x = best.x
        out["lr"][env], out["beta"][env] = 1 / (1 + np.exp(-x[0])), min(np.exp(x[1]), BETA_MAX)
        out["phi"][env] = 1 / (1 + np.exp(-x[2]))
        out["nll"] += float(best.fun)
    return out


def value(q, beta, phi):
    """A future trial at belief q under the participant's choice rule, averaged over the task's ten magnitude
    pairs and both car-to-pair assignments (each pair appears 16 times per 160): expected reward (/80) and
    probability of winning."""
    q = np.asarray(q, float)[..., None]
    rew = win = 0.0
    for P in (PAIRS, PAIRS[:, ::-1]):
        m1, m2 = P[:, 0], P[:, 1]
        c1 = expit(beta * (phi * (2 * q - 1) + (1 - phi) * (m1 - m2)))
        rew = rew + (c1 * q * m1 + (1 - c1) * (1 - q) * m2).mean(-1)
        win = win + (c1 * q + (1 - c1) * (1 - q)).mean(-1)
    return rew / 2, win / 2


NAMES = ["EVm", "RPEm", "P", "PPE", "Vnext", "dV", "Wnext", "dW"]


def regressors(D, fits):
    """Per participant x 160 x k, in NAMES order: the trial's own channels (EVm, RPEm, P, PPE), and the
    forecast of a later trial after the outcome and its revision, for reward (Vnext, dV) and for winning
    (Wnext, dW)."""
    n = len(D["h"])
    F = np.zeros((n, 160, len(NAMES)))
    extra = dict(q=np.zeros((n, 160)), p=np.zeros((n, 160)))
    for i in range(n):
        f = fits[i]
        q = beliefs(D["w1"][i], D["vol"][i], f["lr"])
        car = D["ch"][i]
        p = np.where(car == 0, q, 1 - q)
        Mc = np.where(car == 0, D["m1"][i], D["m2"][i])
        win = np.where(car == 0, D["w1"][i], 1 - D["w1"][i])
        env = np.repeat(D["vol"][i], B)
        lr = f["lr"][env]
        qn = q + lr * (D["w1"][i] - q)                       # belief after the outcome
        qp, qm = q + lr * (1 - q), (1 - lr) * q              # after car 1 wins, after car 2 wins
        Vn, Wn, Vp, Wp, Vm, Wm = (np.zeros(160) for _ in range(6))
        for e in (0, 1):
            s_ = env == e
            Vn[s_], Wn[s_] = value(qn[s_], f["beta"][e], f["phi"][e])
            Vp[s_], Wp[s_] = value(qp[s_], f["beta"][e], f["phi"][e])
            Vm[s_], Wm[s_] = value(qm[s_], f["beta"][e], f["phi"][e])
        # the innovation: the next trial's value after the outcome, minus its forecast before it (which already
        # averages over the outcome, since the belief will have moved by the next choice)
        dV = Vn - (q * Vp + (1 - q) * Vm)
        dW = Wn - (q * Wp + (1 - q) * Wm)
        F[i] = np.stack([p * Mc, Mc * (win - p), p, win - p, Vn, dV, Wn, dW], -1)
        extra["q"][i], extra["p"][i] = q, p
    return F, list(NAMES), extra


# --- ratings and the memory kernel, by block

def ratings(D):
    """Happiness z-scored within participant and block; NaN where unrated."""
    h = D["h"].copy()
    z = np.full_like(h, np.nan)
    for b in (0, 1):
        x = h[:, b * B:(b + 1) * B]
        z[:, b * B:(b + 1) * B] = (x - np.nanmean(x, 1, keepdims=True)) / np.nanstd(x, 1, keepdims=True)
    return z


def kernel(gam, kap, L=B):
    """Jump kernel (1, kappa, kappa gamma, ...); gamma = kappa is Rutledge's single geometric."""
    return np.r_[1.0, kap * gam ** np.arange(L - 1)]


def filtered(F, k):
    """sum_{j <= t} k(t - j) F_j within each block (the break between blocks ends the echo)."""
    out = np.zeros_like(F)
    T = np.zeros((B, B))
    for t in range(B):
        T[t, :t + 1] = k[:t + 1][::-1]
    for b in (0, 1):
        sl = slice(b * B, (b + 1) * B)
        out[:, sl] = np.einsum("st,ptk->psk", T, F[:, sl])
    return out


def design(F, gam, kap, trend=True):
    X = filtered(F, kernel(gam, kap))
    if trend:                                               # drift within a block (Jangraw et al. 2023)
        tt = np.tile(np.arange(B) / B, 2)
        X = np.concatenate([X, np.broadcast_to(tt[None, :, None], X.shape[:2] + (1,))], -1)
    return X


def lsq(X, z, sel, w=None):
    """Least squares with a fixed effect per participant-block, on participants sel. Returns w, rss, n."""
    Xs, zs = X[sel], z[sel]
    rows_X, rows_y = [], []
    for b in (0, 1):
        sl = slice(b * B, (b + 1) * B)
        m = ~np.isnan(zs[:, sl])
        cnt = m.sum(1, keepdims=True)
        xm = np.where(m[..., None], Xs[:, sl], 0).sum(1, keepdims=True) / cnt[..., None]
        ym = np.where(m, zs[:, sl], 0).sum(1, keepdims=True) / cnt
        rows_X.append((Xs[:, sl] - xm)[m]); rows_y.append((zs[:, sl] - ym)[m])
    A, y = np.concatenate(rows_X), np.concatenate(rows_y)
    if w is None:
        w = np.linalg.lstsq(A, y, rcond=None)[0]
    r = y - A @ w
    return w, float(r @ r), len(y)


def best_kernel(F, z, sel, jump=True):
    def rss(p):
        g = float(np.clip(p[0], 0.0, 0.999))
        k = float(np.clip(p[1], 0.0, 2.0)) if jump else g
        return lsq(design(F, g, k), z, sel)[1]
    grid = [(g, k) for g in np.arange(0.1, 1.0, 0.1) for k in (np.arange(0.0, 1.01, 0.2) if jump else [g])]
    p0 = min(grid, key=rss)
    p = minimize(rss, p0 if jump else [p0[0]], method="Nelder-Mead", options=dict(xatol=1e-3, fatol=1e-7)).x
    g = float(np.clip(p[0], 0.0, 0.999))
    return g, (float(np.clip(p[1], 0.0, 2.0)) if jump else g)
