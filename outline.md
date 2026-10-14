# Convolutional Utility

Scaffold, not prose. Tags: *standard* (textbook or cited result) · *synthesis* (known
pieces, new assembly) · *speculation*. Math is in `formalism/core.md` and
`formalism/decision.md`; sources are in `bibliography.md`.

Reading: **hedonic**. Anticipation and memory are felt, and welfare is the life-sum of
experienced utility.

Audience: LessWrong. The premise is old in economics and absent from LessWrong; the post's
value is the reframing, bringing anticipation, memory and belief-dependent welfare into the
familiar decision-theory vocabulary. Economists' results are support to cite, not a
deflation.

Spine, leading candidate: **beliefs are welfare** (D5), with your past self as predictor
(D1, D3, D6) as the second act and the life-sum results (P5, P6) as setup. Alternatives:
centrality ("moments matter by their echo"), discounting ("discounting is an echo").

## Sections

- **Hook.** Discounting looks forward. Run the same kernel backward for memory, let
  echoes echo, and treat a life as a signal convolved with a kernel.
- **The model.** One equation: experienced utility is base utility plus anticipation and
  memory of experienced utility, plus felt news about it (core, the canonical model).
  *synthesis*
  - Present it in full, with the coefficient table: what `a, α, m, μ, n, ν, λ` each
    do, and the two conditions (`M < 1`, `λ(k_n·g) < 1`).
  - The direct form is its reduced form, mentioned as an equivalent model under
    reparametrization (P2, N4); recursion stretches anticipation's reach and makes news
    about further-off events felt more.
  - An agent that cares only about the next and previous moments already acts on its whole
    life, exponentially (P2).
  - Well-foundedness favours light-tailed primitives, and recursion still delivers
    quasi-hyperbolic present bias (P1d, P3, P4).
  - Present bias is the signature of caring directly about more than the next moment
    (P2, P3).
  - The kernel family is free (exponential, hyperbolic): the model is a frame for
    interpreting utility, not a fit (P10).
- **Lineage.** Credit the premise, claim the synthesis and the results. *standard*
  - Jevons and Bentham
  - Bergstrom's one-paragraph sketch
  - Caplin & Leahy's multiple counting
  - Ray, Vellodi & Wang's backward discounting
  - Hersch & Weltman's atomism
- **Well-foundedness.** *synthesis*
  - Echo share `M` (P1b): the echo must be less than the whole.
  - Bounded at every lifespan (`M < 1`) differs from monotone on this life
    (`ρ(K_T) < 1`) (P1c). Footnote.
  - Why hedonic. Echoes are real experiences, so `Σ_t e(t)` counts them honestly. This
    is Caplin & Leahy's Jevonian defence and Kahneman et al.'s instant-utility axiom.
- **What the life-sum says: moments as centrality.** *synthesis*
  - Moments matter in proportion to their echo.
  - The interior is flat: the planner has no pure time preference (Ramsey).
  - Deficits at birth and death. A kernel with no forward or backward bias favours a good
    midlife.
  - No moment of a life sees these weights. Each moment rates the life through its own
    anticipation and memory, never from the god's-eye view.
  - Shape: the first-moment theorem (P6) — anticipation's lever arm against memory's.
    - In a linear echo model shape is a boundary effect, not a slope effect.
    - Its size is about reach over lifespan (`4M₁/T`): sizeable for whole lives only if
      anticipation and memory reach across decades; strongest for short sequences.
  - Directionality: improvement wins iff anticipation reaches further, *or* memory works
    by contrast.
  - Each self is a lens (P7): judging a life from its end inherits recency. Two lines.
  - The James Dean effect from contrast memory (P8). *speculation*; evidence is
    evaluative. Cut candidate.
- **What the momentary self does.** *synthesis*
  - Discounting is the forward resolvent.
  - Recursion makes exponential primitives present-biased: one-sided case *standard*;
    two-sided P4 *not found*.
  - Anticipated remembering weakens the bias. The size depends on the boundary (D4,
    footnote).
- **Beliefs are welfare.** (D5) *synthesis / speculation*
  - Felt anticipation is a forecast, so learning changes how your life feels now.
    Welfare is scored by the objective expectation of the felt life.
  - In expectation the truth is free (tower property; a textbook benchmark). Pathwise
    it is not: bad news hurts now.
  - What prices information is nonlinearity in beliefs. Dread outweighing savoring does
    it only in the recursive model, where you anticipate your own future dread.
    *not found; checked*
  - The delusional optimist feels better than the realist on the same base utility, if
    unaware. Prior art: Brunnermeier & Parker's optimal expectations.
  - A sophisticated near-Bayesian gains nothing from self-deception: doubt spoils the
    good news (Bénabou). "Doublethink" as a theorem.
  - Felt news (core N1–N3, Kőszegi–Rabin in kernel form): elation and disappointment
    when forecasts change, realization included. One term prices optimism and
    information.
    - News is a schedulable pain: its cost is its size times the life weight `w(r)`.
      Feel it clumped, early if news about the far future is felt less.
    - Optimism pays iff anticipation mass beats remembered, loss-weighted
      disappointment: optimism for long-awaited events, bracing for short-notice ones.
      Credit Gollier & Muermann (the model) and van Dijk et al. (the timing claim);
      bracing is documented, its hedonic payoff is not (Golub, Gilbert & Wilson).
    - News over experienced utility (N4): good news about far events is felt now,
      because tomorrow you'll be looking forward; cancelling a plan costs the
      anticipation too. Needs `λ(k_n·g) < 1`, and beyond it bad news has no felt state:
      a despair spiral. *checked; reading speculative.* Credit Kimball & Willis (elation
      over lifetime-utility news, solved simultaneously, the same threshold) and the
      bistability models of depression and panic.
    - The 2×2, echoes × news: the echo axis carries remembered excitement, present bias and
      dread-of-dread; the news axis carries the jolt, the cost of cancellation and the
      despair threshold. Linear, all four are one model. Regime choice is open (a9).
    - Recursion has content exactly where the model is nonlinear. *synthesis*
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
    - Strict updateless affect (feel by the prior) is optimal against dread-of-dread;
      against loss-averse news the optimum is batching.
    - Updateless action is what makes it feasible: once a policy acts for you, you can
      stop watching.
    - P(doom): act on the forecast, feel it in batches. *speculation as psychology*
    - Credit Pagel (the formal case: ignore the portfolio, delegate, commit to
      inattention) and Soares ("Detach the grim-o-meter"; "Simply locate yourself", the
      updateless structure, which ties back to measure-weighting in the anthropics coda).
  - LessWrong precedents to credit: Raemon on the Litany of Gendlin; jimrandomh's
    utility-of-belief example; Yudkowsky on pleasant surprises; Bostrom's psychological
    reaction hazards.
  - Objection to answer: "Not for the Sake of Happiness (Alone)" (value is not only
    hedonic). "Doublethink" is an ally: Bénabou's cancellation formalizes it.
- **Decision theory: your past self as predictor.** (`decision.md`)
  - A choice is Newcomb-like when already-felt anticipation depends on an accurate
    prediction of it (D1). *synthesis*
  - One dial, `J` = how much the felt past depends on the present choice (D2).
    *synthesis*
    - `J = 0` is fixed-past sequential choice (CDT).
    - `J = J_pf` is advance commitment, i.e. the planner.
    - FDT and EDT pick `J` by their own dependence theories. Neither equals the planner
      by default.
    - Economists' commitment and personal-equilibrium tools line up with this
      (Kőszegi–Rabin).
  - The savoring trap (D3). Selves sharing the life-sum objective, with the past held
    fixed, push pleasures toward the unremembered end and hurry pains. Mechanism
    *standard* (Kőszegi 2010; Caplin & Leahy 2001). Exact stopping conditions *not
    found*. The exceptions are sophisticated preemption.
  - Its sign is opposite to present bias's preproperation. Savoring delay and
    procrastinated pleasures have rival explanations. *speculation*
  - Reliability is worth its anticipation (D6). A flaky self anticipates every plan at a
    discount, so follow-through pays across all plans. Parfit's hitchhiker inside one
    life.
- **Anthropics.** (`decision.md` A1–A2) *synthesis* Coda.
  - Anticipation is a forecast, so it is measure-weighted. Doom branches count as zero,
    so a likely early end discounts the future correctly.
  - Copy-counting would let a branching future outweigh a single past without bound.
  - Under measure-weighting, branching is welfare-invisible: it adds up to normality.
  - Utility weights, not SSA/SIA credences.
  - A context window as a life: hard boundaries both ends, retrieval-style memory that need
    not fade (well-founded only for short contexts or weak echo), and instances as A1's
    tree. *speculation*
- **Utilitarian corollaries.** *synthesis / speculation*
  - Forgotten pain counts less, but not zero (Parfit's amnesia case; Lee 2022; Shardlow
    2025).
  - Interpersonal kernels are Bergstrom systems, with the double-counting debate
    attached. Total-empathy mass must be < 1.
- **The shape-of-a-life debate.**
  - Take Brown's explaining-away horn openly.
  - Velleman's narrative view is the foil.
  - Hersch & Weltman's "begs the question" is the objection to answer.
- **Limits.**
  - Real kernels are sign-asymmetric and nonlinear (dread > savouring).
  - Power-law forgetting threatens `M` and `M₁`.
  - The evidence for a past–future asymmetry is thin.
  - Identification (P10).
