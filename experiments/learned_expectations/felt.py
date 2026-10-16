"""Batched closed-form felt welfare for one event with two outcomes and a belief held until it resolves.

An event is announced at 0 and resolves at s with outcome z_A (objective probability p) or z_B. The self
holds belief q in outcome A from 0 until s. With the belief held, forecasts do not move before s, so the
only felt news is the jolt at the announcement (against a no-event prior) and the news at s (core N3,
canonical). With c = E_q z + Nbar_q the forecast change at 0 is c R_0[:, s], one-signed, so
  s_0 = c k_n.R_0[:, s] / (1 - k_n.g_0) if c >= 0, else lam c k_n.R_0[:, s] / (1 - lam k_n.g_0),
  e_pre = c R_0[:s, s] + s_0 g_0[:s]   (the forecast at 0 is realized until s),
  e_post(z) = R_s(z delta_0 + mem_s) + psi(z - E_q z - Nbar_q) g_s.
Welfare is p sum e_post(z_A) + (1-p) sum e_post(z_B) + sum e_pre. Everything is batched over events.
"""
import numpy as np
import torch

torch.set_default_dtype(torch.float64)


def K_matrix(T, a, al, m, mu):
    d = np.arange(T)[None, :] - np.arange(T)[:, None]
    return np.where(d > 0, a * al ** np.clip(d, 0, None), 0.0) + np.where(d < 0, m * mu ** np.clip(-d, 0, None), 0.0)


class Felt:
    def __init__(self, T, s, a, al, m, mu, n, nu, lam):
        self.T, self.s, self.lam = T, s, lam
        K = K_matrix(T, a, al, m, mu)
        R0 = np.linalg.inv(np.eye(T) - K)
        Rs = np.linalg.inv(np.eye(T - s) - K[s:, s:])
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
