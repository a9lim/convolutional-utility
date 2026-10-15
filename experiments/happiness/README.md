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
  `(1, κ, κγ, κγ², …)` with `κ = mμ` and `γ = μ(1 + m)`: a jump at lag 0, then a slower
  geometric, `κ < γ`. Rutledge's kernel is the case `κ = γ`.

## Results so far

Great Brain Experiment (`gbe_report.txt`, `gbe.png`):
- **Replication.** Rutledge's model gives `γ = 0.68` per trial (their lab sample: 0.61 ± 0.30
  SD).
- **The recursive kernel fits better.** A jump at lag 0, then `γ = 0.89`: `κ = 0.412` [0.408,
  0.418], `γ = 0.890` [0.886, 0.896] (95% bootstrap over participants). Held-out error falls
  1.3% against Rutledge's kernel, six times what splitting prediction errors by sign buys
  (0.23%). Read recursively: `μ = γ − κ = 0.48` per trial, `m = κ/μ = 0.86` [0.84, 0.89].
  A transient-plus-mood model has the same shape, so the kernel is consistent with the
  recursion rather than proof of it.
- **News echoes like everything else.** Fitted separately, the kernels of certain rewards,
  expected values and prediction errors nearly coincide (`γ` 0.88, 0.87, 0.89; `κ` 0.48, 0.51,
  0.40), and buy only 0.06% more. A felt state that is remembered whole predicts this; a
  model in which surprise is only transient does not.
- **Loss-averse news, identified.** With base utility pinned by safe choices (the same for
  certain and risky payoffs) and news identified by mixed trials: `λ = 1.42` [1.37, 1.50],
  news `n = 0.52` [0.49, 0.56] per unit of base utility, base loss aversion 1.20 [1.17,
  1.22], and anticipation of a chosen gamble's EV negative, `a = −0.30` [−0.32, −0.29]:
  taking a gamble feels worse than its expected value, beyond what it pays. (Splitting RPE
  by sign within gain-only or loss-only trials is not identified: there a gamble's EV equals
  the size of its RPE.)

Forbes & Bennett 2024 (`forbes_report.txt`):
- **The same kernel in another task.** Jump kernel `γ = 0.885, κ = 0.516` (experiment 1) and
  `γ = 0.883, κ = 0.457` (experiment 2), against single geometrics of 0.80 and 0.76;
  cross-validated error over people 1.0% and 1.6% lower. Fitted person by person (56 ratings
  each), `κ` is below `γ` for 57% and 62% of people and above for 18% and 17%.
- **Only bad surprises register, and only on one's own choices.** Here every payoff is a
  lottery's, so RPE weights are news net of anticipation; their difference is news by sign.
  Positive RPE adds nothing beyond the outcome (−0.002), negative RPE lowers affect (0.05 and
  0.09 per 100 points; difference [0.00, 0.10] and [0.04, 0.15]), as Forbes & Bennett report.
  In experiment 1 RPE registers on free choices (0.05 positive, 0.08 negative) and not on
  forced ones. A better unchosen outcome lowers affect slightly (regret), a worse one raises
  it (relief).
