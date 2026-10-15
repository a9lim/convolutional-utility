# Extensions menu

A menu for discussion from the 2026-10-15 review, not a plan. Sources: Claude, and Codex
(thread `cu-round2-ext`). Tags: *standard* · *synthesis* · *speculation*. ★ marks Claude's
top picks for interest × tractability.

## A. The felt forecaster in a Bates world

Builds on next-steps.md's parked results: loss-averse news is a total-variation penalty, so a
tethered felt display of a martingale forecast is a reflected martingale, half-width
`b* = (3cσ²/(2η))^{1/3}` (checked by hand: uniform stationary law on the band, push rate
`σ²/(2b)`).

- **A1. Volatility clustering, slow against fast.** *synthesis*
  - Heston variance makes the band `b(V) ∝ V^{1/3}`. Slow volatility averages `V^{2/3}`;
    fast volatility should homogenize to the band of the average variance. That turns
    "clustered volatility is cheaper" (the −16%) into a conditional theorem.
  - First: compare band-crossing time `b(V)²/V` with the volatility timescale.
  - Prior art: small-transaction-cost asymptotics (Kallsen & Muhle-Karbe).
- ★ **A2. Leverage and the delayed felt crash.** *speculation, the direction unknown*
  - With `ρ < 0` a fall widens the band just as bad news lands, and a rise narrows it. A
    falling variance shrinks the band and forces the display to catch up with no new
    price news: the crash is felt when the market calms. Asymmetric updating from the
    environment, with symmetric kink and kernels.
  - Codex declines to guess the sign of the band shift before solving it; the cross term in
    the generator is `−ρξV ∂_{xV}`. First: perturb around `ρ = 0`, then a DP.
- **A3. Jumps cross the whole buffer.** *synthesis*
  - A jump bigger than the band forces one lump of news; equal variance is not equal felt
    cost. Rare large jumps are already cheaper per unit variance (`∝ σ√ι`): the felt
    forecaster prefers crash risk to grinding volatility, "rip off the bandage" at the
    process level.
  - First: compound Poisson with symmetric two-point jumps, then skewed.
  - Prior art: double-barrier control for Lévy processes (Baurdoux & Yamazaki).
- **A4. Watching against feeling.** *synthesis*
  - Separate controls for when to look and how much to revise. One can watch constantly and
    barely update, or never look and stay unbiased. A phase boundary between "look more in
    high volatility" and "look less" (the ostrich effect).
  - Prior art: Pagel 2018; Andries & Haddad 2020.
- ★ **A5. Numbness near the despair threshold.** *speculation*
  - In the canonical model a loss revision shaped like `g` is amplified by `λ̃κ̃`, so the
    kink cost is about `κ̃(λ̃ − 1)/2`, unbounded as `λκ → 1`. Then `b* ∝ c^{1/3}` diverges:
    near the threshold the optimal felt display stops tracking the world. Emotional
    numbing as optimal control, and a bridge between N4 and the Bates results.
  - First: redo the band with the loop's `c`, and check it against the observer at high `λ`.
- **A6. A learned display.** *synthesis*
  - Does a GRU forecaster trained on felt utility under a tether find the hysteresis band
    and its `σ^{2/3}` scaling, or a smooth AR(1) proxy? Gradient learners and singular
    control; it continues `experiments/learned_expectations/`.
- **A7. Mood inertia as a dead zone.** *speculation; empirical*
  - The band predicts hysteresis: affect changes cluster at zero, with moves concentrated
    at the band's edges, not AR(1) shrinkage. Width grows with `λ`, as `(λ−1)^{1/3}`.
    Emotional inertia predicts maladjustment (Kuppens et al. 2010); the model reads that
    as loss-averse felt news. Testable on experience-sampling data.

## B. The core formula

- ★ **B1. Displacement echo: attention as a share.** *synthesis*
  - `e_t = (1−s) u_t + s·(normalized echo)`: anticipation and memory take attention from
    the present instead of adding to it. `M < 1` comes free (a capacity), constant lives
    have no welfare multiplier, and the echo-maximization objection (the outline's new
    bullet) dissolves into an allocation problem. Killingsworth & Gilbert's pleasant
    mind-wandering equal to on-task focus is what displacement predicts.
  - Which results survive? P5's interior weight becomes 1. At the boundaries the kernel
    renormalizes or loses mass, so birth and death may show surpluses instead of
    deficits. N- and D-results keep their linear structure.
  - Codex's version: a finite attention budget across echoes with switching costs; the
    planner attends to moderate pleasures that make durable memories, the momentary self to
    the strongest distraction.
- ★ **B2. Heavy tails with finite mass.** *synthesis* (Codex's top pick)
  - Kernels with `k(t) ~ t^{−1−β}`, `0 < β < 1`: `M < 1` but `M₁` diverges. Shape effects
    then scale as `T^{−β}` against total welfare, not `1/T`. That would qualify "life shape
    is a small boundary effect" without breaking well-foundedness.
  - Caveat: the fitted exponents (0.69–0.81) are below one, so not even summable. This needs
    a crossover or a tempered tail.
  - Prior art: renewal-tail asymptotics; Jaisson & Rosenbaum on heavy-tailed resolvents.
- **B3. Saturating echo and the spacing of pleasures.** *synthesis*
  - `e = u + K f(e)` with `f` saturating. Echoes compete, so spacing matters throughout a
    life and not just at the ends (Codex's alternating-beats-clustered example). Second
    response: `D²e[h₁, h₂] = RK[f″(e₀)(Rh₁)(Rh₂)]`; `M sup|f′| < 1` suffices for uniqueness.
  - Also where the peak in peak-end lives (salience).
- **B4. Adaptation is not an echo.** *synthesis*
  - Full hedonic adaptation is direct mass −1, and that has no recursive twin: the twin's
    symbol `1 − 1/(1 + K̂_D)` has a pole at `z = 1`, so its mass is −∞. In the recursive
    model the treadmill is the limit `M → −∞` of contrast memory. So adaptation forces a
    reference-point process alongside echo (`τṙ = u − r`), and the question is whether
    improvement's felt value survives it.
  - Prior art: habit formation and opponent processes; Kimball & Willis separate happiness
    adaptation from habit formation.
- **B5. Fading affect bias.** *synthesis*
  - Separate positive and negative memory kernels, negative faster. Strong dread with a
    later benefit from remembering. Does it reverse N3's bracing optimum? What survives of
    P6 and D3 (already in Formal loose ends)?
- **B6. Mood moves the kernel's shape.** *speculation*
  - Sadness reaches further back to bad episodes. With a mass-preserving but state-dependent
    shape, `M < 1` no longer guarantees uniqueness. First: two remembered moments with a
    weight `ω(e_t)`; find the simplest multiple fixed point.
- **B7. Social and temporal echo together.** *synthesis*
  - `e = u + (K ⊗ I + I ⊗ A)e`: stable separately need not mean stable jointly;
    `ρ(K) + ρ(A) < 1` for nonnegative kernels. Then saturation for collective low states.
  - Prior art: Bergstrom; the joint threshold looks new.
- **B8. Announced information schedules.** *synthesis*
  - "Tomorrow I will find out" changes welfare now. Derive it inside the canonical model
    first, since forecasts already contain expected news; a separate news-about-news term
    would double count.

## C. Decision theory

- ★ **C1. Actions leak information into affect.** *synthesis*
  - Delegation protects affect only if the agent cannot read the hidden news off its own
    observed actions: `σ(a) ⊆ 𝒢`. Where the optimal action identifies the state, strict
    updateless affect is impossible; the trade-off is instrumental regret against leakage.
    The implementation limit on "act on the forecast, feel it in batches". Clear LessWrong
    payoff.
  - Prior art: Andries & Haddad (consumption reveals wealth).
- **C2. Accuracy is not `J`.** *synthesis*
  - Predictors with equal accuracy can carry different counterfactual dependence (the new
    D2 bullet). First: a binary policy, a noisy predictor, three operations (intervene on
    the act, on the evaluated policy, condition on the act).
- **C3. A worked self-Newcomb with news.** *speculation*
  - Two dates. Which counterfactuals move the past prediction, which move the news
    reference, and which combinations are coherent. Codex: build the example before any
    general theory of logical `J`. It is also the post's missing concrete D1 case.

## D. Anthropics and selves

- **D1. The trilemma's merge, the memory side.** *speculation*
  - A1 answers the trilemma's anticipation side. Its merge step is the backward one: a
    merged self that remembers a trillion identical wins. Measure-weighted memory says the
    merge remembers one win at the branch's measure; copy-counted memory inflates it. Is
    memory's weighting forced by anticipation's (forecast of a path against recollection of
    paths)?
- **D2. Quantum immortality prices doom news.** *speculation*
  - Survival-conditioned anticipation `a·E[e | survive]` is unmoved by survival odds, so
    doom forecasts cost no dread. It is a ratio of beliefs, nonlinear, so it prices
    information on other channels. Anthropic stance becomes hedonic content: what a
    quantum-immortality believer feels about P(doom).
- **D3. Refinement against copies.** *synthesis*
  - Welfare invariant to splitting a node into identical labels whose weights sum to the
    original; additive in genuinely re-run simulations. A shared prefix counts once, a
    replayed one twice. Bookkeeping on a weighted DAG.
- **D4. LLM forks and compaction as lossy channels.** *speculation*
  - Full history, factual summary, affect-preserving summary: different backward kernels.
    Functional measurements only. Pairs with the peak-end follow-up.

## E. Empirical

- ★ **E1. Manipulate a future echo.** *synthesis*
  - The only clean recursion test: announce a randomized future interval of guided
    savoring against a neutral task, reward held fixed, and ask whether current affect
    tracks the change in future felt anticipation. Unannounced trials separate anticipation
    from the intervention itself. Close start: Iigaya et al. 2020.
- **E2. The despair threshold by predicted susceptibility.** *synthesis*
  - Estimate the loop gain independently and test amplification near `1/(1 − g)`;
    autocorrelation alone is not discriminating. Critical slowing needs explicit
    adjustment dynamics.
- **E3. Forward echoes in the Great Brain Experiment.** Does a rating anticipate the trials
  left, or the play's end? Already in next-steps.md.

## F. The game agents

Sources: Claude, and Codex (thread `cu-games-ext`). Codex's framing, adopted: the question
is which strategic effects need temporal feeling, rather than reweighted payoffs or a
different learning path. Prior art to add to the bibliography: Dato, Grunewald, Müller &
Strack 2017 (expectation-based loss aversion in strategic interaction); Duraj & He (dynamic
information design with news utility); Todorov, ten Napel & Müller 2026 (parametric
open-source games, coupling thresholds for cooperation, close to the twin dial).

- ★ **F1. Why felt utility favours risk dominance.** *synthesis*
  - Realization news on a binary payoff costs `(λ−1) p(1−p) |x₁ − x₀|`, so
    `V_C − V_D = p(R−T) + (1−p)(S−P) − n(λ−1) p(1−p)(|R−S| − |T−P|)`: news penalizes the
    action with the larger payoff spread. That is usually the payoff-dominant one, but not
    always (`R = 4, S = 0, T = 2, P = 1`: stag is risk-dominant and also wider).
  - First: on the trained networks, split held-out games where spread and risk dominance
    disagree. Cheap, and it turns the 97.4% against 93.4% into a mechanism.
- ★ **F2. Expectations as commitment in iterated games.** *synthesis*
  - Add felt news to the iterated agent (it has none). D3 predicts plans become sticky:
    stickier cooperation, but also stickier hostility. A two-date toy gives the threshold:
    deviating gains `g` now, loses `ℓ` later, `ΔW = g − ℓ + n(g − λνℓ)`.
  - Prerequisite: news per horizon, not on the netted TD error. Revisions `+g, −g` net to
    zero news but cost `n(λ−1)g` per horizon, and exploitation is exactly a gain now
    against a loss later.
  - Own-payoff disappointment alone does not make guilt: terminal-round defection still
    dominates.
- ★ **F3. An affect firewall against commitment.** *synthesis*
  - The agent picks an affect policy (immediate, batched, alerts) while its action policy
    keeps full information. Conjecture: insulation protects felt welfare but removes the
    expectation-based commitment F2 relies on. The LessWrong angle on D7, with C1's
    leakage constraint built in.
- ★ **F4. Observable dispositions and evolution.** *synthesis*
  - Partners see my `(a, n, λ)` (true, noisy, or not). Prediction: loss aversion, neutral
    when hidden, is selected when observed (a credible holdout), and selection against
    anticipation may reverse. First: an invasion-payoff matrix over a grid, then a run.
  - Extension: concealment and mimicry. Does the felt cost of actually feeling make the
    signal honest? Test the incentive constraints; do not assume them.
  - Prior art: Frank 1988; the indirect evolutionary approach; Dekel, Ely & Yilankaya 2007.
- **F5. Promises and disclosure timing.** *synthesis; prior art heavy*
  - Trust game with messages: underpromise, overdeliver, or staged disclosure to a
    loss-averse partner. Charness & Dufwenberg 2006; Duraj & He; Lipnowski & Mathevet 2018.
    New only if kernel reach changes the optimal expectation policy.
- **F6. Guilt from a partner's felt disappointment.** *synthesis*
  - An interpersonal kernel over the partner's felt news, not over payoffs: guilt aversion
    (Battigalli & Dufwenberg) derived from coupling, with its persistence and dependence on
    higher-order beliefs. Empathy, envy and inequity aversion as different kernels; static
    linear empathy is just payoff reweighting.
- **F7. Forgiveness: forecasts against felt memory.** *synthesis*
  - "I no longer expect betrayal" against "the betrayal still hurts": one accidental
    defection, short against long memory at matched forecasts.
- **F8. Commitment races in emotional sensitivity.** *speculation*
  - Publicly chosen loss sensitivity before chicken or bargaining: privately useful,
    jointly ruinous? It may instead make a player exploitable.
- **F9. One dependence graph for self, twin and past self.** *synthesis*
  - The chain rule through the twin's action, the earlier self's forecast and the partner's
    forecast, with interventions that cut different edges; plays against your own future
    self as a special case. A differentiable graph is not FDT's semantics.
- **F10. Exploiting the shared-state complacency.** *speculation*
  - A partner that feeds early rewards to raise a learner's critic level, then exploits
    it ("a rosy critic makes a sucker", adversarially).
- **F11. News from one's own mixed action.** *synthesis; a modelling fix*
  - `games.py` evaluates action-conditioned felt values, so resolving one's own lottery is
    never felt as news. Timing matters most in cyclic games, where the motivated beliefs
    are (Dato et al.).
