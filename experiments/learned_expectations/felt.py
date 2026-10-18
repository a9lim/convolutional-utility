"""The felt engine: experienced utility of the canonical model (formalism/core.md) for every learner.

- Kernels: `K_matrix` (anticipation above the diagonal, memory below), `kernel_parts` (the anticipation, memory
  and news kernels apart), `resolvents` (the remaining-life resolvent at every date).
- `news_root`: the felt news s = kn . phi_lam(d + s g) of a forecast revision d, exact (piecewise linear).
- `Event`: one event with two outcomes and a belief held until it resolves, in closed form, batched over events
  (the game, partners, dependence and trust agents).
- `BeliefPath`: the same event under any belief path (the observer, core N3).
- `rounds_direct`, `rounds_canonical`: felt utility per round from realized payoffs and a critic's forecasts, the
  reinforcement-learning reading (the rounds agents).
- `kl`, the cost of self-deception; calibrations `LIFE` (weekly), `EVENT` (one game as an event) and `ROUNDS`
  (rounds of play), all canonical (linear news, lam = 1); `X4`, loss-averse news at its choice-revealed strength,
  as an override (`dict(EVENT, **X4)`).
`python felt.py` checks Event against BeliefPath (canonical and X4), Event's bilinear form at lam = 1, news_root
against a damped iteration, rounds_canonical against its defining fixed point, and rounds_direct's signed echoes.
"""
import numpy as np
import torch

torch.set_default_dtype(torch.float64)

LIFE = dict(a=0.0643, al=0.7, m=0.3967, mu=0.3, n=0.2, nu=0.7, lam=1.0)              # formalism/calibration.md, weekly
EVENT = dict(T=16, s=8, a=0.15, al=0.8, m=0.1, mu=0.6, n=0.3, nu=0.7, lam=1.0)       # one game as an event
ROUNDS = dict(a=0.3, m=0.2, mu=0.6, n=0.3, nu=0.8, lam=1.0)                          # per round; nu is the critic's discount
X4 = dict(lam=2.0)              # loss-averse news (core X4) at the choice-revealed strength; felt news is 1.0-1.2


def kernel_parts(T, a, al, m, mu, n, nu):
    """Kf[t, t'] anticipation (t' > t), Kb memory (t' < t), Kn news (t' >= t), each a geometric in |t' - t|."""
    d = np.arange(T)[None, :] - np.arange(T)[:, None]
    return (np.where(d > 0, a * al ** np.clip(d, 0, None), 0.0), np.where(d < 0, m * mu ** np.clip(-d, 0, None), 0.0),
            np.where(d >= 0, n * nu ** np.clip(d, 0, None), 0.0))


def K_matrix(T, a, al, m, mu):
    d = np.arange(T)[None, :] - np.arange(T)[:, None]
    return np.where(d > 0, a * al ** np.clip(d, 0, None), 0.0) + np.where(d < 0, m * mu ** np.clip(-d, 0, None), 0.0)


def resolvents(K):
    """R_t = (I - K[t:, t:])^{-1} for every t: the remaining life from t."""
    T = len(K)
    return [np.linalg.inv(np.eye(T - t) - K[t:, t:]) for t in range(T)]


def phi(x, lam):
    return torch.where(x >= 0, x, lam * x)


def news_root(d, g, kn, lam):
    """Felt news s = kn . phi_lam(d + s g) of revisions d (..., n), with g > 0 the column a felt change spreads
    through. Linear at lam = 1. Below the threshold h(s) = s - kn . phi_lam(d + s g) is increasing, so the root's
    piece is found by evaluating h at every kink at once; the piece's affine solution carries the gradient."""
    if lam == 1.0:
        return (d @ kn) / (1 - kn @ g)
    n = d.shape[-1]
    with torch.no_grad():
        D = d.reshape(-1, n)
        br = torch.sort(-D / g, dim=1).values
        X = D[:, None, :] + br[:, :, None] * g[None, None, :]
        h = br - (torch.where(X >= 0, X, lam * X) * kn).sum(-1)
        k = (h < 0).sum(1)
        rows = torch.arange(D.shape[0])
        lo = torch.where(k > 0, br[rows, (k - 1).clamp_min(0)], br[:, 0] - 1)
        hi = torch.where(k < n, br[rows, k.clamp_max(n - 1)], br[:, -1] + 1)
        mid = ((lo + hi) / 2).reshape(d.shape[:-1] + (1,))
    c = torch.where(d + mid * g >= 0, 1.0, lam)
    return ((c * d) @ kn) / (1 - (c * g) @ kn)


def kl(q, p):
    q, p = q.clamp(1e-9, 1 - 1e-9), torch.as_tensor(p).clamp(1e-9, 1 - 1e-9)
    return q * torch.log(q / p) + (1 - q) * torch.log((1 - q) / (1 - p))


class Event:
    """Felt welfare of one event with two outcomes and a belief held until it resolves, batched over events.

    An event is announced at 0 and resolves at s with outcome z_A (objective probability p) or z_B. The self holds
    belief q in outcome A from 0 until s. With the belief held, forecasts do not move before s, so the only felt
    news is the jolt at the announcement (against a no-event prior) and the news at s (core N3, canonical). With
    c = E_q z + Nbar_q the forecast change at 0 is c R_0[:, s], one-signed, so
      s_0 = c k_n.R_0[:, s] / (1 - k_n.g_0) if c >= 0, else lam c k_n.R_0[:, s] / (1 - lam k_n.g_0),
      e_pre = c R_0[:s, s] + s_0 g_0[:s]   (the forecast at 0 is realized until s),
      e_post(z) = R_s(z delta_0 + mem_s) + psi(z - E_q z - Nbar_q) g_s.
    Welfare is p sum e_post(z_A) + (1-p) sum e_post(z_B) + sum e_pre.
    """

    def __init__(self, T, s, a, al, m, mu, n, nu, lam):
        self.T, self.s, self.lam = T, s, lam
        K = K_matrix(T, a, al, m, mu)
        R = resolvents(K)
        R0, Rs = R[0], R[s]
        kn = n * nu ** np.arange(T)
        k0 = kn @ R0[:, 0]
        if lam * max(k0, kn[:T - s] @ Rs[:, 0]) >= 1:
            raise ValueError("past the news threshold")
        kap = kn[:T - s] @ Rs[:, 0]
        self.kt, self.lt = kap / (1 - kap), lam * (1 - kap) / (1 - lam * kap)
        self.R0s = torch.tensor(R0[:s, s])                   # pre-s rows of the event column
        self.g0 = torch.tensor(R0[:s, 0])
        self.jolt = (kn @ R0[:, s], k0)                      # numerator weight, loop gain at 0
        self.Kps = torch.tensor(K[s:, :s])                   # memory of the pre-s path in post-s rows
        self.Rs = torch.tensor(Rs)

    def psi(self, y):
        return torch.where(y >= 0, self.kt * y, self.lt * self.kt * y)

    def nbar(self, q, zA, zB):
        """Expected news at s under q, per event. With r the probability of the higher outcome and D the gap,
        gains are felt at slope kt and losses at lt kt, and the fixed point is
        N = -kt (lt - 1) r (1 - r) D / (1 + kt (r + lt (1 - r))): always the mixed branch, smooth in q."""
        r = torch.where(zA >= zB, q, 1 - q)
        D = (zA - zB).abs()
        return -self.kt * (self.lt - 1) * r * (1 - r) * D / (1 + self.kt * (r + self.lt * (1 - r)))

    def welfare(self, q, p, zA, zB):
        """Objective expected felt life-sum, batched over events."""
        Ez, Nb = q * zA + (1 - q) * zB, self.nbar(q, zA, zB)
        c = Ez + Nb
        num, k0 = self.jolt
        s0 = torch.where(c >= 0, c * num / (1 - k0), self.lam * c * num / (1 - self.lam * k0))
        e_pre = c[:, None] * self.R0s[None, :] + s0[:, None] * self.g0[None, :]          # (B, s)
        base = (e_pre @ self.Kps.T) @ self.Rs.T                                          # (B, T-s)
        g1 = self.Rs[:, 0].sum()
        post_A = base.sum(1) + (zA + self.psi(zA - Ez - Nb)) * g1
        post_B = base.sum(1) + (zB + self.psi(zB - Ez - Nb)) * g1
        return e_pre.sum(1) + p * post_A + (1 - p) * post_B

    def weights(self):
        """At lam = 1 welfare is bilinear, alpha m(q) + beta m(p) with m(x) = x z_A + (1 - x) z_B: beta weighs what
        happens (the outcome, its memory and the news it brings), alpha the forecast held from the announcement
        (its anticipation and jolt, less the letdown it sets up). Kinked news has no such form."""
        if self.lam != 1.0:
            raise ValueError("bilinear only at lam = 1")
        one, zero = torch.ones(1), torch.zeros(1)
        return float(self.welfare(one, zero, one, zero)[0]), float(self.welfare(zero, one, one, zero)[0])


class BeliefPath:
    """The observer's event under a belief path: at each t < s the self holds q_t, forecasts its felt life
    rationally given q_t (expected news included) and expects to keep q_t until s. A change of belief revises
    forecasts, so it is felt as news; realization is news against the last belief.

    Closed forms (core N3): with the remaining-life resolvent R_t and its column g_t, the self at t forecasts
    x_t = R_t(E_q u + mem_t) + Nbar_q R_t[:, s-t] + s_t g_t, where s_t is its felt news against x_{t-1} and
    Nbar_q = E_q[psi(z - E_q z - Nbar_q)] the news it expects at s; psi has slopes kt = kappa/(1-kappa) and
    lt kt, lt = lam(1-kappa)/(1-lam kappa), kappa = kn . g_s. After s: e = R_s(u + mem_s) + psi(z - E z - Nbar) g_s.
    """

    def __init__(self, T, s, a, al, m, mu, n, nu, lam):
        self.T, self.s, self.lam = T, s, lam
        K = K_matrix(T, a, al, m, mu)
        self.K = torch.tensor(K)
        self.R = [torch.tensor(R) for R in resolvents(K)]
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
        for gh in (True, False):                              # which outcomes are gains against the forecast
            for gl in (True, False):
                ch, cl = (1.0 if gh else self.lt), (1.0 if gl else self.lt)
                N = self.kt * (q * ch * ah + (1 - q) * cl * al_) / (1 + self.kt * (q * ch + (1 - q) * cl))
                if ((ah - N >= 0) == gh) and ((al_ - N >= 0) == gl):
                    return N
        raise RuntimeError("no consistent branch")

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
            st = news_root(x0 - x_prev[t:], Rt[:, 0], self.kn[:T - t], self.lam)
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


def signed(x, k, ratio=1.0):
    """k x, kinked at zero with loss/gain strength ratio at geometric mean k: gains k / sqrt(ratio), losses
    k sqrt(ratio) (core X1-X2)."""
    if ratio == 1.0:
        return k * x
    return torch.where(x >= 0, k / ratio ** 0.5 * x, k * ratio ** 0.5 * x)


def rounds_direct(r, C, feel=ROUNDS):
    """Felt utility per round from realized payoffs r (G, K) and critic forecasts C (direct echoes, news over base
    payoffs; a first pass, not the canonical model):
      e_k = r_k + nu A(C_{k+1}) + sum_j mu^j M(r_{k-j}) + n phi_lam(delta_k),   delta_k = r_k + nu C_{k+1} - C_k,
    anticipation as the critic's forecast of what is to come and news as its felt TD error. Canonically A(x) = a x
    and M(x) = m x; the optional sign asymmetries kink them at payoff zero with loss/gain ratios `dread` (a-/a+,
    X1) and `rumination` (m-/m+, X2) at geometric means a and m. The aggregate forecast is kinked, not each
    round it forecasts, as the news is."""
    G, K = r.shape
    Cn = torch.cat([C[:, 1:], torch.zeros(G, 1)], 1)                 # C_{k+1}, zero after the last round
    delta = r + feel["nu"] * Cn - C
    news = torch.where(delta >= 0, delta, feel["lam"] * delta) * feel["n"]
    M = signed(r, feel["m"], feel.get("rumination", 1.0))
    mem = torch.zeros_like(r)
    for k in range(1, K):
        mem[:, k] = sum(feel["mu"] ** j * M[:, k - j] for j in range(1, k + 1))
    return r + feel["nu"] * signed(Cn, feel["a"], feel.get("dread", 1.0)) + mem + news


def rounds_canonical(r, C, feel=ROUNDS, shift=0.0):
    """Canonical felt utility over the critic's forecasts of felt utility: e_k = x_k + n phi(e_k + nu C_{k+1} - C_k),
    x_k = r_k + a nu C_{k+1} + sum_j m mu^j e_{k-j} - shift; the root is on the branch of x_k + nu C_{k+1} - C_k.
    shift: a felt reference's pull h r (notes/adaptation.md), inside the solve, so memory echoes adapted states."""
    G, K = r.shape
    Cn = torch.cat([C[:, 1:], torch.zeros(G, 1)], 1)
    es = []
    for k in range(K):
        mem = sum(feel["m"] * feel["mu"] ** j * es[k - j] for j in range(1, k + 1)) if k else 0.0
        x = r[:, k] + feel["a"] * feel["nu"] * Cn[:, k] + mem - shift
        z = x + feel["nu"] * Cn[:, k] - C[:, k]
        c = torch.where(z >= 0, 1.0, feel["lam"])
        es.append(x + feel["n"] * c * z / (1 - feel["n"] * c))
    return torch.stack(es, 1)


if __name__ == "__main__":
    gen = torch.Generator().manual_seed(0)
    for name, cal in (("canonical", EVENT), ("X4", dict(EVENT, **X4))):
        ev, path, gap = Event(**cal), BeliefPath(**cal), 0.0
        for _ in range(40):
            q, p = torch.rand(2, generator=gen).unbind()
            zA, zB = (torch.rand(2, generator=gen) * 2 - 1).unbind()
            W = path.run(torch.full((cal["s"],), float(q)), float(zA), float(zB), float(p))[0]
            gap = max(gap, abs(float(W - ev.welfare(q[None], p[None], zA[None], zB[None])[0])))
        print(f"Event against BeliefPath at held beliefs, 40 events, {name}: {gap:.1e}")
    ev = Event(**EVENT)
    al, be = ev.weights()
    q, p, zA, zB = torch.rand(4, 2000, generator=gen)
    zA, zB = 2 * zA - 1, 2 * zB - 1
    m = lambda x: x * zA + (1 - x) * zB  # noqa: E731
    res = float((ev.welfare(q, p, zA, zB) - al * m(q) - be * m(p)).abs().max())
    print(f"Event at lam = 1 as alpha m(q) + beta m(p), alpha {al:.4f}, beta {be:.4f}, 2000 events: {res:.1e}")
    kn, g = torch.tensor(0.08 * 0.7 ** np.arange(12)), torch.rand(12, generator=gen) + 0.5     # lam kappa < 1
    d = torch.randn(200, 12, generator=gen)
    s = news_root(d, g, kn, 2.0)
    x = torch.zeros(200)
    for _ in range(5000):
        x = 0.5 * x + 0.5 * (phi(d + x[:, None] * g, 2.0) @ kn)
    print(f"news_root against a damped iteration: {float((s - x).abs().max()):.1e}")
    r, C = torch.randn(50, 10, generator=gen), torch.randn(50, 10, generator=gen)
    Cn = torch.cat([C[:, 1:], torch.zeros(50, 1)], 1)
    for name, f in (("canonical", ROUNDS), ("X4", dict(ROUNDS, **X4))):
        e = rounds_canonical(r, C, f)
        mem = torch.stack([sum(f["m"] * f["mu"] ** j * e[:, k - j] for j in range(1, k + 1)) if k else torch.zeros(50)
                           for k in range(10)], 1)
        res = e - (r + f["a"] * f["nu"] * Cn + mem + f["n"] * phi(e + f["nu"] * Cn - C, f["lam"]))
        print(f"rounds_canonical against its fixed point, {name}: {float(res.abs().max()):.1e}")
    f = dict(ROUNDS, dread=3.0, rumination=0.5, **X4)
    e, gap = rounds_direct(r, C, f), 0.0
    for i in range(50):
        for k in range(10):
            c = float(Cn[i, k])
            ant = f["a"] * f["nu"] * c * (3.0 ** 0.5 if c < 0 else 3.0 ** -0.5)
            mem = sum(f["m"] * f["mu"] ** j * float(r[i, k - j]) * (0.5 ** 0.5 if r[i, k - j] < 0 else 0.5 ** -0.5)
                      for j in range(1, k + 1))
            dl = float(r[i, k]) + f["nu"] * c - float(C[i, k])
            gap = max(gap, abs(float(e[i, k]) - (float(r[i, k]) + ant + mem + f["n"] * dl * (f["lam"] if dl < 0 else 1.0))))
    print(f"rounds_direct with dread 3, rumination 0.5, X4 against a loop: {gap:.1e}")
