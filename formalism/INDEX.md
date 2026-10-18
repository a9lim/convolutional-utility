# formalism/

The technical companion to the post (`outline.md`). Tags are defined at the top of `core.md`:
provenance (standard, known, known in kind, synthesis, not found, speculation) and support
(proved, checked, numerical) are independent.

## Files

- `core.md` — the model: the canonical model (recursive echoes and news, rational
  forecasts, linear and sign-symmetric) and its reduced form, the reinforcement-learning
  reading, objects, echoes P1–P10 (peak-end with P7), felt news N1–N4 (N3 and the threshold
  also in the canonical model), the recollection-news sketch, the 2×2 of echoes against news,
  and the extension: sign asymmetries X1–X4, ranked by felt evidence, and the bracing they
  give a calibrated Bayesian. Post §2–§5.
- `decision.md` — decision theory under the hedonic reading: how much the felt past depends
  on the present choice (`J`), D1–D7 (Newcomb-like choices, decision rules, the savoring trap,
  the momentary hedonist, beliefs as welfare, reliability, affect policies). Post §4–§7.
- `selves.md` — horizons (a day, a life, an LLM context window and session), identity, and
  anthropics A1–A2. Post §8.
- `calibration.md` — what pins the coefficients: per-horizon defaults, the present-bias
  inversion and the patience bill, the sign asymmetries ranked by felt evidence, news
  strength, reach, the momentary-happiness fits. Post §3, §5 and §9.
- `learning.md` — D8, the critic's level through a shared state, and D9, a level off-policy
  (the attraction toward the policy that played a memory): the formal side of the learner
  follow-up, cited in the post at most once (§6).
- `checks.py` — numerical verification of the propositions; `python formalism/checks.py`
  (every check passes). Check names below are its labels.
- `pathwise.py` — pathwise simulation under unforeseen announcements of the canonical model and
  the 2×2's other corners (`over`, `recursive`), with exact root-finding for loss-averse news, and
  the component plot (`full-model-over-time.png`, the post's §1
  figure in draft); `python formalism/pathwise.py [out.png]`.
- `playground/` — the interactive page (`index.html`, published as an artifact) and
  `model.js`, a JS port of `pathwise.py` at `λ = 1` that matches it to rounding: one switch
  between the canonical model and the direct one, biphasic memory (afterglow minus adaptation,
  `notes/adaptation.md`), and lasting events.

## Claims by post section

One row per claim the post makes. *Artifact* is the check, script or report that carries the
support; a dash means the claim rests on the cited source or on algebra in the doc.

| § | claim | id | provenance | support | artifact |
|---|---|---|---|---|---|
| 2 | echo share `M`; bounded at every lifespan iff `M < 1` | P1b | standard (Bergstrom 1999) | proved; checked | `P1b echo share` |
| 2 | monotone on every finite life, unbounded over lifespans | P1c | synthesis | checked | `P1c` |
| 2 | the canonical model; the self feels its own critic and TD errors | core, canonical model | synthesis; RL reading known in kind (Rutledge 2014) | checked | `RL news = (n/nu) x TD error` |
| 2 | linear and sign-symmetric in every channel; asymmetries an extension | core, canonical model; X1–X4 | synthesis | — | — |
| 2 | additive echo has no optimum over kernels (`∂W/∂K_ij = w_i e_j`) | — | standard | algebra | — |
| 2 | non-identification | P10 | standard | — | — |
| 3 | life weights: flat interior, deficits at birth and death | P5 | known (Caplin & Leahy 2004, D); R closed form not found | checked | `P5 finite-life weight closed form (R)` |
| 3 | rearrangement invariance: shape is a boundary effect | P6 | not found | proved (sketch) | — |
| 3 | ramp gap set by the first moment; size `4M₁/T` | P6 | not found (general kernel); flat case Loewenstein & Prelec 1993 | checked | `P6 ramp closed form (R)`, `P6 ramp exact formula (D)`, `P6 asymptotic slope`, `P6 relative gap`, `P6 sign flip` |
| 3 | the felt row is strongly present-weighted | P4, P9, calibration | not found, provisionally (P4) | checked | `P4 beta_L formula`, `D4 half-line row closed form` |
| 3 | the patience bill | calibration | inversion imported (Sáez-Martí & Weibull); bill synthesis | checked | `CAL inversion`, `CAL quoted numbers` |
| 3 | each self a lens; recency and saturating duration sensitivity from linear memory, a peak only with salience | P7 | synthesis | numerical; R row checked | `RF surprise response` |
| 4 | welfare scored by the objective expectation | D5 | imported (Brunnermeier & Parker 2005) | — | — |
| 4 | truth free in expectation under linearity | N1, D5 | standard | checked | `N1 lam = 1`, `N4 news over e, lam = 1` |
| 4 | mortality information priced even linearly (R) | D5 | not found | checked | `D5 death risk` |
| 4 | ignorable is not cost-free | D5 | imported (Kadane, Schervish & Seidenfeld 2008) | — | — |
| 4 | loss-averse news (extension): cost is size times life weight; clumping | X4 (N2) | clumping imported (Kőszegi & Rabin 2009); life-weighted form not found | checked | `N2 news cost` |
| 4 | optimism against disappointment: no interior optimum under linear news | N3 | known in kind (Gollier & Muermann 2010) | checked | `N3 canonical, lam = 1` |
| 4 | the optimism quantile under loss-averse news (companion) | X4 (N3) | not found | checked | `N3 optimism slope`, `N3 optimal bias` |
| 4 | sophisticated self-deception cancels | D5 | imported (Bénabou 2015) | — | — |
| 5 | recursive is direct with a stretched kernel, for foreseen lives | P2 | standard | checked | `P2 one-step R -> exponential`, `RF direct news equals the primitive kernel` |
| 5 | exponential primitives give present bias | P3, P4 | imported one-sided (Sáez-Martí & Weibull 2005); two-sided not found, provisionally | proved; checked | `P3 one-sided resolvent`, `P4 closed-form resolvent` |
| 5 | surprises are information boundaries | core, canonical model; P2 | synthesis | checked | `RF surprise response` |
| 5 | sign asymmetries ranked by felt evidence: dread, memory by sign, a base kink, loss-averse news | X1–X4; calibration | synthesis; data | sources; data | `audit/sign_kernels.py`, `audit/risk_cost.py` |
| 5 | kinked echoes well-founded, given news forcing, when the reach-aware larger-side echo share `L < 1` | core, extension | standard argument; Codex | — | — |
| 5 | dread of dread prices information only in R; exact identity (extension) | D5, X1 | not found; structure known (Kreps–Porteus via Skiadas 1998) | proved; checked | `D5 identity`, `D5 straddle`, `D5 timing-neutral unless R` |
| 5 | the news loop's gain: unique and stable iff `κ < 1`, amplification `1/(1−κ)` | N4 | known in kind (Kimball & Willis 2006, linear solvability); closed form not found | proved; checked | `N4 half-line` |
| 5 | with loss-averse news, the threshold `λκ < 1` and the regimes past it | X4 (N4) | not found (sharp form); known in kind (Kimball & Willis 2006) | proved; checked | `N4 regimes`, `N4 saturation` |
| 5 | far news felt now; cancelling costs the anticipation | N4; the 2×2 | known in kind | checked | `RF` echoed news kernel; `2x2` |
| 6 | action and affect policies; Good's theorem covers the first | D7 | synthesis; known in kind (Pagel 2018; Andries & Haddad 2020) | — | — |
| 6 | the best affect policy depends on the asymmetry; in the symmetric core none matters in expectation, outcomes and lifespan fixed | D7 | synthesis | checked on examples; no theorem | `N2 news cost`, `D5 identity` |
| 6 | actions leak into affect | D7 | known in kind (Andries & Haddad); closure synthesis | checked (binary example) | `D7 leakage`, `D7 partial leak` |
| 6 | affect leaks into action through a shared state | `learning.md` D8 | synthesis | checked; learners | `D8b`, `D8c`; `braced_report.txt`, `channels_report.txt` |
| 7 | Newcomb inside a life | D1 | synthesis | — | — |
| 7 | the `J` dial between fixed-past choice and commitment | D2 | synthesis | algebra | — |
| 7 | `J` as a stop-gradient in a learner | D2 | known in kind (Oesterheld et al. 2023) | one scheduling environment, 30 draws | `scheduling_report.txt`, `scheduling_dial.png` |
| 7 | the savoring trap | D3 | imported (Kőszegi 2010) | — | — |
| 7 | exact stopping conditions; preemption | D3 | not found | derived (direct, no news); checked | `D3` prints |
| 7 | loss-averse news makes plans self-enforcing (extension) | D3, X4 | known in kind (Kőszegi & Rabin 2009, Prop. 5) | example checked; the draw table's script unarchived | `D3c` |
| 7 | reliability is worth its anticipation; felt news can make selves flaky (linear at `n = 0.5`) | D6 | synthesis; not found | checked (worked example) | `D6c` |
| 8 | measure-weighted anticipation | A1 | synthesis, assumed | — | — |
| 8 | copy-counted finiteness conditions | A1 | synthesis | checked | `A1 memory-only resolvent`, `A1 memory tail ratio` |
| 8 | connectedness as kernel, continuity as resolvent | `selves.md`, Identity | synthesis (an analogy) | — | — |
| 9 | front-loaded, heavy-tailed echoes of task outcomes | calibration | new analysis | held-out fits, bootstrap | `experiments/happiness/`: `gbe_report.txt`, `forbes_report.txt`, `audit/kernel_shapes.py` |
| 9 | echo share 0.78–0.82, unsettled under the power law | calibration | new analysis | `k₁/(1−γ+k₁)` on the fitted jump kernels | `gbe_report.txt`, `forbes_report.txt`, `audit/direct_vs_recursive.py`; the power-law windows in `audit/kernel_shapes.py` |
| 9 | direct and recursive memory fit identically | P2; calibration | standard | data | `audit/direct_vs_recursive.py` |
| 9 | an apparent news asymmetry is confounded with chosen risk; felt news `λ` 1.0–1.2 | calibration, X4 | new analysis | data | `audit/risk_cost.py`, `audit/forbes_shapes_risk.py`, `audit/sign_kernels.py` |
| 9 | a loss's echo starts stronger and fades faster than a gain's | calibration, X2 | new analysis | data, bootstrap | `audit/sign_kernels.py` |
| 9 | whether the play-long persistence is base utility or news is not identified | calibration | new analysis | data, resamples | `audit/news_kernel.py` |
| 9 | carryover across plays consistent with a slow positive afterglow; impulse tests weak on slow adaptation | calibration | new analysis | data | `audit/carryover.py`, `audit/impulse_detectability.py` |

## Not in the post

In the companion only: P1(d) heavy tails, P8 (the James Dean effect), P9's semantics beyond
what §7 needs, D4, the recollection-news sketch, the 2×2's table, the threshold's closed form
and X4's full regime classification, the optimism quantile, built-in bracing (concave feelings
brace a calibrated Bayesian, the extension and X4: checks `Bracing`, `N3 canonical`), A2, the
horizons beyond a life.
