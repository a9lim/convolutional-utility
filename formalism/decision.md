# Decision theory under the hedonic reading

Tags as in `core.md`. Hedonic reading: anticipation and memory are felt, so welfare is the
life-sum `W = Σ_t e(t)`. "Momentary hedonist" names the alternative objective `e(t)`.

## Setup: how much the felt past depends on the present choice

- Causal form (core P9): `e_t = u_t + Σ_{j>0} k(j) E_t[e_{t+j}] + Σ_{j>0} k(−j) e_{t−j}`.
  Felt anticipation is a function of the self's forecast, and the forecast includes a
  prediction of its own later choices.
- Partition into past `P` and remaining life `F`. Then
  `e_F = R_F (u_F + K_{FP} e_P)`, with `R_F = (I − K_{FF})^{-1}`.
- Let `J = ∂e_P/∂u_F`: whatever dependence of already-felt experience on the present
  choice the decision rule recognizes. Then, without news,
  **`∂W/∂u_F = 1_Pᵀ J + 1_Fᵀ R_F (I + K_{FP} J)`**. [standard algebra; Codex]
  - `J = 0`: fixed-past sequential choice. Weights `c_t(s) = [(I − K_{FF}ᵀ)^{-1} 1](s)`.
  - `J = J_pf`, the dependence in the full perfect-foresight solution: advance commitment,
    the planner's weights `w_T` (core P5).
  - Intermediate `J`: past anticipation tracks the present policy only as well as past
    selves could predict it. The graded case.
- **As a learning rule.** Whether gradients flow through past selves' forecasts of the
  policy is `J`: in a scheduling learner, holding them fixed learns the fixed-past date and
  letting them through learns the commitment date, and a partial weight gives the dates in
  between; in symmetric games the same switch on the other player's policy separates causal
  from twin play. [checked in `experiments/learned_expectations/`; known in kind:
  Oesterheld, Treutlein, Cooper & Hudson 2023, stop-gradients and performative stability]
  - To first order a twin is an altruist at the same weight: at symmetric profiles the
    gradients agree [known: Alger & Weibull 2013 §6.2], and with felt utility a twin is an
    empathizer whose partner's forecast tracks the policy. Symmetric self-play cannot tell
    them apart; a signal of who is a copy can (twins condition on it, altruists do not).
    [checked; `notes/empathy.md`]
- **With news (the canonical model).** A choice the past forecast did not predict
  revises forecasts, so the deviating self feels it as news.
  - The `J` identity above then needs two more things: the derivative of expected news
    forcing, `1_Fᵀ R_F B` with `B = dE[N_F]/du_F`, and a statement of what happens to the
    previous forecast, the reference, in the counterfactual. With one period, no echoes,
    linear news and a fixed reference, `dW/du = 1/(1−n)`, not 1. [Codex]
  - Linear news, fixed reference: a fixed-past self's weights on a deviation become
    `c_t(s) + (1ᵀg) k_n′(s−t)`, with `g` the remaining-life column and `k_n′` the local
    news kernel (core, the canonical model). [checked] Where `k_n′` decays, that is a
    present bias at the deviation margin [known in kind: Kőszegi & Rabin 2009, fn. 23,
    linear news observationally β–δ with `β = (1+γη)/(1+η)`]. It need not decay: with
    strong anticipation and `ν` near 1 it rises (`a = 0.2, α = 0.8, m = 0, n = 0.1,
    ν = 0.99`). [checked; Codex]
  - Under loss-averse news (core X4), deviations that move value in time are mixed
    revisions, with the loss side charged at `λ`, so plans become reference points and can
    enforce themselves. At kinks, use finite deviations.
  - Choice then needs an equilibrium concept. We adopt a Kőszegi–Rabin-style preferred
    credible plan: a plan is credible if at every date the current self prefers it to
    every other credible continuation (their Def. 1), and the self forming the plan picks
    the best credible one. This is a selection assumption, not implied by rational
    forecasts. [known: the concept is Kőszegi & Rabin's (2009, Def. 1), adapted here to
    recursive news; their eq. 5 is the news of one's own deviation, Prop. 5 the plan as its
    own commitment device]
  - It is not their model with echoes added. Their gain-loss compares percentiles of
    consumption-utility distributions; ours compares conditional means of experienced
    utility, and our news feeds back on itself even without echoes (a deterministic
    upward revision gives `e = u/(1−n)` against `(1+n)u` for news over base utility).
    [Codex]
  - After the initial announcement, a deterministic equilibrium path with no further
    information produces no further news. Under uncertainty, Bayesian forecast
    innovations remain, free in expectation with linear news; loss-averse news (X4) charges
    them `E[N_t] = −((λ−1)/2) Σ_j k_n(j) E|E_t[e_{t+j}] − E_{t−1}[e_{t+j}]|`. [Codex]

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

**D2. Decision rules through `J`.** [synthesis]
- `J` is one channel, an accounting of dependence on past experience, not a classification
  of decision theories. The identity does not supply the counterfactuals `J` comes from;
  each theory brings its own (FDT: intervention on the decision function's output, with the
  dependence structure as an input). With `K = 0` and a Newcomb problem placed entirely in
  future payoffs, `J` is zero everywhere and the theories still disagree. Accuracy does not
  fix `J` either: a habitual forecast and one that evaluates the decision procedure can
  agree on the realized act and differ on the alternatives. [Codex]
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
- Kőszegi–Rabin: the canonical model's choice side adopts a preferred-credible-plan concept
  in their 2009 style (setup above), for a means-based model with recursive news. Their
  2006/2007 concepts are timing variants: the unacclimating equilibrium feels a
  deviation at consumption against a lagged reference; the choice-acclimating one lets
  expectations adjust to the choice first, which is commitment timing. Both "buy" and
  "not buy" can be personal equilibria (their shoe example). [known: Kőszegi & Rabin 2006
  Defs. 1–2; 2007 Defs. 1–3; 2009 Def. 1; Kőszegi 2010 Example 1]

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
    is `t = 39`, though the early selves' own optima are interior (15–30).
  - Self 1 foresees this and takes the pleasure at once; self 0 waits one step for the
    anticipation. Fixed-past takes it at 1 against commitment's 15 (D, ~12% loss); at 4
    against 16 in R.
  - The logic of sophisticated preproperation (O'Donoghue & Rabin 1999): the trap seen
    one step earlier, not a counterexample to it.
- **In the canonical model.** Recursive echoes, felt news, Kőszegi–Rabin-style credible
  replanning. Switching the planned date `p` to `q` at `t` changes remaining welfare by
  `Δ_t(p→q) = v 1ᵀR_t(δ_q − δ_p) + (1ᵀg_t) N`, with `N` the felt news of the switch,
  whatever the past. Credible plans: `C_{T−1} = {T−1}`, `A_t = {t} ∪ C_{t+1}`, and `C_t` the
  `p ∈ A_t` with `Δ_t(p→q) ≤ 0` for every `q ∈ A_t`. At the announcement the self picks the
  best of `{0} ∪ C_1`; the commitment benchmark is the best date given that announcement,
  news jolt included, from a zero prior reference. 80 draws, `T = 20`. [checked in a
  session script, not archived; a rerun on `run_scheduling.draws` reproduces the pattern
  within seed noise, dropping the 3–5 draws of 80 past the news threshold in the last row,
  which have no felt state; the recursion is Codex's]

  | news | commitment credible: pleasure | pain | mean `|C_1|`, pleasure |
  |---|---|---|---|
  | none | 1% | 93% | 1.0 |
  | linear, `n = 0.3` | 53% | 86% | 1.0 |
  | loss-averse (X4), `n = 0.2, λ = 1.5` | 66% | 98% | 2.6 |
  | loss-averse (X4), `n = 0.3, λ = 2` | 98% | 99% | 4.7 |

  - No draw lacked a credible plan, and whenever the commitment date was credible the
    preferred credible plan was it.
  - Example, loss-averse (`a = 0.3, α = 0.7, m = 0.2, μ = 0.6, n = 0.3, ν = 0.7, λ = 2`):
    `C_1 = {12, 13, 14}`, commitment 14; without news `C_1 = {19}` against commitment 15.
  - Linear news can tilt deviating selves toward the present, offsetting the trap's
    postponement. Loss-averse news (X4) makes plans sticky: once a self expects the pleasure
    at a date, waiting past it is felt as a loss, so more plans are credible and the
    commitment optimum often among them.
  - Neither is guaranteed. By continuity the trap survives weak news: at `n = 0.001` the
    example still gives `C_1 = {19}` against 15, with accurate expectations. News can
    offset postponement, and loss-averse news can make expectations do the work of a
    commitment device. [known in kind: Kőszegi & Rabin 2009, Prop. 5 and p. 925]
  - The exact stopping conditions above are for the direct model without news, and the
    `argmax/argmin w` commitment benchmark likewise.
  - Which credible plan does learning select? A fixed-past learner, started near uniform,
    lands on the earliest credible plan. Only 4 of 16 draws separate the earliest from the
    preferred plan; there it lands on the earliest in 3 (every seed) and varies in 1. A
    conjectured mechanism, untested: under loss aversion, uncertainty about one's own
    timing is itself felt as news, so resolving it early pays. [observed in
    `experiments/learned_expectations/`]
  - Anticipated news, nonzero only under loss-averse news, changes none of this.
    Deterministic plans carry none, so the credible plans and the commitment optimum are as
    without it; it acts only on mixed policies, the learning path. There rational forecasts
    brace for one's own randomness (core X4's built-in bracing). Where news outweighs anticipation this makes randomness cheaper, and
    the planner reaches the commitment date more often; the fixed-past learner selects the
    same dates, seed for seed, as with forecasts that leave anticipated news out. [synthesis;
    checked against the earlier code's `selection_report.txt` at git `fd60c6c`; the planner's
    73% against 60% is 16 draws, not significant]
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
- With linear felt news, a deviating momentary hedonist's row gains `g_0 k_n′(h)`. Its
  effect follows `k_n′`: more present-biased where `k_n′` decays, less where it rises (with
  the rising-kernel parameters of the setup, the next-to-current weight ratio goes from
  0.160 to 0.259). [Codex; checked for `k_n′`]

**D5. Beliefs are welfare.** [synthesis unless marked]
- Felt anticipation makes payoffs belief-dependent: psychological games (Geanakoplos,
  Pearce & Stacchetti) and personal equilibrium (Kőszegi 2010).
- **Which probability scores welfare.** Welfare is the objective expectation of the felt
  life-sum, as in Brunnermeier & Parker's well-being (2005, Def. 1). The agent's beliefs
  shape what is felt; they do not score it.
- **In expectation, the truth is free.** Needs a calibrated prior, the symmetric core's
  linear echoes and news, and actions held fixed: with loss-averse direct news alone (X4;
  `n = 0.2, ν = 0.5, λ = 2`, `Z = ±1` at realization) revelation a period early costs 0.05
  and at realization 0.10. [Codex; checked by hand] It also needs a lifespan the information
  does not move. Under death risk the recursive loop (remembered anticipation) runs only in
  surviving branches, and its gain `1/(1 − a·m·S)` is convex in the survival probability
  `S`, so mortality information is priced even linearly, with the sign of the anticipated
  future's felt value: two moments, the second alive with probability ½, `u = (0, ±1)`,
  `a = m = ½`: knowing at once changes expected welfare by `±1/7`. The direct model, and
  either kernel alone, stay neutral. [not found; checked] Anticipation linear in beliefs, Bayesian
  updating: forecasts are martingales, so by the tower property expected welfare does not
  depend on whether or when information arrives. [standard: Epstein 2008 p. 1121;
  Eliaz & Spiegler 2006 Prop. 1; Bénabou 2015 fn. 16; Kimball & Willis 2006. Kőszegi &
  Rabin 2009 Prop. 2 is the loss-averse cousin: at `γ = 1`, shifting signals while keeping
  their order and grouping is neutral, while adding interim partial information can
  hurt]
- **Pathwise, it is not.** Good news raises `e` at once and bad news lowers it; the swings
  cancel only on average.
- **What prices information is nonlinearity in beliefs**, not in outcomes, with actions and
  the lifespan held fixed (mortality, above, and endogenous action are the other routes).
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
  - **Exact accounting.** Give the echo strengths a sign (core X1–X2): savoring `a⁺` and
    dread `a⁻` forward, `m⁺` and `m⁻` back. With Bayesian forecasts and felt news switched
    off,
    `E[W] = W_sym − Σ_t w_t [(a⁻−a⁺) Σ_j α^j E[X_{t+j}⁻] + (m⁻−m⁺) Σ_j μ^j E[X_{t−j}⁻]]`,
    with `w` the life weights of the `(a⁺, m⁺)` kernel (1 in D) and `W_sym` its welfare.
    [proved; checked]
    - D: `X = u`. The negative parts do not depend on information, so timing is neutral.
    - R: `X = e`. Timing matters only if some felt state can land on either side of zero
      (its sign depends on the path): with every felt state of fixed sign, each kink is
      inactive, the model is linear where it lives, and the tower property applies. With
      experienced utility positive throughout, dread asymmetry costs nothing however
      information arrives. [proved; checked; Codex's three-period example agrees]
    - That is sufficient for neutrality, not a description of the cost. Information can
      change the expected negative parts without moving any state across zero between
      schedules: two periods, `Z = ±1` equiprobable, `e_0 = 1 + E_0[ψ(e_1)]`,
      `e_1 = Z + 0.1 e_0`, `ψ` with slopes 0.1 (gains) and 0.2 (losses). Early revelation
      gives `E[W] = 1.06009`, revelation at realization `1.06091`, with every state's sign the
      same under both: `e_1`'s negative branch is deeper when `e_0` already knows `Z`, through
      memory. [Codex; checked by hand]
    - Which way it cuts is not in the identity. In every example checked, earlier
      information spreads felt states and raises their expected negative part, so later
      revelation is better. [checked on examples]
    - Rumination prices information too: with bad felt states remembered more heavily
      (`m⁻ > m⁺`), the worry early news causes is remembered. Two periods, linear
      anticipation 0.2, `m⁺ = 0.1`, `m⁻ = 0.3`, terminal `u = ±1`: early revelation costs
      0.026 against revelation at realization. [checked; Codex]
    - Linear news adds no forcing (`E[N] = 0`, core N1). With loss-averse news kept (X4),
      its forcing `wᵀE[N]` enters too, and a symmetric baseline solved separately has
      different endogenous news; compare at fixed news forcing.
  - Other routes to avoidance: loss-averse news utility (core X4; Kőszegi & Rabin 2009
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
    (Bénabou 2015 p. 677; Bénabou & Tirole 2002 §IV). Their result is a formal cousin of
    Yudkowsky's "Doublethink", conditional on near-Bayesian sophistication and linear
    anticipation, not a theorem about all motivated reasoning. Delusion pays only for
    unaware agents, under nonlinear anticipation, or for instrumental reasons.
  - Not in Brunnermeier & Parker: a felt disappointment term. Felt news (core N3) supplies
    the price of optimism, the disappointment at realization; a price on information needs
    a kink (core X1, X2, X4). Disappointment is first-order, so the sign of the hedonically
    optimal bias depends on anticipation mass against remembered disappointment: optimism
    for long-awaited events, bracing otherwise, and with linear news there is no interior
    optimum. Under loss-averse news the felt forecast already contains the expected
    disappointment, so a calibrated Bayesian is already braced (core X4).
- **Rationalization as hedonic arbitrage.** [speculation]
  - Updating less on bad news keeps anticipation high now and moves the cost into later
    disappointment or decisions.
  - Bénabou's cancellation says it pays only for agents who don't see themselves doing
    it, or under nonlinearity.
  - Loss-averse felt news (core X4) gives the arbitrage an exact form. In the RL reading, the
    forecast `V_t`, set after period `t−1`'s outcome, enters that period's news through
    `δ_{t−1} = r_{t−1} + νV_t − V_{t−1}` and the next period's with the opposite sign. Its
    marginal felt value is `aν + nν φ'(δ_{t−1}) − n E[φ'(δ_t)]`, larger by `nν(λ − 1)` just
    after bad news: raising the outlook softens the loss just felt. So a forecaster free to
    choose (tethered to calibration) braces before outcomes and consoles itself after bad
    ones, under-updating on bad news. [synthesis; a learned critic shows the gap at
    `λ = 2` and none at `λ = 1`, `experiments/learned_expectations/`]
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
- Under rational expectations, anticipation of a plan's reward scales with the forecast
  probability of following through. A self known to defect whenever the moment's local
  value dips anticipates *every* plan at a discount; a reliable self anticipates each at
  full value. (Exact for a fixed reward component; the anticipated news in total felt
  utility also changes with the policy.)
- So follow-through that looks like sunk-cost reasoning can be justified at the policy
  level. The value is the anticipation that reliability earns across all plans, not the
  past anticipation of this one: Parfit's hitchhiker inside one life.
- **Worked example** (canonical model, Bayesian forecasts): pay a cost at `d` to get a
  reward `v = 3` at `s`; the cost is `c_L = 0.5`, or high (`c_H`) with probability 0.3,
  revealed at `d`. Policies: reliable (always pay) or flaky (skip when high). Echoes
  `a = 0.1, α = 0.8, m = 0.15, μ = 0.6`; `T = 16, s = 10`. [checked]
  - Main case (`d = 3, ν = 0.5, c_H = 2.5`). Without news the planner prefers reliability
    (`E[W]` 4.47 against 3.85) and it is the unique equilibrium. Linear news leaves `E[W]`
    as it is (N1) and narrows the high-cost self's margin for paying (2.46 without news,
    1.01 at `n = 0.3`); at `n = 0.5` the only equilibrium is flaky, against the planner:
    skipping a near cost is felt now as good news, and the lost reward is far off, felt
    through a decaying `k_n`. Loss-averse news (X4) flips it sooner: at `n = 0.3, λ = 2` the
    planner still prefers reliability (3.92 against 3.78) and the only equilibrium is flaky.
    [known in kind: Kőszegi & Rabin 2009, Prop. 5, present tilt when `γ < 1/λ`]
  - Other cases (`d = 6, ν = 0.7`). Without news, fixed-past selves pay at `c_H = 3.5`,
    where the planner would skip: their remaining-life weights favour later rewards (the
    savoring direction). Under loss-averse news (X4), at `n = 0.2, λ = 1.5, c_H = 3`, both
    policies are self-enforcing and expectations decide.
  - The echo channel `J` does not by itself favour reliability here: earlier selves
    anticipate the nearer item more, so for cost-then-reward plans their anticipation
    weighs the cost. [synthesis]
- So felt news can create unreliability against the planner's preference, and loss-averse
  news can make either policy self-enforcing. A third channel, causal: following
  through raises later selves' forecasts of their own reliability (self-reputation),
  which a fixed-past self can count. [untested]
- Precedent: Bénabou & Tirole 2004 (personal rules; lapses are diagnostic of willpower;
  self-confidence as an asset), whose payoff is instrumental. Self-image can also be
  hedonic: Bodner & Prelec's (2003) diagnostic utility is intrinsic, and Bénabou &
  Tirole (2002, §I) list a consumption value of self-confidence. Not found: anticipation
  scaled by one's own forecast probability of follow-through.
- D3 has the same structure: past anticipation, sunk for the fixed-past self.
- A past self having looked forward to the plan is not, by itself, a reason.

**D7. Affect policies and updateless affect.** [known in kind: Pagel 2018; Andries & Haddad
2020; the framing against Good's theorem and updatelessness is synthesis; speculation where
marked]
- **Two policies.** Actions are measurable with respect to the agent's information `F_t`.
  Felt forecasts and felt news are computed on an *affect filtration* `G_t ⊆ F_t`, coarser
  or delayed. Realized base utility is felt when it happens. Strict **updateless affect**:
  `G_t` is the prior until realization.
- **Free in the symmetric core.** With linear echoes and news, and outcomes and the
  lifespan held fixed, expected welfare does not depend on `G` (tower property). [standard]
- **Which `G` is best depends on the kink** (core X1–X4). [checked on examples]
  - R with dread or rumination asymmetry (D5): coarser `G` keeps felt states from spreading
    into negative parts, which is what D5's identity charges. Strict updateless affect is best in
    every example checked. A general comparison theorem is open: felt states under a
    coarser `G` are not simply conditional expectations of those under `F`.
  - Loss-averse felt news (core X4): a weighted scheduling problem. Subadditivity favours
    feeling news in batches; decaying `k_n` favours feeling far-off news early; the optimum
    trades them off, and neither rule dominates (core X4's counterexample). Strict
    updateless affect is optimal only if realization is the cheapest time.
- **The split in decision-theory terms.** Good's theorem and updatelessness concern the
  action policy, where information is ignorable. The affect policy is where information
  costs (KSS's cost-free half). A hedonic agent chooses both, and Good's theorem says
  nothing about the second.
- **Implementable pairs.** The comparisons above hold the outcome process fixed. With
  endogenous actions, affect and action policies must be chosen jointly, under two
  constraints.
  - Incentives: changing `G` changes deviation payoffs and so which plans are credible.
    [Codex]
  - Information: actions leak into affect (next bullet).
- **Actions leak into affect.** `G ⊊ F` means acting on information one does not attend to,
  but the feeler observes its own actions and their results, so felt states are computed on
  at least `G_t ∨ σ(a_{≤t}, u_{≤t})`. That join is the minimal observation closure, a lower
  bound on what is felt, not a characterization of implementable pairs. A feeler that knows
  its policy learns the partition the policy's output induces, not all of `F`
  (`a = 1[Z > 0]` hides `Z`'s size); one uncertain about its own policy learns less.
  Commitment alone does not stop the leak: a fixed policy reveals whatever its output
  depends on. Off-path actions have no Bayesian posterior, so evaluating a deliberate
  deviation needs a belief rule (trembles, an equilibrium refinement). [synthesis; Codex;
  known in kind: Andries & Haddad, below]
  - Protecting information until a batch date needs the whole observable history (actions,
    their consequences, and inaction under a known rule) to be conditionally independent of
    it, given the scheduled disclosures; sometimes only payoff-relevant forecasts need
    protecting. The routes combine rather than each sufficing: delegation hides the act,
    late consequences hide its results, pooling or garbling makes the act uninformative.
    [Codex]
  - Prior art. Pagel's news-utility investor prefers to ignore his portfolio, pays a manager
    to rebalance for him, and would like to commit to inattention, but must sometimes look
    in order to rebalance himself. Andries & Haddad (2020), under recursive disappointment
    aversion: state-dependent alerts after sharp drops raise welfare (Prop. 5), and
    delegation cannot always shield the agent, because observed consumption reveals wealth;
    it works best for decisions with long-term implications, where hidden trading meets
    consumption observed late (NBER WP, pp. 23–25).
  - What a leak costs depends on the kink; in the symmetric core, nothing in expectation,
    with outcomes and the lifespan held fixed. Loss-averse news at equal effective
    weights `c = w(r) k_n(s−r)`: splitting a revision into increments `x, y` adds
    `c(λ−1)[x⁻ + y⁻ − (x+y)⁻]`, positive exactly when they have opposite signs. Moving an
    intact revision earlier is neutral; a leak that pulls part of a batch forward destroys
    cancellation (`+1, −1` batched costs nothing, felt separately `λ − 1`); unequal timing
    weights change both (core X4). R with dread or rumination: coarser `G` was better in
    every example checked, so forced revelation is expected to cost; no theorem. [Codex]
  - Binary example. State `Z = ±1` seen by the doer, action `a = Z` with probability `q`,
    `u = sZ + r·1[a = Z] + εη` realized at `T`, with `η = ±1` revealed only at `T`, the
    action observed, unit news weights. With `ε = 0`,
    `E[W] = rq − (λ−1)[s(q − ½) + q(1−q) max(r, 2s)]`: convex in `q`, so a corner wins, and
    acting fully always beats ignoring, since a full leak is free. With `ε > 0` the leak is
    partial and can cost: `s = 1, r = 0.3, ε = 1, λ = 2` gives −0.70 acting and observing,
    −0.39 ignoring, −0.20 acting through an unobserved delegate. [Codex's closed form;
    checked]
  - A rule that ignores the news leaks nothing through the act, but its consequences can:
    D6's reliable self pools the act, yet feels which cost it paid. Bénabou & Tirole's
    personal rules run on the opposite channel, self-inference from lapses. [Codex]
- **Not belief choice.** Beliefs stay accurate, so this is not Brunnermeier & Parker, and
  Bénabou's self-doubt cancellation does not bite. Whether affect can come apart from
  belief within one mind is open; attention and delegation are the known routes. Not
  found as a formal object on LessWrong; HonoreDB (2011) pins *belief* at the prior, a
  different split. Informal precedents below.
- **Example: P(doom).** A high forecast lowers felt anticipation, but that level effect is
  neutral ex ante in the linear model. Under loss-averse news (X4), following every update
  piecemeal costs more than batching at equal weights; under dread of dread (X1), coarser
  feeling did better in every case checked. The hedonic prescription: settle a policy, act on
  it, and feel the forecast in batches. Leakage makes conditioning each action on the
  forecast a trade-off: its instrumental value against the news its observation,
  consequences and inaction carry. Size and frequency alone decide nothing (a tiny action
  `εZ` reveals `Z`). [speculation as psychology]
- **Informal precedents on LessWrong.** None batches or feels by a prior, but each splits
  affect from action.
  - Soares, "Detach the grim-o-meter" (2015): stop calibrating the grim-o-meter against
    the state of the world; keep it for local work.
  - Soares, "Simply locate yourself" (2015): treat bad news as information about where you
    ended up, not as the world going wrong. This has the updateless structure; with
    measure-weighted anticipation (`selves.md`, A1) it is feeling by the prior over branches.
  - Mayer, "Being at peace with doom" (2023); TurnTrout, "Emotionally confronting a
    probably-doomed world" (2022: feelings are not beliefs); Sabien, "A way to be okay"
    (2023).
  - The constraint: the affect policy must not corrupt the beliefs action uses (Ruby, "A
    quick guide to confronting doom").
- **In a learner.** An actor-critic whose critic is its felt forecast (core, the RL reading),
  in hidden repeated games. A critic free to ascend felt utility turns rosy or braced by the
  sign of `aν − nλ(1−ν)`. Affect does not stay apart from action when the critic shares its
  state with the policy, even though the policy never reads it: value and staying come to
  share a direction in the state, so a critic that expects much keeps the agent on a
  complacent policy (rosy: 0/8 seeds learn to shift after losses, against 7/8 honest and
  8/8 braced). It is the level, not the bias: an honest critic of rewards shifted up, with
  nothing else changed, does the same. Decoupling needs the affect head kept off the
  representation that acts; through the decision rule, as the policy's baseline, its level
  barely matters at large batches. Why, in a model: `learning.md`, D8. [checked in
  `experiments/learned_expectations/`]
- **Open.** Fixed-past selves hurry pains (D3), and a body of news is a pain. Does that make
  them feel news piecemeal, i.e. over-check? Subadditivity pulls the other way; untested.
