# Death dates: counterfactual lifespans in the additive model

**Status: exploring (2026-10-18); a9's question after the menu's G1, not the post.** How the
canonical model handles a death date that varies: across foreseen lifespans, under risk, and
with information about it. Additive reading throughout (`displacement.md`: additive, Z and
survival-weighted Pr coincide here). Checks: `death.py` (`python notes/death.py`). Reviewed
by Codex (thread `cu-death`), whose corrections and counterexamples are folded in.

## Setup

- Death date `D`: the life is `[0, D)`. Dead moments are hedonic zero, so a forecast of
  `e_{t+j}` is `E_t[e_{t+j} 1{alive}]`, survival-weighted: A1's measure-weighting on the
  time axis (`selves.md`).
- Information: a diagnosis arrives `L` periods before death. `L = 0` is sudden death,
  `L ≥ T` foreseen from birth, with news at birth against a calibrated prior over `D`.
  "Warned" means the death is known by the update before it; a diagnosis that only raises
  the risk does not count.
- Welfare is `E[Σ_{t<D} e_t]`, scored by the objective measure (D5). Base utility does not
  depend on `D`, and actions are fixed (a warning has no value for preparation), except in
  the decisions section.
- Constant hazard `h` makes survival-weighted anticipation a shorter reach,
  `aα^j → aα^j(1−h)^j`. *standard for expected lifetime utility (Yaari 1965); applied to
  felt anticipation, synthesis*

## The dead feel no news

- **Identity.** With linear news and Bayesian forecasts, the living's expected felt news is
  `E[Σ_{t<D} N_t] = E[Σ_j k_n(j) Ê_{D−1}[e_{D+j}]]`: the news-weighted forecast the dying
  self held of its unlived future, the news it would have felt on learning it had died,
  sign flipped. Unmasked forecasts are a martingale over all branches, and the only
  revision no one feels is the dying branch's; already-dead branches revise nothing.
  Recursion does not break it: expected future relief is inside the forecasts. Warned
  deaths have their forecasts at zero beforehand, so with warnings the term is zero.
  *synthesis, exact counterpart not located; checked, recursive and direct; Codex's proof*
- This is raw felt news, not its welfare: zero expected news with a warning still moves
  welfare through echoes (below).
- **Pathwise**: every survived period is a little good news (relief at
  `h·Σ_j nν^j S(j) e_{t+j}` per period), and the bad news of a sudden death lands on no one.
  Epicurus for the news channel only: the deprivation itself is still counted.
- The sign is the sign of the dying self's forecast of its unlived future. A bad future
  reverses it: surviving is bad news felt, dying a relief unfelt.
- **The core's neutrality needs a fixed lifespan.** "Forecasts carry no expected future
  news" (core, the canonical model) holds for unmasked innovations; with mortality the felt
  news of the living has a nonzero mean. D5 already carries the qualifier.
- **Mortality adds feedback.** Anticipated relief is echo: under constant hazard the forward
  mass is `M_h = A_h + B + hn/(1 − ν(1−h))`, and `M_0 < 1` with `κ < 1` does not bound it
  (Codex: `a = 0.9, α = ½, m = 0, n = 0.3, ν = 0.99` has `M_0 = 0.9`, `κ = 0.3`,
  `M_h = 1.066` at `h = 0.05`; finite lives stay solvable, `e_0` = 9.5, 30, 99 at
  `T` = 30, 80, 150). Uniform boundedness under risk needs `sup_h M_h < 1`, P1(c)'s
  finite-against-uniform split again. *checked*

## What knowing the death date is worth

Linear news unless stated; good future (`u = 1`), life calibration, death uniform on
16–30 of a 30-period life. *numerical illustrations, not thresholds*

- **Mechanisms**, not an additive decomposition (news moves felt states, which move both
  forecasts and echoes):
  - the dividend above favours ignorance, first order in `n`;
  - D5's loop convexity favours knowing: remembered anticipation runs only in surviving
    branches;
  - a revelation's good news is echoed by the surviving branch, the doomed branch's bad
    news has less future to echo it.
- **Two periods, exactly** (Codex; one-step weights `a, m`, `p = P(D = 1)`). With
  `c = a + np(a+ν)/(1−n)`, `W_known = u₀ + (1−p)(1+a)(u₁ + mu₀)/(1 − mc)` and
  `W_sudden = u₀ + (1−p)(1+a)(u₁ + mu₀)/(1 − np − am(1−p))`. When `u₁ + mu₀ > 0`, knowing
  wins iff `am − n(1 − mν) + n² > 0`: the echo loop against the news, with a news loop
  on knowing's side. *checked against the tree, 147 draws*
  - In D5's example (`a = m = ½`, `ν = 0.7`) knowing always wins; its value dips from 1/7
    at `n = 0` to 0.137 at `n = 0.1`, then rises (0.47 at `n = 0.5`).
- **At the calibrations, ignorance wins.** Sudden death beats foreseen-from-birth by +0.68
  (about 2% of welfare); direct echoes +0.45; without news −0.035 (D5's route alone).
  Knowing wins with weak news and strong echoes (`n = 0.05`, `M = 0.9`: +0.7 to +2.4 by
  timing; about zero at `M = 0.64`).
- **Any warning forfeits the dividend**: +0.09 at `L = 1`, +0.03 at `L = 2`, gone by
  `L = 8`. What remains is selection: relief correlates with a long remaining life, which
  echoes it.
- **Loss-averse news.** Exactly, `E Σ N^{(λ)} = (the dividend) − (λ−1) E Σ_{t<D, j}
  k_n(j)(−ΔF_t^{t+j})₊`, both terms on the same loss-averse fixed point (Codex): the
  uncancelled death boundary against the losses actually felt.
  - At the calibrations (`λ = 2`): sudden +0.68 > foreseen from birth 0 > long warning
    (−0.11 at `L = 8`) > short warning (−0.54 at `L = 1`).
  - Not a theorem. With weak news and strong echoes the order reverses (Codex: `n = 0.01,
    a = 0.4, m = 0.5`, death uniform on 1–8: sudden 10.43 < `L = 1` 10.82 < `L = 4`
    11.23 < foreseen 11.27). And a diagnosis's jolt is not just news about horizons `L`
    away, weighted `ν^L`: it changes present anticipation and the present felt state, and
    a diagnosis not arriving is news too.
- **Bad future (`u = −0.5`)**: at `λ = 1` the linear model reverses exactly (sudden −0.34);
  at `λ = 2` foreseen from birth is best and sudden worst (−0.77).
- The hook: most people say they would not want to know (Gigerenzer & Garcia-Retamero
  2017, unverified). The model gives a reason before any loss aversion, and predicts the
  preference reverses for those who expect their future to be worse than zero.

## Hazard and the felt state of the living

- **Stationary closed form** (sudden death, constant `h`): `e* = u/(1 − M_h)`,
  `A_h = aα(1−h)/(1 − α(1−h))`. *checked; Codex derived it independently*
- Hazard shortens anticipation and adds relief:
  `M_h − M_0 = h[n/(1−ν+νh) − aα/((1−α)(1−α+αh))]`.
  - Near zero the sign is `N − M₁⁺`: news mass `n/(1−ν)` against anticipation's first
    moment `aα/(1−α)²`. *checked on random draws*
  - At finite `h` it can flip (Codex: `a = 0.1, α = ½, m = 0, n = 0.03, ν = 0.9`, `N > M₁⁺`,
    yet `e*` falls below `e*(0)` at `h = 0.2`).
  - With `α = ν` the sign is constant, and the felt state is invariant at every `h` iff
    `n = A`. The day calibration sits exactly there (`n = A = 0.2`, `α = ν = 0.8`).
  - Life calibration: `N = 0.67 > M₁⁺ = 0.50`; a weekly hazard of 0.02 raises the
    stationary felt state by 0.5%.
- Stationary experience is not welfare from birth: memory fills from birth, and the first
  moment has survival-weighted anticipation but no relief yet (next item).
- **Survival optimism.** A self that forecasts as if it will not die lives the hazard-free
  felt state, and the disappointment that would collect on its optimism is its death, which
  no one feels. Unlike optimism about outcomes one lives to see (N3; Brunnermeier & Parker),
  it is never corrected by news; it forgoes the relief instead.
  - Stationary, it wins iff `M_h < M_0`. From birth a boundary term favours it: at the day
    calibration the stationary states are equal, yet it wins by 0.8% of welfare at `h = 0.1`
    (Codex's exact case: 1/27 at equal stationary states). At the life calibration the
    Bayesian wins from birth, by 0.9% at `h = 0.05` and 0.2% at `h = 0.01`. *checked*
  - A restricted subjective-belief extension, not a Bayesian result: coherent immortal
    forecasts of its own experience, no informative decline or diagnosis, no separate cost
    of holding a false belief (Codex).
  - Menu D2 (quantum immortality prices doom news), in the linear model.

## Where death's harm lands

- **A foreseen extra period**, in the long-life limit, adds the interior weight
  `1/(1−M)` (1.472 at the life calibration): 83% is the new moment's own felt state, its
  memories of the life included, which no one else experiences; 17% is the raise in the
  living, set off by their anticipation of it and carried by recursive feedback.
  Deprivation is mostly unfelt. A comparison of two foreseen lives, not an intervention
  with felt experience fixed, and without news against a common prior.
- **Lucretius.** With a stationary kernel and a constant life, a period added at either
  end gives the same total welfare (translation), allocated differently (the new first
  moment 1.213, the new last 1.223). The welfare symmetry holds; forward news is one source
  of the attitude asymmetry (learning of a later death revises forecasts, learning of an
  earlier birth does not), not the whole: an earlier birth can change what is remembered,
  news about one's past can change forecasts, and the retrospective comparison involves
  `J`. Brueckner & Fischer's bias toward future goods, partly located in the news kernel.
  *synthesis; prior art from memory*
- **Hedonic zero is load-bearing** for every comparison here, as for any comparison across
  lifespans (core, Objects).

## Decisions that move the death date

A risk taken off plan at `t₀` (past felt states and forecasts fixed, the decision itself news
at `t₀`) against the same risk foreseen from birth (commitment). Life calibration, plan hazard
0.01, `t₀ = 40`; per unit of extra death probability, life-sums seen from birth (reaching
`t₀` has probability 0.67). *numerical*

- **The semantics barely differ.** Fixed past −53.7, commitment −53.6: the cost is the
  deprivation, which neither semantics moves. Commitment adds the earlier selves' lost
  anticipation, the fixed past adds the decision's news; at linear news these nearly cancel.
- **The momentary self feels about 1% of it**: −0.90, its lost anticipation plus the news
  of the choice (`≈ (A + N − n)·e*`), against a survivor's remaining felt life of about 80.
  A self choosing by its current felt state takes mortal risks almost freely, because the
  deprivation is felt by no one. The Epicurean recklessness objection, as arithmetic.
- **Loss-averse news** bites only once the risk exceeds the plan's own hazard: the decision
  revises later horizons by about `h(1−h) − δ`, while arrival relief stays a gain. At
  `δ = 0.02`, `λ = 2`: momentary −1.36, fixed past −54.1, commitment −53.6.
- `J` alone is not the whole decision (Codex): a mortality action changes which selves
  exist and with what probability, as well as their felt states. On a fixed tree,
  `W′ = w′ᵀe + wᵀ(I−H)^{−1}(b′ + H′e)`, the first term the change in occupancy weights.

## Open

- **The exact decision case** (Codex's first computation): three periods, one costly action
  lowering next-period mortality; advance commitment against a later choice holding past
  experience and its forecast reference fixed; a common mortality draw coupling the
  counterfactuals; willingness to pay under the life-sum, linear news first, then `λ = 2`.
  It separates the value of survival, relief, lost disappointment and past anticipation.
- A known date against a dated hazard (mortality rising with age, a diagnosis with an
  uncertain lead).
- Dread of death: anticipating zero is not bad here, so fear of death lives only in news
  (a diagnosis), or needs a kink or a disvalue of dying.
- **Prior art.** Read in full before any priority claim:
  - Fels 2015, "On the value of information: why people reject medical tests":
    Kőszegi–Rabin news utility applied to testing, disappointment and timing; close to the
    loss-averse ordering (abstract seen by Codex).
  - Schünemann, Strulik & Trimborn 2023 (*J. Health Econ.*): anticipatory utility and
    endogenous beliefs in a life-cycle model of health and longevity, Huntington's testing
    included; relevant to the decision case.
  - Kőszegi 2003 (health anxiety and avoided information); Caplin & Leahy 2001.
  - Oster, Shoulson & Dorsey 2013 and the corrigendum: less overoptimism than first
    reported, concentrated among people with more advanced symptoms; genetic status is not
    a death date.
  - James 2016, an economic model of mortality salience and death denial (abstract only).
  - Yaari 1965 (record verified, text not); Brueckner & Fischer 1986; Nagel 1970;
    Gigerenzer & Garcia-Retamero 2017.
