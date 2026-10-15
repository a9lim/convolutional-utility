# Momentary happiness data

The recursive echo model against trial-level ratings of "How happy are you right now?" in a
risky-choice task (Rutledge, Skandali, Dayan & Dolan 2014).

## Data

- **Great Brain Experiment** smartphone task (Rutledge et al. 2014's replication sample;
  deposited by R. B. Rutledge, Zenodo record 4421847, mirror of Dryad
  doi:10.5061/dryad.prr4xgxkk; CC0). 47,067 participants, 91,058 plays of 30 trials (11 gain,
  8 mixed, 11 loss; safe option against a 50/50 gamble), 12 ratings per play.
  `Rutledge_risk_and_happiness_task_2023.zip` (87.5 MB, MD5
  `899fb2380a25b208bf9a445e0c06b9d8`), unzipped to `data/gbe/extracted/`.
- **Forbes & Bennett 2024** (OSF `m7dtw`): two experiments, 150 participants each, 4 blocks of
  53 trials and 56 affect ratings per person; CSVs in `data/forbes/exp1`, `data/forbes/exp2`.
- `data/` is gitignored; the downloads are data only (the GBE archive's MATLAB script is not run).

## Code

- `gbe.py`: flattens the MATLAB structs to per-play arrays (`data/gbe/tidy.npz`), Rutledge's
  regressors (certain reward CR, a chosen gamble's expected value EV and prediction error
  RPE), the kernels, and the fit: least squares with a fixed effect per play, ratings
  z-scored within participant.
- `run_gbe.py`: the model comparison on held-out participants, a bootstrap over participants,
  the structural model for news by sign, and per-component kernels; writes `gbe_report.txt`
  and `gbe.png`.
- `forbes.py`, `run_forbes.py`: the same models on Forbes & Bennett, cross-validated over
  people, with each person's own kernel; writes `forbes_report.txt`.

Run from the repo root: `python experiments/happiness/run_gbe.py` (about 13 minutes),
`python experiments/happiness/run_forbes.py`.

## The models

A trial's felt contribution is `CR`, or for a gamble its outcome `EV + RPE`, plus the
gamble's anticipated `EV` and its felt news on `RPE`. A rating reads the current felt
state, that contribution plus echoes of earlier ones through a kernel `k(lag)`.

- Rutledge et al.: `k = γ^lag`, one geometric.
- Recursive memory over felt states, `e_t = f_t + m Σ_j μ^j e_{t−j}`, has resolvent kernel
  `(1, k₁, k₁γ, k₁γ², …)` with `k₁ = mμ` and `γ = μ(1 + m)`: a jump at lag 0, then a slower
  geometric, `k₁ < γ`. Rutledge's kernel is the case `k₁ = γ`. (`k₁` is the lag-1 weight,
  `kappa` in the code and reports; core's `κ` is the news-loop gain.)
- Direct (one-layer) memory, `e_t = f_t + m′ Σ_j μ′^j f_{t−j}`, has kernel
  `(1, m′μ′, m′μ′², …)`: the same two-parameter family, with `γ = μ′` and `k₁ = m′μ′`, and any
  sign of `γ − k₁`. Rutledge's kernel is the direct case `m′ = 1`. The fits below cannot tell
  the two readings apart (core P2), and neither from transient-plus-mood.
- Shape alternatives (audit): a power law `(1 + lag)^{−ρ}` (one parameter) and a hyperbola
  `(1 + h·lag)^{−ρ}` (two).

## Results so far

Great Brain Experiment (`gbe_report.txt`, `gbe.png`, `audit/`):
- **Replication.** Rutledge's model gives `γ = 0.68` per trial (their lab sample: 0.61 ± 0.30
  SD per person; ours is a pooled fit).
- **Echoes are front-loaded, with a slow tail.** The jump kernel (`γ = 0.882, k₁ = 0.419`)
  cuts held-out within-play error 1.3% against Rutledge's (1.7% with prediction errors split by
  sign, where `γ = 0.890, k₁ = 0.412`; 20-resample bootstrap [0.886, 0.896], [0.408, 0.418]).
  But it is not the best shape: a one-parameter power law (`ρ = 0.81`) beats it by 0.48%
  [0.40, 0.56] and a hyperbola by 0.66% (paired bootstrap over held-out participants). A free
  30-lag kernel decays progressively (successive ratios 0.52, 0.71, 0.86, …), not one drop
  then a constant ratio. Recursive reading of the sign-split fit: `μ = 0.48`, `m = 0.86`;
  direct reading: `μ′ = 0.89`, `m′ = 0.46`, with identical fit
  (`audit/direct_vs_recursive.py`).
- **Echo share, not memory mass.** `B = k₁/(1−γ+k₁) ≈ 0.78`, the share of a sustained input's
  long-run response that comes from earlier trials, is the same under every reading (the
  memory mass is 0.78 read recursively and 3.5 read directly). It depends on the tail: under
  the power law, whose exponent is below one, it is 0.81 over 30 trials, 0.87 over 100 and
  0.93 over 1000, so it does not settle (core P1(d)).
- **Seconds count within a play, not between players.** The lag-1 weight is 0.61 after a safe
  last trial and 0.13 lower after a gamble (whose spinner takes seconds), and, within safe
  trials, falls with choice latency (`audit/confounds.py`). On the hyperbola, the raw seconds
  between outcome and rating add nothing (−0.011% [−0.029, +0.006]); the apparent clock in the
  jump kernel (−0.19%) was its shape. Delays against the play's own pace do count, about 1% of
  an echo per second (`θ ≈ 0.010`; −0.046% [−0.064, −0.028]), so slower players do not forget
  more per trial, but a delay within a play costs. Each gamble resolved in between lowers an
  echo (`η = 0.93`) and each rating in between raises it (`ρ = 1.15`) (`audit/felt_clock.py`).
  The clock factor multiplies a hyperbola in trials, which is not a hyperbola in seconds; a
  kernel fitted directly in elapsed seconds is open. The lag-1 trial never precedes a rating
  in this design, so a reset at ratings cannot be tested directly. Pooling heterogeneous people also makes a jump:
  Forbes-like data simulated with each person's own single geometric give a pooled jump with
  `B ≈ 0.8` and a third of the real advantage (`audit/forbes_pooling_null.py`). Real people
  still front-load more than that null (below).
- **Age reshapes the kernel; whether through a slower felt clock is not settled.** From 18–24
  to 60–69, relative to the current trial, the lag-1 echo shrinks and the tail lengthens: the
  hyperbola's exponent falls from 0.71 [0.68, 0.75] to 0.49 [0.42, 0.56], and the jump
  kernel's `k₁` from 0.46 to 0.34 while `γ` rises from 0.86 to 0.91. The test is of one felt
  clock from seconds to years, felt rate `∝ age^−q` (Janet `q = 1`; Lemlich 1975,
  `ds/dt ∝ 1/s`, `q = ½`). A hyperbolic kernel on such a clock keeps its shape: ratings
  simulated from a pure Lemlich clock return a flat exponent (0.60–0.66) and `q = 0.48`, so
  that form is out. A fast transient plus a slow mood is not: slowed by Lemlich's or Janet's
  factor, it leaves the current outcome more of its transient at the rating, and gives the
  same crossing (the trial hyperbola's exponent 1.8 → 0.65 or 0.38). Sensitivity to delays
  within a play is flat across age (`q ≈ 0.16`), but for a hyperbolic clock that need not
  scale with the clock's speed. The jump kernel's decay alone gives `q = 0.56` [0.35, 0.75]; it
  returns 0.26 from a true 0.5, so it is not a clock estimate. Bands are cross-sectional, so
  age carries cohort and selection into a smartphone game; intervals for the within-play
  sensitivity rest on 16 draws (`audit/felt_clock.py`).
- **No adaptation dip; luck's afterglow lasts days.** A biphasic kernel, afterglow minus a
  slow negative tail `c γ^lag`, collapses to the jump kernel within a play (the fitted reach
  of the negative part goes to 0); a hyperbola minus an exponential gains 0.026% [0.014,
  0.037] by flattening the positive tail, never crossing zero. Between plays, a play's luck
  (summed RPE, random given choices) lifts the next play's pre-trial rating by 45% [40, 50]
  of its end-of-play effect after a median 4.4 minutes, 23% [5, 44] after 22 minutes, 10%
  [−1, 21] after 10 hours, 6% [−5, 17] after 2.4 days and −2% [−16, 11] after 38 days:
  roughly a power law in wall-clock time with exponent about 0.3, positive throughout. Raw
  ratings, since within-person z-scores would make a lucky play mechanically lower the
  person's others. Not a cursor artefact: a cursor starting at 50 carries less (28%) than a
  random start (61%). Game points may not move a reference the way life circumstances do;
  months and years are out of reach here (`audit/biphasic.py`, `audit/carryover.py`).
- **News does not echo like the outcome.** Fitted separately, the kernels of certain rewards,
  expected values and prediction errors nearly coincide (`γ` 0.88, 0.87, 0.89), but the RPE
  regressor there still carries the outcome's base utility. With base utility in its own
  regressor, news alone has `γ` at the bound 0.999 (`k₁` 0.27): a persistent level, luck
  accumulated over the play, against `γ ≈ 0.79` for base utility (`audit/news_kernel.py`).
- **Chosen risk lowers happiness; loss-averse news is not identified.** The structural model
  (base utility pinned by safe choices, linear in money; news by mixed trials) gives
  `λ = 1.42` [1.37, 1.50], `n = 0.52`, base loss aversion 1.20 and `a = −0.30`. But splitting
  news by sign is `½(β₊+β₋)·RPE + ½(β₊−β₋)·|RPE|`, and in a 50/50 gamble `|RPE|` is half the
  gamble's range, known at choice: asymmetric news and a felt cost of the chosen gamble's
  spread are the same regressor. Adding one constant cost of having gambled (−0.024 SD) takes
  `λ` to 1.04 [0.95, 1.13] and fits slightly better. `a = −0.30` mostly reflects linear base
  utility extrapolated from safe amounts (30–55) to gamble outcomes (±150): with power utility
  `ρ = 0.8`, `a = −0.15` and `λ = 1.36`, or 1.13 with the gamble cost (`audit/risk_cost.py`).
  Under linear base utility, gamble outcomes feel worse than their EV implies, as diminishing
  sensitivity predicts.

Forbes & Bennett 2024 (`forbes_report.txt`, `audit/`):
- **The same front-loading.** Jump kernel `γ = 0.885, k₁ = 0.516` (experiment 1) and
  `γ = 0.883, k₁ = 0.457` (experiment 2), against single geometrics of 0.80 and 0.76;
  cross-validated error over people 1.0% and 1.6% lower. A power law (`ρ` 0.69, 0.76) does
  better, 2.5% and 2.8%. Fitted person by person (56 ratings each), `k₁` is below `γ` for 57%
  and 62% of people (31% and 39% in the pooling null) and above for 18% and 17%; `k₁ > γ` is
  inconsistent with recursion at any noise level.
- **Bad surprises register more, and only on one's own choices.** Every payoff is a lottery's,
  so RPE weights are news net of anticipation. Positive RPE adds nothing beyond the outcome
  (−0.002), negative RPE lowers affect (0.05 and 0.09 per 100 points), as Forbes & Bennett
  report. Probabilities vary here (0.25, 0.5, 0.75), which separates spread from `|RPE|`: with
  the chosen lottery's SD as a regressor the asymmetry vanishes in experiment 1 (RPE+ 0.028,
  RPE− 0.025; SD −0.052 [−0.097, −0.019]) and shrinks in experiment 2 (the `|RPE|` term −0.026
  [−0.069, 0.013]). In experiment 1 RPE registers on free choices and not on forced ones. A
  better unchosen outcome lowers affect slightly (regret), a worse one raises it (relief).

## Audit (2026-10-14)

`audit/`: a fresh-eyes review of the claims above (a subagent, rerun by Claude; data under
`data/`, paths relative). Run each from anywhere, e.g. `python
experiments/happiness/audit/kernel_shapes.py`; `confounds.py` needs `extract_timing.py` first
(it writes `data/gbe/extra.npz`, choice latencies and spinner times). Outputs are in
`audit/audit_report.txt`.
- `direct_vs_recursive.py`: both parametrizations, identical fit; the readings' parameters.
- `free_kernel.py`: a free 30-lag kernel against power, hyperbolic, geometric-plus-constant
  and double-exponential shapes (the hyperbola is within 0.03% of the free kernel).
- `kernel_shapes.py`: Rutledge, jump, power law and hyperbola on held-out participants, with
  paired bootstrap differences; the jump by task version.
- `risk_cost.py`: the structural model with a cost of having gambled and power utility.
- `news_kernel.py`: per-component kernels with base utility separated from news.
- `confounds.py`: the lag-1 weight by trial type and latency, and the rating boundary.
- `felt_clock.py`: trials against seconds (raw, and against the play's own pace) on the jump
  and the hyperbola; kernels by age band against a felt clock `∝ age^−q`; a recovery check on
  ratings simulated from a pure Lemlich clock; the two-timescale counterexample. Stages
  `pooled`, `age`, `within`, `null`, `mixture` (needs `extract_timing.py`; about 25 minutes in
  all on 12 cores).
- `forbes_shapes_risk.py`, `forbes_pooling_null.py`: kernel shapes, the lottery-SD
  separation, and the pooling null on Forbes & Bennett.
- `biphasic.py` (2026-10-15): afterglow-minus-adaptation kernels within a play (the audit
  split) and within a Forbes & Bennett block (5-fold CV), against the jump kernel and the
  hyperbola.
- `carryover.py` (2026-10-15): a play's luck against the change in the next play's pre-trial
  rating, by the gap between plays (day number and time of day from the archive), and the
  same between Forbes & Bennett blocks.
