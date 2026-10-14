"""The scheduling agent (decision.md D3): learning to time one pleasure, with the J dial as a gradient setting.

A pleasure of value v is announced at 0 and must be taken in [0, T). The policy is tabular: pi_t, the
probability of taking it at t if not yet taken (forced at T-1). Felt utility is the canonical model with
recursive echoes and felt news, forecasts rational under a self-model of the same policy. With linear
news (lam = 1) forecasts are linear in the policy, so every world (the date tau it is taken) is solved
exactly. With lam > 1 the forecasts leave out anticipated news (certainty-equivalent in news); deterministic
plans carry none, so the fixed points are still exactly the credible plans of decision.md D3, though the
learning path differs. Per world: at t, world tau knows tau if tau <= t and otherwise expects u from the self-model's stopping
distribution after t; then x_t = R_t(E_t u + mem_t) + s_t g_t, s_t = kn.(x0_t - x_{t-1})/(1 - kappa_t).

The dial: forecasts use pi_f = pi.detach() + w (pi - pi.detach()).
- w = 0: no gradient through past selves' forecasts of the policy. Gradient ascent on the life-sum then
  gives each self its fixed-past incentive (the past does not depend on its own action), so fixed points
  are sophisticated fixed-past (CDT) equilibria.
- w = 1: the full gradient, including how the policy shaped past anticipation: the commitment planner.
"""
import numpy as np
import torch

torch.set_default_dtype(torch.float64)


def K_matrix(T, a, al, m, mu):
    d = np.arange(T)[None, :] - np.arange(T)[:, None]
    return np.where(d > 0, a * al ** np.clip(d, 0, None), 0.0) + np.where(d < 0, m * mu ** np.clip(-d, 0, None), 0.0)


class Schedule:
    def __init__(self, T, a, al, m, mu, n, nu, v=1.0, lam=1.0):
        self.T, self.v, self.lam = T, v, lam
        K = K_matrix(T, a, al, m, mu)
        self.K = torch.tensor(K)
        self.R = [torch.tensor(np.linalg.inv(np.eye(T - t) - K[t:, t:])) for t in range(T)]
        self.kn = torch.tensor(n * nu ** np.arange(T))
        self.kap = [float(self.kn[:T - t] @ self.R[t][:, 0]) for t in range(T)]
        if lam * max(self.kap) >= 1:
            raise ValueError("past the news threshold")

    def news(self, d, g, kn):
        """Felt news per world, s = kn . phi_lam(d + s g). Linear at lam = 1; otherwise the root's piece is
        found at every kink at once (h is increasing below the threshold) and its affine solution carries
        the gradient."""
        if self.lam == 1.0:
            return (d @ kn) / (1 - kn @ g)
        lam, n = self.lam, d.shape[1]
        with torch.no_grad():
            br = torch.sort(-d / g, dim=1).values
            X = d[:, None, :] + br[:, :, None] * g[None, None, :]
            h = br - (torch.where(X >= 0, X, lam * X) * kn).sum(-1)
            k = (h < 0).sum(1)
            rows = torch.arange(d.shape[0])
            lo = torch.where(k > 0, br[rows, (k - 1).clamp_min(0)], br[:, 0] - 1)
            hi = torch.where(k < n, br[rows, k.clamp_max(n - 1)], br[:, -1] + 1)
            mid = (lo + hi) / 2
        c = torch.where(d + mid[:, None] * g >= 0, 1.0, lam)
        return ((c * d) @ kn) / (1 - (c * g) @ kn)

    def policy(self, theta):
        return torch.cat([torch.sigmoid(theta), torch.ones(1)])

    @staticmethod
    def stop_dist(pi):
        """P(tau = k) for the stopping time of per-period take probabilities pi."""
        surv = torch.cat([torch.ones(1), torch.cumprod(1 - pi[:-1], 0)])
        return surv * pi

    def run(self, theta, w=1.0):
        """Felt experience in every world (rows: tau, columns: t) and the welfare E[sum_t e_t]."""
        T, v = self.T, self.v
        pi = self.policy(theta)
        pi_f = pi.detach() + w * (pi - pi.detach())
        P = self.stop_dist(pi)
        worlds = torch.arange(T)
        cols, x_prev = [], torch.zeros(T, T)          # x_prev: each world's forecast of e_{t..} at t-1
        for t in range(T):
            n_rem = T - t
            # expected u_{t..} given information at t, per world
            cond = self.stop_dist(pi_f[t + 1:]) if t + 1 < T else torch.zeros(0)
            future = torch.cat([torch.zeros(1), v * cond])                      # not yet taken
            now = torch.nn.functional.one_hot(torch.tensor(0), n_rem) * v       # taken at t
            past = torch.zeros(n_rem)                                           # taken before t
            uh = torch.where((worlds > t)[:, None], future[None, :],
                             torch.where((worlds == t)[:, None], now[None, :], past[None, :]))
            mem = torch.stack(cols, 1) @ self.K[t:, :t].T if t else torch.zeros(T, n_rem)
            x0 = (uh + mem) @ self.R[t].T
            s = self.news(x0 - x_prev[:, t:], self.R[t][:, 0], self.kn[:n_rem])
            x = x0 + s[:, None] * self.R[t][:, 0][None, :]
            cols.append(x[:, 0])
            x_prev = torch.cat([torch.zeros(T, t), x], 1)
        e = torch.stack(cols, 1)
        return P @ e.sum(1), e, P


def learn(sched, w, steps=6000, lr=0.1, init=None, seed=0, conditional=True):
    """Gradient ascent on the life-sum with the dial at w. Each self's gradient is divided by the
    probability of reaching it and by its sigmoid slope, so the update follows that self's incentive
    conditional on being there (the fixed-past self at t), in utility units: off-path selves learn
    too, and saturated logits cannot stall a small incentive. Adam's second-moment memory is short so
    steps track the current incentives. Returns the stopping distribution."""
    g = torch.Generator().manual_seed(seed)
    T = sched.T
    # start near uniform over the remaining dates: take at t with probability 1/(T - t)
    th0 = init if init is not None else torch.logit(1 / torch.arange(T, 1, -1, dtype=torch.float64)) \
        + 0.5 * torch.randn(T - 1, generator=g)
    th = th0.clone().requires_grad_(True)
    opt = torch.optim.Adam([th], lr=lr, betas=(0.9, 0.9))
    decay = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    for _ in range(steps):
        opt.zero_grad()
        W, _, _ = sched.run(th, w)
        (-W).backward()
        if conditional:
            with torch.no_grad():
                pi = torch.sigmoid(th)
                reach = torch.cat([torch.ones(1), torch.cumprod(1 - pi, 0)])[:-1]
                th.grad /= (reach * pi * (1 - pi)).clamp_min(1e-300)
        opt.step()
        decay.step()
        with torch.no_grad():
            th.clamp_(-30, 30)
    with torch.no_grad():
        return sched.stop_dist(sched.policy(th))


def reference(sched, v=1.0):
    """Exact benchmarks (decision.md D3): the commitment date and the subgame-perfect fixed-past date
    (backward induction over credible plans, chosen at the announcement), plus the credible set C_1."""
    T = sched.T
    R = [r.numpy() for r in sched.R]
    kn = sched.kn.numpy()

    def news(d, t):
        out = sched.news(torch.tensor(d)[None, :], sched.R[t][:, 0], sched.kn[:T - t])
        return float(out[0])

    def delta(t, p, q):
        d = v * (R[t][:, q - t] - R[t][:, p - t])
        return d.sum() + R[t][:, 0].sum() * news(d, t)

    C = [T - 1]
    for t in range(T - 2, 0, -1):
        A = sorted(set([t] + C))
        C = [p for p in A if all(delta(t, p, q) <= 1e-12 for q in A if q != p)]
    W = np.array([(v * R[0][:, x] + news(v * R[0][:, x], 0) * R[0][:, 0]).sum() for x in range(T)])
    sched.C1 = C
    return int(max([0] + C, key=lambda x: W[x])), int(np.argmax(W)), W
