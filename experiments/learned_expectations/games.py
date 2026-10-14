"""A general game-playing agent with felt utility: random 2x2 games, one network, self-play.

Each game is an event: both players move at the announcement, moves are revealed at s, and my payoff
then depends on the other's move. That is felt.py's event, with the objective probability set by the
other player's actual policy and my belief about it chosen, tethered by KL(q || p)/tau. One network sees
(my payoffs, their payoffs) and plays either role. Variants:
- "payoff":     expected payoffs only (the Nash baseline; beliefs irrelevant).
- "calibrated": felt welfare, beliefs forced to the truth (what felt utility alone does to play).
- "free":       felt welfare, action and belief chosen separately (decision.md D7's decoupled affect).
- "coupled":    felt welfare, the action must softly best-respond to the agent's own belief, so motivated
                beliefs move play (Brunnermeier & Parker's trade-off).
Training is simultaneous gradient play: each player's objective takes the other's policy as given.
"""
import numpy as np
import torch

from felt import Felt

torch.set_default_dtype(torch.float64)

FEEL = dict(T=16, s=8, a=0.15, al=0.8, m=0.1, mu=0.6, n=0.3, nu=0.7, lam=2.0)


def sample_games(B, gen):
    """Bimatrix games: A[b, i, j] row player's payoff, Bm[b, i, j] column player's (i row move, j column)."""
    return torch.rand(B, 2, 2, generator=gen) * 2 - 1, torch.rand(B, 2, 2, generator=gen) * 2 - 1


def views(A, Bm):
    """Each player's view: (my payoffs, their payoffs), indexed [my move, their move]."""
    return (A, Bm), (Bm.transpose(1, 2), A.transpose(1, 2))


def pure_nash(A, Bm):
    """Boolean (B, 2, 2): which pure profiles are Nash equilibria of the payoff game."""
    row_best = A >= A.max(1, keepdim=True).values
    col_best = Bm >= Bm.max(2, keepdim=True).values
    return row_best & col_best


def classify(A, Bm):
    """0: no pure equilibrium (cyclic); 1: one, Pareto-efficient; 2: one, Pareto-dominated (PD-like);
    3: two (coordination or anti-coordination)."""
    ne = pure_nash(A, Bm)
    k = ne.flatten(1).sum(1)
    cls = torch.where(k == 0, 0, torch.where(k >= 2, 3, 1))
    idx = ne.flatten(1).float().argmax(1)
    a_ne, b_ne = A.flatten(1).gather(1, idx[:, None])[:, 0], Bm.flatten(1).gather(1, idx[:, None])[:, 0]
    dominated = ((A.flatten(1) > a_ne[:, None]) & (Bm.flatten(1) > b_ne[:, None])).any(1)
    return torch.where((cls == 1) & dominated, 2, cls)


CLASSES = ["cyclic", "unique, efficient", "unique, dominated (PD-like)", "two equilibria"]


class Net(torch.nn.Module):
    def __init__(self, width=128):
        super().__init__()
        self.trunk = torch.nn.Sequential(torch.nn.Linear(8, width), torch.nn.Tanh(),
                                         torch.nn.Linear(width, width), torch.nn.Tanh())
        self.act = torch.nn.Linear(width, 1)      # logit of playing my move 0
        self.bel = torch.nn.Linear(width, 1)      # logit of believing they play their move 0

    def forward(self, mine, theirs):
        h = self.trunk(torch.cat([mine.flatten(1), theirs.flatten(1)], 1))
        return torch.sigmoid(self.act(h)[:, 0]), torch.sigmoid(self.bel(h)[:, 0]), h


def felt_values(felt, q, p, mine):
    """Felt welfare of each of my moves given belief q and their actual P(move 0) = p."""
    return torch.stack([felt.welfare(q, p, mine[:, i, 0], mine[:, i, 1]) for i in (0, 1)], 1)


def kl(q, p):
    q, p = q.clamp(1e-9, 1 - 1e-9), p.clamp(1e-9, 1 - 1e-9)
    return q * torch.log(q / p) + (1 - q) * torch.log((1 - q) / (1 - p))


def objectives(net, felt, A, Bm, variant, tau=3.0, beta=8.0, ent=0.02, w=0.0):
    """Each player's objective. The other's policy enters as p = pi.detach() + w (pi - pi.detach()): at w = 0
    it is held fixed (causal play, Nash); at w = 1 the gradient also flows through it, which in a
    symmetric game is play against a copy of one's own policy (the twin). In "coupled" a player's move
    is its soft best response to the felt value it expects under its own belief."""
    (m1, t1), (m2, t2) = views(A, Bm)
    (pi1, q1, _), (pi2, q2, _) = net(m1, t1), net(m2, t2)
    if variant == "coupled":
        pi1, pi2 = [torch.sigmoid(beta * (Vs[:, 0] - Vs[:, 1]))
                    for Vs in (felt_values(felt, q1, q1, m1), felt_values(felt, q2, q2, m2))]
    out = []
    tie = lambda x: x.detach() + w * (x - x.detach())
    for pi, q, mine, p in ((pi1, q1, m1, tie(pi2)), (pi2, q2, m2, tie(pi1))):
        if variant == "payoff":
            V = torch.stack([p * mine[:, i, 0] + (1 - p) * mine[:, i, 1] for i in (0, 1)], 1)
        else:
            V = felt_values(felt, p if variant == "calibrated" else q, p, mine)
        obj = pi * V[:, 0] + (1 - pi) * V[:, 1]
        if variant in ("free", "coupled"):
            obj = obj - kl(q, p) / tau
        H = -(pi.clamp(1e-9) * pi.clamp(1e-9).log() + (1 - pi).clamp(1e-9) * (1 - pi).clamp(1e-9).log())
        out.append(obj + ent * H)
    return out, (pi1, q1, pi2, q2)


def train(variant, steps=3000, batch=512, seed=0, lr=1e-3, tau=3.0, w=0.0, symmetric=False):
    gen = torch.Generator().manual_seed(seed)
    torch.manual_seed(seed)
    net, felt = Net(), Felt(**FEEL)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    for it in range(steps):
        A, Bm = sample_games(batch, gen)
        if symmetric:
            Bm = A.transpose(1, 2)
        (o1, o2), _ = objectives(net, felt, A, Bm, variant, tau=tau, w=w)
        loss = -(o1 + o2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    return net, felt
