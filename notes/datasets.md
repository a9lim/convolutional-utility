# Data for the constants

**Status: scouting (2026-10-18), nothing fitted yet.** Candidate data for the canonical
model's constants (`a, α, m, μ, n, ν`) and biphasic memory (`c γ^j`) beyond the trial-scale
fits in `experiments/happiness/`. Four scouting agents searched; Claude checked that the top
open sources resolve and that the LLM bans below are real. Item wording comes from the
repositories' codebooks, and designs mostly from the papers. As fits land, distill them into
the experiment READMEs and `formalism/calibration.md`.

## What the task fits leave open

- Anticipation at every scale. The Great Brain Experiment's trials are independent, so
  nothing in a play is known in advance beyond the chosen gamble's EV.
- News about later moments (`ν > 0`). Every revision in those tasks is about the current
  trial.
- Memory beyond minutes, and adaptation at any scale. No step changes within a play, and
  impulse tests are blind to slow adaptation (`adaptation.md`).

## Identification

- Field data give the effective kernel, not the primitives. The recursive reading has content
  at information boundaries (core, surprises). An announcement with a known lead time, such
  as a morning announcement of an afternoon stressor or a grade release, shows the jolt on
  hearing and the ramp after it, which is where recursive and direct shapes could part.
  *speculation, untested*
- Reach scales with the event, so fit per horizon (seconds, hours, days, months), as
  `calibration.md` does. One kernel across scales is the felt-clock question.
- The cleanest minute-scale anticipation design is a dread (a stressor). The core is
  sign-symmetric, and X1 ranks dread over savoring, so a pleasant counterpart is needed too.
- Recall items are memory readouts: PHQ-4/9 (two weeks), SPANE (four weeks), next-day
  episode ratings (ATUS, DRM). Model the measurement as a window over `e`, not as `e_t`.

## Anticipation (`a, α`)

- **EMOTE #20, Trier stress day** (Koval & Kuppens 2012, *Emotion* 12: 256). Format: N = 73,
  about 60 beeps a day (about 12 minutes apart), 2 days.
  - On day 2, participants are told in the morning that a stress test comes later;
    `es_TSST` marks it.
  - Fits a dread ramp at minute resolution, then the post-stressor decay.
  - Access: request-only (EMOTE, below).
- **EMOTE #17** (Kuppens, Oravecz & Tuerlinckx 2010, *JPSP* 99: 1042; N = 80, 10 a day,
  14 days) and **#5** (Provenzano et al. 2021; N = 36, 10 a day, 7 days).
  - Both carry `FUTUREXP`, "Think about what will happen in the next hour: how pleasant do
    you expect this to be?", an explicit forecast at every beep.
    - Its effect on current affect, net of lagged affect and the current situation, is
      lead-1h anticipation.
    - The next beep's situation minus this forecast is news.
  - #5 also has "did something positive/negative happen since the last beep".
  - Caveat: the forecast is of the situation's pleasantness, and mood colours it.
- **EMOTE #2, exam results** (Kalokerinos, Erbas, Ceulemans & Kuppens 2019, *Psych. Sci.*
  30: 863). Format: N = 101, 10 a day, 2 days before and 7 days after grade release.
  - `exam_beepnum = 0` marks the beep at which grades arrive.
  - Gives a pre-release ramp, the jump, and the decay.
  - The scout saw no actual or expected grade in the variable list.
- **Dolton & MacKerron 2018** (NIESR DP 493, preliminary; Mappiness, about 3M pings, fans
  around football matches).
  - The microdata are restricted, but the published tables can be fitted as moments now:
    - Table 1: hourly coefficients before and after matches, by win, draw and loss.
    - Table 3: bookmaker odds; build-up is about 1.8 points higher when favoured, and an
      expected win that is lost hurts more.
  - The pre-match hours mix anticipation with travel and the pub.
  - Check the published version (the text and Table 1 disagree on which hour is +1.5).
- **Time-use diaries, hour-scale leads and lags of activities.**
  - ATUS Well-Being Module (BLS 2010, 2012, 2013, 2021; open CSVs): affect for 3 episodes a
    day plus the full timed diary.
  - UK Time Use Survey 2014–15 (UK Data Service SN 8128; registration): enjoyment for every
    10-minute slot.
  - Both are rated next day or in hindsight, and people schedule good activities next to
    each other; weak for `a`.
  - ATUS: before 25 March 2013, a bug usually excluded the last eligible episode of the day
    from sampling (BLS notice; use the adjusted weights).
- No public lab data rates affect during a wait. The nearest: Jangraw et al.'s
  announced-duration cohorts (below), whose mood drifts the same whether the wait is
  announced at 7 or 12 minutes. That is weak evidence for a small `α` at the end of a wait.

## News about later (`n, ν`)

- **Blain & Rutledge 2020** (*eLife* 9: e57977; GitHub `BastienBlain/MSWB_LearningNotReward`,
  `PublicCode/Blain_MoodTracksLearning_data.mat`, 0.8 MB, no license).
  - 75 people × 160 trials: 80 stable, 80 volatile (reversals every 20); magnitudes vary
    independently of probability; 46 ratings each; true probabilities in the file.
  - An outcome revises the win probability of every later trial. Their finding, that
    happiness tracks probability prediction errors, is the `ν > 0` signature.
  - Needs our own learner for the belief, as in the LLM readout fit.
- **Lloyd et al. 2026** (bioRxiv, zero prediction errors; Figshare project 276021, CC BY;
  GitHub `bethlloyd/Zero_prediction_errors`).
  - Gaussian rewards; online n = 97 (3 × 80 trials), EEG n = 40; happiness every 3 trials.
  - Trials that force outcome = prediction (about 19%) separate belief revision from the
    current prediction error. A preprint.
- Day scale:
  - **EMOTE #70 AURA** (Moeck et al. 2023, *Emotion* 23: 2219; N = 209, 9 a day,
    7 days): end-of-day forecasts of tomorrow against next-day retrospectives.
  - **EMOTE #27** (Dejonckheere et al. 2019; N = 104, 7 a day, 14 days): "how unexpected
    was this event".
- On request:
  - Villano, Otto, Ezie, Gillis & Heller 2020 (*JEP: General* 149: 1755): expected grade
    within 30 minutes of the exam, then 45-minute sampling for 8 hours after the grade.
    The paper itself reports per-step decay 0.94 for positive affect and 0.96 for negative
    (half-lives about 6 and 8 hours), already usable as an hour-scale anchor.
  - ESCAPE (Neubauer, Smyth & Sliwinski 2018): "will anything stressful happen in the next
    few hours", then "did it". This is the ideal forecast-then-outcome item, with no
    public data.

## Memory at hours to days (`m, μ`)

- **openESM 0010** (Bringmann et al. 2013, *PLoS ONE* 8: e60188; CC BY-NC). Format:
  N ≈ 130, 10 a day.
  - Pleasantness of "the most important event between the current and previous response",
    with momentary affect. A distributed lag at 90-minute spacing sees 1–2 lags.
- **EMOTE event-since-last-beep family** (#16, #22, #23, #27, #80, #81; about 800 people
  pooled). Event reports share method variance with mood.
- **openESM 0073** (Sicorello 2024; N = 227, 6 a day, 10 days): best and worst event since
  the last survey.

## Adaptation (`c, γ`): steps

- **Within a task, minutes.** Steps were missing from the Great Brain Experiment; these have
  them.
  - **Keren et al. 2021** (*eLife*; OSF `vw7sz`). The "structured" task has three
    unsignalled 27-trial blocks with mean prediction error +5, −5, +5 (n ≈ 80–89) and a
    rating every 2–3 trials.
    - Their primacy model, where the expectation is the mean of all past outcomes, is the
      non-fading reference: the `γ → 1` edge of the adaptation lobe.
    - Use the open-loop structured cohort; the adaptive one sets outcomes from mood.
  - **Jangraw et al. 2023** (*Nat. Hum. Behav.* 7: 596; OSF `km69z`, 206 MB, NIMH public
    domain; code `djangraw/MoodDrift`).
    - Open-loop +/−/+ gambling blocks: Weekly-Rest-02 and 03, n = 164 and 160.
    - RestAfterWins: gambling, then 30 ratings at 15-second spacing at rest; the afterglow's
      decay without new outcomes.
    - Mood drifts down at rest. Fit the drift with the kernel, or it reads as adaptation.
  - **Carrillo et al. 2026** (*PLOS Comput. Biol.*; GitHub `MBB-team/AssessingCompPhenMood`).
    - A mood rating after every one of 75 trials. One task, the "Riven" puzzle, gives
      every participant the same fixed feedback sequence.
    - Each task is run twice, two weeks apart, which gives kernel reliability.
    - Each trial ends with an effort, delay or risk choice.
- **Weeks to years.**
  - **Dartmouth College Experience Study** (openESM 0040; in `data/dartmouth/`, md5
    checked). Format: 218 people, 35,186 affect ratings, Sept 2017 – July 2022, weekly.
    - The `affect` column is the PAM picture index (1–16), not valence. The grid row
      `(index − 1) // 4` tracks `feel_good` and `stressed` (r ≈ ±0.12) and the column
      tracks nothing. Confirm the rubric (Pollak et al. 2011) before the step test.
    - `depressed` (PHQ-4, two-week recall) rises from April 2020.
    - Design: `adaptation.md`, step data.
  - **OpenResearch Unconditional Cash Study** (data.openresearchlab.org; request form and
    signed agreement, personal email accepted, no fee).
    - $1,000 against $50 a month for 36 months, randomized, N = 3,000.
    - SPANE at baseline and months 1, 2, 11, 17, 23, 29 and 35; PHQ-9 and life
      satisfaction on other waves.
    - A randomized sustained step with a known end; afterglow then the decay of the
      treatment gap. No announcement lead.
    - The scout reports that the agreement bans "public or consumer AI" and permits API or
      enterprise use without training. Unverified; read it before any agent touches the
      data.
  - **Understanding Society COVID-19 study** (UK Data Service SN 8644, with SN 6614;
    registration, with a route for non-UK-academic users).
    - About 42,000 adults, monthly from April 2020, linked to 2019 interviews: the lockdown
      as a dated step with a baseline.
    - GHQ-12 is symptom-based.
    - The UKDS terms on AI tools are unverified.

## EMOTE and openESM

- **EMOTE** (emotedatabase.com; Kalokerinos, Koval, Kuppens et al. 2026, PsyArXiv `h7kxd`).
  - 39 datasets, mostly Leuven and Melbourne. Free: ORCID login, a request form, about
    three weeks, vetted by the data owners.
  - No reposting; the request page has no AI clause.
  - a9 submits. One request can cover #2, #5, #17, #20, #27, #70 and the event family.
- **openESM** (openesmdata.org; Siepe et al. 2026, *Behav. Res. Methods* 58(8);
  `openesm-project/openesm`).
  - 63 datasets with per-dataset licenses; R and Python packages.
  - Harmonized ids and metadata, not harmonized items. Only about 6 have event or
    expectation items.

## Out for this workflow

- **SOEP** (including SOEP-IS's day reconstruction module) and **HRS**: both data-use
  policies say LLMs and other AI tools may not be used to manage, process or analyze the
  data (checked 2026-10-18). SOEP also excludes unaffiliated users.
- **HILDA**: approved institutional researchers only.
- **GLOBEM** (PhysioNet): credentialed, and its guidance prefers local models.
- **Mappiness, Villano and Heller, Sweeny's waiting studies** (bar exam, biopsy), **ESCAPE**:
  request from the authors (a9's emails).
- **Choice only** (no affect ratings): Iigaya et al. 2016, 2020; Story et al. 2013.

## Order

1. Open now, in-task: Blain & Rutledge for `n, ν`; Keren and Jangraw open-loop steps for a
   minutes-scale `c, γ`, alongside the Great Brain Experiment's audit.
2. Moments now: Dolton & MacKerron's hourly tables (`a`, with odds for `n`); Villano's decay.
3. EMOTE request (a9): the Trier day and `FUTUREXP` for `a, α`; exam release for all three.
4. Dartmouth step test, after the PAM rubric.
5. OpenResearch and Understanding Society once their AI terms are read.
