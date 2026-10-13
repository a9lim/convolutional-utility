# Decision theory and anthropics under the hedonic reading

Tags as in `core.md`. Hedonic reading: anticipation and memory are felt, so welfare is the
life-sum `W = Σ_t e(t)`. "Momentary hedonist" names the alternative objective `e(t)`.

## Setup: how much the felt past depends on the present choice

- Causal form (core P9): `e_t = u_t + Σ_{j>0} k(j) E_t[e_{t+j}] + Σ_{j>0} k(−j) e_{t−j}`.
  Felt anticipation is a function of the self's forecast, and the forecast includes a
  prediction of its own later choices.
- Partition into past `P` and remaining life `F`. Then
  `e_F = R_F (u_F + K_{FP} e_P)`, with `R_F = (I − K_{FF})^{-1}`.
- Let `J = ∂e_P/∂u_F`: whatever dependence of already-felt experience on the present
  choice the decision rule recognizes. Then
  **`∂W/∂u_F = 1_Pᵀ J + 1_Fᵀ R_F (I + K_{FP} J)`**. [standard algebra; Codex]
  - `J = 0`: fixed-past sequential choice. Weights `c_t(s) = [(I − K_{FF}ᵀ)^{-1} 1](s)`.
  - `J = J_pf`, the dependence in the full perfect-foresight solution: advance commitment,
    the planner's weights `w_T` (core P5).
  - Intermediate `J`: past anticipation tracks the present policy only as well as past
    selves could predict it. The graded case.

## Propositions

**D1. When a choice is Newcomb-like.** [synthesis; nearest prior art Bernheim & Thomadsen
2005, unread (abstract: anticipatory emotions plus imperfect memory resolve Newcomb);
Geanakoplos 1996 casts Newcomb as a one-player psychological game]
- A choice has Newcomb structure when an earlier, *already-experienced* payoff (felt
  anticipation) depends on a sufficiently accurate prediction of the later decision
  procedure.
- The earlier self is a natural predictor but not automatically a good one. Forecasts
  can come from habit, a promise, a mistaken self-model, or less information.
- Memory changes what the chooser *knows* about the earlier payoff, not the dependence
  itself.

**D2. Decision rules as choices of `J`.** [synthesis]
- **CDT**: `J = 0`.
- **FDT**: `J` comes from the logical dependence of past forecasts on the decision
  function. It equals `J_pf` only when those forecasts were accurate evaluations of that
  function on the realized input, which is extra assumption, not a consequence of
  identity. Compare Yudkowsky & Soares's transparent Newcomb, where FDT acts on a
  dependence specified for the observed input.
- **EDT**: `J` comes from the conditional correlation between action and past payoff,
  after conditioning on everything known. Memory can screen off this channel, but other
  correlations may remain. EDT need not lie between CDT and FDT.
- Hori–Kanaya's "mortality"/"eternity" split is the boundary-condition analogue, not a
  classification of decision theories.
- Core P9 stands: under imperfect foresight, the full fixed point misdescribes realized
  experience whatever the decision theory.
- Kőszegi–Rabin, as an analogy only:
  - unacclimating personal equilibrium (UPE) ≈ fixed-expectations sequential choice
    with consistency;
  - choice-acclimating personal equilibrium (CPE) ≈ choice followed by expectations
    adjusting, i.e. commitment timing, which a causal agent can implement;
  - preferred personal equilibrium (PPE) = the best self-enforcing plan.
  [known: Kőszegi & Rabin 2006 Def. 2; 2007 Defs. 1, 3]

**D3. The savoring trap.** Mechanism [known: Kőszegi 2010 §3.2 and Example 2, crediting
Loewenstein 1987 and Caplin & Leahy 2001]; exact stopping results [not found; checked].
- The mechanism: past anticipation is realized irreversibly, and later selves do not
  internalize it. Time inconsistency and welfare loss follow even between selves with
  *identical* utility functions.
- Backward induction is legitimate here only because past anticipation enters as an
  additive sunk term (Kőszegi §6.1). For general belief-dependent payoffs it fails
  (Geanakoplos, Pearce & Stacchetti; Battigalli & Dufwenberg).
- The problem: one indivisible pleasure or pain, schedulable from `t₀`. Selves share the
  life-sum objective. Compare a sophisticated fixed-past equilibrium (backward induction
  over selves) with the commitment optimum (`argmax/argmin w` over `[t₀, T)`, crediting
  no anticipation before the news).
- **Direct geometric model, exact.** Let `N = T − 1`, `A_h = Σ_{j≤h} aβ^j`,
  `B_h = Σ_{j≤h} mα^j`.
  - Fixed-past weight: `c_t(s) = 1 + A_{s−t} + B_{N−s}`.
  - Delaying by `d` (with `h = N − t`) gains `A_d − α^{h−d} B_d`: new anticipation minus
    lost memory.
  - **Pleasure:** taken at death (`τ = N`) iff `A_h > B_h` for every `h`, iff `aβ > mα`
    and `A_N > B_N`. If `β ≥ α`, it is taken at `τ = N − h*`, where
    `h* = max({0} ∪ {h ≤ N : mα^h ≥ aβ})`. It lands in a terminal region whose depth is
    the number of memory steps before memory weight falls below the first step of
    anticipation.
  - **Pain:** `τ ∈ {0, N}`. Taken at death iff `aβ < mα` and `A_N < B_N`. Fixed-past
    timing is never later than commitment timing (the commitment weight
    `1 + A_s + B_{N−s}` is concave, so its minimum is at an endpoint).
  - Commitment: a pleasure goes to the interior peak of the concave weight.
- **Numerics, D and R.** Over 900 draws, fixed-past timing is not earlier than
  commitment for pleasures in 99% of cases, and not later for pains in 100%. Pleasure
  loss: median ~7.5%, max ~54% of the event's life-value.
- **The exceptions are preemption.** When fixed-past takes a pleasure *earlier* than
  commitment, the terminal region has unravelled to the front. Example (`β < α`, outside
  the closed form): `a = 0.0465, β = 0.896, m = 0.0196, α = 0.964, T = 40`. [checked]
  - Each self compares only "now" against what later selves will do. `B_h ≥ A_h` first
    at `h = 38`, so every self from `t = 2` on prefers death to now and the continuation
    is `t = 39`, though each self's own optimum is interior (15–30).
  - Self 1 foresees this and takes the pleasure at once; self 0 waits one step for the
    anticipation. Fixed-past takes it at 1 against commitment's 15 (D, ~12% loss); at 4
    against 16 in R.
  - The logic of sophisticated preproperation (O'Donoghue & Rabin 1999): the trap seen
    one step earlier, not a counterexample to it.
- **Commitment versus FDT.** A causal agent with a binding commitment at news time
  reaches the commitment optimum. FDT's claimed advantage is reaching it without a
  device, *if* past forecasts track the policy (D2).
- **Psychology (speculation).**
  - Savoring delay (Loewenstein) can be optimal under commitment itself.
  - Procrastinated pleasures (Shu & Gneezy) are not evidence for the trap. Their
    activities carry effort costs, and their own mechanism (future effort discounted,
    future free time overpredicted) is what present bias predicts for costly pleasures.
  - The discriminating case is an *effortless* pleasure under sophistication.
    Sophisticated present bias preproperates it, and sophistication makes that worse
    (O'Donoghue & Rabin). Sophisticated fixed-past selves with anticipation postpone it.
  - Waiting is itself disliked and dread outweighs savoring (Hardisty & Weber 2020;
    Dawson & Johnson 2026), which weakens the pleasure side's premise.

**D4. Momentary hedonist: boundary treatment changes the present bias.** [checked]
- Fixed-past (half-line) row: `R⁺₀₀ = 1/H`, `β_L = 1 − H/(1+a)`.
- Bilateral row: `β_L = 1 − 1/((1+a) r(0))` (core P4).
- Example `a = m = 1, β = 0.3, α = 0.2`: fixed-past `r(0) = 1.088`, `β_L = 0.541`;
  bilateral `r(0) = 1.215`, `β_L = 0.588`.
- This compares boundary treatments, not a theorem about FDT. Momentary hedonists at
  different times also have different objectives.

**D5. Beliefs are welfare.** [synthesis unless marked; the sources marked "to verify" are
being read]
- Felt anticipation makes payoffs belief-dependent: psychological games (Geanakoplos,
  Pearce & Stacchetti) and personal equilibrium (Kőszegi 2010).
- **In expectation, the truth is free.** Linear model, fixed kernels, rational
  expectations: felt anticipation is a martingale, so by the tower property expected
  welfare does not depend on whether or when information arrives. [standard; Kimball &
  Willis 2006 make the same point for news utility]
- **Pathwise, it is not.** Good news raises `e` at once and bad news lowers it; the swings
  cancel only on average.
- **Asymmetric kernels price information.** If felt anticipation is concave in the
  forecast (dread outweighs savoring), information is a mean-preserving spread of the
  forecast, so by Jensen it lowers expected welfare even when no decision depends on it.
  Convex gives information seeking. [known in kind: Caplin & Leahy 2001; Kőszegi & Rabin
  2009 — to verify; on LessWrong, jimrandomh 2011's utility-of-belief example]
- **Optimism is welfare; the bill is decisions and disappointment.** An upward-biased
  forecast raises anticipation now, and under R it is remembered too. The linear model
  charges for it only through worse decisions, so it endorses delusion wherever no
  decision hangs on the belief. A real price needs a disappointment term (realized versus
  anticipated, as in Kőszegi–Rabin gain-loss utility) or memory of the forecast error.
  [known: Brunnermeier & Parker 2005, optimal expectations — to verify]
- **Rationalization as hedonic arbitrage.** Updating less on bad news than on good keeps
  anticipation high now and moves the cost into later disappointment or decisions. A
  candidate mechanism for asymmetric updating. [speculation; Bénabou & Tirole on motivated
  beliefs — to verify]
- **Instrumental versus intrinsic value of information.** [known: Kadane, Schervish &
  Seidenfeld 2008; Skyrms 1990]
  - Good's theorem: free information has nonnegative expected value because the agent can
    always act as if it had not seen it. KSS split "free" in two: *ignorable* (every
    decision rule stays available) and *cost-free* (ignoring it also leaves utility
    unchanged). Skyrms: really free needs utility independent of the result.
  - Felt anticipation makes information ignorable but not cost-free. KSS's own examples
    (the mystery's ending; Huntington's testing) are of this kind.
  - LessWrong's discussion is about the ignorable half. FDT says information is never
    negatively valued (Yudkowsky & Soares §4), and updatelessness is what removes an
    updateful agent's motive to avoid it. Exceptions run through action or bargaining:
    observation probabilities that depend on the policy (Diffractor 2018), and
    strategicness under logical uncertainty (Soto 2024; Demski 2019; Kokotajlo 2019).
  - So updatelessness about actions does not remove the hedonic cost: it lands on the
    felt forecast, not the action. [synthesis]
- **Updateless affect.** An agent whose felt anticipation tracks its prior forecast while
  its actions use the posterior keeps the decisions and drops the swings. Expected welfare
  is equal in the linear model and strictly higher under concave anticipation, before any
  disappointment term. A formal reading of equanimity. Not found on LessWrong; HonoreDB
  (2011) pins *belief* at the prior, a different split. [speculation]
- **Reflective consistency and linearity.** HonoreDB (2011) argues that a reflectively
  consistent UDT agent's utility of belief must be linear (contested). Linear anticipation
  is exactly the case where information is neutral in expectation. Whether reflective
  consistency forces linearity is open. [speculation]

**D6. Reliability is worth its anticipation.** [synthesis; speculation as psychology]
- Under rational expectations, anticipation of a plan scales with the forecast probability
  of following through. A self known to defect whenever the moment's local value dips
  anticipates *every* plan at a discount; a reliable self anticipates each at full value.
- So follow-through that looks like sunk-cost reasoning is justified at the policy level.
  The value is the anticipation that reliability earns across all plans, not the past
  anticipation of this one: Parfit's hitchhiker inside one life.
- Two channels. Acausal: past forecasts tracked the policy (`J ≠ 0`, D2), which a
  fixed-past self at the moment of defection ignores. Causal: following through now
  raises later selves' forecasts of their own reliability (self-reputation), which a CDT
  self can count. [precedent to verify: Bénabou & Tirole 2004, personal rules; Bodner &
  Prelec 2003, self-signaling]
- D3 has the same structure: past anticipation, sunk for the fixed-past self.
- A past self having looked forward to the plan is not, by itself, a reason.

## Anthropics

**A1. Echo on a branching tree: measure-weighting.** [synthesis; checked where marked]
- A `b`-ary tree of successors (copies) with geometric kernels.
- **Stance: anticipation is measure-weighted.** In the causal form, anticipation is a
  forecast `E_t[e_{t+j}]`, which already weights successors by their measure (Born weight,
  probability, share). Death or doom branches enter as zero experience, so a likely early
  end discounts the anticipated future.
- **What measure-weighting rules out.** Copy-counting anticipation would make anticipation
  a *sum* over successors, so a branching future could outweigh a single past without
  bound.
  - Per observer: copy-counted forward mass is `abβ/(1 − bβ)`, which needs `bβ < 1`.
  - Total across observers: a trunk event is remembered by every descendant, so the
    copy-counted total needs `bα < 1` (D) or `b(1+m)α < 1` (R; memory-only resolvent
    `r(−j) = (m/(1+m))((1+m)α)^j`). Example: `b = 2, m = 1, α = 0.3` keeps each observer
    bounded (`M = 0.43`) while the copy-counted total diverges (`b(1+m)α = 1.2`). [checked]
- **Under measure-weighting branching is welfare-invisible.** Forward mass is `aβ/(1 − β)`,
  and the measure-weighted total memory of a trunk event is `m Σ α^j`, the unbranched
  conditions exactly: it adds up to normality.
- These are utility weights, not credences, so they are not SSA or SIA. Armstrong derives
  SSA- or SIA-like *betting* from preferences plus linked decisions, and treats subjective
  anticipation as encoded in the utility function (LW 2011). Precedent for the weighting:
  Greaves's (2004) caring measure.
- Well-foundedness alone does not force measure-weighting (faster decay, bounded depth or
  saturation would also bound the sums); the forecast reading does.

**A2. Imperfect recall.** [synthesis]
- Amnesia cuts particular memory links. It creates self-location uncertainty only when
  the remaining observations fail to fix the current position. In that case `E_t` needs
  a self-locating credence.
- The policy space must be specified, including whether randomization is drawn fresh or
  remembered (Piccione & Rubinstein).
- Aumann, Hart & Perry dispute the planning/action inconsistency itself.
- The ex-ante-optimal policy is compatible with CDT plus generalized thirding and with
  EDT plus generalized double-halving (Oesterheld & Conitzer 2024). So "planning-optimal"
  is not a uniquely FDT verdict, and no FDT claim is made here.
