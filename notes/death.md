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
  `aα^j → aα^j(1−h)^j`. *standard for expected lifetime utility (Yaari 1965, text
  unread); inside felt anticipation known in kind (James 2016, two periods: `ĉ₂ = ŝc₂`)*

## The dead feel no news

- **Identity.** With linear news and Bayesian forecasts, the living's expected felt news is
  `E[Σ_{t<D} N_t] = E[Σ_j k_n(j) Ê_{D−1}[e_{D+j}]]`: the news-weighted forecast the dying
  self held of its unlived future, the news it would have felt on learning it had died,
  sign flipped. Unmasked forecasts are a martingale over all branches, and the only
  revision no one feels is the dying branch's; already-dead branches revise nothing.
  Recursion does not break it: expected future relief is inside the forecasts. Warned
  deaths have their forecasts at zero beforehand, so with warnings the term is zero.
  *not found (in Kőszegi & Rabin 2009 and Fels 2015 the realization is always felt; Kopczuk
  & Slemrod 2005 and Schünemann et al. 2023 have no news term); checked, recursive and
  direct; Codex's proof*
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
- **Against Kőszegi–Rabin.** With news over a felt realization, timing is neutral at
  `λ = 1`, and at `λ > 1`, `γ < 1` early full information is preferred: the realization's
  disappointment is felt at full weight, news ahead of it at `γ` (Fels 2015, Prop. I.1,
  after Kőszegi & Rabin 2009, Prop. 2). Mortality removes that realization in the dying
  branch, so the dividend exists at `λ = 1` and ignorance can beat early knowledge.
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
    (−0.11 at `L = 8`) > short warning (−0.54 at `L = 1`). Among warnings, earlier beats
    later, Fels's Obs. 5 for medical tests under Kőszegi–Rabin news *known in kind*; the
    sudden end on top is the unfelt realization.
  - Not a theorem. With weak news and strong echoes the order reverses (Codex: `n = 0.01,
    a = 0.4, m = 0.5`, death uniform on 1–8: sudden 10.43 < `L = 1` 10.82 < `L = 4`
    11.23 < foreseen 11.27). And a diagnosis's jolt is not just news about horizons `L`
    away, weighted `ν^L`: it changes present anticipation and the present felt state, and
    a diagnosis not arriving is news too.
- **Bad future (`u = −0.5`)**: at `λ = 1` the linear model reverses exactly (sudden −0.34);
  at `λ = 2` foreseen from birth is best and sudden worst (−0.77).
- **The hook.** In a representative German sample 87.7% would not want to know "today when
  you will die" and 4.2% would; Spain replicates (Gigerenzer & Garcia-Retamero 2017,
  p. 186). They explain it by anticipated regret, and find, with age as the proxy, that the
  nearer an event the less it is wanted, though not robustly for one's own death date. The
  model gives a reason before any loss aversion, and predicts the preference reverses for
  those who expect their future to be worse than zero.

## Hazard and the felt state of the living

- **Stationary closed form** (sudden death, constant `h`): `e* = u/(1 − M_h)`,
  `A_h = aα(1−h)/(1 − α(1−h))`. *checked; Codex derived it independently*
- Hazard shortens anticipation and adds relief:
  `M_h − M_0 = h[n/(1−ν+νh) − aα/((1−α)(1−α+αh))]`.
  - Near zero the sign is `N − M₁⁺`: news mass `n/(1−ν)` against anticipation's first
    moment `aα/(1−α)²`. *not found; checked on random draws*
  - Nearest: Kopczuk & Slemrod (2005) make surviving Bayesian news about one's frailty,
    which lowers fear (eq. 4). Relief here needs no frailty to learn about; a known
    constant hazard is enough.
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
  - Death denial as optimism about survival is known in kind: James (2016,
    `ŝ = s + d(1−s)` inside anticipation), Kopczuk & Slemrod (2005, repressed mortality
    signals), Schünemann et al. (2023, denial of a Huntington's shock, corrected at onset).
    In each, denial costs decisions or effort; never being corrected by news: *not found*.
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
  `J`. The future-bias reply is Parfit's (1984; Brueckner & Fischer 1986, unread), here
  partly located in the news kernel, and the life-sum's symmetry is the SEP's point that a
  preference for future life is irrational for "the life- or pleasure-gourmand" (Luper
  2026, §5.2). *synthesis; Parfit via Luper*
- **Hedonic zero is load-bearing** for every comparison here, as for any comparison across
  lifespans (core, Objects).

## Decisions that move the death date

**The exact case.** Three moments; 0 and 1 certain, 2 alive with probability `s + aδ`; paying
(`a = 1`) costs `c` at 1. Death sudden unless stated. Three evaluators: commitment (the plan
foreseen at 0, life-sum), fixed past (the plan `a_p` foreseen at 0, the choice news at 1,
remaining life-sum `e₁ + s_a e₂`), and the momentary self (`e₁`). Willingness to pay per unit
of survival, `δ → 0`, linear news, in base-utility units (a monetary value of a statistical
life would need a map from spending to felt utility):

- **Four channels**, from Codex's `W′ = w′ᵀe + wᵀ(I−H)^{−1}(b′ + H′e)`: `v = e₂[ω + Σ_t w_t
  ∂_s K_{t2}]/w₁`, with `w` the evaluator's weights.
  - Occupancy: the saved moment's own felt state, its memories included.
  - Anticipation of it, by every self whose forecast the evaluator lets depend on the
    choice: moment 1 always, moment 0 under commitment.
  - News of the choice (`+nν`): paying for safety off plan is good news about moment 2.
    Fixed past and momentary self only.
  - Lost relief (`−n`): a safer life makes surviving less of a relief, the dividend
    shrinking as fewer deaths go unfelt. Exactly `−ns/(1−n)` of every evaluator's WTP
    (Codex): −22.5% at `s = 0.9`, −12.5% at `s = 0.5`, `n = 0.2`. It is the partial
    effect, not news's total effect: the saved moment's occupancy already carries its own
    relief. *Known in kind: Macé & Peter (2021), prevention under Kőszegi–Rabin loss
    aversion makes the good outcome less elating; here the bad outcome's disappointment is
    unfelt.*
- **Closed forms** (Codex; `A = aα`, `B = mμ`, `A₂ = aα²`, `B₂ = mμ²`, `r = 1 − n + ns`,
  `q = A + nν`): `v_F = e₂(1−n)(1−n+q)/(r + sB)`, `v_M = e₂(1−n)q/r`,
  `v_C = e₂(1−n)G/Q` with `G = 1 + A + A² + A₂ + BA₂ − AB` and
  `Q = (1+A)r + s[B(1+A₂) + B₂(A − A₂)]`. *Synthesis, exact counterpart not located;
  checked against finite differences and the general solvers.*
- **Life calibration, `s = 0.9`**: commitment 0.91 (occupancy 1.03, anticipation 0.09, lost
  relief −0.21); fixed past 0.87 (0.85, 0.05, news 0.17, −0.20); momentary 0.18 (0.05, 0.17,
  −0.04).
  - The momentary self's share is `v_M/v_F = q(r + sB)/(r(1 − n + q))`, between zero and
    one with no universal value: 20% here, larger with strong anticipation, about 1% over a
    long remaining life (below).
- **Commitment against fixed past** differs by a few percent, signed by the earlier selves'
  anticipation (of the payment as well as the saved moment) against the news of choosing
  (the cost's revision now as well as the good news about survival). The
  sequential self under-invests in safety at both calibrations (0.87 against 0.91) and over-
  invests with strong anticipation (`a = 0.4, α = 0.6, m = 0.4, μ = 0.5`: 1.24 against
  1.21); in random draws it under-invests about two thirds of the time. *Known in kind:
  Strulik & Werner (2021), whose hyperbolic discounters revise their health plans and die
  about five years early; here the present bias comes from echoes, the choice is news, and
  the sign can flip.*
- **Loss-averse news makes safety plans sticky.** Off plan "no", paying is a felt loss now
  (the cost at horizon 0) and a gain later; off plan "yes", skipping is a loss about
  survival (signs provable at the thresholds, Codex). Both plans are credible between
  `F(1 + A − λn + nν)` and `F(1 + A − n + λnν)`, `F = e₂(1−n)/(r + sB)`, a band of width
  `Fn(λ−1)(1+ν)`. Life calibration, `λ = 2`: `[0.70, 1.00]` around the commitment 0.91, so
  the preferred personal equilibrium is the commitment choice (D3's mechanism, for
  mortality). *Known in kind: Kőszegi & Rabin (2009), Prop. 5, plans as their own
  commitment device.*
  - Containment is an inequality, `1 + A − λn + nν ≤ Θ ≤ 1 + A − n + λnν` with
    `Θ = G(r + sB)/Q`, not a theorem: about two thirds of random draws at `λ = 2`; the
    life calibration needs `λ ≥ 1.33`, strong anticipation 1.13.
  - It fails with short news reach (life calibration with `ν = 0.1`: commitment 0.90 above
    the band `[0.58, 0.77]`, so the safety plan is not credible and the sequential self
    skips) or weak news (`n = 0.001`: 1.09 below `[1.105, 1.107]`, over-investment).
    *Codex's counterexamples; checked*
- **How death comes changes what safety is worth.** Commitment WTP per unit survival, life
  calibration, three moments: sudden 0.91, warned a period ahead 1.07, foreseen from birth
  1.09 at `λ = 1`; at `λ = 2`, 0.91, 1.27, 1.25 (eight moments, risk before the fifth:
  2.85, 3.26, 3.32 and 2.85, 3.71, 3.49). Under sudden death the dividend makes safety
  cost relief; a warned death's news is felt and averages out at `λ = 1`, so that channel
  is gone, and at `λ = 2` the diagnosis is a felt loss that safety avoids. A premium for deaths after illness over sudden ones is debated in
  the value-of-statistical-life literature ("cancer premium"; not read here). *numerical*
- **The fixed past with a warning** (four moments, the choice at 1, the diagnosis at 2):
  sudden, commitment 0.91 against fixed past 0.83, band `[0.64, 0.93]` at `λ = 2`; warned,
  1.07 against 0.98, and at `λ = 2` 1.26 against `[0.92, 1.29]`. The sequential self
  under-invests either way; a warning widens the band in step with the WTP. *numerical*

**Over a long life** (risk off plan at `t₀ = 40`, plan hazard 0.01, life calibration; per unit
of extra death probability, life-sums from birth, reaching `t₀` with probability 0.67):

- Fixed past −53.7, commitment −53.6: the deprivation dominates, and neither semantics
  moves it.
- The momentary self feels about 1% of it: −0.90 against a survivor's remaining felt life
  of about 80. A self choosing by its current felt state takes mortal risks almost freely,
  because the deprivation is felt by no one: the Epicurean recklessness objection, as
  arithmetic.
- Loss-averse news bites only once the risk exceeds the plan's own hazard: the decision
  revises later horizons by about `h(1−h) − δ`, while arrival relief stays a gain. At
  `δ = 0.02`, `λ = 2`: momentary −1.36, fixed past −54.1, commitment −53.6. *numerical*

## Open

- A longer horizon for the decision case, and the band's containment as a condition rather
  than a share of draws. Schünemann, Strulik & Trimborn (2023) is the quantitative cousin
  for health investment with endogenous longevity.
- A known date against a dated hazard (mortality rising with age, a diagnosis with an
  uncertain lead).
- Dread of death: anticipating zero is not bad here, so fear of death lives only in news
  (a diagnosis), or needs a disvalue. The literature has two: an anticipated terminal
  deficit that weighs more as death nears (Schünemann et al. 2023, eq. 3), and fear
  increasing in the perceived hazard (Kopczuk & Slemrod 2005). Either adds a felt cost of
  hazard to set against the relief here.
- **Prior art still unread** (`references/inbox/`): Yaari 1965; Brueckner & Fischer 1986;
  the journal version of Fels 2015. What was read is in `bibliography.md`, value of
  information (economics) and field evidence.
