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
