# formalism/

- `core.md` — the model, with status tags: the canonical model (recursive echoes and news,
  rational forecasts) and its reduced form; objects; echo propositions P1–P10; felt news
  N1–N4 (N3 and the threshold also in the canonical model), the recollection-news sketch and
  the 2×2; calibration per horizon; horizons, identity and peak-end
- `decision.md` — decision theory (CDT/EDT/FDT through `J`, the savoring trap, beliefs as
  welfare, reliability, affect policies, the shared-state critic) and anthropics (branching
  copies, imperfect recall) under the hedonic reading, D1–D8 and A1–A2
- `checks.py` — numerical verification of `core.md` and `decision.md`;
  `python formalism/checks.py`
- `pathwise.py` — pathwise simulation of the recursive model with felt news under
  unforeseen announcements, with exact root-finding, and the component plot
  (`full-model-over-time.png`); `python formalism/pathwise.py [out.png]`
- `playground/` — the interactive page (`index.html`, published as an artifact) and
  `model.js`, a JS port of `pathwise.py` that matches it to rounding, plus the direct model
  and exact root-counting past the despair threshold
