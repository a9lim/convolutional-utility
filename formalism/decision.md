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
- **Exceptions with long memory are not always small.** `a = 0.0465, β = 0.896,
  m = 0.0196, α = 0.964, T = 40`: fixed-past takes the pleasure at 1 against commitment's
  15 (D, ~12% loss), and at 4 against 16 (R).
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

**D5. Beliefs are welfare.** [synthesis]
- Felt anticipation makes payoffs belief-dependent: psychological games (Geanakoplos,
  Pearce & Stacchetti) and personal equilibrium (Kőszegi 2010).
- In the linear model with fixed kernels and rational expectations, the tower property
  removes any ex-ante value of changing when information arrives.
- Information preferences return with nonlinearity, disappointment, attention, or policy
  effects (Caplin & Leahy 2001; Brunnermeier & Parker 2005; Golman, Hagmann & Loewenstein
  2017).
- FDT's "information never hurts" is a claim about *instrumental* value. Under the
  hedonic reading, information can carry intrinsic negative value (dread: Berns et al.
  2006; Kőszegi 2010 §3.3).

**D6. Honouring past anticipation.** [speculation]
- Follow-through that looks like sunk-cost reasoning *can* be justified by a
  policy-level dependence: predictable follow-through generated valuable earlier
  anticipation, the structure of Parfit's hitchhiker.
- A past self having looked forward to the plan is not, by itself, enough.
- CDT may follow through too, for causal reasons such as future memory.

## Anthropics

**A1. Echo on a branching tree.** [synthesis; checked where marked]
- A `b`-ary tree of successors (copies) with geometric kernels.
- **Per observer.** Copy-counting anticipation has forward mass `abβ/(1 − bβ)`.
  - `M_tree = abβ/(1 − bβ) + mα/(1 − α) < 1` is a uniform contraction condition for
    bounded experienced utility on the infinite tree.
  - For finite trees the authoritative test is the spectral radius; the row-mass
    condition is only sufficient.
  - Share-weighted anticipation restores `aβ/(1 − β)`.
- **Total across observers** is a separate condition. A trunk event is remembered by
  every descendant.
  - Direct model: the remembered effect is `m Σ_j (bα)^j`, which needs `bα < 1`.
  - Recursive model: memory-only `r(−j) = (m/(1+m))((1+m)α)^j`, which needs
    `b(1+m)α < 1`. [checked]
  - Example: `b = 2, m = 1, α = 0.3` keeps each observer bounded (`M = 0.43`) while
    total welfare diverges (`b(1+m)α = 1.2`).
- **Two dials.** How a present mind represents its possible successors (normalized
  anticipation or not), and how welfare aggregates across them.
  - These are utility weights, not credences, so do not call them SSA and SIA. Armstrong
    derives SSA- or SIA-like *betting* from preferences plus linked decisions, without
    anthropic probabilities, and treats subjective anticipation as encoded in the
    utility function (LW 2011).
  - Share-weighting has a precedent in Greaves's (2004) caring measure.
  - Well-foundedness does not force normalization. Faster decay, bounded depth, or
    saturation would also do.

**A2. Sleeping Beauty: utility-adjusted betting weights.** [toy; checked]
- Setup: the heads awakening is remembered on Wednesday (weight `x_M`); the tails
  awakenings are not. Sunday's single shared anticipation is counted once in expected
  welfare.
- Per-event Sunday anticipation (`a` per awakening): tails:heads = `2(1+a):(1+a+x_M)`.
  This is 4:3 at `a = x_M = 1`, 1:1 at `x_M = 1 + a`, and goes to 0 as `x_M → ∞`.
- Normalized (average-awakening) anticipation: `(2+a):(1+a+x_M)`, so 1:1 at
  `a = x_M = 1`.
- Day-specific Sunday weights `a_M, a_T`: `(2 + a_M + a_T):(1 + a_M + x_M)`.
- Erasure alone does not equalize echo. These are betting weights, not updated
  probabilities about the coin. Armstrong's 2:1 versus 1:1 contrast is about total
  versus copy-average objectives for the offered bets.
- Precedent: Armstrong (2011 v1 §§2, 3.3.2) already shows memory-only value giving
  SSA-like odds. The asymmetric erasure and the mixed anticipation/memory weights are
  new here.

**A3. Imperfect recall.** [synthesis]
- Amnesia cuts particular memory links. It creates self-location uncertainty only when
  the remaining observations fail to fix the current position. In that case `E_t` needs
  a self-locating credence.
- The policy space must be specified, including whether randomization is drawn fresh or
  remembered (Piccione & Rubinstein).
- Aumann, Hart & Perry dispute the planning/action inconsistency itself.
- The ex-ante-optimal policy is compatible with CDT plus generalized thirding and with
  EDT plus generalized double-halving (Oesterheld & Conitzer 2024). So "planning-optimal"
  is not a uniquely FDT verdict, and no FDT claim is made here.
