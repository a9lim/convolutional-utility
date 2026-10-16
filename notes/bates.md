# A felt forecaster in a Bates world

**Status: parked by a9 as its own project, not the post.** A felt learner tracking a
near-martingale price (geometric Brownian motion, Heston stochastic volatility, Merton
jumps): how its prediction moves as it tries to match the martingale, and how its felt
utility moves with it. Extensions: `extensions-menu.md`, section A.

## First results

From the 2026-10-14 review: a DP in that session's scratchpad (not archived), with Codex
(thread `cu-extensions`) agreeing independently.

- **Loss-averse news is a total-variation penalty.**
  `φ_λ(x) = ((1+λ)/2)x − ((λ−1)/2)|x|`, so equal-weight loss-averse news is a telescoping
  term minus `c = n(λ−1)/2` times the belief path's total variation. A felt forecast that
  tracks a diffusion exactly therefore costs without bound (infinite total variation).
- **The tethered display is a reflected martingale.** A felt display tethered by
  `(η/2)(q − M)²` to the martingale forecast `M` stays unchanged inside a band and is pushed
  at its edges, half-width `b* = (3cσ²/(2η))^{1/3}`. Singular control (Harrison–Taksar); the
  cube-root law of transaction costs. The band is centered by anticipation, not by `λ`.
  Checked by hand: uniform stationary law on the band, push rate `σ²/(2b)`.
  - The DP matches, with the discrete-monitoring correction `b − 0.583σ√dt`.
  - Watching continuously then costs finitely, `∝ σ^{4/3}` (DP slope 1.32).
  - The kink alone gives no asymmetric updating; that needs unequal weights, memory
    asymmetry or state dependence.
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

## Still to check

- Lumpy jump news against diffusive news of the same variance, beyond the per-unit-variance
  comparison above.
- Built-in bracing tracking volatility. The ostrich effect is documented (Karlsson,
  Loewenstein & Seppi 2009; Sicherman et al. 2016) and known in kind in models (Andries &
  Haddad; Pagel).
- Archive the DP.
