"""A trust game with felt empathy and the interpersonal J (notes/empathy.md). Run:
python experiments/learned_expectations/run_trust.py   (writes trust_report.txt and trust_sweeps.json, the
thresholds along lam, a and n)

Ann trusts at 0, or takes the outside option (payoff 0, no event). Trusting announces an event: Ann holds a
belief q that Bob honors from 0 until he chooses at s, when his move is revealed: she gets H if he honors,
L if he grabs (felt.Event; her anticipation is already felt when he chooses, decision.md D1's timing).
Bob gets h or g > h, felt as a sure payoff from 0 (he knows his own move). Bob maximizes his felt welfare
plus w times Ann's. Finite deviations between pure policies:
- J = 0, Ann's forecast fixed at q: honoring gains Ann W(q, 1) - W(q, 0); at q = 1 grabbing lets her down
  (guilt), at q = 0 honoring surprises her.
- J = 1, Ann's forecast tracks Bob's policy: W(1, 1) - W(0, 0); her anticipation counts, her news does not.
Bob resists a temptation g - h up to w x gain / (his felt weight on his own payoff). J = 1 resists more iff
W(1, 0) > W(0, 0): Ann's anticipation of honor outweighs her letdown (direct model: A > n lambda). In the
canonical model W(q, p) = alpha m(q) + beta m(p) (felt.Event.weights): J = 0 resists (H - L) beta / (alpha + beta)
per unit empathy whatever Ann expects, J = 1 resists H - L, and J = 1 resists more iff alpha > 0. Within this event
family with linear echoes and base utility, expectation-dependent guilt needs loss-averse news (X4)."""
import json
import os
import sys

import numpy as np

import torch

sys.path.insert(0, os.path.dirname(__file__))
from felt import EVENT, X4, Event  # noqa: E402

torch.set_default_dtype(torch.float64)
HERE = os.path.dirname(__file__)
H, L, h = 0.5, -0.5, 0.3


def gains(F):
    W = lambda q, p: float(F.welfare(torch.tensor([float(q)]), torch.tensor([float(p)]), torch.tensor([H]),
                                     torch.tensor([L]))[0])
    z = torch.tensor([h, h + 1e-6])
    own = float(torch.diff(F.welfare(z, z, z, z))[0]) / 1e-6          # Bob's felt weight on a sure payoff
    return dict(guilt=W(1, 1) - W(1, 0), surprise=W(0, 1) - W(0, 0), policy=W(1, 1) - W(0, 0),
                letdown=W(1, 0), braced=W(0, 0), trust=W(1, 1), own=own)


def calibrations():
    """Canonical rows (lam = 1), then loss-averse news (X4) at felt and choice-revealed strength."""
    out = {"EVENT (a 0.15, n 0.3, s 8)": EVENT,
           "no news (n 0)": dict(EVENT, n=0.0),
           "weak news (n 0.1)": dict(EVENT, n=0.1),
           "news n 0.2": dict(EVENT, n=0.2),
           "no anticipation (a 0)": dict(EVENT, a=0.0),
           "weak anticipation (a 0.05)": dict(EVENT, a=0.05),
           "stronger anticipation a 0.2": dict(EVENT, a=0.2)}
    for s in (2, 14):
        out[f"anticipation horizon s {s}"] = dict(EVENT, s=s)
    out["X4, felt strength (lam 1.2)"] = dict(EVENT, lam=1.2)
    out[f"X4 (lam {X4['lam']:g})"] = dict(EVENT, **X4)
    out[f"X4 (lam {X4['lam']:g}), n 0.2"] = dict(EVENT, n=0.2, **X4)
    out[f"X4 (lam {X4['lam']:g}), no anticipation"] = dict(EVENT, a=0.0, **X4)
    return out


if __name__ == "__main__":
    lines = []
    say = lambda s: (print(s, flush=True), lines.append(s))
    say(f"Ann: outside 0, honor {H}, grab {L}; Bob: honor {h}, grab {h} + t. Ann's felt welfare W(q, p): her belief q "
        "that Bob honors, his actual P(honor) p. Temptation Bob resists, per unit empathy w: t* / w = gain / own.")
    say("Forward kernel mass a sum alpha^j is 0.58 at EVENT and 0.77 at a 0.2, inside the well-founded range.")
    say(f"{'calibration':38s} {'W(1,1)':>7s} {'W(1,0)':>7s} {'W(0,0)':>7s} | {'own':>5s} | t*/w: "
        f"{'J0, q=1':>8s} {'J0, q=0':>8s} {'J1':>8s} | J1 vs J0 (q=1) | {'alpha':>6s} {'beta':>6s}")
    for name, kw in calibrations().items():
        try:
            g = gains(Event(**kw))
        except ValueError as e:
            say(f"{name:38s} {e}")
            continue
        t0, t0s, t1 = (g[k] / g["own"] for k in ("guilt", "surprise", "policy"))
        ab = "{:+6.3f} {:6.3f}".format(*Event(**kw).weights()) if kw["lam"] == 1.0 else f"{'-':>6s} {'-':>6s}"
        say(f"{name:38s} {g['trust']:7.3f} {g['letdown']:7.3f} {g['braced']:7.3f} | {g['own']:5.2f} | "
            f"{t0:8.3f} {t0s:8.3f} {t1:8.3f} | {'J1 resists more' if t1 > t0 + 1e-12 else ('J0 resists more' if t0 > t1 + 1e-12 else 'equal'):15s} | {ab}")
    say("Reading: canonical rows (lam 1) have one threshold at J = 0 whatever Ann expects, beta / (alpha + beta), and J = 1 "
        "resists more iff alpha > 0. Under X4, for w t*(q=0)/w < t < w t*(q=1)/w Bob honors iff Ann expects him to (guilt "
        "makes trust self-fulfilling); J = 1 has one threshold.")
    open(os.path.join(HERE, "trust_report.txt"), "w").write("\n".join(lines) + "\n")
    rows = []
    for sweep, key, xs, lams in (("lam", "lam", np.round(np.arange(0.5, 2.51, 0.05), 2), (None,)),
                                 ("a", "a", np.round(np.arange(0.0, 0.301, 0.01), 2), (1.0, X4["lam"])),
                                 ("n", "n", np.round(np.arange(0.0, 0.501, 0.02), 2), (1.0, X4["lam"]))):
        for lam in lams:
            for x in xs:
                kw = dict(EVENT, **{key: float(x)}, **({} if lam is None else {"lam": lam}))
                try:
                    g = gains(Event(**kw))
                except ValueError:
                    continue
                rows.append(dict(sweep=sweep, x=float(x), lam=kw["lam"], **{k: round(g[c] / g["own"], 4) for k, c in (
                    ("J0_expects_honor", "guilt"), ("J0_expects_grab", "surprise"), ("J1", "policy"))}))
    json.dump(rows, open(os.path.join(HERE, "trust_sweeps.json"), "w"))
