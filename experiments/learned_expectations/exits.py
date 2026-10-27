"""The exit agent (notes/death.md, chosen dates): does a learner learn to exit? Sketched 2026-10-27, not yet run.

A foreseen base path u_t over T moments (a good life with a bad patch) and a tabular exit policy pi_t, the
probability of making t the last moment if alive at t (t < T - 1; the life ends at T - 1 regardless). World tau is
the last lived moment; moments after it do not exist: no felt state, anticipation, memory or news. Felt utility is
the canonical model, recursive echoes and felt news kinked per horizon, with optional biphasic memory (adaptation
c g^j of mass h = c g/(1 - g), notes/adaptation.md). Forecasts are Bayesian under a self-model of the same policy,
so they include anticipated news; at t, world tau's self knows tau if tau <= t (its own exit now) and otherwise
holds the self-model's stopping distribution after t. The life and the policy are expected from birth: before
it, every world holds the policy's prior over last moments, so the first self feels news only of its own deviation.

Learners (the dial as in scheduling.py: forecasts use pi.detach() + w (pi - pi.detach())):
- momentary: each self ascends its own felt state with past selves' forecasts fixed; its incentive is
  e[t, t] - E[e[tau, t] | tau > t], exiting against continuing, in utility units (death.md's rule);
- remaining-life: the life-sum at w = 0, each self's fixed-past incentive, normalized as in scheduling.learn;
- planner: the life-sum at w = 1.
Exact benchmarks: deterministic plans solved by the same engine. An off-path world's felt states are the felt
states of a deviation into it, so one solve evaluates every one-shot deviation from a plan, with death.md's
prescribed continuation (never exit again).
"""
import numpy as np
import torch

from felt import kernel_parts

torch.set_default_dtype(torch.float64)


class Exits:
    def __init__(self, u, a, al, m, mu, n, nu, lam=1.0, h=0.0, g=0.9):
        T = len(u)
        self.T, self.lam, self.n = T, lam, n
        Kf, Kb, Kn = kernel_parts(T, a, al, m, mu, n, nu)
        if h:
            c = h * (1 - g) / g
            d = np.arange(T)[:, None] - np.arange(T)[None, :]
            Kb = Kb - np.where(d > 0, c * g ** np.clip(d, 0, None), 0.0)
        self.Kf, self.Kb, self.Kn = (torch.tensor(K) for K in (Kf, Kb, Kn))
        self.u = torch.tensor(np.asarray(u, float))
        tau, t = torch.meshgrid(torch.arange(T), torch.arange(T), indexing="ij")
        self.alive = (t <= tau).to(torch.float64)                       # [tau, t]

    def policy(self, theta):
        """pi_t for t < T - 1, and 1 at T - 1, the natural end."""
        return torch.cat([torch.sigmoid(theta), torch.ones(1)])

    @staticmethod
    def stop_dist(pi):
        surv = torch.cat([torch.ones(1), torch.cumprod(1 - pi[:-1], 0)])
        return surv * pi

    def forecasts(self, pi_f):
        """Q[t + 1, tau, tau']: the weight world tau's self at t puts on world tau'; Q[0] is the prior."""
        T = self.T
        rows = [self.stop_dist(pi_f)[None, :].expand(T, T)]
        for t in range(T):
            cond = self.stop_dist(pi_f[t + 1:]) if t + 1 < T else torch.zeros(0)
            wait = torch.cat([torch.zeros(t + 1), cond])
            rows.append(torch.where((torch.arange(T) > t)[:, None], wait[None, :], torch.eye(T)))
        return torch.stack(rows)

    def solve(self, Q, iters=60):
        """Felt states e[tau, t], zero after tau: base, anticipation of forecasts, memory within the world, and news
        on Q_t e - Q_{t-1} e at every horizon (Q_{-1} the prior). Linear given the sign of each news term, so
        iterate the signs; the final solve carries the gradient."""
        T, lam = self.T, self.lam
        Q, D = Q[1:], Q[1:] - Q[:-1]
        L0 = torch.einsum("tu,tab->atbu", self.Kf, Q) + torch.einsum("tu,ab->atbu", self.Kb, torch.eye(T))
        live = self.alive.reshape(-1)
        u, I, c = (self.alive * self.u[None, :]).reshape(-1), torch.eye(T * T), torch.ones(T, T, T)
        for _ in range(iters):
            L = (L0 + torch.einsum("tu,atu,tab->atbu", self.Kn, c, D)).reshape(T * T, T * T) * live[:, None]
            e = torch.linalg.solve(I - L, u).reshape(T, T)
            if lam == 1.0:
                return e
            with torch.no_grad():
                c_new = torch.where(torch.einsum("tab,bu->atu", D, e) < -1e-13, lam, 1.0)
            if torch.equal(c_new, c):
                return e
            c = c_new
        raise RuntimeError("news sign pattern did not settle")

    def run(self, theta, w=1.0):
        """Felt states in every world, the expected life-sum, and the distribution of the last moment."""
        pi = self.policy(theta)
        pi_f = pi.detach() + w * (pi - pi.detach())
        P = self.stop_dist(pi)
        e = self.solve(self.forecasts(pi_f))
        return P @ e.sum(1), e, P

    def momentary(self, e, pi):
        """Each self's felt state exiting minus continuing, e[t, t] - E[e[tau, t] | tau > t], for t < T - 1."""
        return torch.stack([e[t, t] - self.stop_dist(pi[t + 1:]) @ e[t + 1:, t] for t in range(self.T - 1)])


def initial(T, kind, t_exit=None):
    """Starting logits: naive (rarely exits, expects to continue), uniform (exit uniform over the remaining dates,
    scheduling.learn's start) or primed (a weakly held plan to exit at t_exit, rarely otherwise)."""
    rare = float(torch.logit(torch.tensor(1e-3)))
    if kind == "naive":
        return torch.full((T - 1,), rare)
    if kind == "uniform":
        return torch.logit(1 / torch.arange(T, 1, -1, dtype=torch.float64))
    th = torch.full((T - 1,), rare)
    th[t_exit] = 0.0
    return th


def learn(ex, kind, init="uniform", t_exit=None, steps=3000, lr=0.1, noise=0.5, seed=0):
    """kind: momentary, remaining or planner. Returns the learned distribution of the last moment."""
    gen = torch.Generator().manual_seed(seed)
    th = (initial(ex.T, init, t_exit) + noise * torch.randn(ex.T - 1, generator=gen)).requires_grad_(True)
    opt = torch.optim.Adam([th], lr=lr, betas=(0.9, 0.9))
    decay = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    for _ in range(steps):
        opt.zero_grad()
        if kind == "momentary":
            with torch.no_grad():
                pi = ex.policy(th)
                th.grad = -ex.momentary(ex.solve(ex.forecasts(pi)), pi)
        else:
            W, _, _ = ex.run(th, 0.0 if kind == "remaining" else 1.0)
            (-W).backward()
            with torch.no_grad():
                pi = torch.sigmoid(th)
                reach = torch.cat([torch.ones(1), torch.cumprod(1 - pi, 0)])[:-1]
                th.grad /= (reach * pi * (1 - pi)).clamp_min(1e-300)
        opt.step()
        decay.step()
        with torch.no_grad():
            th.clamp_(-30, 30)
    with torch.no_grad():
        return ex.stop_dist(ex.policy(th))


def plan(T, tau):
    """Logits for 'exit after tau, never again off path' (tau = T - 1: never exit)."""
    th = torch.full((T - 1,), -30.0)
    if tau < T - 1:
        th[tau] = 30.0
    return th


def equilibria(ex, taus, tol=1e-12):
    """The plans among taus (and never exiting) that are equilibria for momentary selves, with the never-exit
    continuation off path, and each plan's felt path."""
    out = {}
    for tau in sorted(set(taus) | {ex.T - 1}):
        with torch.no_grad():
            pi = ex.policy(plan(ex.T, tau))
            e = ex.solve(ex.forecasts(pi))
            gain = ex.momentary(e, pi)
        ok = all(gain[t] <= tol for t in range(ex.T - 1) if t != tau) and (tau == ex.T - 1 or gain[tau] >= -tol)
        if ok:
            out[tau] = e[tau, :tau + 1].clone()
    return out


if __name__ == "__main__":
    # Self-checks, CPU, seconds: the never-exit plan against a direct foreseen solve; the lam = 1 exit incentive
    # against death.md's S/(1 - n); the full (w = 1) gradient against finite differences (w = 0 omits the forecast
    # channel by design).
    from felt import LIFE
    prm = {k: v for k, v in LIFE.items() if k != "lam"}
    T, t0 = 24, 10
    u = np.ones(T)
    u[t0 + 1] = -3.0
    Kf, Kb, _ = kernel_parts(T, *(prm[k] for k in ("a", "al", "m", "mu", "n", "nu")))
    direct = np.linalg.solve(np.eye(T) - Kf - Kb, u)
    for lam in (1.0, 2.0):
        ex = Exits(u, **prm, lam=lam)
        with torch.no_grad():
            pi = ex.policy(plan(T, T - 1))
            e = ex.solve(ex.forecasts(pi))
        print(f"lam {lam}: never-exit plan against the foreseen solve {np.abs(e[T - 1].numpy() - direct).max():.1e}")
    ex = Exits(u, **prm)
    with torch.no_grad():
        pi = ex.policy(plan(T, T - 1))
        gain = ex.momentary(ex.solve(ex.forecasts(pi)), pi).numpy()
    j = np.arange(1, T)
    S = [-sum((prm["a"] * prm["al"] ** j[:T - 1 - t] + prm["n"] * prm["nu"] ** j[:T - 1 - t]) * direct[t + 1:])
         for t in range(T - 1)]
    print(f"lam 1: exit incentive against -S/(1 - n) {np.abs(gain - np.array(S) / (1 - prm['n'])).max():.1e}")
    th = initial(T, "uniform") + 0.3 * torch.randn(T - 1, generator=torch.Generator().manual_seed(0))
    ex2 = Exits(u, **prm, lam=2.0, h=0.5, g=0.85)
    thg = th.clone().requires_grad_(True)
    ex2.run(thg)[0].backward()
    fd = [(float(ex2.run(th + d)[0]) - float(ex2.run(th - d)[0])) / 2e-6 for d in 1e-6 * torch.eye(T - 1)[[0, 9, 17]]]
    print(f"w 1, lam 2, biphasic: gradient against finite differences "
          f"{max(abs(float(thg.grad[i]) - f) for i, f in zip((0, 9, 17), fd)):.1e}")
