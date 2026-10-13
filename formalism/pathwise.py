"""Pathwise simulation of the recursive model with felt news (core.md, felt news).
Run: python formalism/pathwise.py [out.png]

Deterministic announcements. At each t the self solves for its felt e_t and its forecast path x of e on
[t, T), given current forecasts of u, realized past e, and its previous forecast path. Forecasts are
certainty-equivalent: later selves are forecast to receive no further news (no anxiety term).
    x = u_hat[t:] + A x + mem_past + s e_0,   s = felt news at t
over="u": s = sum_j nu(j) mu(u_hat_{t+j} - u_prev_{t+j})        news over base utility
over="e": s = sum_j nu(j) mu(x_j - x_prev_{t+j}), a 1-D root     news over experienced utility
The root is unique iff lam * (nu . g) < 1, with g = (I - A)^{-1} e_0 (core N4)."""
import sys

import numpy as np


def kernels(T, a, b, m, al):
    j = np.arange(T)
    return np.where(j > 0, a * b ** j, 0.0), np.where(j > 0, m * al ** j, 0.0)


def forecast_u(T, base, events, t):
    """events: (announce, when, value, cancel); announce None means unannounced until it happens."""
    u = np.full(T, float(base))
    for ann, s, v, cancel in events:
        if cancel is not None and cancel <= min(t, s):
            continue
        if s <= t or (ann is not None and ann <= t):
            u[s] += v
    return u


def run(T, base, events, kf, kb, nu, lam, over):
    mu = lambda x: np.where(x >= 0, x, lam * x)
    e = np.zeros(T)
    comp = {k: np.zeros(T) for k in ("base", "anticipation", "memory", "news")}
    loop = np.zeros(T)

    def path(t, uh):
        n = T - t
        i, j = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
        A = np.where(j > i, kf[np.clip(j - i, 0, T - 1)], 0) + np.where(j < i, kb[np.clip(i - j, 0, T - 1)], 0)
        mem_past = np.array([e[:t][::-1] @ kb[k + 1:k + 1 + t] for k in range(n)]) if t else np.zeros(n)
        Rinv = np.linalg.inv(np.eye(n) - A)
        return Rinv @ (uh[t:] + mem_past), Rinv[:, 0]

    u_prev = forecast_u(T, base, events, -1)
    x_prev, _ = path(0, u_prev)
    for t in range(T):
        uh = forecast_u(T, base, events, t)
        x0, g = path(t, uh)
        n = T - t
        if over == "u":
            s = nu[:n] @ mu(uh[t:] - u_prev[t:])
        else:
            loop[t] = lam * (nu[:n] @ np.abs(g))
            if loop[t] >= 1:
                raise RuntimeError(f"news over e not well-founded at t={t}: lam (nu . g) = {loop[t]:.3f}")
            h = lambda s: s - nu[:n] @ mu(x0 + s * g - x_prev[t:])
            lo, hi = -1e3, 1e3
            for _ in range(200):
                mid = (lo + hi) / 2
                lo, hi = (mid, hi) if h(mid) < 0 else (lo, mid)
            s = (lo + hi) / 2
        x = x0 + s * g
        e[t] = x[0]
        comp["base"][t] = uh[t]
        comp["anticipation"][t] = kf[1:n] @ x[1:]
        comp["memory"][t] = e[:t][::-1] @ kb[1:t + 1] if t else 0.0
        comp["news"][t] = s
        x_prev = np.concatenate([np.zeros(t), x])
        u_prev = uh
    return e, comp, loop


T = 60
KF, KB = kernels(T, 0.1, 0.85, 0.1, 0.75)
NU = np.array([0.3] + [0.1 * 0.7 ** j for j in range(1, T)])
EVENTS = [(5, 20, 3.0, None),       # trip announced at 5, happens at 20
          (25, 45, 3.0, 40),        # second trip announced at 25, cancelled at 40
          (None, 33, -3.0, None)]   # unannounced loss at 33

if __name__ == "__main__":
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    out = sys.argv[1] if len(sys.argv) > 1 else "notes/full-model-over-time.png"
    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)
    colors = {"base": "#7f7f7f", "anticipation": "#2a7ab9", "memory": "#d08a1e", "news": "#c0392b"}
    for ax, over, title in [(axes[0], "u", "News over base utility"), (axes[1], "e", "News over experienced utility")]:
        e, c, loop = run(T, 0.0, EVENTS, KF, KB, NU, 2.0, over)
        t = np.arange(T)
        for k, col in colors.items():
            ax.plot(t, c[k], color=col, lw=1.6, label=k)
        ax.plot(t, e, color="black", lw=2.4, label="experienced utility e")
        ax.axhline(0, color="#bbb", lw=0.8)
        for x, txt in [(5, "trip 1\nannounced"), (20, "trip 1"), (25, "trip 2\nannounced"),
                       (33, "surprise\nloss"), (40, "trip 2\ncancelled")]:
            ax.axvline(x, color="#ddd", lw=0.8, zorder=0)
            ax.text(x + 0.3, 4.1, txt, fontsize=8, va="top", color="#555")
        lo = min(e.min(), min(v.min() for v in c.values()))
        ax.set_ylim(lo * 1.08, 4.2)
        ax.set_title(f"{title}   (life-sum {e.sum():+.2f})", loc="left", fontsize=11)
    axes[0].legend(loc="lower left", fontsize=8, ncol=5, frameon=False)
    axes[1].set_xlabel("time")
    fig.suptitle("Recursive model with felt news: a = m = 0.1, β = 0.85, α = 0.75 (M = 0.87), "
                 "ν(0) = 0.3, λ = 2", fontsize=11)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"saved {out}")
