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
- **The model.** Base `u` and a kernel `k` (anticipation for `τ > 0`, memory for
  `τ < 0`); direct `e = (I+K)u` or recursive `e = (I−K)^{-1}u`. *synthesis*
  - Direct and recursive are two readings of one agent (P2). An agent that cares only
    about the next and previous moments already acts on its whole life, exponentially.
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
    - Its size is about reach over lifespan (`4μ₁/T`): sizeable for whole lives only if
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
  - Loss-averse news utility (Kőszegi–Rabin) prices optimism (disappointment) and
    information in one extension.
  - Rationalization as hedonic arbitrage: updating less on bad news keeps anticipation
    high now. *speculation*; asymmetric updating is empirically contested.
  - Instrumental value of information (Good's theorem, FDT) versus intrinsic hedonic
    value: information can be ignorable without being cost-free (Kadane, Schervish &
    Seidenfeld). LessWrong's updatelessness discussion covers only the ignorable half.
  - Updateless affect: feel by the prior, act on the posterior. A formal reading of
    equanimity. *speculation*
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
  - Power-law forgetting threatens `M` and `μ₁`.
  - The evidence for a past–future asymmetry is thin.
  - Identification (P10).
