# Convolutional Utility

Scaffold, not prose. Tags: *standard* (textbook or cited result) · *synthesis* (known
pieces, new assembly) · *speculation*. Math is in `formalism/core.md` and
`formalism/decision.md`; sources are in `bibliography.md`.

Reading: **hedonic**. Anticipation and memory are felt, and welfare is the life-sum of
experienced utility.

## Candidate spine

- **Hook.** Discounting looks forward. Run the same kernel backward for memory, let
  echoes echo, and treat a life as a signal convolved with a kernel.
- **The model.** Base `u` and a kernel `k` (anticipation for `τ > 0`, memory for
  `τ < 0`); direct `e = (I+K)u` or recursive `e = (I−K)^{-1}u`. *synthesis*
- **Lineage.** Credit the premise, claim the synthesis and the results. *standard*
  - Jevons and Bentham
  - Bergstrom's one-paragraph sketch
  - Caplin & Leahy's multiple counting
  - Ray, Vellodi & Wang's backward discounting
  - Hersch & Weltman's atomism
- **Well-foundedness.** *synthesis*
  - Echo share `M` (P1b): the echo must be less than the whole.
  - Bounded at every lifespan (`M < 1`) is a different condition from monotone on this
    life (`ρ(K_T) < 1`) (P1c).
  - Why hedonic. Echoes are real experiences, so `Σ_t e(t)` counts them honestly. This
    is Caplin & Leahy's Jevonian defence and Kahneman et al.'s instant-utility axiom.
- **What the life-sum says: moments as centrality.** *synthesis*
  - Moments matter in proportion to their echo.
  - The interior is flat: the planner has no pure time preference (Ramsey).
  - Deficits at birth and death.
  - Shape: the first-moment theorem (P6) — anticipation's lever arm against memory's. It
    is a boundary effect, not a slope effect.
  - Directionality: improvement wins iff anticipation reaches further, *or* memory works
    by contrast.
  - Each self is a lens (P7): judging a whole life from its end inherits recency.
  - The James Dean effect from contrast memory (P8). *speculation* as psychology.
- **What the momentary self does.** *synthesis*
  - Discounting is the forward resolvent.
  - Recursion makes exponential primitives present-biased: one-sided case *standard*;
    two-sided P4 *not found*.
  - Anticipated remembering weakens the bias.
- **Decision theory: your past self as predictor.** (`decision.md`)
  - A choice is Newcomb-like when already-felt anticipation depends on an accurate
    prediction of it (D1). *synthesis*
  - One dial, `J` = how much the felt past depends on the present choice (D2).
    *synthesis*
    - `J = 0` is fixed-past sequential choice (CDT).
    - `J = J_pf` is advance commitment, i.e. the planner.
    - FDT and EDT pick `J` by their own dependence theories. Neither equals the planner
      by default.
  - The savoring trap (D3). Selves sharing the life-sum objective, with the past held
    fixed, push pleasures toward the unremembered end and hurry pains. Mechanism
    *standard* (Kőszegi 2010; Caplin & Leahy 2001). Exact stopping conditions *not
    found*.
  - Its sign is opposite to present bias's preproperation. Savoring delay and
    procrastinated pleasures have rival explanations. *speculation*
  - The momentary hedonist's present bias depends on the boundary treatment (D4).
  - Beliefs are welfare (D5). In the linear model, information timing is neutral (tower
    property).
- **Anthropics.** (`decision.md` A1–A3) *synthesis / speculation*
  - Branching copies: copy-counting anticipation is well-founded only if it fades faster
    than copying.
  - Bounded utility per observer ≠ summable total welfare across observers
    (`b(1+m)α < 1`).
  - Two dials: how a mind represents its successors, and how welfare aggregates across
    them. These are utility weights, not SSA/SIA credences.
  - Sleeping Beauty: memory protocols move utility-adjusted betting weights.
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
