# Death dates: counterfactual lifespans in the additive model

**Status: exploring (2026-10-18; chosen dates 2026-10-27); a9's questions after the menu's G1,
not the post.** How the canonical model handles a death date that varies: across foreseen
lifespans, under risk, with information about it, and by choice. Additive reading throughout (`displacement.md`: additive, Z and
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

## Chosen death dates

An agent that can end its life at any moment, a biological immortal's only death. Checks:
`death.py` 16. Reviewed by Codex (`cu-death`).

- **The planner's increment.** Appending a moment to a foreseen life changes the life-sum by
  the new moment's own felt state times `1 + 1ᵀR_D k_f`, the earlier selves' anticipation of
  it, echoed (1.20 at the life calibration: the 83% above). An extension pays iff the moment it
  adds would feel good, its memories of the life included. *standard block algebra; checked*
  - That signs adjacent comparisons, not the optimum: with `u = (1, −2, 10)` the first failed
    extension is at `D = 1`, the best date `D = 3` (Codex). First failure is the optimum under
    single crossing, which holds for a nonincreasing, nonpositive base tail with geometric
    memory: once an appended moment feels bad, every later one does (Codex's argument).
    *derived; checked on random tails*
  - With nonnegative kernels and base utility above zero, extending always pays. The readings
    that could quit while ahead (Tr, Rn, Pr; full adaptation) are already out
    (`displacement.md`, `adaptation.md`), so in the surviving model a good immortal life is
    never worth ending.
  - **Living on memories.** Base utility 1 for 100 periods, then `−c`: the planner lives on
    past the crossing for 3, 2, 1, 0 periods (`c` = 0.02, 0.05, 0.1, 0.3) at the life
    calibration, 28, 17, 10, 0 with memory reach `μ = 0.9` at the same mass, and 155, 113, 83,
    39 with `μ = 0.95`, `B = 0.5`. At fixed mass, reach buys the time. *numerical*
- **The momentary self's exit.** Its past fixed on a foreseen plan, choosing death at `t₀ + 1`:
  its felt state falls by `S/(1 − λn)` if `S > 0`, `S/(1 − n)` if not (with `λn < 1`), where
  `S = Σ_{j≥1} [aα^j e_{t₀+j} + nν^j ψ_λ(e_{t₀+j})]` and `ψ_λ` has slope `λ` on positive felt
  states (losing a good moment is a felt loss), the kink taken per horizon as in X4. It prefers
  exit iff `S < 0`, a kernel-weighted forecast of its own felt states, mostly the next ten
  periods at the life calibration. Its present base utility cancels between the branches and
  enters only through the memories it leaves. *derived; checked*
  - At `λ = 1` the same functional rule holds when the coming states were just learned: the
    revision against the old forecasts is common to both branches (Codex). The continuation's
    felt states must then be solved from the actual past and the announcement's news, not the
    foreseen path. *derived*
  - **A temporary patch.** `k` periods at base level `x` in a good life (`u = 1`), 500 left.
    The momentary self prefers exit below `x*` = −3.29, −0.57, −0.095, −0.069 (`k` = 1, 4,
    13, 52); the remaining-life self below −489, −122, −37, −8.6. With 2000 left the
    momentary thresholds agree to every printed digit (geometric tails, so asymptotically) and
    the remaining-life ones scale with the life left (−1957, −492, −152, −37). At `λ = 2` the
    momentary self is a little more reluctant (−5.05, −0.82, −0.117, −0.087). *numerical*
  - **Immortality with an exit.** With summable kernels and an eventually uniformly positive
    base path, a finite patch leaves the remaining life-sum infinite, so the remaining-life
    self never exits, while the momentary threshold does not move. The momentary self values a
    stationary future at `(A + nν/(1 − ν))/(1 − n)` = 0.77 felt moments at `λ = 1` (1.80 at
    `λ = 2`). So the momentary self has a deviation incentive to exit at any stretch that tips
    `S` (a quarter at −0.1, a week at −3.3). Whether a life it controls ends there is the
    stopping problem in personal equilibrium (below): a sophisticated plan foresees later exits.
    *numerical; synthesis*
  - **The aftermath.** Exit preference outlasts the patch. One period at −100 in a good life:
    `S` = −20.5 before it, −2.5 during, −0.53 the period after, +0.30 the one after that
    (Codex). Remembered distress lowers the near future, so a wait as long as the patch does not
    filter it, and the delay needed can grow with depth (logarithmically, with geometric memory).
    Reassessment after a delay helps only if the later self must renew the request. Cooling-off
    periods, in the model, need to cover the patch's remembered tail as well as the patch.
    *checked; Codex's counterexample*
  - Prior art: Hamermesh & Soss (1974, *JPE* 82(1): 83–98), exit when discounted remaining
    lifetime utility falls below a threshold, the remaining-life rule; Becker & Posner (2004,
    an unpublished draft marked not for citation), the option value of waiting under uncertain
    future utility, which is not waiting out a known patch; Williams (1973, in *Problems of the
    Self*) on the tedium of immortality, here a claim about base utility that echoes do not
    supply. *bibliographic details verified (Codex, Gemini); texts unread*
- **The exit in equilibrium.** Checks: `death.py` 17 (plans), `exit.py` (the Markov exit).
  Reviewed by Codex (`cu-death`).
  - **The concept.** A plan is an equilibrium with a prescribed off-path continuation: no self
    before the planned date prefers exiting, the planned exiter prefers exiting to continuing,
    and the continuation after a deviation (never exiting again) is itself self-enforcing on the
    revised history. That is not yet the preferred credible plan, which would compare every
    credible continuation.
  - **Plans stick in a band** (`λ > 1`). Continuing against a planned exit revises forecasts up
    from zero: the patch's bad moments are losses at `λ`, the good future gains at 1, the mirror
    of exiting against a plan to continue. At the life calibration both "never exit" and "exit
    before the patch" are equilibria for a one-period patch between −5.05 and −2.13 at `λ = 2`
    (−3.66 to −2.95 at `λ = 1.2`), a four-period one between −0.82 and −0.42 (−0.62 to −0.52).
    Kőszegi & Rabin's plans as their own commitment (2009, Prop. 5), for exit: an expected
    continuation protects, an expected exit fulfils itself. *checked*
  - **At `λ = 1` the band closes when `α = ν`, as at the life calibration.** Different plans give
    different remembered pasts, so reference cancellation alone does not close it; with matched
    kernels, anticipation and news hang on one scalar `Σ_j α^j e_{τ+j}`, and at its zero the
    plans' prefixes coincide (Codex's argument). With `ν = 0.5` a band opens under linear news
    (one-period patch, about −2.192 to −2.180; both plans strict at −2.1858). *derived (Codex);
    checked*
  - **Which equilibrium expectations select.** Foreseen plans carry no news, so a self that picks
    the equilibrium best for itself compares foreseen felt paths that do not depend on `λ` (selves
    at the same date in two foreseen lives, not a choice with one past held fixed). Every prefix
    self ranks two plans by the sign of `Z_τ = Σ_j α^j e_{τ+j}` (Codex), so formation time does
    not matter; with `α = ν` that sign is the `λ = 1` exit criterion, and the pick switches
    exactly at the `λ = 1` edge (−3.29 for one period, −0.57 for four). The preferred-equilibrium
    refinement thus selects one branch within these matched-kernel bands; it does not remove the
    other equilibrium, and loss aversion decides only where expectations are set by something
    else, such as history, habit or a stated plan. The life-sum prefers never exiting
    throughout. *derived (Codex); checked*
    - D3's fixed-past learner lands on the earliest credible plan; here that would be the exit.
      *speculation, untested*
  - **The Markov exit** (AR(1) mood on a grid, mean 1, no memory): the exit policy over
    (previous, current) moods as a fixed point, references the previous self's forecasts given
    it continued (Codex checked the structure). At `λ = 1` it exits iff `S(s) < 0`, whatever the
    previous mood. With `α = ν` it reduces to `v = Πu + βΠv₊`, `β = α(1 + a) < 1`, a
    contraction: the policy is unique (up to exact indifference) and independent of news
    strength `n` (Codex). *derived; checked*
  - **Under loss-averse news state-contingent policies can stick too.** A two-state mood
    (`u = ±1.4`, stationary mean 1) has two strict equilibria at `λ = 2`, never exiting and
    exiting after two lows in a row (27 periods expected), and so does the grid at persistence
    0.55, sd 1.5 (Codex). Expectations select, and momentary selves disagree about which: in the
    two-state case selves in good moods prefer the equilibrium with exits (by 0.0018 and 0.00003)
    and selves in bad moods never exiting (by 0.0022 and 0.0036). The good-mood preference comes
    through felt news, their anticipation falling slightly (Codex). Never exiting has the
    higher mean over stationary mood pairs, and positive stationary welfare, so an infinite
    life-sum. *checked*
  - **The lifespan of an immortal with an exit**, under momentary control (`λ = 1`, life
    calibration without memory, weekly; expected weeks from the stationary mood, on a fine grid
    of 601 points over ±6 sd; the coarse 31-point, ±3 sd grid in brackets):

    | persistence | sd 0.5 | sd 0.75 | sd 1 | sd 1.5 |
    |---|---|---|---|---|
    | 0.5 | ∞ (∞) | ∞ (∞) | 2.2 million (∞) | 2100 (∞) |
    | 0.8 | 37,000 (∞) | 492 (471) | 112 (113) | 36 (36) |
    | 0.9 | 1460 (1215) | 170 (184) | 72 (61) | 35 (32) |
    | 0.95 | 790 (719) | 169 (150) | 86 (78) | 47 (42) |
    | 0.98 | 975 (928) | 269 (230) | 149 (124) | 87 (91) |

    ∞: no mood within the grid's span tips `S`, not immortality: the Gaussian tail goes further.
    The coarse grid's errors reach 20%, and refinement moves discrete stopping boundaries
    non-monotonically (Codex), so these are orders of magnitude. Persistence is what kills: the
    present does not enter, and a transient low predicts little. With a positive recurrent mean
    and linear news the remaining-life self never exits; under loss-averse news that needs
    positive long-run experienced welfare, not a positive mean mood (Codex: persistence 0.5, sd
    10, `λ = 2` has mean mood 1 and mean felt state −0.69). *numerical, grid-dependent; without
    memory, so without the aftermath*
  - **With memory.** The stock `H_{t+1} = μ(H_t + e_t)` joins the state, on a grid (converged:
    262.0 against 261.9 weeks at 121 and 241 points). A self's own felt state is remembered, so
    its continuation depends on it, and through its news on the previous mood even at `λ = 1`.
    Worse memories, exits at better moods: at persistence 0.9, sd 1, the highest exiting mood is
    −0.2 with the worst stock on the grid, −1.0 with the best. Expected remaining weeks after a
    forced-continuation start (300 weeks in which every self continues, then exits allowed;
    Codex checked 100 and 1000), on 31 moods, the coarse grid; no memory / the life
    calibration's `μ = 0.3`, `B = 0.17` / `μ = 0.9` at the same mass / `μ = 0.9`, `B = 0.5`:

    | `λ` | persistence, sd | none | `μ` 0.3 | `μ` 0.9 | `μ` 0.9, `B` 0.5 |
    |---|---|---|---|---|---|
    | 1 | 0.9, 1 | 60 | 60 | 91 | 260 |
    | 1 | 0.95, 0.75 | 149 | 149 | 202 | 492 |
    | 2 | 0.9, 1 | 60 | 44 | 64 | 142 |
    | 2 | 0.95, 0.75 | 148 | 106 | 155 | 322 |

    - **Long memory protects**: the agent lives on its memories through a low, about four times
      longer with slow, heavier memory. A finer mood grid moves both ends together (65 against
      265 at 61 moods).
    - **Short memory can go either way.** In the two cases shown it leaves first exits unchanged
      under linear news, the stock still holding the good weeks before the dip when the mood
      first reaches the exit line; that is not general: on a 15-mood grid (persistence 0.9, sd
      0.9) it halves the expected lifespan, 121 to 58 weeks (Codex).
    - **Under loss-averse news short strong memory hastened exit** in both cases (60 to 44
      weeks). A remembered downturn jolt is the plausible channel, not isolated from the
      changes in anticipation, references and policy. *numerical; the domain and spacing of the
      memory grid checked (Codex)*
  - In these models, exit incentives follow forecasts of experienced utility, news and (with
    memory) the aftermath included; depth, persistence, reference history and equilibrium
    selection all matter. Self-enforcing plans and multiple state-contingent equilibria are
    exhibited, the full stopping problem is not characterized. For agents with an exit option,
    what the model offers is that how the option is held in expectation can matter, not only
    when it is used. *speculation*
- **Under biphasic memory** (`adaptation.md`'s chosen form: afterglow minus a slow adaptation lobe
  `c γ^j` of mass `h`; a year's adaptation, `h = ½`). Checks: `death.py` 18, `exit.py` 4. Reviewed
  by Codex (`cu-death`).
  - The momentary rule is unchanged: signed memory is common to both branches and cancels from
    `S`, though it changes the felt path `S` reads. Stability: `Re(1 − K̂) ≥ 1 − A − B₊ − h(1 − g)/
    (1 + g)` on the unit circle, 0.67 at this calibration, so no zeros and winding zero (Codex).
    *derived*
  - **Positive levels can become intolerable after a large enough relative drop.** A foreseen
    permanent drop from 1 to `y` after 400 weeks: at `y = 0.3` the felt state is negative for 16
    weeks (lowest −0.12) though base utility stays positive, and the momentary self has an exit
    incentive on 14 dates, from just before the drop; at `y = 0.1`, 56 and 55; at `y ≥ 0.5`,
    none. Without adaptation, none at any positive `y`. The remembered high is the bar: a
    contrast trough. Levels still count: an equal drop from 2 to 1.3 opens none (lowest +0.73).
    And highs can hurt: a year at 4 followed by a return to 1 gives exit incentives on 16 dates
    after the high ends (Codex). *checked*
  - **The planner looks through the trough.** Its increments are negative for lives ending at
    402 to 417 weeks and welfare is back above the best earlier ending at 435: no single
    crossing, so "extend while the next moment feels good" holds only locally (its multiplier,
    1.20 here, is no longer positive by construction under signed memory; Codex checked it). A
    short epilogue at a lower level loses and a long one pays, as in `adaptation.md`'s EMA case.
    *checked*
  - **Thresholds become relative.** For downward patches, never exiting stops being an
    equilibrium below levels of −1.60 for a week (−3.29 without adaptation), +0.05 for four
    weeks (−0.57), +0.35 for a quarter (−0.05), +0.37 for a year (0): a patch at positive base
    utility ends it when it sits far enough below the bar. These are lower thresholds only:
    for a year-long patch never exiting holds only up to 3.01, above which the high's end
    triggers exit incentives (Codex). *checked*
  - **An aftermath, then rebound relief.** After four weeks at −2, against a life without the
    crisis on the same dates: 0.41 against 0.86 a week after, then 1.01 against 0.86 for weeks 4
    to 13, as the adaptation stock falls: the bar dropped during the crisis. Without adaptation
    there is only the aftermath (0.83 against 1.47), then the old level. *checked*
  - **Markov, with the adaptation lobe only** (expected remaining weeks; 31 moods, coarse):

    | persistence, sd | `h` | mean mood 1 | mean mood 2 | felt mean matched |
    |---|---|---|---|---|
    | 0.9, 1 | 0 | 60 | 1218 | |
    | 0.9, 1 | 0.5 | 31 | 175 | 78 |
    | 0.9, 1 | 2 | 14 | 33 | 166 |
    | 0.95, 0.75 | 0 | 149 | ∞ on the grid | |
    | 0.95, 0.75 | 0.5 | 63 | 592 | 210 |
    | 0.95, 0.75 | 2 | 24 | 84 | 1161 |

    - **Adaptation flattens the dependence on the mean mood** (mean 2 against mean 1: ×20,
      ×5.7, ×2.3 at persistence 0.9): the hazard follows changes more than levels.
    - **At a fixed mean mood adaptation shortens lives in these examples; matching the
      stationary felt mean of the no-exit models reverses the order.** That mean is exactly
      `E[u]/(1 − A + h)` for a stationary never-exit life under linear news (Codex), not the mean
      among living selves under exits. Raising the mean mood to match it (1.59 at `h = ½`, 3.35
      at `h = 2`), adaptation lengthens lives (78 and 166 against 60 at persistence 0.9; 210 and
      1161 against 149 at 0.95). So adaptation's other dynamics, adaptation to long lows among
      them, can more than offset its contrast effects; the comparison does not isolate a single
      channel. Stock grid, domain and burn-in checked by Codex. *numerical*
  - Afterglow and adaptation together need a second memory stock (a two-dimensional grid): open.
- **A hidden lottery against a chosen date.** A date drawn uniformly on a window and never
  announced, against a known date at the window's mean, adds +0.683 on 16–30 (2.1% of welfare)
  and +1.023 on 46–90 (1.0%), the same at `λ = 2`: sudden survival brings only gains and the
  known date no news. Against revelation at birth it is +0.682 and +1.023 (+0.684 on 16–30 at
  `λ = 2`, where revelation brings felt losses); that comparison changes echoes as well as news,
  so it is not a clean split. No optimization over death distributions, and under constant
  positive utility both lose to living on. *numerical*
  - **The gain is bounded in the mean lifespan** (Codex): with felt states in `[0, E_max]` for
    both lives, `|E W_hidden − W_known| ≤ E_max(N + J)/(1 − M)`, `N = Σ_j k_n(j)`,
    `J = Σ_j j (k_f(j) + k_b(j))` (3.07 at 46–90). An `O(1)` gain, a vanishing share of a long
    life, under uniform stability (which `M < 1` alone does not give, 6b). *derived; checked*
- With other people, a death is news to those who feel it: `vicarious.md`, grief.

## Open

- Learning selection: does a fixed-past learner, which lands on the earliest credible plan in
  D3, learn to exit? Sketched in `experiments/learned_expectations/exits.py` and `run_exits.py`,
  predictions written there, not yet run. The preferred credible plan in the full sense, rather than a prescribed
  continuation; proofs of the band's edges, numerical here.
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
