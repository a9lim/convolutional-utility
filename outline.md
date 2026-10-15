# Convolutional Utility

Scaffold, not prose. Tags: *standard* (textbook or cited result) · *synthesis* (known
pieces, new assembly) · *speculation*. Math is in `formalism/core.md` and
`formalism/decision.md`; sources are in `bibliography.md`.

Reading: **hedonic**. Anticipation and memory are felt, and welfare is the life-sum of
experienced utility.

Audience: LessWrong. The premise is old in economics; LessWrong has scattered informal
precedents (`bibliography.md`, the second LessWrong scan) but no unified treatment; the post's
value is the reframing, bringing anticipation, memory and belief-dependent welfare into the
familiar decision-theory vocabulary. Economists' results are support to cite, not a
deflation.

Form: one flagship post, about 8–10k words, each result in a few paragraphs with one
figure. Proofs and checks live in a technical companion (the `formalism/` docs, polished
into an appendix). The LLM peak-end study is a follow-up.

Spine: **experience echoes.** What you feel now contains what you expect and remember, and
what you feel is what counts. So one equation reprices the shape of a life (Act I), the
value of information (Act II) and the logic of choice (Act III); a coda takes it to selves.

## Sections

- **Hook.** Discounting looks forward. Run the same kernel backward for memory, let
  echoes echo, and treat a life as a signal convolved with a kernel.
- **Act 0: the model.**
  - **The equation.** Experienced utility is base utility plus anticipation and memory of
    experienced utility, plus felt news about it (core, the canonical model). *synthesis*
    - Present it in full, with the coefficient table: what `a, α, m, μ, n, ν, λ` each
      do, and the two conditions (`M < 1`; `λκ < 1`, closed form
      `κ = (n/H)(1−νμ)/(1−νq)`). Forecasts are rational, expected news included.
    - The direct form is its reduced form for foreseen lives, an equivalent model under
      reparametrization (P2); recursion stretches anticipation's reach and makes news about
      further-off events felt more. A surprise is an information boundary: it misses the
      anticipation paths, so recursion has content even on an infinite line.
    - Illustrative parameters per horizon (a waking day, a life): echo about 30% of
      steady-state experience, recursion stretching reach by 21–28%, and a strongly
      present-weighted felt row (`β ≈ 0.05`–`0.08`). Scenarios, not estimates. The robust part is
      the inversion: explaining measured patience by the momentary felt row needs an echo
      share near one, so patience, if hedonic, belongs to the life-sum. *synthesis*
    - An agent that cares only about the next and previous moments already acts on its whole
      life, exponentially (P2).
    - Well-foundedness favours light-tailed primitives, and recursion still delivers
      quasi-hyperbolic present bias (P1d, P3, P4).
    - Present bias is the signature of caring directly about more than the next moment
      (P2, P3).
    - The kernel family is free (exponential, hyperbolic): the model is a frame for
      interpreting utility, not a fit (P10).
  - **Well-foundedness.** *synthesis*
    - Echo share `M` (P1b): the echo must be less than the whole.
    - Bounded at every lifespan (`M < 1`) differs from monotone on this life
      (`ρ(K_T) < 1`) (P1c). Footnote.
    - Why hedonic. Echoes are real experiences, so `Σ_t e(t)` counts them honestly. This
      is Caplin & Leahy's Jevonian defence and Kahneman et al.'s instant-utility axiom.
    - It answers double counting, not echo maximization: the model endorses amplifying
      echoes of good felt states and damping echoes of bad ones (`∂W/∂K_ij = w_i e_j`).
      Accept it: savoring is welfare. The linear model has no optimum over kernels
      (welfare grows without bound as `M → 1`), so attention and saturation are the
      missing costs, and more pleasure is not larger numbers (P10). [Codex]
  - **Lineage.** Credit the premise, claim the synthesis and the results. *standard*
    - Jevons and Bentham
    - Bergstrom's one-paragraph sketch
    - Caplin & Leahy's multiple counting
    - Ray, Vellodi & Wang's backward discounting
    - Hersch & Weltman's atomism
- **Act I: a life.**
  - **What the life-sum says: moments as centrality.** *synthesis*
    - Moments matter in proportion to their echo.
    - The interior is flat: given time-neutral aggregation of experience (assumed in `W`),
      echoes add no pure time preference over base utility (Ramsey). Derived for `u`, not
      for `e`.
    - Deficits at birth and death. A kernel with no forward or backward bias favours a good
      midlife.
    - No moment *feels* these weights: each felt state weighs the life through its own
      anticipation and memory. A self can still choose by the life-sum (D3's selves do).
    - Shape: the ramp theorem (P6) — for linear ramps, anticipation's lever arm against
      memory's (the first moment `M₁`). Ramps only: an end pulse against a start pulse
      compares echo masses, so `M₁ < 0` can still favour the improving pulse.
      - In a linear echo model shape is a boundary effect, not a slope effect.
      - Its size is about reach over lifespan (`4M₁/T`): sizeable for whole lives only if
        anticipation and memory reach across decades; strongest for short sequences.
    - Directionality, for ramps: the rising ramp wins iff `M₁ > 0` (at equal amplitudes,
      iff anticipation reaches further), *or* memory works by contrast.
    - Each self is a lens (P7): judging a life from its end inherits recency. Two lines.
    - The James Dean effect from contrast memory (P8). *speculation*; evidence is
      evaluative. Cut candidate.
  - **What the momentary self feels.** *synthesis* Its choice weights only if it maximizes
    current experience; a life-sum chooser is the other case.
    - Discounting is the forward resolvent.
    - Recursion makes exponential primitives present-biased: one-sided case *standard*;
      two-sided P4 *not found*.
    - Anticipated remembering weakens the bias. The size depends on the boundary (D4,
      footnote).
  - **The shape-of-a-life debate.**
    - Take Brown's explaining-away horn openly.
    - Velleman's narrative view is the foil.
    - Hersch & Weltman's "begs the question" is the objection to answer.
- **Act II: beliefs.**
  - **Beliefs are welfare.** (D5) *synthesis / speculation*
    - Felt anticipation is a forecast, so learning changes how your life feels now.
      Welfare is scored by the objective expectation of the felt life.
    - In expectation the truth is free (tower property; a textbook benchmark), given
      linear echoes and news, a calibrated prior, and actions held fixed. Pathwise it is
      not: bad news hurts now.
    - What prices information is nonlinearity in beliefs. Dread outweighing savoring, as a
      kernel on outcomes, does it only in the recursive model, where you anticipate your
      own future dread. (Concavity in the posterior itself prices information in any
      model; that is the known case.)
      - Exact identity: the cost is the dread excess times the life-weighted expected
        negative part of anticipated felt states (felt news aside). It bites only when
        some felt state can land on either side of zero; heavier memory of bad states
        (rumination) prices information the same way. *proved; direction checked on
        examples*
      - Credit the structure to Kreps–Porteus (a concave aggregator prefers late
        resolution); the felt-flow form and the direct/recursive contrast are ours.
    - The delusional optimist feels better than the realist on the same base utility, if
      unaware. Prior art: Brunnermeier & Parker's optimal expectations.
    - A sophisticated near-Bayesian gains nothing from self-deception: doubt spoils the
      good news (Bénabou). "Doublethink" as a theorem.
    - Felt news (core N1–N3, Kőszegi–Rabin in kernel form): elation and disappointment
      when forecasts change, realization included. One term prices optimism and
      information.
      - News is a schedulable pain: its cost is its size times the life weight `w(r)`.
        Clumping helps at equal weights, early helps when news about the far future is felt
        less; the schedule trades them off. Credit Andries & Haddad (recursive
        disappointment aversion prefers single-date revelation) and Kőszegi–Rabin.
      - Optimism pays iff anticipation mass beats remembered, loss-weighted
        disappointment: optimism for long-awaited events, bracing for short-notice ones.
        Credit Gollier & Muermann (the model) and van Dijk et al. (the timing claim);
        bracing is documented, its hedonic payoff is not (Golub, Gilbert & Wilson).
      - In the canonical model a calibrated Bayesian is already braced: the forecast of how
        the event will feel contains the expected disappointment, so realized news is more
        often relief. The news loop amplifies loss aversion; near the threshold the felt
        reference sinks while the optimal belief bias stays bounded. *not found; checked*
        - Figure: the optimal felt belief path under a cost of self-deception. Calibrated
          far from the event, braced as it nears, frozen over the last few periods because
          each further revision is itself felt as news. At the life calibration optimism
          never pays. A network trained on felt welfare captures a median 71% of the
          reference optimizer's gain on ten held-out events (one run;
          `experiments/learned_expectations/`). *checked*
      - News over experienced utility (N4): good news about far events is felt now,
        because tomorrow you'll be looking forward; cancelling a plan costs the
        anticipation too. Needs `λκ < 1`. Memory feeds the loop and anticipation does not.
        Just past it, bad news has no felt state (the loop runs away) and good news has a
        tipping point; bounded gain-loss can give a stable low state over a range of shocks,
        bistability. *proved; reading speculative.* Credit Kimball & Willis (elation over
        lifetime-utility news, solved simultaneously, a sufficient version of the threshold)
        and the bistability models of depression and panic.
      - The 2×2, echoes × news: the echo axis carries remembered excitement, present bias and
        dread-of-dread; the news axis carries the jolt, the cost of cancellation and the
        despair threshold. Linear, all four are one model; the canonical model is the
        recursive/recursive corner.
      - Recursion has content at the boundaries of a life and of information, and under
        nonlinearity. *synthesis*
    - Recollection news, the mirror of news: felt changes in how the past is remembered.
      Forecasts meet their realization, recollections only meet reminders, so rosy bias is
      cheaper backward. Rationalization may live mostly on the memory side.
      *speculation*
    - Rationalization as hedonic arbitrage: updating less on bad news keeps anticipation
      high now. *speculation*; asymmetric updating is empirically contested.
    - Instrumental value of information (Good's theorem, FDT) versus intrinsic hedonic
      value: information can be ignorable without being cost-free (Kadane, Schervish &
      Seidenfeld). LessWrong's updatelessness discussion covers only the ignorable half.
    - Affect policies (D7): act on everything you know, feel by a coarser or batched
      information flow.
      - A hedonic agent picks an action policy and an affect policy. Good's theorem and
        updatelessness govern the first only.
      - Strict updateless affect (feel by the prior) is best against dread-of-dread in every
        case checked (no theorem yet); against loss-averse news the optimum is a weighted
        schedule, batching where weights are equal.
      - Updateless action is what makes it feasible: once a policy acts for you, you can
        stop watching.
      - P(doom): act on the forecast, feel it in batches. *speculation as psychology*
      - Credit Pagel (the formal case: ignore the portfolio, delegate, commit to
        inattention), Andries & Haddad (alerts and delegation) and Soares ("Detach the
        grim-o-meter"; "Simply locate yourself", the updateless structure, which ties back
        to measure-weighting in the coda).
    - LessWrong precedents to credit: Raemon on the Litany of Gendlin; jimrandomh's
      utility-of-belief example; Yudkowsky on pleasant surprises; Bostrom's psychological
      reaction hazards.
    - Objection to answer: "Not for the Sake of Happiness (Alone)" (value is not only
      hedonic). "Doublethink" is an ally: Bénabou's cancellation formalizes it.
- **Act III: choices.**
  - **Decision theory: your past self as predictor.** (`decision.md`)
    - A choice is Newcomb-like when already-felt anticipation depends on an accurate
      prediction of it (D1). *synthesis*
    - One dial, `J` = how much of the felt past a decision rule counts as depending on the
      present choice (D2). Nothing is moved: for FDT the past forecast is an output of the
      function now being chosen. *synthesis*
      - `J = 0` is fixed-past sequential choice (CDT).
      - `J = J_pf` is advance commitment, i.e. the planner.
      - FDT reaches the planner when past forecasts were accurate evaluations of the
        decision function on the realized input (the transparent-Newcomb condition); EDT
        need not. Otherwise each picks `J` by its own dependence theory.
    - With felt news, deviating from the plan your past selves predicted is itself felt
      as news, so plans become reference points. Choice needs a credible-plan concept;
      adopt Kőszegi–Rabin's preferred credible plan, credited, for a means-based model
      with recursive news. *known in kind*
    - The savoring trap (D3). Without news, selves sharing the life-sum objective with the
      past held fixed push pleasures toward the unremembered end and hurry pains.
      Mechanism *standard* (Kőszegi 2010; Caplin & Leahy 2001); exact stopping conditions
      *not found*; the exceptions are sophisticated preemption.
      - With felt news it is fragile: the commitment plan is credible in 1% of draws
        without news, 66% at felt calibration, 98% with strong loss aversion.
        Expectations can do a commitment device's work, but weak news keeps the trap.
        *checked*
    - Its sign is opposite to present bias's preproperation. Savoring delay and
      procrastinated pleasures have rival explanations. *speculation*
    - Reliability (D6). Anticipation scales with forecast follow-through, so flakiness
      discounts every plan. But in the model the echoes alone make selves over-reliable
      about delayed rewards; felt news is what can make them flaky against their own
      interest. *checked on examples*
- **Coda: selves.**
  - **Anthropics.** (`decision.md` A1–A2) *synthesis*
    - Anticipation as a forecast of one continuing path is measure-weighted. That is an
      assumption: a forecast of total successor experience is also an expectation. Doom
      branches count as zero (hedonic neutral), so a likely early end discounts the
      future. This is the unnormalized choice; anticipation renormalized on survival
      (quantum immortality) would not discount.
    - It takes the conserved-measure horn of Yudkowsky's Anthropic Trilemma: copying
      yourself on a lottery win changes how many experience winning, not what you should
      anticipate.
    - Copy-counting would let a branching future outweigh a single past without bound.
    - Under measure-weighted anticipation *and* aggregation, branching is
      welfare-invisible: it adds up to normality. The second weighting is an axiom (total
      utilitarianism with measure as the population weight; right for Everett branches);
      real copies are extra welfare subjects, and there `bμ < 1` (`bq < 1` in R) is what
      keeps the copy-counted aggregate finite. The trilemma's trillion copies land here.
    - Aggregation weights are normative; they are not SSA/SIA credences.
    - A context window as a life: hard boundaries both ends, retrieval-style memory that need
      not fade (U-shaped use of context; echo compounds unless per-step echo is weak), and
      instances as A1's tree. *speculation*
  - **Identity.** The model needs none: kernel weight links moments, whatever agent they
    belong to. Parfit's connectedness is the direct kernel, continuity the resolvent, as an
    analogy: Parfit's continuity is all-or-nothing over thresholded links, and the resolvent
    grades it. Parfit proposed discounting by connectedness (Bartels & Rips find rated
    connectedness predicts patience). Compaction and sleep are soft boundaries crossed by
    memory and anticipation. *synthesis*
  - **Utilitarian corollaries.** *synthesis / speculation*
    - Forgotten pain counts less, but not zero (Parfit's amnesia case; Lee 2022; Shardlow
      2025).
    - Interpersonal kernels are Bergstrom systems, with the double-counting debate
      attached. Total-empathy mass must be < 1.
- **Limits.**
  - Real kernels are sign-asymmetric and nonlinear (dread > savouring).
  - Power-law forgetting threatens `M` and `M₁`.
  - The evidence for a past–future asymmetry is thin.
  - Identification (P10).
- **Technical companion.** The canonical model and its well-foundedness proofs; P4's
  closed form and P5–P6's life weights and ramp; N3 in the canonical model; the
  threshold's closed form and regimes; D5's identity; D3's stopping conditions; the checks
  and the playground.
