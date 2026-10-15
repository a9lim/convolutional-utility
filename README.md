# Convolutional Utility

Working abstract:

- Experienced utility as base utility convolved with a two-sided kernel: anticipation
  forward, memory backward, recursive (echoes of echoes), with felt news when forecasts
  change. The one-layer direct model is its reduced form for foreseen lives; surprises are
  information boundaries where the two part.
- The recursive model is well-founded iff the echo share `M` is below one. A finite life
  can stay monotone above that, but its echo grows without bound with lifespan. Felt news
  about experienced utility adds a threshold, `λκ < 1`, with a closed form in which memory,
  not anticipation, feeds the loop; past it, bad news runs away.
- Calibrated to felt anchors for a waking day and a life, echo is about 30% of experience,
  and the momentary self's felt row is nearly myopic: patience is not felt echo.
- Summed over a life, each moment is weighted by its centrality in the
  anticipation/memory graph. The interior is flat (no pure time preference), with deficits
  at birth and death.
- Preference for improving over declining lives at equal base total is set by the
  kernel's first moment. In a linear model it is a boundary effect, sized by the kernel's
  reach over the lifespan.
- For the momentary self, recursion turns exponential primitives into strict present
  bias; memory weakens it.
- Beliefs are welfare: felt anticipation is a forecast, so learning is not hedonically
  neutral. The truth is free in expectation but not pathwise. Dread outweighing savoring
  prices information only in the recursive model, where you anticipate your own future
  dread, and only when information moves a felt state across zero. Under recursive news a
  calibrated Bayesian is already braced. Unaware optimism buys experienced utility at the
  cost of decisions.
- Felt anticipation that tracks a prediction of your later choice makes that choice
  Newcomb-like. Decision rules differ in how much they let the present choice move the
  already-felt past.
- With the past held fixed, selves sharing the life-sum objective fall into a savoring
  trap: pleasures drift toward the unremembered end of life and pains are hurried. The
  mechanism is known (Kőszegi 2010); the exact stopping conditions are new.
- In momentary-happiness data (the Great Brain Experiment, 47,067 people; Forbes & Bennett's
  two experiments), the recursive model's kernel, a jump at the latest outcome and then a
  slower decay, beats the single exponential, with matching constants across datasets;
  surprise echoes like everything else, and news is loss-averse (`λ ≈ 1.4`).
  (`experiments/happiness/`)
- Learners that feel their own forecasts reproduce the decision theories by a gradient
  setting, brace or turn rosy by the sign of anticipation against chronic disappointment,
  and console themselves after bad news. A critic that shares its state with the policy
  carries its level into action: high expectations, biased or not, keep a learner
  complacent. Selection on payoff over generations of learners favors weak anticipation and
  real news, a braced critic. (`experiments/learned_expectations/`)
- Anthropics: measure-weighted anticipation makes branching welfare-invisible;
  copy-counting would let a branching future outweigh the past without bound.
- Prior art: the premise is old in economics (Jevons; Bergstrom 1987/1999; Caplin & Leahy
  2004; Ray, Vellodi & Wang 2024; Hersch & Weltman 2022) and absent from LessWrong. The
  post's value is the reframing, plus the specific results in `formalism/`.

Target: a LessWrong post.
