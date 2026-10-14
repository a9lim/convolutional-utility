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
- **Forbes & Bennett 2024** (OSF `m7dtw`): two experiments, 150 participants each, 212 trials
  and 56 affect ratings per person; CSVs in `data/forbes/exp1`, `data/forbes/exp2`. Not yet
  fitted.
- `data/` is gitignored; the downloads are data only (the GBE archive's MATLAB script is not run).

## Code

- `gbe.py`: flattens the MATLAB structs to per-play arrays (`data/gbe/tidy.npz`), Rutledge's
  regressors (certain reward CR, a chosen gamble's expected value EV and prediction error
  RPE), the kernels, and the fit: least squares with a fixed effect per play, ratings
  z-scored within participant.
- `run_gbe.py`: the model comparison on held-out participants, a bootstrap over participants,
  and per-component kernels; writes `gbe_report.txt` and `gbe.png`.

Run from the repo root: `python experiments/happiness/run_gbe.py`.

## The models

A trial's felt contribution is `CR`, or for a gamble its outcome `EV + RPE`, plus the
gamble's anticipated `EV` and its felt news on `RPE`. A rating reads the current felt
state, that contribution plus echoes of earlier ones through a kernel `k(lag)`.

- Rutledge et al.: `k = γ^lag`, one geometric.
- Recursive memory over felt states, `e_t = f_t + m Σ_j μ^j e_{t−j}`, has resolvent kernel
  `(1, κ, κγ, κγ², …)` with `κ = mμ` and `γ = μ(1 + m)`: a jump at lag 0, then a slower
  geometric, `κ < γ`. Rutledge's kernel is the case `κ = γ`.

## Results so far

- **Replication.** Rutledge's model gives `γ = 0.72` per trial (their lab sample: 0.61 ± 0.30
  SD).
- **The recursive kernel fits better.** A jump at lag 0, then `γ = 0.90`: `κ = 0.450` [0.445,
  0.456], `γ = 0.899` [0.895, 0.905] (95% bootstrap over participants). Held-out error falls
  1.07% against Rutledge's kernel, eight times what splitting prediction errors by sign
  buys (0.14%). Read recursively: `μ = γ − κ = 0.45` per trial, `m = κ/μ = 1.00` [0.97, 1.04].
  A transient-plus-mood model has the same shape, so the kernel is consistent with the
  recursion rather than proof of it.
- **News echoes like everything else.** Fitted separately, the kernels of certain rewards,
  expected values and prediction errors nearly coincide (`γ` 0.88, 0.87, 0.90; `κ` 0.51, 0.55,
  0.43), and buy only 0.06% more. A felt state that is remembered whole predicts this; a
  model in which surprise is only transient does not.
- **Weights.** EV moves happiness 0.70 times as much as a certain reward; prediction errors
  about 1.5 times. Negative prediction errors weigh 1.26 times positive ones [1.24, 1.27],
  pooled. That ratio is not clean evidence of loss-averse news: within gain-only and
  loss-only trials a gamble's EV equals the size of its RPE, so the sign split is identified
  only across trial types, where it is confounded with how gains and losses are felt in
  themselves. Mixed trials, where EV and RPE vary independently, are the clean test; not
  yet done.
