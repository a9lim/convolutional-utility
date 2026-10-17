# Convolutional Utility

A research project behind one LessWrong post, working title *Experience Echoes*.

**The idea.** What you feel now includes how you feel about other times: looking forward,
looking back, and the jolt when your forecasts change. Take the hedonic reading, where those
feelings are experiences and welfare is the life-sum of experience. Experienced utility is
then base utility plus felt anticipation forward, felt memory backward and felt news on
revisions, recursively (you remember looking forward; you look forward to remembering). For
foreseen lives and linear echo this is a convolution of base utility with a two-sided
kernel, hence the name. The core weighs gains and losses alike; sign asymmetries are an
extension, ranked by their felt evidence.

**What follows.**

- A moment matters by its place in a web of echoes. Interior moments approach the same
  weight, so echoes add no pure time preference; birth and death weigh less; under linear,
  stationary echo, the shape of a foreseen life matters only through its ends.
- Learning can change how a life feels without changing what you do. With calibrated
  forecasts, linear echoes and news, fixed actions and a fixed lifespan, information is
  neutral in expectation but moves welfare on each path; once gains and losses are weighed
  apart, dread of dread (the best-supported asymmetry) and loss-averse news put a price on
  it. So a hedonic agent chooses an affect policy, what it feels by, as
  well as an action policy, and its own actions leak into the first.
- The self that looked forward to a choice is a predictor of it, so ordinary choices inside
  one life can be Newcomb-like. How much of that already-felt anticipation a decision rule
  counts as depending on the present choice separates fixed-past choice from commitment.

**What is imported and what is new.** The premise and most of the machinery are old:
anticipatory and memory utility (Jevons; Loewenstein; Caplin & Leahy), recursive
interdependence (Bergstrom), news utility (Kőszegi & Rabin), optimal expectations (Brunnermeier
& Parker), the savoring trap (Kőszegi). The post's job is mostly to bring them to LessWrong's
own questions: the Litany of Gendlin, value of information and updatelessness, Newcomb and
FDT, discount rates, the Anthropic Trilemma. The candidate results, not found in the
literature passes, are narrower: shape as a boundary effect (and the ramp theorem),
recursion's price on information under dread, a calibrated Bayesian being already braced
(flagged: it needs loss-averse news), the news loop's gain, and a reanalysis of public
momentary-happiness data. Two framings are new
assemblies with close prior art: affect policies and their leaks, and the past self as
predictor. The full lists are at the top of `outline.md`.

**Evidence.** Proofs and numerical checks for the model (`formalism/`); trial-level ratings
from 47,067 people, whose echoes of task outcomes are front-loaded and heavy-tailed but do not
single out the recursive form (`experiments/happiness/`); small learned agents, mostly a
follow-up line on decision theory by learning (`experiments/learned_expectations/`).

**Reading order.** `outline.md` (the post's scaffold, authoritative) → `formalism/INDEX.md`
(every claim's proposition, support and artifact) → the experiment READMEs. `next-steps.md`
is the plan; `AGENTS.md` maps the repository.
