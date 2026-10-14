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
2005, partial: anticipation felt *after* the choice, with forgetting making the recalled
action signal the prediction (Thm. 1), so their dependence is causal self-inference;
Geanakoplos 1996 casts Newcomb as a one-player psychological game]
- A choice has Newcomb structure when an earlier, *already-experienced* payoff (felt
  anticipation) depends on a sufficiently accurate prediction of the later decision
  procedure.
- The earlier self is a natural predictor but not automatically a good one. Forecasts
  can come from habit, a promise, a mistaken self-model, or less information.
- Memory changes what the chooser *knows* about the earlier payoff, not the dependence
  itself. Bernheim & Thomadsen's route is the other one: imperfect memory creates a
  dependence of *later* anticipation on the choice, through what the remembered action
  reveals.

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
- **Direct geometric model, exact.** Let `N = T − 1`, `A_h = Σ_{j≤h} aα^j`,
  `B_h = Σ_{j≤h} mμ^j`.
  - Fixed-past weight: `c_t(s) = 1 + A_{s−t} + B_{N−s}`.
  - Delaying by `d` (with `h = N − t`) gains `A_d − μ^{h−d} B_d`: new anticipation minus
    lost memory.
  - **Pleasure:** taken at death (`τ = N`) iff `A_h > B_h` for every `h`, iff `aα > mμ`
    and `A_N > B_N`. If `α ≥ μ`, it is taken at `τ = N − h*`, where
    `h* = max({0} ∪ {h ≤ N : mμ^h ≥ aα})`. It lands in a terminal region whose depth is
    the number of memory steps before memory weight falls below the first step of
    anticipation.
  - **Pain:** `τ ∈ {0, N}`. Taken at death iff `aα < mμ` and `A_N < B_N`. Fixed-past
    timing is never later than commitment timing (the commitment weight
    `1 + A_s + B_{N−s}` is concave, so its minimum is at an endpoint).
  - Commitment: a pleasure goes to the interior peak of the concave weight.
- **Numerics, D and R.** Over 900 draws, fixed-past timing is not earlier than
  commitment for pleasures in 99% of cases, and not later for pains in 100%. Pleasure
  loss: median ~7.5%, max ~54% of the event's life-value.
- **The exceptions are preemption.** When fixed-past takes a pleasure *earlier* than
  commitment, the terminal region has unravelled to the front. Example (`α < μ`, outside
  the closed form): `a = 0.0465, α = 0.896, m = 0.0196, μ = 0.964, T = 40`. [checked]
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
- Example `a = m = 1, α = 0.3, μ = 0.2`: fixed-past `r(0) = 1.088`, `β_L = 0.541`;
  bilateral `r(0) = 1.215`, `β_L = 0.588`.
- This compares boundary treatments, not a theorem about FDT. Momentary hedonists at
  different times also have different objectives.

**D5. Beliefs are welfare.** [synthesis unless marked]
- Felt anticipation makes payoffs belief-dependent: psychological games (Geanakoplos,
  Pearce & Stacchetti) and personal equilibrium (Kőszegi 2010).
- **Which probability scores welfare.** Welfare is the objective expectation of the felt
  life-sum, as in Brunnermeier & Parker's well-being (2005, Def. 1). The agent's beliefs
  shape what is felt; they do not score it.
- **In expectation, the truth is free.** Anticipation linear in beliefs, Bayesian
  updating: forecasts are martingales, so by the tower property expected welfare does not
  depend on whether or when information arrives. [standard: Epstein 2008 p. 1121;
  Eliaz & Spiegler 2006 Prop. 1; Kőszegi & Rabin 2009 Prop. 2 (`γ = 1`); Bénabou 2015
  fn. 16; Kimball & Willis 2006]
- **Pathwise, it is not.** Good news raises `e` at once and bad news lowers it; the swings
  cancel only on average.
- **What prices information is nonlinearity in beliefs**, not in outcomes.
  - Utility concave in the posterior gives information aversion, convex gives seeking.
    [known: Eliaz & Spiegler 2006 Remark 1, two states, "not an original result";
    Bénabou & Tirole 2002 §V.B; one-shot anticipatory models: Kőszegi 2003, Caplin & Eliaz
    2003, Schweizer & Szech 2018; on LessWrong, jimrandomh 2011]
  - Dread outweighing savoring as a *kernel on outcomes* keeps anticipation linear in
    beliefs, so in the direct model information timing stays neutral. [checked]
  - In the recursive model it does not: a self anticipates its own later *felt states*,
    which contain later forecasts, so the asymmetry lands on a belief. Recursion has
    content here. [known in structure: a concave Kreps–Porteus aggregator prefers late
    resolution (Skiadas 1998, Prop. 1; Epstein 2008); Caplin & Leahy (2001, fn. 12) note
    that Kreps–Porteus leaves the assignment of utility across periods open, which the
    kernels fill. The felt-flow form, the D/R contrast and the identity below were not
    found. checked]
  - **Exact accounting.** Give the echo strengths a sign: savoring `a⁺` and dread `a⁻`
    forward, `m⁺` and `m⁻` back, an extension of the canonical equation separate from
    news's `λ`. With Bayesian forecasts and felt news switched off,
    `E[W] = W_sym − Σ_t w_t [(a⁻−a⁺) Σ_j α^j E[X_{t+j}⁻] + (m⁻−m⁺) Σ_j μ^j E[X_{t−j}⁻]]`,
    with `w` the life weights of the `(a⁺, m⁺)` kernel (1 in D) and `W_sym` its welfare.
    [proved; checked]
    - D: `X = u`. The negative parts do not depend on information, so timing is neutral.
    - R: `X = e`. Timing matters only if information moves some felt state across zero.
      With experienced utility positive throughout, dread asymmetry costs nothing however
      information arrives. [proved; checked; Codex's three-period example agrees]
    - Which way it cuts is not in the identity. In every example checked, earlier
      information spreads felt states and raises their expected negative part, so later
      revelation is better. [checked on examples]
    - Rumination prices information too: with bad felt states remembered more heavily
      (`m⁻ > m⁺`), the worry early news causes is remembered. Two periods, linear
      anticipation 0.2, `m⁺ = 0.1`, `m⁻ = 0.3`, terminal `u = ±1`: early revelation costs
      0.026 against revelation at realization. [checked; Codex]
    - With canonical news kept, its forcing `wᵀE[N]` enters too, and a symmetric baseline
      solved separately has different endogenous news; compare at fixed news forcing.
  - Other routes to avoidance: loss-averse news utility (core N2; Kőszegi & Rabin 2009
    Props. 1–4: partial information hurts, clumped information helps; Pagel 2018:
    inattention), and chosen beliefs with linear anticipation (Brunnermeier & Parker 2005
    pp. 1108–09; Oster, Shoulson & Dorsey 2013).
  - Limits. Bayesian belief-utility cannot produce attitudes that reverse with the prior
    (Eliaz & Spiegler Props. 2–3), and information choices cannot reveal which beliefs
    are good (their ordinality result, an analogue of P10). In the lab, 76% prefer sooner
    information and ~90% clumped (Falk & Zimmermann 2016).
- **Optimism is welfare; who pays.** [known: Brunnermeier & Parker 2005]
  - An upward-biased forecast raises anticipation now (first order) at a decision cost
    (second order). Brunnermeier & Parker's felicity is memory + flow + anticipation, so
    this is the direct model under objective probabilities.
  - The linear model charges only through decisions, so for an *unaware* optimist it
    endorses delusion wherever no decision hangs on the belief.
  - For a sophisticated near-Bayesian with linear anticipation, self-deception gains
    nothing: censoring bad news makes good news suspect, and the two effects cancel
    (Bénabou 2015 p. 677; Bénabou & Tirole 2002 §IV). This is Yudkowsky's "Doublethink"
    as a theorem. Delusion pays only for unaware agents, under nonlinear anticipation, or
    for instrumental reasons.
  - Not in Brunnermeier & Parker: a felt disappointment term. The felt-news extension
    (core N2–N3) supplies both the price of optimism (the news at realization) and a price
    on information. Disappointment is first-order, so the sign of the hedonically optimal
    bias depends on anticipation mass against remembered, loss-weighted disappointment:
    optimism for long-awaited events, bracing otherwise. In the canonical model the felt
    forecast already contains the expected disappointment, so a calibrated Bayesian is
    already braced (core N3).
- **Rationalization as hedonic arbitrage.** [speculation]
  - Updating less on bad news keeps anticipation high now and moves the cost into later
    disappointment or decisions.
  - Bénabou's cancellation says it pays only for agents who don't see themselves doing
    it, or under nonlinearity.
  - The evidence for asymmetric updating is contested. Supporting: Eil & Rao 2011;
    Möbius et al. 2022; Sharot et al. 2011. Against, as artifact or plain conservatism:
    Shah et al. 2016; Coutts 2019; Barron 2021.
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
- **Updateless affect**: feel by a coarser information flow than you act on. D7.
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
  self can count.
- Precedent for the mechanism: Bénabou & Tirole 2004 (personal rules; lapses are
  diagnostic of willpower, and self-confidence is an asset) and Bodner & Prelec 2003
  (self-signaling). Their payoff is instrumental: confidence sustains future effort. The
  hedonic payoff here, anticipation earned by being believed by yourself, was not found.
- D3 has the same structure: past anticipation, sunk for the fixed-past self.
- A past self having looked forward to the plan is not, by itself, a reason.

**D7. Affect policies and updateless affect.** [known in kind: Pagel 2018; Andries & Haddad
2020; the framing against Good's theorem and updatelessness is synthesis; speculation where
marked]
- **Two policies.** Actions are measurable with respect to the agent's information `F_t`.
  Felt forecasts and felt news are computed on an *affect filtration* `G_t ⊆ F_t`, coarser
  or delayed. Realized base utility is felt when it happens. Strict **updateless affect**:
  `G_t` is the prior until realization.
- **Free in linear models.** Without felt news or nonlinearity, expected welfare does not
  depend on `G` (tower property). [standard]
- **Which `G` is best depends on the nonlinearity.** [checked on examples]
  - R with dread or rumination asymmetry (D5): coarser `G` keeps felt states from spreading
    across zero, which is what D5's identity charges. Strict updateless affect is best in
    every example checked. A general comparison theorem is open: felt states under a
    coarser `G` are not simply conditional expectations of those under `F`.
  - Loss-averse felt news (core N2): a weighted scheduling problem. Subadditivity favours
    feeling news in batches; decaying `k_n` favours feeling far-off news early; the optimum
    trades them off, and neither rule dominates (core N2's counterexample). Strict
    updateless affect is optimal only if realization is the cheapest time.
- **The split in decision-theory terms.** Good's theorem and updatelessness concern the
  action policy, where information is ignorable. The affect policy is where information
  costs (KSS's cost-free half). A hedonic agent chooses both, and Good's theorem says
  nothing about the second.
- **Updateless action makes batched affect feasible.** `G ⊊ F` means acting on information
  one does not attend to: delegation, rules executed without fresh deliberation, long
  evaluation periods. Once a policy is acting for you, you can stop watching. Pagel's
  news-utility investor is the formal case: he prefers to ignore his portfolio, pays a
  manager to rebalance for him, and would like to commit to inattention. Andries & Haddad
  (2020) find the same under recursive disappointment aversion: state-dependent alerts
  after sharp drops raise welfare, and delegation cannot always shield the agent, because
  observed consumption reveals wealth (NBER WP, Prop. 5, pp. 23–24).
- **Not belief choice.** Beliefs stay accurate, so this is not Brunnermeier & Parker, and
  Bénabou's self-doubt cancellation does not bite. Whether affect can come apart from
  belief within one mind is open; attention and delegation are the known routes. Not
  found as a formal object on LessWrong; HonoreDB (2011) pins *belief* at the prior, a
  different split. Informal precedents below.
- **Example: P(doom).** A high forecast lowers felt anticipation, but that level effect is
  neutral ex ante in the linear model. Following every update piecemeal costs more than
  batching at equal weights when `λ > 1`. The hedonic prescription: settle a policy, act on
  it, and feel the forecast in batches. [speculation as psychology]
- **Informal precedents on LessWrong.** None batches or feels by a prior, but each splits
  affect from action.
  - Soares, "Detach the grim-o-meter" (2015): stop calibrating the grim-o-meter against
    the state of the world; keep it for local work.
  - Soares, "Simply locate yourself" (2015): treat bad news as information about where you
    ended up, not as the world going wrong. This has the updateless structure; with
    measure-weighted anticipation (A1) it is feeling by the prior over branches.
  - Mayer, "Being at peace with doom" (2023); TurnTrout, "Emotionally confronting a
    probably-doomed world" (2022: feelings are not beliefs); Sabien, "A way to be okay"
    (2023).
  - The constraint: the affect policy must not corrupt the beliefs action uses (Ruby, "A
    quick guide to confronting doom").
- **Open.** Fixed-past selves hurry pains (D3), and a body of news is a pain. Does that make
  them feel news piecemeal, i.e. over-check? Subadditivity pulls the other way; untested.

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
  - Per observer: copy-counted forward mass is `abα/(1 − bα)`, which needs `bα < 1`.
  - Total across observers: a trunk event is remembered by every descendant, so the
    copy-counted total needs `bμ < 1` (D) or `b(1+m)μ < 1` (R; memory-only resolvent
    `r(−j) = (m/(1+m))((1+m)μ)^j`). Example: `b = 2, m = 1, μ = 0.3` keeps each observer
    bounded (`M = 0.43`) while the copy-counted total diverges (`b(1+m)μ = 1.2`). [checked]
- **Under measure-weighting branching is welfare-invisible.** Forward mass is `aα/(1 − α)`,
  and the measure-weighted total memory of a trunk event is `m Σ μ^j`, the unbranched
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
