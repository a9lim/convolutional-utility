"""The observer: an agent that chooses its beliefs to maximize its own felt life-sum (core N3, canonical).

An event is announced at 0 and resolves at s with outcome z_hi (objective probability p) or z_lo. At each
t < s the self holds a subjective probability q_t of the high outcome. Its forecasts of experienced
utility are rational given q_t, expected news included, and it expects to keep q_t until s. A change of
belief revises forecasts, so it is felt as news; realization is news against the last belief. Welfare is
the objective expected life-sum, less a cost of self-deception sum_t KL(q_t || p) / tau.

Closed forms (core N3): with the remaining-life resolvent R_t and its column g_t, the self at t forecasts
x_t = R_t(E_q u + mem_t) + Nbar_q R_t[:, s-t] + s_t g_t, where s_t is its felt news against x_{t-1} and
Nbar_q = E_q[psi(z - E_q z - Nbar_q)] the news it expects at s; psi has slopes kt = kappa/(1-kappa) and
lt kt, lt = lam(1-kappa)/(1-lam kappa), kappa = kn . g_s. After s: e = R_s(u + mem_s) + psi(z - E z - Nbar) g_s.
"""
import numpy as np
import torch


torch.set_default_dtype(torch.float64)


def K_matrix(T, a, al, m, mu):
    d = np.arange(T)[None, :] - np.arange(T)[:, None]
    return np.where(d > 0, a * al ** np.clip(d, 0, None), 0.0) + np.where(d < 0, m * mu ** np.clip(-d, 0, None), 0.0)


class World:
    def __init__(self, T, s, a, al, m, mu, n, nu, lam):
        self.T, self.s, self.lam = T, s, lam
        K = K_matrix(T, a, al, m, mu)
        self.K = torch.tensor(K)
        self.R = [torch.tensor(np.linalg.inv(np.eye(T - t) - K[t:, t:])) for t in range(T)]
        self.kn = torch.tensor(n * nu ** np.arange(T))
        if max(lam * float(self.kn[:T - t] @ self.R[t][:, 0]) for t in range(T)) >= 1:
            raise ValueError("past the news threshold")
        kap = float(self.kn[:T - s] @ self.R[s][:, 0])
        self.kt, self.lt = kap / (1 - kap), lam * (1 - kap) / (1 - lam * kap)

    def psi(self, y):
        return torch.where(y >= 0, self.kt * y, self.lt * self.kt * y)

    def nbar(self, q, zh, zl):
        """Expected news at s under belief q: Nbar = q psi(zh - Ez - Nbar) + (1-q) psi(zl - Ez - Nbar).
        Piecewise linear in Nbar: solve each branch pair in closed form and keep the consistent one."""
        Ez = q * zh + (1 - q) * zl
        ah, al_ = zh - Ez, zl - Ez
        for ch in (1.0, self.lt):
            for cl in (1.0, self.lt):
                N = self.kt * (q * ch * ah + (1 - q) * cl * al_) / (1 + self.kt * (q * ch + (1 - q) * cl))
                if ((ah - N >= 0) == (ch == 1.0)) and ((al_ - N >= 0) == (cl == 1.0)):
                    return N
        raise RuntimeError("no consistent branch")

    def news(self, d, g, kn):
        """Felt news s = kn . phi(d + s g). Below the threshold h(s) = s - kn . phi(d + s g) is increasing,
        so the root's piece is found by evaluating h at every kink at once; the piece's affine solution
        carries the gradient."""
        with torch.no_grad():
            dn, gn, kv, lam = d.numpy(), g.numpy(), kn.numpy(), self.lam
            br = np.sort(-dn / gn)                         # g > 0 on the remaining life
            X = dn[None, :] + br[:, None] * gn[None, :]
            h = br - (np.where(X >= 0, X, lam * X) @ kv)
            k = np.searchsorted(h, 0.0)                    # first kink with h >= 0
            lo = br[k - 1] if k > 0 else br[0] - 1.0
            hi = br[k] if k < len(br) else br[-1] + 1.0
            mid = (lo + hi) / 2
        c = torch.where(d + mid * g >= 0, 1.0, self.lam)
        return (kn @ (c * d)) / (1 - kn @ (c * g))

    def run(self, q, zh, zl, p, prior="none"):
        """Felt life for belief path q (length s). Returns (welfare, e_pre, e_post_hi, e_post_lo)."""
        T, s = self.T, self.s
        if prior == "none":
            x_prev = torch.zeros(T)
        else:  # calibrated: the rational forecast under p, so q_0 = p is no news
            Ez = p * zh + (1 - p) * zl
            uh = torch.zeros(T)
            uh[s] = Ez
            x_prev = self.R[0] @ uh + self.nbar(torch.tensor(p), zh, zl) * self.R[0][:, s]
        e_pre = []
        for t in range(s):
            Rt = self.R[t]
            mem = self.K[t:, :t] @ torch.stack(e_pre) if t else torch.zeros(T - t)
            Ez = q[t] * zh + (1 - q[t]) * zl
            uh = torch.zeros(T - t)
            uh = uh + torch.nn.functional.one_hot(torch.tensor(s - t), T - t) * Ez
            x0 = Rt @ (uh + mem) + self.nbar(q[t], zh, zl) * Rt[:, s - t]
            st = self.news(x0 - x_prev[t:], Rt[:, 0], self.kn[:T - t])
            x = x0 + st * Rt[:, 0]
            e_pre.append(x[0])
            x_prev = torch.cat([torch.zeros(t), x])
        e_pre = torch.stack(e_pre)
        mem_s = self.K[s:, :s] @ e_pre
        Ez, Nb = q[-1] * zh + (1 - q[-1]) * zl, self.nbar(q[-1], zh, zl)
        post = []
        for z in (zh, zl):
            u = torch.zeros(T - s)
            u[0] = z
            post.append(self.R[s] @ (u + mem_s) + self.psi(z - Ez - Nb) * self.R[s][:, 0])
        W = e_pre.sum() + p * post[0].sum() + (1 - p) * post[1].sum()
        return W, e_pre, post[0], post[1]


def kl(q, p):
    return q * torch.log(q / p) + (1 - q) * torch.log((1 - q) / (1 - p))


def objective(world, q, zh, zl, p, tau):
    return world.run(q, zh, zl, p)[0] - kl(q, p).sum() / tau


def best_step_path(world, zh, zl, p, tau, grid=49):
    """Best path that is calibrated far out and constant over the last L periods (a grid search)."""
    best = (-np.inf, None)
    with torch.no_grad():
        for L in range(1, world.s + 1):
            for ql in np.linspace(0.02, 0.98, grid):
                q = torch.tensor([p] * (world.s - L) + [ql] * L)
                f = float(objective(world, q, zh, zl, p, tau))
                if f > best[0]:
                    best = (f, q)
    return best


def optimal_beliefs(world, zh, zl, p, tau, steps=3000, lr=0.05):
    """Optimum of W - sum_t KL(q_t || p)/tau over belief paths. The objective has kinks wherever two
    consecutive beliefs agree (a zero revision, priced at lam on one side), so beliefs are sticky and
    smooth optimizers stall; Adam with a decaying rate, started from the calibrated path, two tilted
    ones and the best step path, handles them."""
    p_logit = float(np.log(p / (1 - p)))
    step = best_step_path(world, zh, zl, p, tau)
    inits = [torch.full((world.s,), p_logit + d) for d in (0.0, -1.0, 1.0)]
    inits.append(torch.logit(step[1].clamp(1e-6, 1 - 1e-6)))
    best = step
    for th0 in inits:
        th = th0.clone().requires_grad_(True)
        opt = torch.optim.Adam([th], lr=lr)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
        for _ in range(steps):
            opt.zero_grad()
            q = torch.sigmoid(th)
            f = objective(world, q, zh, zl, p, tau)
            (-f).backward()
            opt.step()
            sched.step()
            if f.item() > best[0]:
                best = (f.item(), q.detach().clone())
    return best
