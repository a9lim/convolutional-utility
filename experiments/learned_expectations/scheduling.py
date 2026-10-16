"""The scheduling agent (decision.md D3): learning to time one pleasure, with the J dial as a gradient setting.

A pleasure of value v is announced at 0 and must be taken in [0, T). The policy is tabular: pi_t, the
probability of taking it at t if not yet taken (forced at T-1). Felt utility is the canonical model with
recursive echoes and felt news, forecasts rational under a self-model of the same policy: Bayesian over the
worlds tau (the date it is taken), so they include anticipated news. At t, world tau knows tau if tau <= t and
otherwise holds the self-model's stopping distribution after t. The felt fixed point is piecewise linear in
e[tau, t]; it is solved exactly by iterating on the sign pattern of the news terms. Deterministic plans carry
no anticipated news, so the credible plans of decision.md D3 are found by the deterministic recursion in
reference().

The dial: forecasts use pi_f = pi.detach() + w (pi - pi.detach()).
- w = 0: no gradient through past selves' forecasts of the policy. Gradient ascent on the life-sum then
  gives each self its fixed-past incentive (the past does not depend on its own action), so fixed points
  are sophisticated fixed-past (CDT) equilibria.
- w = 1: the full gradient, including how the policy shaped past anticipation: the commitment planner.
"""
import numpy as np
import torch

from felt import kernel_parts, news_root, resolvents

torch.set_default_dtype(torch.float64)


class Schedule:
    def __init__(self, T, a, al, m, mu, n, nu, v=1.0, lam=1.0):
        self.T, self.v, self.lam = T, v, lam
        Kf, Kb, Kn = kernel_parts(T, a, al, m, mu, n, nu)                       # [t, t']
        self.K = torch.tensor(Kf + Kb)
        self.R = [torch.tensor(R) for R in resolvents(Kf + Kb)]
        self.kn = torch.tensor(n * nu ** np.arange(T))
        self.kap = [float(self.kn[:T - t] @ self.R[t][:, 0]) for t in range(T)]
        if lam * max(self.kap) >= 1:
            raise ValueError("past the news threshold")
        self.Kf, self.Kb, self.Kn = torch.tensor(Kf), torch.tensor(Kb), torch.tensor(Kn)

    def policy(self, theta):
        return torch.cat([torch.sigmoid(theta), torch.ones(1)])

    @staticmethod
    def stop_dist(pi):
        """P(tau = k) for the stopping time of per-period take probabilities pi."""
        surv = torch.cat([torch.ones(1), torch.cumprod(1 - pi[:-1], 0)])
        return surv * pi

    def forecasts(self, pi_f):
        """Q[t, tau, tau']: the weight world tau's self at t puts on world tau' (its information set)."""
        T, rows = self.T, []
        for t in range(T):
            cond = self.stop_dist(pi_f[t + 1:]) if t + 1 < T else torch.zeros(0)
            wait = torch.cat([torch.zeros(t + 1), cond])
            rows.append(torch.where((torch.arange(T) > t)[:, None], wait[None, :], torch.eye(T)))
        return torch.stack(rows)

    def solve(self, Q, iters=60):
        """Felt experience e[tau, t]: e = u + anticipation of forecasts + memory + news, the news on
        Q_t e - Q_{t-1} e at every horizon (Q_{-1} = 0: the announcement is a surprise). Linear given the
        sign of each news term, so iterate the signs; the final solve carries the gradient."""
        T, lam = self.T, self.lam
        D = Q - torch.cat([torch.zeros(1, T, T), Q[:-1]])
        L0 = torch.einsum("tu,tab->atbu", self.Kf, Q) + torch.einsum("tu,ab->atbu", self.Kb, torch.eye(T))
        u, I, c = self.v * torch.eye(T).reshape(-1), torch.eye(T * T), torch.ones(T, T, T)
        for _ in range(iters):
            L = L0 + torch.einsum("tu,atu,tab->atbu", self.Kn, c, D)
            e = torch.linalg.solve(I - L.reshape(T * T, T * T), u).reshape(T, T)
            if lam == 1.0:
                return e
            with torch.no_grad():
                c_new = torch.where(torch.einsum("tab,bu->atu", D, e) < -1e-13, lam, 1.0)
            if torch.equal(c_new, c):
                return e
            c = c_new
        raise RuntimeError("news sign pattern did not settle")

    def run(self, theta, w=1.0):
        """Felt experience in every world (rows: tau, columns: t) and the welfare E[sum_t e_t]."""
        pi = self.policy(theta)
        pi_f = pi.detach() + w * (pi - pi.detach())
        P = self.stop_dist(pi)
        e = self.solve(self.forecasts(pi_f))
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

    def news(d, t):
        return float(news_root(torch.tensor(d)[None, :], sched.R[t][:, 0], sched.kn[:T - t], sched.lam)[0])

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


if __name__ == "__main__":
    # Self-checks: an independent damped iteration on the felt equations, finite-difference gradients, and
    # deterministic plans against the reduced form used by reference().
    T, prm = 20, (0.3, 0.7, 0.2, 0.6, 0.3, 0.7)
    sch = Schedule(T, *prm, lam=2.0)
    th = torch.logit(1 / torch.arange(T, 1, -1, dtype=torch.float64)) \
        + 0.5 * torch.randn(T - 1, generator=torch.Generator().manual_seed(0))
    W, e, _ = sch.run(th)
    Q = sch.forecasts(sch.policy(th)).numpy()
    Kf, Kb, Kn, u = sch.Kf.numpy(), sch.Kb.numpy(), sch.Kn.numpy(), np.eye(T)
    phi = lambda x: np.where(x >= 0, x, 2.0 * x)
    x = u.copy()
    for _ in range(100000):
        F = np.einsum("tab,bu->atu", Q, x)                                   # F[tau, t, t']: forecast at t
        Fp = np.concatenate([np.zeros((T, 1, T)), F[:, :-1]], 1)
        new = u + np.stack([F[:, t] @ Kf[t] + x @ Kb[t] + phi(F[:, t] - Fp[:, t]) @ Kn[t] for t in range(T)], 1)
        if np.abs(new - x).max() < 1e-12:
            break
        x = 0.3 * new + 0.7 * x
    print(f"damped iteration against the exact solve: {np.abs(new - e.numpy()).max():.1e}")
    thg = th.clone().requires_grad_(True)
    sch.run(thg)[0].backward()
    fd = [(float(sch.run(th + h)[0]) - float(sch.run(th - h)[0])) / 2e-6
          for h in 1e-6 * torch.eye(T - 1)[[0, 5, 12]]]
    print(f"gradient against finite differences: {max(abs(float(thg.grad[i]) - f) for i, f in zip((0, 5, 12), fd)):.1e}")
    _, _, Wref = reference(sch)
    det = [float(sch.run(torch.where(torch.arange(T - 1) == x_, 30.0, -30.0))[0]) for x_ in (0, 7, 15)]
    print(f"deterministic plans against the reduced form: {max(abs(a_ - Wref[x_]) for a_, x_ in zip(det, (0, 7, 15))):.1e}")
