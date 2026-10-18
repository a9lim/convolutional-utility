# Momentary happiness data

The recursive echo model against trial-level ratings of "How happy are you right now?" in a
risky-choice task (Rutledge, Skandali, Dayan & Dolan 2014).

**In the post** (`outline.md`, §9). The data constrain the kernel's shape and show what the
model cannot identify; they do not validate recursion. Echoes of task outcomes are
front-loaded with a slow tail, closer to a power law than to a single exponential, in all three
datasets; about 80% of a sustained outcome stream's fitted response comes from earlier trials;
direct and recursive memory fit identically; an apparent loss-averse news asymmetry is
confounded with chosen risk, and a lottery-risk regressor absorbs or reduces it where
probabilities vary; a loss's echo starts stronger than a gain's and fades faster. Whether the
play-long persistence belongs to base utility or to news is not identified. The felt-clock,
carryover, adaptation and range analyses stay here, as do news about later trials (Blain &
Rutledge) and the step tests (Keren, Jangraw).

## Data

- **Great Brain Experiment** smartphone task (Rutledge et al. 2014's replication sample;
  deposited by R. B. Rutledge, Zenodo record 4421847, mirror of Dryad
  doi:10.5061/dryad.prr4xgxkk; CC0). 47,067 participants, 91,058 plays of 30 trials (11 gain,
  8 mixed, 11 loss; safe option against a 50/50 gamble), 12 ratings per play.
  `Rutledge_risk_and_happiness_task_2023.zip` (87.5 MB, MD5
  `899fb2380a25b208bf9a445e0c06b9d8`), unzipped to `data/gbe/extracted/`.
- **Forbes & Bennett 2024** (OSF `m7dtw`): two experiments, 150 participants each, 4 blocks of
  53 trials and 56 affect ratings per person; CSVs in `data/forbes/exp1`, `data/forbes/exp2`.
- **Blain & Rutledge 2020** (*eLife* 9: e57977; GitHub `BastienBlain/MSWB_LearningNotReward`,
  `PublicCode/Blain_MoodTracksLearning_data.mat`, MD5 `a2b8ec33b80365c886bc367bbf30854b`, no
  license stated): a car-race bandit whose win probability must be learned, 75 participants,
  a stable and a volatile block of 80 trials each, 46 ratings. In `data/blain/`.
- **Keren et al. 2021** (*eLife*; OSF `vw7sz`, `Figure2_SourceData/Structured experiment
  data`, 79 xlsx files, one empty): the open-loop up-down-up task, 3 blocks of 27 trials, 37
  ratings. In `data/keren/structured/`.
- **Jangraw et al. 2023** (*Nat. Hum. Behav.* 7: 596; OSF `km69z`,
  `PassageOfTimeDysphoria_Data.zip`, 206 MB, MD5 `f51220d6a6cea49f850dc7930fffc256`, NIMH
  public domain): the same task after a rest period, 3 blocks of 22 trials, 29 ratings, in the
  cohorts Weekly-Rest-02 and -03 (folders `COVID02`, `COVID03`; complete runs per the archive's
  data checks); RestAfterWins (`Return1`). Unzipped in part to `data/jangraw/extracted/`.
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
- `blain.py`, `run_blain.py`: news about later trials in Blain & Rutledge's bandit. A delta-rule
  learner fitted to choices gives each trial's belief; the trial's own channels and the
  forecast of later trials, free and tied to them; writes `blain_report.txt`.
- `steps.py`, `run_steps.py`: kernel shapes, biphasic memory included, at the step changes in
  luck of Keren's and Jangraw's up-down-up task; writes `steps_report.txt`.

Run from the repo root: `python experiments/happiness/run_gbe.py` (about 13 minutes),
`python experiments/happiness/run_forbes.py`, `run_blain.py` (about 12 minutes),
`run_steps.py`.

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
- **No adaptation lobe detected; carryover is consistent with a slow positive afterglow.** A biphasic kernel, afterglow minus a
  slow negative tail `c γ^lag`, collapses to the jump kernel within a play (the fitted reach
  of the negative part goes to 0); a hyperbola minus an exponential gains 0.026% [0.014,
  0.037] by flattening the positive tail, never crossing zero. Between plays, a play's luck
  (summed RPE, random given choices) lifts the next play's pre-trial rating by 45% [40, 50]
  of its end-of-play effect after a median 4.4 minutes, 23% [5, 44] after 22 minutes, 10%
  [−1, 21] after 10 hours, 6% [−5, 17] after 2.4 days and −2% [−16, 11] after 38 days:
  roughly a power law in wall-clock time with exponent about 0.3, positive throughout. Raw
  ratings, since within-person z-scores would make a lucky play mechanically lower the
  person's others. Not a cursor artefact: a cursor starting at 50 carries less (28%) than a
  random start (61%). The gap is the player's choice, and unlucky players replay sooner (65%
  of the unluckiest fifth within 10 minutes, 42% of the luckiest): if that selection also
  runs on mood, short-gap carryover is inflated. An impulse test is nearly blind to slow
  adaptation: even complete adaptation lets a 5-minute pulse leave at most 27% of itself as
  a negative lobe at 4 minutes (time constant 7 minutes), 7.6% at 22 minutes, 0.3% at 10
  hours and under 0.1% beyond, far inside these intervals. So the data rule out only fast
  adaptation, and a positive afterglow could mask even that; slow adaptation shows in
  responses to sustained changes, where the lobe accumulates (`audit/biphasic.py`,
  `audit/carryover.py`, `audit/impulse_detectability.py`).
- **Range adaptation, partial and fast.** After a run of high-stakes trials (the mean of each
  trial's largest offered amount over the previous five, random draws), outcomes move
  happiness less: per s.d. of recent stakes, positive RPE −2.8% [−3.7, −1.7], negative RPE
  −1.9% [−2.9, −0.9], EV −1.6% [−3.1, −0.4], certain rewards −1.1% [−2.5, +0.2]. Full
  divisive normalization over that window would be −16%, so about a tenth of it; too small
  to improve held-out error. Forbes & Bennett are too noisy to tell (positive RPE carries no
  weight there, so its ratio is undefined) (`audit/divisive.py`).
- **Where the persistence sits is not identified.** Fitted separately, the kernels of certain
  rewards, expected values and prediction errors nearly coincide (`γ` 0.88, 0.87, 0.89), but
  the RPE regressor there still carries the outcome's base utility. With base utility in its
  own regressor the fit has two near-tied optima: news persists through the play (`γ` at the
  bound 0.999, `k₁` 0.28) with base utility at `γ = 0.78`, or base utility persists
  (`γ = 0.94`) with fast news (`γ = 0.45`, `k₁` 0.70). The second fits slightly better on
  held-out players (0.648694 against 0.648754) and in 6 of 8 participant resamples, by under
  0.01% of the error. Something persists over a play, accumulated luck or the outcomes
  themselves, but the data do not say which (`audit/news_kernel.py`; the same two optima with
  outcomes and news split by sign, `audit/sign_kernels.py`).
- **Chosen risk lowers happiness; loss-averse news is not identified.** The structural model
  (base utility pinned by safe choices, linear in money; news by mixed trials) gives
  `λ = 1.42` [1.37, 1.50], `n = 0.52`, base loss aversion 1.20 [1.18, 1.23] and `a = −0.30`. But splitting
  news by sign is `½(β₊+β₋)·RPE + ½(β₊−β₋)·|RPE|`, and in a 50/50 gamble `|RPE|` is half the
  gamble's range, known at choice: asymmetric news and a felt cost of the chosen gamble's
  spread are the same regressor. Adding one constant cost of having gambled (−0.024 SD) takes
  `λ` to 1.04 [0.95, 1.13] and fits slightly better. `a = −0.30` mostly reflects linear base
  utility extrapolated from safe amounts (30–55) to gamble outcomes (±150): with power utility
  `ρ = 0.8`, `a = −0.15` and `λ = 1.36`, or 1.13 with the gamble cost (`audit/risk_cost.py`);
  with a kernel per term, 1.17 with the gamble cost (`audit/sign_kernels.py`). Under linear
  base utility, gamble outcomes feel worse than their EV implies, as diminishing sensitivity
  predicts. Base loss aversion stays at 1.20 under the gamble cost and under curvature, but
  its kink sits at zero points, about where the pre-trial forecast stands, so it reads
  equally as loss-averse news on seeing the offer.
- **A loss's echo starts stronger and fades faster.** With base utility's kernel split by
  sign, starting from the best shared fit: a trial's loss moves the current rating 1.28
  [1.25, 1.31] times an equal gain; its echo is 1.13 times a gain's one trial on, 1.03 at ten
  and 0.94 at twenty, crossing one near thirteen, with per-trial decay 0.942 [0.937, 0.944]
  against 0.952 [0.949, 0.954]. The echo masses over a play are alike (1.02 [0.99, 1.05]; the
  whole effect 1.05 [1.03, 1.09]). Held-out error falls 0.012%. Read as memory, it is the
  fading affect bias at trial scale (`audit/sign_kernels.py`; intervals from 16 resamples that
  refit only the two split kernels, so too narrow).

Forbes & Bennett 2024 (`forbes_report.txt`, `audit/`):
- **The same front-loading.** Jump kernel `γ = 0.885, k₁ = 0.516` (experiment 1) and
  `γ = 0.883, k₁ = 0.457` (experiment 2), against single geometrics of 0.80 and 0.76;
  cross-validated error over people 1.0% and 1.6% lower. A power law (`ρ` 0.69, 0.76) does
  better, 2.5% and 2.8%. Fitted person by person (56 ratings each), `k₁` is below `γ` for 57%
  and 62% of people (31% and 39% in the pooling null) and above for 18% and 17%. A true
  kernel with `k₁ > γ` lies outside the nonnegative geometric recursive family; estimates from
  56 ratings are noisy, so some fits land there by chance.
- **Bad surprises register more, and only on one's own choices.** Every payoff is a lottery's,
  so RPE weights are news net of anticipation. Positive RPE adds nothing beyond the outcome
  (−0.002), negative RPE lowers affect (0.05 and 0.09 per 100 points), as Forbes & Bennett
  report. Probabilities vary here (0.25, 0.5, 0.75), which separates spread from `|RPE|`: with
  the chosen lottery's SD as a regressor the asymmetry vanishes in experiment 1 (RPE+ 0.028,
  RPE− 0.025; SD −0.052 [−0.097, −0.019]) and shrinks in experiment 2 (the `|RPE|` term −0.026
  [−0.069, 0.013]). In experiment 1 RPE registers on free choices and not on forced ones. A
  better unchosen outcome lowers affect slightly (regret), a worse one raises it (relief).
  Base utility by sign gives 1.16 and 1.14, and 0.95 and 1.00 with the SD.

News about later trials, Blain & Rutledge 2020 (`blain_report.txt`):
- **The design.** Here an outcome is news about later trials: it moves the belief about which
  car wins, and with it the value of every remaining trial.
  - A delta-rule learner fitted to choices, one learning rate, inverse temperature (capped at
    50, as in the paper) and probability weight per environment, reproduces the paper's
    learning rates: 0.160 and 0.446, against 0.16 and 0.47.
  - Each trial's own channels: the reward magnitude (EVm anticipated at choice, RPEm on
    arrival) and winning itself (the believed win probability P, and PPE = win − P).
  - News about later trials, dF = w_EVm dV + w_P dW:
    - dV, dW are the innovations in a later trial's expected reward and win probability under
      the participant's own choice rule. That is the value after the outcome minus its forecast
      before it, which already averages over the outcome.
    - The weights convert them into a proxy for the revision of a later trial's expected
      own-trial input.
  - In these proxies dF shares PPE's sign on 98% of trials when the chosen car was believed
    better and 1% when it was believed worse. There a win generally worsens the forecast of
    later trials (the race gets less predictable) and a loss improves it.
- **Expected-win and PPE regressors improve prediction; the tested future-value proxies add no
  reliable gain.**
  - The trial's own channels cut held-out error 14% against Blain & Rutledge's PPE-only model
    (that model is +16.7% [+12.2, +20.9] worse).
  - Post-outcome ratings rise with the filtered pre-outcome win probability (0.81 z per unit).
  - Adding dV and dW free: −0.03% [−0.36, +0.28]. Adding dF with one free strength: −0.01%
    [−0.26, +0.25]. That strength is 0.41 on the full sample, median 0.40 [−0.15, +0.93].
  - dF, its sign split and the injection below are rebuilt from each training fold's or
    resample's own arrival fit.
- **The sign test.** Felt news about later trials would raise PPE's weight where dF shares its
  sign over where it opposes it, by 0.149 per unit of strength (injecting dF into the same
  design; median 0.150 [0.122, 0.178]).
  - The observed gap is −0.022 [−0.147, +0.101]. Over the slope, resample by resample, the
    implied strength is −0.14 [−0.97, +0.66].
  - These are percentile ranges under a surrogate model; their coverage as a bound on the
    strength is not established.
- **In the canonical model's terms.** News on arrival in the win channel: r = w_PPE / w_P = 1.30
  [1.14, 1.49].
  - Reading r as `1/(1−κ)` assumes the memory-only interior model, with P's weight the expected
    win's base utility and no further anticipation at choice. On that reading the news loop
    gain is κ = 0.23 [0.12, 0.33].
  - The effective news kernel over base revisions is then (r − 1) ν^h (core, the reduced form;
    Codex).
  - A plug-in sensitivity fit puts news about later trials at that strength, applying the next
    trial's innovation to all remaining trials, with the kernel refitted at each ν. The best
    tested reach is ν = 0.6 per trial (about 9 s), and full-sample error rises at 0.8 and 0.9.
    Across 100 participant bootstraps the best grid value spans [0, 0.8].
  - This is not an upper bound on canonical news reach. Forecasts are not propagated by
    horizon, the interior reduction is used near a block's end, and the strength is plugged in.
  - The magnitude channel's ratio, w_RPEm / w_EVm = 0.74 [0.29, 1.41], is imprecise. Its
    difference from the win channel's is +0.57 [−0.23, +1.19], so one shared news strength is
    not rejected.
- **Caveats.** Beliefs come from a fitted learner. Intervals are from a bootstrap over 75
  participants, and likelihood-ratio sets are nominal. Codex's repairs not yet made are in
  `next-steps.md`.
  - Anticipation of later trials is not identified. The unrestricted level coefficients
    (Vnext, Wnext) take opposite signs, −4.3 and +1.0; learning trends and mood drift are
    possible confounds.

Step changes in luck, Keren et al. 2021 and Jangraw et al. 2023 (`steps_report.txt`):
- **The design.** Three unsignalled blocks of mostly good, then bad, then good luck: 27 trials
  each in Keren's version (78 people), 22 in Jangraw's. Mean prediction error per trial by
  block: +1.3, −1.0, +1.1 points (Keren); +2.0, −0.7, +2.0 (Jangraw).
  - Jangraw's two weekly cohorts are pooled: 316 sessions from 171 people, 145 of them in both
    weeks.
  - The model is the GBE one (CR, EV, RPE through one kernel) with a linear drift and a fixed
    effect per session. Folds and bootstraps are by person.
- **The tested adaptation terms bring no reliable predictive gain.**
  - Biphasic memory collapses to the jump kernel in both datasets. Its negative part takes
    zero reach (Keren) or the afterglow's own reach (Jangraw), so it has no lobe of its own.
    Held-out error against the jump kernel: +0.003% [−0.001, +0.007] (Keren) and +0.061%
    [−0.021, +0.154] (Jangraw).
  - A hyperbola minus a slow exponential does no better: +0.05% and +0.09% against the
    hyperbola.
  - Nor do running means of all earlier inputs as covariates: +0.62% [+0.26, +0.95] and +0.18%
    [+0.12, +0.24]. That is a reference from the whole history, in the spirit of Keren's primacy
    model but not that model.
  - The early-to-late residual contrasts within blocks show no consistent adaptation-shaped
    pattern. Mood climbs more than the kernel predicts through Keren's first good block (+0.20 z
    [+0.05, +0.33]), the opposite sign.
- **How far an adaptation tail sits from the fitted model.**
  - The method: inject, without noise, a tail that cancels a fraction `f` of the jump kernel's
    positive mass, with reach `1/(1−γ)` trials. Refit the whole jump model (kernel, weights,
    drift, fixed effects). D² is what it cannot absorb, over the residual variance.
  - Results by `f`. Cancelling it all within 10–20 trials leaves D² = 44–70 (Jangraw) and
    26–39 (Keren). Half leaves 5–12, a quarter 1–2.5. A 50-trial reach leaves 12 and 8 at
    `f = 1`.
  - D² is an uncalibrated distance, not the power of the cross-validated comparison.
  - So the injection analysis does not establish bounds on adaptation's strength or timescale.
    A recovery simulation through the actual pipeline would (`next-steps.md`).
- **RestAfterWins, after a winning streak ends.** 25 people, raw 0–1 ratings.
  - A closed-loop winning block, whose prediction errors grow to keep mood rising, then 30
    ratings at rest 15 s apart. Mood is 0.73 before the block and 0.77 at its end.
  - At rest it falls to 0.29 [0.14, 0.45] below the pre-task rating (ratings 21–30), and below
    it for 68% of people at the last.
  - The rest period that opens the weekly cohorts, with no outcomes yet, drifts −0.010 per
    minute. The RestAfterWins files log no durations; at the weekly cohorts' timing, ratings
    21–30 come about 17 minutes after the pre-task rating.
  - Illustrative subtraction: if that slope held throughout the gambling and the rest, drift
    alone gives −0.17, leaving −0.12 [−0.28, +0.04]. So this is no evidence of a fall beyond
    drift.
  - If there were one, two readings would compete: an adaptation lobe, or the canonical model's
    news. An unexpectedly early ending would be bad news about future wins; a foreseen one
    would only end anticipation. Participants' expectations about stopping were not measured.

## Audit

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
- `risk_cost.py`: the structural model with a cost of having gambled and power utility;
  news and base loss aversion.
- `news_kernel.py`: per-component kernels with base utility separated from news, from two
  starts, and which optimum wins across participant resamples.
- `sign_kernels.py`: base utility's kernel split by sign, nested in the best shared fit
  (each from two starts, with and without a cost of having gambled), and a bootstrap of the
  loss-to-gain ratios by lag.
- `confounds.py`: the lag-1 weight by trial type and latency, and the rating boundary.
- `felt_clock.py`: trials against seconds (raw, and against the play's own pace) on the jump
  and the hyperbola; kernels by age band against a felt clock `∝ age^−q`; a recovery check on
  ratings simulated from a pure Lemlich clock; the two-timescale counterexample. Stages
  `pooled`, `age`, `within`, `null`, `mixture` (needs `extract_timing.py`; about 25 minutes in
  all on 12 cores).
- `forbes_shapes_risk.py`, `forbes_pooling_null.py`: kernel shapes, the lottery-SD
  separation, and the pooling null on Forbes & Bennett.
- `biphasic.py`: afterglow-minus-adaptation kernels within a play (the audit
  split) and within a Forbes & Bennett block (5-fold CV), against the jump kernel and the
  hyperbola.
- `impulse_detectability.py`: the largest adaptation lobe a play-length pulse can
  leave at each gap, over all time constants; why `carryover.py` cannot see slow adaptation.
- `divisive.py`: sensitivity to outcomes against recent offered stakes (range
  adaptation), with a level term, in both datasets.
- `carryover.py`: a play's luck against the change in the next play's pre-trial
  rating, by the gap between plays (day number and time of day from the archive), and the
  same between Forbes & Bennett blocks.
