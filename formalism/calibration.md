# Calibration

Tags as in `core.md`; proposition ids refer to `core.md` (P, N) and `decision.md` (D). The post
uses this in its model and data sections (`outline.md`, §2 and §9).


What pins the coefficients, as far as known. Choice-revealed and felt quantities differ, and
the hedonic reading needs the felt ones.
- Constraints, not values: `M < 1`; `λκ < 1`.
- **Defaults per horizon.** Set from echo masses (`A = aα/(1−α)`, `B = mμ/(1−μ)`) and
  reaches, using the anchors below. [synthesis; derived quantities checked]

  | horizon (period) | `a` | `α` | `m` | `μ` | `n` | `ν` | `λ` | `M` | `λκ` |
  |---|---|---|---|---|---|---|---|---|---|
  | waking day (an hour) | 0.05 | 0.8 | 0.1 | 0.5 | 0.2 | 0.8 | 1.5 | 0.30 | 0.32 |
  | life (a week) | 0.064 | 0.7 | 0.4 | 0.3 | 0.2 | 0.7 | 1.5 | 0.32 | 0.34 |

  - Day: `A = 0.2`, `B = 0.1`; anticipation reaches about five hours, memory two. Life:
    `A = 0.15`, `B = 0.17`; a week's afterglow is short (mostly gone in a week), anticipation
    reaches a few weeks.
  - These are illustrative scenarios: the anchors pin orders of magnitude, not masses (see
    anticipation below).
  - What follows: echo is about 30% of steady-state experience. Recursion stretches reach
    by 21–28% (5.0 → 6.4 hours ahead, +28%; 3.3 → 4.0 weeks, +21%). Life weights dip by
    about a sixth at birth and death (1.22 and 1.21 against an interior 1.47, P5). Felt news is well
    inside its local threshold, which allows `λ` up to 4.64 (day) and 4.42 (life).
  - The momentary self's felt row is strongly present-weighted: `β_L ≈ 0.055` (day) and
    `0.076` (life) on P4's bilateral row, `0.051` and `0.068` on the causal half-line row
    (P9), against choice-revealed `β ≈ 0.7`–`0.97`. The row is what a momentary hedonist
    would choose by; a life-sum maximizer is patient whatever it is (flat interior weights,
    P5). So the claim is conditional: patience from the felt row alone needs an echo share
    near 0.94 (the bill below), against the illustrative scenarios' 0.3, so patient choices
    more plausibly run on something other than felt echo (life-sum or evaluative weights). The robust input is
    only that felt anticipation mass is well below one: the felt row's total weight on the
    whole future is then about `A/(1−A)` of the present (one-sided), however that mass is
    spread. `β_L` itself depends on the spread (one-step anticipation has `β_L = 1` and a
    tiny `δ`). [synthesis; checked]
  - An LLM context window has a measured shape of memory access (not of a felt kernel) and
    unanchored strengths (`selves.md`, Horizons).
    Nothing anchors a session.
- **Present bias and patience invert to primitives** (one-sided P3): `a = β_L/(1−β_L)`,
  `α = δ_lr (1−β_L)`, with `δ_lr` the long-run per-period discount factor. [known:
  Sáez-Martí & Weibull 2002 WP §4.4, eqs. 15–17; checked]
  - Hence `M = β_L δ_lr / (1 − δ_lr + β_L δ_lr)`, and with `δ_lr = 1/(1+ρ)` the base-utility
    share is exactly `1 − M = ρ/(ρ + β_L)`. [checked]
  - The bill, conditional on explaining choice weights through felt echoes: `M` lies below
    `δ_lr` and rises to it as `β_L → 1`, so it is set by patience, not by present bias.
    Long-run patience from felt echo alone would make nearly all experience echo
    (`β_L = 0.7`, annual 4%: `M = 0.94`; daily periods: `M = 0.9998`; two-sided with modest
    memory, `m = 0.2, μ = 0.5`: `M = 0.965`). Identifying a choice-revealed discount curve with the momentary
    self's felt row is itself a behavioral assumption. [Codex]
  - Experience sampling bounds the positive echo's contrast, not its share: pleasant
    mind-wandering, mostly about past and future, leaves momentary happiness where on-task
    focus has it, while unpleasant mind-wandering costs a lot (`b = −0.5`, n.s., against
    `−23.9` on a 0–100 scale; Killingsworth & Gilbert 2010). [synthesis]
  - Measured present bias: `β_QH ≈ 0.97` for money in convex time budgets (Imai, Rutter &
    Camerer 2021), `0.82`–`0.87` for money across methods and `0.66` for non-monetary goods
    (Cheung, Tymula & Wang 2021), `0.88`–`0.90` for effort (Augenblick, Niederle & Sprenger
    2015), `0.52` with "now" in minutes (McClure et al., via Ericson & Laibson 2019). It
    depends on how long "now" is.
- **Loss aversion λ.** Choice-revealed: `1.96` (`1.74` bias-corrected; Brown et al. 2024
  meta-analysis). Structural news utility, annual periods: `λ ≈ 2.3`–`3.0` with
  `η ≈ 0.87`–`1.1` and prospective weight `γ ≈ 0.59`–`0.87` (Pagel 2017, Table 1; 2018,
  Table 1); a lab kink `η(λ−1) ≈ 1.7` (Gill & Prowse 2012). Felt: smaller. Losses are not
  experienced as worse than equal gains, a forecasting error (Kermer et al. 2006);
  disappointment exceeds elation 1.4–1.9 times (Mellers et al. 1997); surprise asymmetry
  1.0–1.45 (Shepperd & McNulty 2002); only downside surprise registers in Forbes & Bennett
  (2024). In 50/50 gambles, asymmetric news is the same regressor as a felt cost of the
  chosen gamble's spread (`|RPE|` is half its range), so the Great Brain Experiment's
  `λ = 1.42` falls to 1.04 [0.95, 1.13] once a cost of having gambled is allowed; where
  probabilities vary (Forbes & Bennett) the lottery's spread absorbs the asymmetry in one
  experiment and shrinks it in the other. Chosen risk lowers momentary happiness; whether
  as loss-averse news is not identified there. [checked in `experiments/happiness/audit/`]
  Working range for felt `λ`: 1–2, from the studies above.
- **Surprise n**, relative to the outcome's own effect: `≈ 0.25` each way, measured right
  after the outcome (Shepperd & McNulty); `0.1`–`0.15`, downside only (Forbes & Bennett).
  Working range for events: `0.1`–`0.3`.
  - In lab models of momentary happiness (trials of about 10 s), prediction errors move
    happiness about as much as certain rewards (weight ratio 1.1–1.3), and a chosen
    gamble's expected value 0.3–0.65 times as much (Rutledge et al. 2014, read from Fig. 2;
    Vanhasbroeck et al. 2021). Splitting the expected value by timing puts most of an
    expected reward's effect at choice, not at outcome (Rutledge, model D).
  - Those weights are on outcomes, news over `u`. Felt news over `e` at that size would be
    past the threshold. [speculation]
- **The threshold in full:** `λκ = λn (1−νμ) / (H (1−νq))`. The memory multiplier
  `(1−νμ)/(H(1−νq))` is near 1 when memory is weak (1.13 at the life defaults) and grows with
  strong, long memory: `m = 0.5, μ = 0.6, ν = 0.9` gives `λκ = 1.45` at `nλ = 0.6` without
  anticipation, and 1.90 with the life default's (`a = 0.064, α = 0.7`). [Codex;
  checked] Felt values sit well inside it; choice-calibrated news utility (`η = 1`,
  `λ = 2.5`) would not.
- **Anticipation against memory.** Thought runs forward about three times as often as back
  (any-future 30% against any-past 9% of thoughts, Baumeister et al. 2020; mind-wandering
  future:past ≈ 1.9, Song & Wang 2012), so `A > B` in attention.
  - Anticipating an experiential purchase lifts momentary happiness by `+1.2` to `+2.4` on
    0–100 (Kumar, Killingsworth & Gilovich 2014), against within-person effects of `+8` to
    `+14` for doing such things (Bryson & MacKerron 2013, Table 2): a ratio of 0.13–0.26
    while thinking about it. That is a lag-specific weight (`aα^h` at lead `h`), not the
    mass `A`; lead time, duration and attention all enter the mapping. [the ratio is
    synthesis, across studies; Codex on the mapping]
  - Vacation anticipation is not identified: Nawijn et al.'s (2010) pre-trip gap shows no
    ramp across waves and matches the post-trip gap, which points to selection.
  - Valuation of future over past events, `×1.2`–`2.0` (Caruso, Gilbert & Wilson 2008), has a
    failed replication of its first study.
- **Reach scales with the event.**
  - Memory: of a ski holiday's mood gain, 13% remains a week later and none after two (de
    Bloom et al. 2010, Table 2); exhaustion and engagement, which behave like recovery stocks,
    keep about a third at two weeks (Kühnel & Sonnentag 2011). A small lab reward's
    afterglow lasts seconds (forgetting factor 0.6–0.85 per ~10 s trial; Rutledge et al. 2014;
    Vanhasbroeck et al.; Blain & Rutledge 2020).
  - In momentary-happiness data (the Great Brain Experiment, 47,067 people, 1.1M ratings;
    Forbes & Bennett's two experiments), echoes of task outcomes are front-loaded with a
    slow tail: a jump kernel (lag 0, then `γ ≈ 0.88` per trial) beats Rutledge's single
    geometric (`γ = 0.68`) on held-out people, and a one-parameter power law beats both, in
    all three datasets (exponents 0.69–0.81). The recursive reading is one two-parameter fit
    to the front-loading; the direct model's geometric memory is the same family (P2), and a
    transient plus a mood level, or pooling people with different geometrics, produce it too.
    Seconds count within a play (about 1% of an echo per second of delay against a player's
    own pace) and not between players, and gambles and ratings in between move the weights.
    With age the lag-1 echo shrinks and the tail lengthens. A hyperbolic kernel on a felt clock
    `∝ age^−q` (Janet, Lemlich) cannot do that; a fast transient plus a slow mood on the same
    clock can, so one felt clock from seconds to years is not yet tested. [checked in
    `experiments/happiness/` and its `audit/`]
  - The reading-invariant quantity is the echo share, `k₁/(1−γ+k₁)` on the jump fit
    `(1, k₁, k₁γ, k₁γ², …)` (`k₁` the lag-1 weight; `kappa` in the code): 0.78,
    0.82 and 0.80 (per person, Forbes & Bennett, median 0.85). It is the memory mass only on
    the recursive reading (3.5 on the direct one). With power-law exponents below one it does
    not settle (Great Brain Experiment exponent): 0.81 over 30 trials, 0.87 over 100, 0.93
    over 1000. So the data put trial-scale
    memory at P1(d)'s heavy-tail edge, which the model must cut off at longer scales (reach
    scaling) or treat as a superposition of exponentials across scales. [checked; the
    reading speculation]
  - Prediction errors do not echo like outcomes once the outcome's base utility is moved to
    its own regressor: news alone persists through the play (`γ` at the bound), a level of
    accumulated luck. [checked in `audit/`]
  - No fast adaptation at task scales. Kernels allowed a slow negative tail stay positive
    within a play and within a Forbes & Bennett block, and between plays a play's luck
    lifts the next play's starting rating by 45% of its end-of-play effect after 4
    minutes, 10% after 10 hours, 6% after 2.4 days and none after a month: a positive,
    heavy-tailed afterglow in wall-clock time (power law, exponent about 0.3). Impulse tests
    are blind to slow adaptation: a pulse of length `δ` leaves at most about `(δ/g)/e` of
    itself as a lobe at gap `g`, so slow adaptation shows only in responses to sustained
    changes. [checked in `audit/`]
  - The front-loading echoes P3's quasi-hyperbolic shape on the memory side (`k₁/γ` 0.46–0.58
    per trial, near the minutes-scale `β_QH ≈ 0.52` above), though a hyperbola fits better
    than the quasi-hyperbolic jump. Both depend on how long a period is. [speculation, the
    comparison]
  - Ceilings from emotional inertia, which also contains slowly moving base utility: affect
    autocorrelation 0.2–0.3 between beeps about 1.6 h apart (Kuppens, Allen & Sheeber 2010,
    Table 1); 0.61 at one hour for valence in a continuous-time fit (Vansteelandt & Verbeke
    2016); 0.34 day to day for negative affect (Brose et al. 2015).
  - Anticipation: days for a small pleasure (Loewenstein 1987: willingness to pay for a kiss
    peaks around three days out), weeks for a vacation.
- **The week as a natural experiment.** The weekend is a predictable high. Friday's lift in
  positive emotions is about half the weekend's (0.2–0.55 by item), and it contains Friday
  evening, so it bounds one-day anticipation from above. Monday is no worse than Tuesday to
  Thursday, Sunday shows no dip, and the day before a midweek holiday shows no lift
  (Helliwell & Wang 2011 WP, Gallup, N ≈ 527,000). Daily felt echo of a weekend is small
  both ways. [synthesis]
- **Sign asymmetry is the empirical default.** Positive echoes add little and negative
  echoes cost a lot (Killingsworth & Gilbert; anticipatory emotion averages `+0.35` on
  `−3..+3` with 38% fear or anxiety, Barsics et al. 2016). Dread outweighs savoring, which is
  what makes D5's dread-of-dread bite in the recursive model.
- Identification (P10; Eliaz & Spiegler's ordinality) means choices alone cannot pin the
  hedonic coefficients. Experience sampling around scheduled events can.
