# Echo as addition or displacement

Drafting sketch (2026-10-15), for a9's decision. Script:
the session scratchpad's `disp.py`; Codex review in thread `cu-displacement`.

- **The dial.** `e = (I − dD)u + Ke`, `d ∈ [0, 1]`: `d = 0` adds echo to the present
  (canonical now), `d = 1` takes the attention from it. `D` is the share taken at each `t`.
  Boundary conventions for attention aimed past birth or death:
  - Z, attention to nothing: `D = M·I`.
  - Tr, unusable attention stays on the present: `D = diag(K1)`.
  - Rn, the budget `M` renormalized over the life: `K → M·P`, `P` row-stochastic.
- **Z is a rescale.** `e_d = (1 − dM) e_0`. Every fixed-kernel result survives: rankings
  across lengths, P5–P6 shapes, `β_L` and the patience bill, D3 timing, D5's sign patterns,
  and felt news with N4's threshold if news enters as `e = cu + Ke + N(e)` (`φ_λ` is
  positively homogeneous). Only comparisons across kernels move, which is where echo
  maximization lives. Exceptions (Codex): displacing the whole felt base `c(u + N)` turns
  the threshold into `cλκ < 1`; saturation, fixed external references and state-dependent
  budgets break proportionality; asymmetric kernels have no single `M`; `c > 0` needs
  `M < 1`. Objection: Z is not implied by A1's zero for death branches, and a one-period
  life gets `e = (1 − M)u`; keep Z as an explicit convention, not the natural reading.
- **Tr and Rn conserve.** `H = (I − K)^{-1}(I − D)` is row-stochastic, so each felt state
  is a convex combination of base utilities, `Σw = T`, and
  `W − Σu = T·Cov(w, u)`: echo creates welfare only through covariance between attention
  received and value. Rn's weights are uniform-teleport PageRank with damping `M`; Tr's are
  termination weights of an absorbing walk. Additive weights are Katz centrality.
  [checked numerically; Codex verified]
- **Tr against Rn.** Read `H` as an attention walk: from `t`, stop with the self-share and
  feel that moment's base utility, else jump along the kernel. Tr keeps every link's
  absolute weight and lets edges hold the walker (self-share rises where targets are
  missing); Rn keeps the self-share at `1 − M` and scales links up so the walker is
  reflected inward. Lost anticipation stays present under Tr and becomes memory under Rn
  (and lost memory becomes anticipation). Symmetric example (`a = m = 0.3, α = μ = 0.5`,
  `T = 5`): Tr weights `1.05, 0.97, 0.94, 0.97, 1.05`, a U; Rn `0.84, 1.09, 1.14, 1.09, 0.84`,
  a hump; Z `0.59 … 0.69`, the additive hump scaled. So Tr reverses P5's "deficits at birth
  and death". Rn needs a fallback where a row has no targets (a one-moment life). A second
  dial, the share of unusable attention that stays present, spans the two.
- **Pr, attention conditioned on existence (a9's reading).** Treat the present as one more
  target (weight `1 − M` at lag 0) and renormalize the whole row, present included, over the
  moments that exist. Lost attention then goes to the present and the remaining targets in
  proportion: at the life calibration the dying self's present share is 0.80 (Tr 0.83, Rn
  0.68, mid-life 0.68). Z is the same distribution unconditioned (mass on missing moments
  lands on zero), so Z against Pr is unconditioned against conditioned, A1's question on the
  time axis. Coherent with A1 if attention is over times and forecasts over branches.
  - Conserves (`Σw = T`). Exact weights: `w = 1 − D′(I − K′ᵀ)^{-1}(r − c)/(1 − M)`, with
    `r, c` the truncated kernel's row and column sums and `D′, K′` the normalized self-shares
    and links. So `w = 1` wherever attention is balanced (each moment receives what it
    gives): a symmetric kernel gives exactly flat weights, no boundary effects at all. At the
    extreme edges `r − c = ±(A − B)`: the end outweighs the beginning iff anticipation mass
    exceeds memory mass. Life calibration (`A ≈ B`) 1.01 and 0.99; long anticipation
    (`A = 0.66, B = 0.15`) 0.29 at birth, 5.47 at death. [checked numerically, 200 draws]
  - Under Rn the dying self's own weight changes only through loops (remembered
    anticipation of now): 0.47 against 0.50 mid-life (symmetric, `T = 5`), 0.28 against 0.20
    (long anticipation).
- **Uncertain death under Pr (a9's question).** Not the expected death date: attention to
  `t + j` is `k(j)·S_t(j)`, with `S_t(j)` the probability of being alive then, renormalized
  with the present and past; the content is the forecast conditional on being alive then.
  Certain death recovers Pr, no risk the plain kernel, continuously in `S`.
  - Conservation holds over branches, measure-weighted (`πᵀH1 = πᵀ1`), not within one: in
    a surprise-death branch the final selves spent attention on times that exist only in the
    other branch, so that branch's welfare depends on the other branch's base utility.
    Pathwise imbalance, balance in expectation, as with the truth being free.
  - Endings weigh in proportion to how foreseen they are. One-step present share before a
    possible death, life calibration: `(1−M)/((1−M) + B + A(1−p))`, 0.68 at `p = 0`, 0.735
    at ½, 0.80 at 1.
  - Three treatments of a doomed branch: Z (attend as usual, its content is zero: likely
    death dilutes the felt state, A1 carried over literally); survival-weighted Pr (attend
    less, redirect to present and past, content conditional); quantum immortality (attend
    as if surviving). Additively the first two coincide (`k·S·E[e | alive] = k·E[e]` with
    zeros), so A1 never had to choose; displacement forces it, and Pr at known edges forces
    survival weighting by continuity. A1 survives modified: a likely early end discounts the
    future's attention, which goes to present and past, not to nothing; the jolt is news.
    No copy-counting: attention to a time totals its measure across copies.
- **Boundaries become substantive under conservation.** Life calibration: the ramp tilt
  per unit welfare doubles (Tr 144, Rn 145, against 72 additive or Z). At `a = 0.09,
  α = 0.88, m = 0.05, μ = 0.75`, Tr weights the last moment 3.6 against 0.96 in the
  interior and 0.43 at birth: self-share times centrality, the dying self's unusable
  anticipation staying present on a moment every earlier self anticipated. The end-pulse
  sign at the life calibration flips between Z/Tr and Rn. Codex's P6 counterexample
  survives all conventions.
- **Evidence.** Killingsworth & Gilbert 2010: mind-wandering to pleasant topics −0.52
  (n.s.), neutral −7.2, unpleasant −23.9 (0–100), relative to on-task. Displacement predicts
  the neutral penalty as share × (on-task value − neutral thought); a share near one half if
  on-task is in the mid-60s and a neutral thought near the midpoint (illustrative, not
  estimated). Addition needs a separate attention cost. Both fit three numbers with three
  anchors. Discriminator, holding thought value and share fixed: the penalty grows with the
  current activity's value under displacement (slope −s) and is flat under addition plus a
  cost; observational activity comparisons do not hold those fixed.
- **Two channels (hypothesis).** Attended thought displaces; tonic mood adds. The
  calibration anchors already split this way: memory anchors (vacation afterglow,
  trial-scale mood, the Great Brain Experiment's persistent luck level) look tonic, the
  anticipation anchor (Kumar et al., "while thinking about it") attentional.
- **Not fixed by displacement.** Anthropic totals: conservation keeps constant lives'
  value, not `wᵀu = Σu`. A root remembered by two children at half attention gets weight
  2, and `u = (1, 0, 0)` gives welfare 2 against base 1; on an infinite binary tree a root
  impulse sums as `Σ(2s)^n`. Summability conditions stay. News left additive keeps N4's
  instability. The regress is anchored (absorbing walk), not removed.
