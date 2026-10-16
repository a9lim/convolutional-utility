"""Agents: named trunks, each read by named heads, and the J dial.

A layout says which trunk each head reads, so whether heads share a representation is configuration: heads on
one trunk shape each other through it (formalism/learning.md D8), a head on its own trunk cannot, and a head with `detach`
reads its trunk without training it. Trunks are tanh MLPs or a GRU cell; heads are linear maps or tanh MLPs,
reading the trunk's features plus any extra inputs given at call time. Roles name the outputs a wing reads,
(head, column) pairs, so one head can carry several.
"""
import numpy as np
import torch

torch.set_default_dtype(torch.float64)


def tie(x, w):
    """x with its gradient scaled by w (the J dial): w = 0 holds x fixed, w = 1 lets the full gradient through."""
    return x.detach() + w * (x - x.detach())


def mlp(sizes, last=True):
    """Linear layers between consecutive sizes, each followed by tanh (the last one only if `last`)."""
    layers = []
    for i, (a, b) in enumerate(zip(sizes[:-1], sizes[1:])):
        layers.append(torch.nn.Linear(a, b))
        if last or i < len(sizes) - 2:
            layers.append(torch.nn.Tanh())
    return torch.nn.Sequential(*layers)


class Agent(torch.nn.Module):
    def __init__(self, trunks, heads, roles=None):
        """trunks: {name: ("mlp", inputs, widths) or ("gru", inputs, width)}.
        heads: {name: dict(trunk=..., out=1, extra=0, hidden=(), detach=False)}.
        roles: {role: (head, column)}.
        Modules are built trunk by trunk, each followed by its heads in order, so a layout always initializes the
        same way."""
        super().__init__()
        for t, spec in trunks.items():
            if spec[0] not in ("mlp", "gru"):
                raise ValueError(f"trunk {t}: unknown kind {spec[0]!r}")
        for name, spec in heads.items():
            if set(spec) - {"trunk", "out", "extra", "hidden", "detach"} or spec.get("trunk") not in trunks:
                raise ValueError(f"head {name}: bad spec {spec}")
        for role, (head, col) in (roles or {}).items():
            if head not in heads or not 0 <= col < heads[head].get("out", 1):
                raise ValueError(f"role {role}: no column {col} of head {head!r}")
        self.kinds = {t: spec[0] for t, spec in trunks.items()}
        self.layout = {name: dict(dict(out=1, extra=0, hidden=(), detach=False), **spec) for name, spec in heads.items()}
        self.roles = dict(roles or {})
        self.trunks, self.heads = torch.nn.ModuleDict(), torch.nn.ModuleDict()
        for t, (kind, n_in, width) in trunks.items():
            self.trunks[t] = mlp((n_in,) + tuple(width)) if kind == "mlp" else torch.nn.GRUCell(n_in, width)
            for name, spec in self.layout.items():
                if spec["trunk"] == t:
                    n = self.width(t) + spec["extra"]
                    self.heads[name] = (mlp((n,) + tuple(spec["hidden"]) + (spec["out"],), last=False)
                                        if spec["hidden"] else torch.nn.Linear(n, spec["out"]))

    def width(self, t):
        if self.kinds[t] == "gru":
            return self.trunks[t].hidden_size
        return [m for m in self.trunks[t] if isinstance(m, torch.nn.Linear)][-1].out_features

    def inputs(self, t):
        if self.kinds[t] == "gru":
            return self.trunks[t].input_size
        return self.trunks[t][0].in_features

    def initial_state(self, G):
        """Zero states of every GRU trunk, for G episodes."""
        return {t: torch.zeros(G, self.width(t)) for t, kind in self.kinds.items() if kind == "gru"}

    def step(self, x, states):
        """Every GRU trunk's next state from one shared record x."""
        return {t: self.features(t, x, h) for t, h in states.items()}

    def record_size(self):
        sizes = {self.inputs(t) for t, kind in self.kinds.items() if kind == "gru"}
        if len(sizes) != 1:
            raise ValueError(f"GRU trunks must read one record, got input sizes {sizes}")
        return sizes.pop()

    def features(self, t, x, h=None):
        """A trunk's features of input x (an MLP), or its next state from input x and state h (a GRU)."""
        return self.trunks[t](x) if self.kinds[t] == "mlp" else self.trunks[t](x, h)

    def read(self, name, z, extra=None):
        """A head's outputs from its trunk's features z, plus its extra inputs."""
        spec = self.layout[name]
        if spec["detach"]:
            z = z.detach()
        if spec["extra"]:
            z = torch.cat([z, extra], 1)
        return self.heads[name](z)

    def heads_on(self, x, names):
        """The named heads' outputs on one input x for every trunk they read, each trunk run once.
        Returns (outputs, features by trunk)."""
        feats, outs = {}, {}
        for name in names:
            t = self.layout[name]["trunk"]
            if t not in feats:
                feats[t] = self.features(t, x)
            outs[name] = self.read(name, feats[t])
        return outs, feats

    def roles_at(self, z, extra=None):
        """Every role's output from trunk features z ({trunk: features}), each head computed once, in role order."""
        outs = {}
        for head, _ in self.roles.values():
            if head not in outs:
                outs[head] = self.read(head, z[self.layout[head]["trunk"]], extra)
        return {role: outs[head][:, col] for role, (head, col) in self.roles.items()}


def balanced_probe(X, y, n_tr, n_classes, steps=2000):
    """Balanced accuracy on held-out rows of a class-weighted linear probe for labels y from features X (trained
    on the first n_tr rows); chance is 1 / n_classes."""
    mu, sd = X[:n_tr].mean(0), X[:n_tr].std(0) + 1e-9
    X = (X - mu) / sd
    w = torch.bincount(y[:n_tr], minlength=n_classes).double()
    w = (w.sum() / (n_classes * w.clamp_min(1)))
    W, b = torch.zeros(X.shape[1], n_classes, requires_grad=True), torch.zeros(n_classes, requires_grad=True)
    opt = torch.optim.Adam([W, b], lr=0.05)
    for _ in range(steps):
        opt.zero_grad()
        torch.nn.functional.cross_entropy(X[:n_tr] @ W + b, y[:n_tr], weight=w).backward()
        opt.step()
    with torch.no_grad():
        pred = (X[n_tr:] @ W + b).argmax(1)
        yt = y[n_tr:]
        return float(np.nanmean([float((pred[yt == k] == k).float().mean()) for k in range(n_classes)]))
