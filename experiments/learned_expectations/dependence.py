"""Inferred dependence: a twin that is not told which partners are copies (notes/empathy.md).

Partner types: copies of the network; mirrors (the network's current policy recomputed each step under a
stop-gradient: lookalikes whose play the learner treats as fixed); strangers and forgers (frozen,
independently trained causal networks from a bank). Each match shows both seats one similarity signal s,
drawn N(1, eta^2) for copies and forgers and N(0, eta^2) for mirrors and strangers. The twin's gradient
(weight w) has three dependence modes:
- "oracle":  through the partner only when it truly is a copy (partners.py's gate on identity);
- "bayes":   in every match, the direct gradient against the partner's actual play, plus w d(s) times the
             dependence gradient evaluated in the copy branch (partner = my own policy), d(s) the posterior
             that the partner is a copy under an assumed model of shares and noise;
- "learned": the same, with d(s) a head on its own small trunk (LAYOUT), fit to identities revealed
             after each match.
With the true model, the bayes twin's expected gradient equals the oracle's, payoff or felt (Codex): the
oracle's identity labels buy nothing in expectation; a miscalibrated d(s) does.
"""
import math

import torch

from agents import Agent, tie
from felt import EVENT, Event
from games import views
from partners import policy, value

torch.set_default_dtype(torch.float64)
TYPES = ("copy", "mirror", "stranger", "forger")
HIGH = ("copy", "forger")                    # types that emit copy-like signals


def posterior(s, shares, eta):
    """P(copy | s) under shares {type: share}; computed in logs, safe for extreme s."""
    if eta <= 0:
        raise ValueError("eta must be positive")
    s = torch.as_tensor(s, dtype=torch.float64)
    terms = {t: math.log(sh) - 0.5 * ((s - (1.0 if t in HIGH else 0.0)) / eta) ** 2
             for t, sh in shares.items() if sh > 0}
    return torch.exp(terms["copy"] - torch.logsumexp(torch.stack(list(terms.values())), 0))


# the twin's policy (partners.LAYOUT) and, on its own trunk, the learned P(copy | s), fit by cross-entropy to
# identities revealed after each match
LAYOUT = dict(trunks={"main": ("mlp", 9, (128, 128)), "dep": ("mlp", 1, (16,))},
              heads={"act": dict(trunk="main"), "dep": dict(trunk="dep")})


def dependence_logit(agent, s):
    return agent.heads_on(s[:, None], ("dep",))[0]["dep"][:, 0]


def signal(typ, B, eta, gen):
    return (1.0 if typ in HIGH else 0.0) + eta * torch.randn(B, generator=gen)


def bank_play(bank, m2, t2, gen):
    """A frozen opponent drawn from the bank for this batch."""
    opp = bank[int(torch.randint(len(bank), (1,), generator=gen))]
    with torch.no_grad():
        return policy(opp, m2, t2, torch.zeros(len(m2)))


def objective(agent, typ, m1, t1, m2, t2, s, pj, F, mode, w, d, wE=0.0, J=0.0):
    """One seat's objective against a partner of type typ playing pj (with gradient only for a copy)."""
    pi = policy(agent, m1, t1, s)
    if mode == "oracle":
        return value(pi, tie(pj, w) if typ == "copy" else pj.detach(), m1, t1, F, wE, J)
    r = policy(agent, m2, t2, s)                              # my own policy in the partner's seat
    dep = value(pi.detach(), r, m1, t1, F, wE, J, ent=0.0) - value(pi.detach(), r.detach(), m1, t1, F, wE, J, ent=0.0)
    return value(pi, pj.detach(), m1, t1, F, wE, J) + w * d * dep


def train(mode="oracle", w=1.0, shares=None, eta=0.5, assume=None, bank=(), felt=False, steps=4000, batch=1024,
          seed=0, lr=1e-3, wE=0.0, J=0.0):
    """shares: {type: share}; assume: (shares, eta) of the bayes twin's model, default the truth; bank: frozen
    networks that play strangers and forgers."""
    if mode not in ("oracle", "bayes", "learned"):
        raise ValueError(f"unknown mode {mode!r}")
    if not bank and any(shares.get(t, 0) > 0 for t in ("stranger", "forger")):
        raise ValueError("strangers and forgers are played by the bank")
    gen = torch.Generator().manual_seed(seed)
    torch.manual_seed(seed)
    agent = Agent(**LAYOUT)
    F = Event(**EVENT) if felt else None
    opt = torch.optim.Adam(agent.parameters(), lr=lr)
    a_shares, a_eta = assume if assume is not None else (shares, eta)
    for it in range(steps):
        loss = 0.0
        for typ, share in shares.items():
            if share == 0:
                continue
            A = torch.rand(batch, 2, 2, generator=gen) * 2 - 1
            (m1, t1), (m2, t2) = views(A, A.transpose(1, 2))
            s = signal(typ, batch, eta, gen)
            pj = policy(agent, m2, t2, s) if typ in ("copy", "mirror") else bank_play(bank, m2, t2, gen)
            if mode == "learned":
                logit = dependence_logit(agent, s)
                loss = loss + share * torch.nn.functional.binary_cross_entropy_with_logits(
                    logit, torch.full_like(s, float(typ == "copy")))
                d = torch.sigmoid(logit).detach()
            else:
                d = posterior(s, a_shares, a_eta) if mode == "bayes" else None
            loss = loss - share * objective(agent, typ, m1, t1, m2, t2, s, pj, F, mode, w, d, wE, J).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    return agent, F


def slope(A, F, s, p, frozen, shares, eta, mode, w, d, wE=0.0, J=0.0):
    """Expected d objective / dP(move 0) at signal s, with copies and mirrors playing p and strangers and
    forgers each frozen policy in `frozen` (averaged after the slope, not before): the posterior mixture of
    each type's gradient. Entropy-free, for one scalar policy per game; its signs at p near 0 and 1 are the
    boundary gradient signs."""
    (m, t), _ = views(A, A.transpose(1, 2))
    logw = {typ: math.log(v) - 0.5 * ((s - (1.0 if typ in HIGH else 0.0)) / eta) ** 2 for typ, v in shares.items() if v > 0}
    z = torch.logsumexp(torch.tensor(list(logw.values())), 0).item()
    post = {typ: math.exp(v - z) for typ, v in logw.items()}
    x = torch.full((len(A),), p, requires_grad=True)
    total = 0.0
    for typ, pt in post.items():
        ys = [x] if typ == "copy" else ([x.detach().clone()] if typ == "mirror" else frozen)
        for y in ys:
            if mode == "oracle":
                o = value(x, tie(y, w) if typ == "copy" else y.detach(), m, t, F, wE, J, ent=0.0)
            else:
                o = value(x, y.detach(), m, t, F, wE, J, ent=0.0) + w * d * value(x.detach(), x, m, t, F, wE, J, ent=0.0)
            total = total + pt / len(ys) * o.sum()
    g, = torch.autograd.grad(total, x)
    return g


if __name__ == "__main__":
    # checks: python dependence.py
    gen = torch.Generator().manual_seed(1)
    A = torch.rand(3000, 2, 2, generator=gen) * 2 - 1
    frozen = [torch.rand(3000, generator=gen) for _ in range(3)]
    eta = 0.5
    print("posterior at extreme signals:", posterior(torch.tensor([-100.0, 0.5, 100.0]),
                                                     {"copy": 0.5, "stranger": 0.25, "forger": 0.25}, eta).tolist())
    for shares in ({"copy": 0.5, "mirror": 0.5}, {"copy": 0.5, "stranger": 0.5},
                   {"copy": 0.5, "stranger": 0.25, "forger": 0.25}):
        for felt in (None, Event(**EVENT)):
            gap = 0.0
            for s in (0.0, 0.5, 1.0):
                for p in (0.1, 0.9):
                    pc = float(posterior(s, shares, eta))
                    o = slope(A, felt, s, p, frozen, shares, eta, "oracle", 1.0, None)
                    b = slope(A, felt, s, p, frozen, shares, eta, "bayes", 1.0, pc)
                    gap = max(gap, float((o - b).abs().max()))
            print(f"{shares}, {'felt' if felt else 'payoff'}: max |oracle - calibrated bayes| expected slope {gap:.1e}")
