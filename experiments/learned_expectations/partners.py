"""Partners: twins, altruists and felt empathy, in a population with a similarity signal (notes/empathy.md).

A population of independently initialized networks plays random symmetric 2x2 games, each one the game agent's (felt.Event)
event: moves at the announcement, revealed at s. Each network's objective mixes matches against a copy of
itself (weight sigma) and against another network (weight 1 - sigma); an input bit says which (flipped
with probability eps, or absent). Beliefs are calibrated. Three dials:
- wT: the gradient through a copy's policy, as in run_twin.py (a non-copy's policy is always held fixed);
- wE: the weight on the partner's utility: its payoff (altruism) or its felt welfare (empathy);
- J:  the gradient through the partner's forecast of my policy, which sets its anticipation and its news
      reference (the interpersonal J).
In the canonical model (lam = 1) felt welfare is alpha m(q) + beta m(p) (felt.Event.weights), so the felt agent is
the payoff agent at scale alpha + beta, the felt twin the payoff twin, and felt empathy altruism at weight
wE (beta + J alpha) / (alpha + beta) toward a partner whose policy is held fixed, or at J = 1 (with a copy's policy
moving at wT > 0 and J < 1, the copy route carries alpha + beta, not beta + J alpha; Codex). Loss-averse news
(felt.X4) breaks all three.
"""
import torch

from agents import Agent, tie
from felt import EVENT, X4, Event
from games import views

torch.set_default_dtype(torch.float64)


LAYOUT = dict(trunks={"main": ("mlp", 9, (128, 128))}, heads={"act": dict(trunk="main")})


def policy(agent, mine, theirs, signal):
    """P(my move 0) from (my payoffs, their payoffs), both indexed [my move, their move], and the bit."""
    x = torch.cat([mine.flatten(1), theirs.flatten(1), signal[:, None]], 1)
    return torch.sigmoid(agent.heads_on(x, ("act",))[0]["act"][:, 0])


def values(felt, q, p, X):
    """Value of each of the owner's moves, X indexed [owner's move, other's move], given the owner's belief
    q that the other plays move 0 and the other's actual P(move 0) = p: expected payoff or felt welfare."""
    if felt is None:
        return torch.stack([p * X[:, i, 0] + (1 - p) * X[:, i, 1] for i in (0, 1)], 1)
    return torch.stack([felt.welfare(q, p, X[:, i, 0], X[:, i, 1]) for i in (0, 1)], 1)


def objective(pi, pj, mine, theirs, copy, felt, wT=0.0, wE=0.0, J=0.0, ent=0.02):
    """Player i's objective in one match; pi, pj are P(move 0) of i and j, each on its own view."""
    return value(pi, tie(pj, wT) if copy else pj.detach(), mine, theirs, felt, wE, J, ent)


def value(pi, p, mine, theirs, felt, wE=0.0, J=0.0, ent=0.02):
    """Player i's objective given the partner's P(move 0) p, carrying whatever dependence on i's parameters
    the caller has routed through it."""
    V = values(felt, p, p, mine)
    obj = pi * V[:, 0] + (1 - pi) * V[:, 1]
    if wE:
        Vj = values(felt, tie(pi, J), pi, theirs.transpose(1, 2))
        obj = obj + wE * (p * Vj[:, 0] + (1 - p) * Vj[:, 1])
    if ent:
        c = pi.clamp(1e-9, 1 - 1e-9)
        obj = obj - ent * (c * c.log() + (1 - c) * (1 - c).log())
    return obj


def signals(copy, B, signal, eps, gen):
    if not signal:
        return torch.zeros(B), torch.zeros(B)
    return [torch.full((B,), float(copy)).logical_xor(torch.rand(B, generator=gen) < eps).double() for _ in range(2)]


def match(n1, n2, A, copy, felt, signal, eps, gen, dials):
    """Both seats' objectives on symmetric games A (B, 2, 2), the column player's payoffs A^T."""
    (m1, t1), (m2, t2) = views(A, A.transpose(1, 2))
    s1, s2 = signals(copy, len(A), signal, eps, gen)
    pi1, pi2 = policy(n1, m1, t1, s1), policy(n2, m2, t2, s2)
    return (objective(pi1, pi2, m1, t1, copy, felt, **dials).mean(),
            objective(pi2, pi1, m2, t2, copy, felt, **dials).mean())


def train(K=4, sigma=0.5, signal=True, eps=0.0, felt=False, feel=EVENT, strangers="others", steps=4000, batch=1024,
          seed=0, lr=1e-3, **dials):
    """strangers: "others" pairs each network with another one; "self" with a mirror: its own current policy
    under a stop-gradient, a lookalike whose play the learner treats as fixed (recomputed every step, it does
    move with the network's parameters between steps)."""
    gen = torch.Generator().manual_seed(seed)
    torch.manual_seed(seed)
    nets = [Agent(**LAYOUT) for _ in range(K)]
    F = Event(**feel) if felt else None
    opt = torch.optim.Adam([w for n in nets for w in n.parameters()], lr=lr)
    for it in range(steps):
        loss = 0.0
        if sigma > 0:
            for n in nets:
                o1, o2 = match(n, n, torch.rand(batch, 2, 2, generator=gen) * 2 - 1, True, F, signal, eps, gen, dials)
                loss = loss - sigma * (o1 + o2) / 2
        if sigma < 1 and strangers == "self":
            for n in nets:
                o1, o2 = match(n, n, torch.rand(batch, 2, 2, generator=gen) * 2 - 1, False, F, signal, eps, gen, dials)
                loss = loss - (1 - sigma) * (o1 + o2) / 2
        elif sigma < 1:
            perm = torch.randperm(K, generator=gen).tolist()
            for a, b in zip(perm[0::2], perm[1::2]):
                o1, o2 = match(nets[a], nets[b], torch.rand(batch, 2, 2, generator=gen) * 2 - 1, False, F, signal,
                               eps, gen, dials)
                loss = loss - (1 - sigma) * (o1 + o2)
        opt.zero_grad()
        loss.backward()
        opt.step()
    return nets, F


def slopes(A, F, sigma, dials, at):
    """d objective / dP(move 0) when every player plays P(move 0) = at, per game: against a copy, against
    another network, and the mixture an agent without the signal faces. Signs give local stability."""
    (m, t), _ = views(A, A.transpose(1, 2))
    out = {}
    for name, copy in (("copy", True), ("other", False)):
        p = torch.full((len(A),), at, requires_grad=True)
        o = objective(p, p if copy else p.detach().clone(), m, t, copy, F, ent=0.0, **dials)
        out[name], = torch.autograd.grad(o.sum(), p)
    out["mixed"] = sigma * out["copy"] + (1 - sigma) * out["other"]
    return out


if __name__ == "__main__":
    # checks: python partners.py
    gen = torch.Generator().manual_seed(1)
    F = Event(**EVENT)
    A = torch.rand(2000, 2, 2, generator=gen) * 2 - 1
    # gradient ownership: in a match between different networks, each objective reaches only its own owner
    a, b = Agent(**LAYOUT), Agent(**LAYOUT)
    for dials in (dict(wT=1.0, wE=0.5, J=1.0), dict(wE=0.5, J=0.0)):
        o1, o2 = match(a, b, A, False, F, True, 0.0, gen, dials)
        ga = torch.autograd.grad(o1, list(a.parameters()) + list(b.parameters()), allow_unused=True)
        gb = torch.autograd.grad(o2, list(a.parameters()) + list(b.parameters()), allow_unused=True)
        leak = max((float(g.abs().max()) for g in ga[len(ga) // 2:] + gb[:len(gb) // 2] if g is not None), default=0.0)
        own = min(float(g.abs().max()) for g in ga[:len(ga) // 2] + gb[len(gb) // 2:])
        print(f"{dials}: largest gradient leaking to the other network {leak:.1e} (own gradients nonzero: {own > 0})")
    # a copy match at wT = 0 trains like a match against a mirror
    for felt in (None, F):
        g = [torch.autograd.grad(sum(match(a, a, A, copy, felt, False, 0.0, torch.Generator().manual_seed(2),
                                           dict(wE=0.5, J=1.0))), list(a.parameters())) for copy in (True, False)]
        print(f"{'felt' if felt else 'payoff'}: copy at wT = 0 against a mirror, max gradient difference "
              f"{max(float((x - y).abs().max()) for x, y in zip(*g)):.1e}")
    # first order, a twin is an altruist (payoffs) and an empathizer at J = 1 (felt), at symmetric profiles
    for name, felt in (("payoff", None), ("felt", F), ("felt, X4", Event(**dict(EVENT, **X4)))):
        gap = max(float((slopes(A, felt, 0.5, dict(wT=0.6), at)["copy"]
                         - slopes(A, felt, 0.5, dict(wE=0.6, J=1.0), at)["other"]).abs().max()) for at in (0.1, 0.5, 0.9))
        print(f"{name}, p = 0.1, 0.5, 0.9: max |twin - empathizer at J = 1| {gap:.1e}")
    # canonical: felt slopes are alpha + beta times payoff slopes, empathy at (wE, J) as altruism at wE rho(J),
    # toward a fixed partner policy or at J = 1; a copy moving at wT > 0 with J < 1 breaks the scalar form
    al, be = F.weights()
    for name, cases, keys in (("held partner or J = 1", (dict(), dict(wT=0.6), dict(wE=0.6, J=0.0), dict(wE=0.6, J=0.4),
                                                           dict(wE=0.6, J=1.0, wT=0.3)), None),
                              ("copy at wT 0.3, wE 0.6, J 0 (fails)", (dict(wE=0.6, J=0.0, wT=0.3),), ("copy",))):
        gap = 0.0
        for dials in cases:
            pay = dict(dials, wE=dials.get("wE", 0.0) * (be + dials.get("J", 0.0) * al) / (al + be))
            for at in (0.1, 0.5, 0.9):
                sf, sp = slopes(A, F, 0.5, dials, at), slopes(A, None, 0.5, pay, at)
                gap = max(gap, max(float((sf[k] / (al + be) - sp[k]).abs().max()) for k in (keys or sf)))
        print(f"canonical felt slopes / (alpha + beta) against payoff slopes at wE rho(J), {name}: max gap {gap:.1e}")
