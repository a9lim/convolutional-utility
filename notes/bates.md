# A felt forecaster in a Bates world

**Status: parked by a9 as its own project, not the post.** A felt learner tracking a
near-martingale price (geometric Brownian motion, Heston stochastic volatility, Merton
jumps): how its prediction moves as it tries to match the martingale, and how its felt
utility moves with it. Two readings of what the price is to the self: a terminal quantity
forecast along the way, or base utility felt every moment. Checks: `bates.py`
(`python notes/bates.py`). Extensions: `extensions-menu.md`, section A.

## Terminal reading

From the 2026-10-14 review, with Codex (thread `cu-extensions`) agreeing independently.

- **Setup.** Base utility is a fixed quantity `X` revealed at a terminal date. Its correct
  forecast `M_t = E[X | F_t]` is a martingale whatever the price dynamics, which set only
  its volatility and jumps. The felt display `q_t` is what anticipation and news act on;
  revelation closes it, `q_T = X`.
- **Loss-averse news is a total-variation penalty.**
  `φ_λ(x) = ((1+λ)/2)x − ((λ−1)/2)|x|`, so equal-weight loss-averse news is a telescoping
  term minus `c = n(λ−1)/2` times the belief path's total variation. A felt forecast that
  tracks a diffusion exactly therefore costs without bound (infinite total variation).
- **The tethered display is a reflected martingale.** A felt display tethered by
  `(η/2)(q − M)²` to the martingale forecast `M` stays unchanged inside a band and is pushed
  at its edges, half-width `b* = (3cσ²/(2η))^{1/3}`. Singular control (Harrison–Taksar); the
  cube-root law of transaction costs. The band is centered by anticipation, not by `λ`.
  Checked by hand: uniform stationary law on the band, push rate `σ²/(2b)`.
  - The DP matches, its edges inside `b*` by 0.55–0.60`σ√dt` (discrete monitoring; the
    Gaussian-walk constant is 0.583). *checked*
  - Watching continuously then costs finitely, `∝ σ^{4/3}` (DP slope 1.333). *checked*
  - The kink alone gives no asymmetric updating, in either reading; that needs unequal
    weights, memory asymmetry or state dependence.
- **Cost is concave in variance.** Clustered volatility at equal mean variance is cheaper
  (two regimes against constant: −16% in one example). Rarer, larger jumps are cheaper per
  unit variance (`∝ σ√ι`).
- **Attention against volatility has no fixed sign.** With a fixed staleness cost,
  `h* ∝ σ^{2/3}` (look less in high volatility, the ostrich direction); with quadratic
  tracking loss, `h* ∝ σ^{−2/3}` (look more). Volatility-scaled bracing unwinds as volatility
  mean-reverts, so there is no supermartingale in general; with the leverage effect, falls
  deepen bracing.
- **Pitfall.** A KL tether does not bound optimism for lognormal prices
  (`sup_Q a E_Q[X] − KL(Q‖P)/τ = ∞`); use log or bounded utility.

## Flow reading

Base utility is the price itself, `u_t = X_t` with `X` a martingale: a log price, or
consumption as in Hall's random walk. The comparison model (news over `u`) unless stated.
From 2026-10-18, with Codex (thread `cu-extensions`) verifying the band and the loop
multiplier.

- **A move is news about every remaining moment.** Every forecast of later base utility is
  `X_t`, so a move `ε_t` revises them all by `ε_t`, arrival (`j = 0`) included. The
  revisions share a sign, so the per-horizon kinks collapse: `N_t = K_t φ_λ(ε_t)` with
  `K_t = Σ_{j<T−t} nν^j`, the whole news kernel. The terminal reading weighs a move by its
  news about one moment, rising toward the reveal; here the weight falls as the remaining
  life shortens. *known in kind* (news utility over consumption flows: Kőszegi & Rabin
  2009, Pagel 2017); *checked*
- **The honest cost is first order in the move.** Per period `K_t (λ−1)/2 · E|ε_t|`, times
  the moment's life weight (N2). With volatility independent of the driving noise,
  `E|ε| = √(2/π) E√(∫v)`, so clustered volatility at equal mean variance is cheaper
  (Jensen; with leverage the exact comparison fails), and rarer, larger jumps are cheaper
  at equal variance (`E|ε| = σ√p`). The price itself, not its log, has local scale `X√v`.
  *synthesis; Codex on the qualifiers*
- **The loop makes losses much dearer than gains.** Canonically a move revises every later
  felt state through the remaining-life resolvent `R` (`v = R1`, `g = Re₀ ≥ 0`), and on the
  branch `λκ < 1` the felt news is `ε k_n·v/(1−κ)` for gains and `λε k_n·v/(1−λκ)` for
  losses. At `pathwise.py`'s defaults (`κ = 0.36`) a unit gain near birth is felt as 6.3, a
  unit loss at `λ = 2` as 29.4. *checked against `pathwise.run`; Codex verified*
  - These are unforeseen-announcement forecasts. Bayesian forecasts put the expected news
    in the reference, so the forcing is `X − m`, not `X`: with `X = ±1`, `n = 0.3`,
    `λ = 2` and no echoes, the expected news is `−3/11`, against `−0.536` unforeseen. The
    sign survives (honest expected news is `≤ 0`), and so does scaling with the innovation
    in a homogeneous benchmark. *Codex; checked by hand*
- **Realization is the tether.** One felt level `q` for all horizons; gap `d = q − X`.
  Continuous time with per-step weights `n → n₀`, `ν = e^{−rΔ}` and welfare `Δ Σ e`:
  - anticipation pays `A q`;
  - arrival compares the realized flow with the display, `n₀ φ_λ(X − q) dt`, a running
    cost on the gap (the increment's own surprise is `O(√Δ)` over a fixed interval, kink
    included);
  - moving `q` is news about every later horizon, a lump `N₊ φ_λ(dq)` with `N₊ = n₀/r`
    (`γn₀/r` with Pagel's `γ`): arrival and revision weights are tied through news reach.
  - Collected: running cost `κ₊d⁺ + κ₋d⁻`, with `κ₊ = λn₀ − A` (optimism: disappointment
    at `λ`, less anticipation) and `κ₋ = A − n₀` (pessimism: anticipation forgone, less
    elation), and revision cost `c = N₊(λ−1)/2` per unit of `|dq|` once the linear part
    telescopes. An L1 tether with its corner at honesty, with a finite stationary band iff
    `n₀ < A < λn₀`. At an endpoint the band escapes to infinite width; outside, a constant
    bias pays without bound; at `λ = 1` only the neutral `A = n₀` survives (N3's missing
    interior optimum). *synthesis; Codex on the scaling and the endpoints*
- **The band is linear in σ.** Reflected on `[−β, α]`, `L = α + β`, the cost is
  `(κ₊α² + κ₋β²)/(2L) + cσ²/L`, so `α : β = κ₋ : κ₊`, `L* = σ√(2c/κ̄)`, cost `σ√(2cκ̄)`,
  with `κ̄ = κ₊κ₋/(κ₊+κ₋)`. Smooth fit (`κ₋β = κ₊α = J`) verifies it against all policies.
  Against the terminal reading: width `σ` for `σ^{2/3}`, cost `σ` for `σ^{4/3}`, a square
  root in the costs for a cube root. *standard control (Harrison–Taksar; Dai & Yao for
  convex holding cost); checked: DP cost to 3e-4, edges 0.58–0.59`σ√dt` inside*
- **Biased anchoring, not asymmetric updating.** The band is a symmetric band of width `L`
  around a constant offset `(α − β)/2`: optimism when `A > (1+λ)n₀/2`, pessimism below. In
  stationarity pushes up and down are equally frequent and responses mirror each other, so
  the kink still gives no asymmetric updating; only from an honest start do the directions
  differ (when optimistic, a fall is tolerated longer than a rise). A quadratic tether
  with linear anticipation also shifts its band; the arrival kink supplies this offset and
  the scaling. *synthesis; Codex*
- **Caveats.**
  - The stationary band needs constant coefficients and an average-cost horizon. In a
    finite life `N₊(t) = (n₀/r)(1 − e^{−r(T−t)})`, whose integration by parts leaves a
    running term, so the band is an interior approximation.
  - **The single display level is load-bearing.** Revisions compare the same calendar
    target, so a display that varies by horizon is felt as news as it rolls toward
    arrival, and the telescoping holds only for a flat display. With a curve the problem
    can be unbounded: at `X ≡ 0`, `n₀ = 1`, `λ = 2`, `a(h) = 0.15e^{−0.1h}` (`A = 1.5`,
    inside the window) and `n(h) = e^{−h}`, an optimistic bump `B` on horizons `[10, 11]`
    gains `B[∫a + n(11) − λn(10)] = 0.0524B` per unit time. Optimism pays without bound
    where anticipation outlasts news. *Codex; checked by hand*
  - N3's calibrations put `Θ` at 1 (day) and 0.7 (life), at or below the window's floor
    (N3's event `Θ`, not this display's).
  - Full adaptation (`adaptation.md`) turns the level into its derivative, so the base
    level telescopes too and only the kinks matter.
- **Prior art** (abstracts read 2026-10-18, full texts not). Dai & Yao 2013 (*Stochastic
  Systems* 3; arXiv 1110.2831) solve the control class: Brownian inventory, convex holding
  cost, proportional adjustment. Choi, Jeon & Koo 2022 (*JET* 200) get consumption inaction
  intervals from loss aversion as two-sided singular control, a control of consumption, not
  of a felt forecast. Macera 2014 (*GEB* 87) chooses belief paths under utility from
  anticipation and its changes, with optimism falling as the payoff nears: the closest
  predecessor of a chosen display in either reading. The display band: *not found*.

## Still to check

- Lumpy jump news against diffusive news of the same variance, beyond the per-unit-variance
  comparison above.
- Built-in bracing tracking volatility. The ostrich effect is documented (Karlsson,
  Loewenstein & Seppi 2009; Sicherman et al. 2016) and known in kind in models (Andries &
  Haddad; Pagel).
- The flow reading's display as a curve over horizons, under horizonwise calibration or a
  distortion cost: honest near horizons and biased far ones?
- The flow reading under Bayesian forecasts in the canonical model: the loop's input
  becomes `X − m`, and the continuous-time order needs a uniform fixed-point argument.
- Jumps through the flow band: a jump past an edge forces one lump, as in A3.
