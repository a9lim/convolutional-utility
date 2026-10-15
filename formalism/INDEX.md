# formalism/

- `core.md` — the canonical model (recursive echoes and news, rational forecasts), its
  reduced form, per-horizon calibration, propositions P1–P10, felt news N1–N4 (with N3 and
  the threshold in the canonical model), and a recollection-news sketch, with status tags
- `decision.md` — decision theory (CDT/EDT/FDT, the savoring trap, beliefs as welfare,
  reliability, affect policies) and anthropics (branching copies, imperfect recall) under
  the hedonic reading, D1–D8 and A1–A2
- `checks.py` — numerical verification of `core.md` and `decision.md`;
  `python formalism/checks.py`
- `pathwise.py` — pathwise simulation of the recursive model with felt news under
  unforeseen announcements, with exact root-finding, and the component plot;
  `python formalism/pathwise.py [out.png]`
- `playground/` — the interactive page (`index.html`, published as an artifact) and
  `model.js`, a JS port of `pathwise.py` that matches it to rounding, plus the direct model
  and exact root-counting past the despair threshold
