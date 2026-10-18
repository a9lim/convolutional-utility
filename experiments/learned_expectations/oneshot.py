"""The game agent: random one-shot 2x2 games, one network for both roles, self-play, felt utility.

Each game is an event: both players move at the announcement, moves are revealed at s, and my payoff then depends
on the other's move. That is felt.Event, with the objective probability set by the other player's actual policy
and my belief about it chosen, tethered by KL(q || p)/tau. One network sees (my payoffs, their payoffs) and plays
either role; an action head and a belief head read one trunk, or the belief head its own (`separate_belief`).
Variants:
- "payoff":     expected payoffs only (the Nash baseline; beliefs irrelevant).
- "calibrated": felt welfare, beliefs forced to the truth (what felt utility alone does to play).
- "free":       felt welfare, action and belief chosen separately (tethered belief choice, not D7's affect filtration).
- "coupled":    felt welfare, the action must softly best-respond to the agent's own belief, so motivated
                beliefs move play (Brunnermeier & Parker's trade-off).
Training is simultaneous gradient play: each player's objective takes the other's policy as given, or, with the
dial w, lets the gradient through it (in a symmetric game, play against a copy: the twin).
In the canonical model (lam = 1) felt welfare is alpha m(q) + beta m(p) (felt.Event.weights), so "calibrated" is
"payoff" at scale alpha + beta, except that the entropy bonus weighs less against it; `scale` gives the payoff
agent the same temperature. Under loss-averse news (felt.X4) it is not.
"""
import torch

from agents import Agent, tie
from felt import EVENT, Event, kl
from games import sample_games, views

torch.set_default_dtype(torch.float64)


def layout(width=128, separate_belief=False):
    trunks = {"main": ("mlp", 8, (width, width))}
    if separate_belief:
        trunks["belief"] = ("mlp", 8, (width, width))
    return dict(trunks=trunks, heads={"act": dict(trunk="main"),
                                      "bel": dict(trunk="belief" if separate_belief else "main")})


def play(agent, mine, theirs):
    """P(my move 0), my belief that they play their move 0, and the action trunk's features."""
    outs, feats = agent.heads_on(torch.cat([mine.flatten(1), theirs.flatten(1)], 1), ("act", "bel"))
    return torch.sigmoid(outs["act"][:, 0]), torch.sigmoid(outs["bel"][:, 0]), feats["main"]


def felt_values(ev, q, p, mine):
    """Felt welfare of each of my moves given belief q and their actual P(move 0) = p."""
    return torch.stack([ev.welfare(q, p, mine[:, i, 0], mine[:, i, 1]) for i in (0, 1)], 1)


def objectives(agent, ev, A, Bm, variant, tau=3.0, beta=8.0, ent=0.02, w=0.0, scale=1.0):
    """Each player's objective. The other's policy enters as p = tie(pi, w): at w = 0 it is held fixed (causal
    play, Nash); at w = 1 the gradient also flows through it, which in a symmetric game is play against a copy of
    one's own policy (the twin). In "coupled" a player's move is its soft best response to the felt value it
    expects under its own belief."""
    (m1, t1), (m2, t2) = views(A, Bm)
    (pi1, q1, _), (pi2, q2, _) = play(agent, m1, t1), play(agent, m2, t2)
    if variant == "coupled":
        pi1, pi2 = [torch.sigmoid(beta * (Vs[:, 0] - Vs[:, 1]))
                    for Vs in (felt_values(ev, q1, q1, m1), felt_values(ev, q2, q2, m2))]
    out = []
    for pi, q, mine, p in ((pi1, q1, m1, tie(pi2, w)), (pi2, q2, m2, tie(pi1, w))):
        if variant == "payoff":
            V = scale * torch.stack([p * mine[:, i, 0] + (1 - p) * mine[:, i, 1] for i in (0, 1)], 1)
        else:
            V = felt_values(ev, p if variant == "calibrated" else q, p, mine)
        obj = pi * V[:, 0] + (1 - pi) * V[:, 1]
        if variant in ("free", "coupled"):
            obj = obj - kl(q, p) / tau
        H = -(pi.clamp(1e-9) * pi.clamp(1e-9).log() + (1 - pi).clamp(1e-9) * (1 - pi).clamp(1e-9).log())
        out.append(obj + ent * H)
    return out, (pi1, q1, pi2, q2)


def train(variant, steps=3000, batch=512, seed=0, lr=1e-3, tau=3.0, w=0.0, symmetric=False, separate_belief=False,
          feel=EVENT, scale=1.0, monitor=None):
    """monitor(step, agent, ev) every 250 steps and at the end; it draws no randomness the training uses."""
    gen = torch.Generator().manual_seed(seed)
    torch.manual_seed(seed)
    agent, ev = Agent(**layout(separate_belief=separate_belief)), Event(**feel)
    opt = torch.optim.Adam(agent.parameters(), lr=lr)
    for it in range(steps):
        A, Bm = sample_games(batch, gen)
        if symmetric:
            Bm = A.transpose(1, 2)
        (o1, o2), _ = objectives(agent, ev, A, Bm, variant, tau=tau, w=w, scale=scale)
        loss = -(o1 + o2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        if monitor and it % 250 == 0:
            monitor(it, agent, ev)
    if monitor:
        monitor(steps, agent, ev)
    return agent, ev
