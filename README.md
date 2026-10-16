# Convolutional Utility

Working abstract:

- Experienced utility as base utility convolved with a two-sided kernel: anticipation
  forward, memory backward, recursive (echoes of echoes), with felt news when forecasts
  change. The one-layer direct model is its reduced form for foreseen lives; surprises are
  information boundaries where the two part.
- With nonnegative kernels, recursive echo is bounded at every lifespan iff the echo share
  `M` is below one. A finite life can stay monotone above that, but its echo grows without
  bound with lifespan. Felt news about experienced utility adds a local threshold, `λκ < 1`,
  for a unique, stable felt state against given forecasts; without memory the loop gain is
  just `n`, and memory adds the feedback, scaled by anticipation through the resolvent. Past
  it, with linear gain-loss, bad news runs away (a bounded gain-loss function always has a
  solution, possibly a low stable one). With expected news inside Bayesian forecasts, only a
  sufficient joint condition is known.
- On illustrative short-reach parameters for a waking day and a life, echo is about 30% of
  steady-state experience, and the momentary self's felt row is strongly present-weighted
  (`β ≈ 0.05`–`0.08`). Robustly: unless felt anticipation outweighs the present several times
  over, explaining measured patience by the felt row would need an echo share near one.
  Patience, if hedonic, belongs to the life-sum, not to felt echo.
- In the linear model, summed over a foreseen life, each moment is weighted by its
  centrality in the anticipation/memory graph. Given time-neutral aggregation of
  experience, the interior is flat (echoes add no pure time preference over base utility),
  with deficits at birth and death.
- For linear ramps on lives long against the kernel's reach, preference for the rising over
  the falling ramp at equal base total is set by the kernel's first moment (short lives have
  counterexamples). It is a ramp result: an end-loaded pulse against a front-loaded one
  compares echo masses instead, and can disagree. In a linear model shape preference is a
  boundary effect, sized by the kernel's reach over the lifespan.
- In the momentary felt state, recursion turns exponential primitives into strict present
  bias (one-sided: known, Sáez-Martí & Weibull; two-sided closed form: not found); memory
  weakens it. It is choice behaviour only for an agent that maximizes current experience.
- Beliefs are welfare: felt anticipation is a forecast, so learning is not hedonically
  neutral. With linear echoes and news, a calibrated prior and a lifespan the information
  does not move, the truth is free in expectation but not pathwise; loss-averse news prices
  it. Dread outweighing savoring, as
  a kernel on outcomes, prices information only in the recursive model, where you anticipate
  your own future dread, and only when some felt state can land on either side of zero; the
  exact cost is the change in life-weighted expected negative parts. Under recursive news a
  calibrated Bayesian is already braced. Unaware optimism buys experienced utility at the
  cost of decisions.
- A hedonic agent chooses an action policy and an affect policy, the information it feels
  by. Good's theorem and updatelessness govern only the first. Under loss-averse news,
  feeling in batches pays, but a self that knows its own policy reads hidden news off its
  own actions and their results, so batched feeling needs an observable history that stays
  uninformative until the batch (delegation that hides the act and its results, or
  pooling).
- Felt anticipation that tracks a prediction of your later choice makes that choice
  Newcomb-like. Decision rules differ in how much of the already-felt past they count as
  depending on the present choice.
- With the past held fixed, selves sharing the life-sum objective fall into a savoring
  trap: pleasures drift toward the unremembered end of life and pains are hurried. The
  mechanism is known (Kőszegi 2010); the exact stopping conditions were not found. Felt news
  makes it fragile: loss-averse news makes the commitment plan credible in most draws.
- In momentary-happiness data (the Great Brain Experiment, 47,067 people; Forbes & Bennett's
  two experiments), echoes of task outcomes are front-loaded with a slow tail, closer to a
  power law than to the standard single exponential, in all three datasets; about 80% of
  the felt response over a play is echo. The recursive kernel fits this but is not singled
  out by it (the direct model's is the same family), and the heavy tail sits at the edge of
  `M < 1`. Chosen risk lowers happiness; whether as loss-averse news or a felt cost of risk
  is not identified in 50/50 gambles, and where it can be separated, risk takes most of it.
  (`experiments/happiness/`, with its `audit/`)
- Small learned agents (toys). A stop-gradient on the self's forecast of its own policy
  reproduces the fixed-past (causal) and commitment (planner) dates; the same switch on a
  twin's policy reproduces defection against cooperation, felt utility or not. A critic
  trained to ascend felt utility braces or turns rosy by the sign of anticipation against
  chronic disappointment, and at `λ = 2` consoles itself after bad news. In one small
  actor-critic setting, a critic that shares its state with the policy carries its level
  into action: targets above realized payoffs, biased or not, keep the learner complacent.
  Selection on payoff over generations robustly lowers anticipation, leaving critics
  roughly honest; selection for felt news shows within generations but not above drift.
  (`experiments/learned_expectations/`)
- Anthropics: copy-counting anticipation would let a branching future outweigh the past
  without bound; anticipation, read as a forecast of one continuing path, is
  measure-weighted (assumed, not derived: the conserved-measure horn of Yudkowsky's
  Anthropic Trilemma). Branching is welfare-invisible only if welfare is also aggregated by
  measure (Everettian branches); real copies are extra welfare subjects, a population-ethics
  question the kernel does not settle.
- Prior art: the premise is old in economics (Jevons; Bergstrom 1987/1999; Caplin & Leahy
  2004; Ray, Vellodi & Wang 2024; Hersch & Weltman 2022). LessWrong has scattered informal
  precedents (hope as a good, two selves, successive selves as a prisoner's dilemma) but no
  unified welfare treatment, and nothing on news utility. The post's value is the
  reframing, plus the specific results in `formalism/`.

Target: a LessWrong post. The authoritative writeup is `outline.md`; the repository map is
in `AGENTS.md`.
