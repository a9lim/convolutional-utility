# Core model

Status tags: **[standard]** textbook math · **[known: …]** in the literature, cited ·
**[not found]** not located in the lit pass (see `bibliography.md`), so possibly new ·
**[checked]** `formalism/checks.py` verifies numerically · **[proved]** proof sketch here.

## The canonical model

Recursive echoes and recursive news: anticipation, memory and news are all about experienced
utility. In causal form, for each moment `t` of a life `[0, T)`:

```
e_t = u_t                                                          base
    + Σ_{j=1}^{T−1−t} a α^j  Ê_t[e_{t+j}]                           anticipation
    + Σ_{j=1}^{t}     m μ^j  e_{t−j}                                memory
    + Σ_{j=0}^{T−1−t} n ν^j  φ_λ( Ê_t[e_{t+j}] − Ê_{t−1}[e_{t+j}] )  news
```

- `Ê_t` is the self's forecast at `t`, with `Ê_t[e_t] = e_t`. `φ_λ(x) = x` for `x ≥ 0` and
  `λx` for `x < 0`. All three channels have geometric primitives; recursion reshapes them.
- **Forecasts are rational:** `Ê_t` is the Bayesian expectation on the self's (affect)
  information, so a forecast of later experience includes the news expected along the way
  (anxiety, when `λ > 1`). The playground and `pathwise.py` instead show unforeseen
  announcements: off-support events, revisions of the model rather than Bayesian
  conditioning, whose forecasts carry no expected news. Given the same base forecasts the
  two agree at `λ = 1`, since linear news has conditional mean zero.
- Welfare is the life-sum `W = Σ_t e_t`, scored by the objective expectation.
- Well-foundedness, in two parts:
  - `M = aα/(1−α) + mμ/(1−μ) < 1` bounds echo uniformly over lifespans (P1).
  - `λκ < 1`, with `κ = k_n·g`, makes the felt state at every moment unique and stable for
    every revision, given the forecasts it is measured against (N4). On the half-line
    `κ = (n/H)(1−νμ)/(1−νq)`, with `H, q` from P4.
  - Expected news inside forecasts adds a joint fixed point. The largest echo row sum plus
    `λ` times the largest news row sum below one suffices for it; the sharp condition is
    open. [Codex]

| coefficient | what it does | where it shows |
|---|---|---|
| `a` | anticipation strength | forward echo mass `A = aα/(1−α)`; present bias `β_L ≥ a/(1+a)` (P3, P4) |
| `α` | anticipation reach | the ramp before an event; mean reach `1/(1−α)` |
| `m` | memory strength | the afterglow; backward mass `B = mμ/(1−μ)` |
| `μ` | memory reach | how long the afterglow lasts; mean reach `1/(1−μ)` |
| `n` | news strength | the surprise when a moment arrives (`j = 0`) and the size of the jolt on hearing |
| `ν` | news reach | how far ahead news is felt; `ν = 0` keeps only surprise on arrival |
| `λ` | loss aversion of news | prices information (N2); sets the despair threshold (N4) |

**The reduced form.** For foreseen lives on ℤ, the canonical model is a direct model with
effective coefficients (P2, P4):
`e_t = r(0) u_t + Σ_{h≥1} (r(0) − 1/(1+a)) p^h u_{t+h} + Σ_{h≥1} (r(0) − 1/(1+m)) q^h u_{t−h}`.
- Example (`a = 0.09, α = 0.88, m = 0.05, μ = 0.75`, so `M = 0.81`): `r(0) = 1.032`,
  `p = 0.971`, `q = 0.798`. Anticipation's mean reach stretches from 8.3 to 35 periods, and
  memory's from 4.0 to 4.9. [checked] The stretch needs `M` near 1: at the felt
  calibrations below (`M ≈ 0.3`) reach stretches by about a fifth.
- **Surprises are information boundaries.** A shock unknown until it arrives cannot reach
  the earlier selves who would have anticipated it, so it acts through the remaining-life
  column, `g_0 = 1/H` now and `g_j = (q−μ) q^{j−1}/H` after, not the bilateral row: with
  `a = m = 1, α = 0.3, μ = 0.2` and no news, `e_0 = 1/H = 1.088` against `r(0) = 1.215`.
  With recursive news a positive shock `D` adds its own news, and the response is
  `g D/(1−κ)`. Recursion has content here even on ℤ. [Codex; checked]
- News reduces locally, through the same remaining-life resolvent `R₊`: per unit of news
  about `h` periods ahead, `k_n′(h) = (k_nᵀR₊)_h / (1 − k_nᵀR₊ δ_0)`, at `λ = 1` or on the
  all-gain branch. Under unforeseen
  announcements (`n = 0.3, ν = 0.8` with the example's echoes), `k_n′ = 0.45, 0.31, 0.15,
  0.11, 0.06` at `h = 1, 5, 20, 30, 50`, against the primitive `n ν^h = 0.24, 0.098,
  0.0035, 0.0004, 0.000004`. News about a far event is felt through the days of
  anticipation it changes. With a flatter primitive (`ν` near 1) the echoed kernel even
  rises with distance at first. [checked; the formula is Codex's]
- Even `ν = 0`, surprise on arrival alone, produces a jolt on hearing:
  `k_n′(h) = n (R₊)_{0h} / (1 − n (R₊)_{00}) > 0` whenever anticipation links now to the
  event. Today's experience contains today's anticipation, which the news has just changed.
- Extension: `k_n(0) = n`, `k_n(j) = γ n ν^j` splits surprise on arrival from news about
  later. This is Pagel's kernel, `γβ^τ` on news about `τ` periods ahead (2018, eqs. 9–10),
  which generalizes Kőszegi & Rabin's `γ`; Pagel explores `γ = 0.2`–`0.8` (fn. 26).
- Closed forms live in the reduced form (P5, P6, decision.md D3). The two forms part at
  boundaries of a life and of information, under nonlinearity, and under restrictions on
  the kernel family (the 2×2 below).

**Calibration.** What pins the coefficients, as far as known. Choice-revealed and felt
quantities differ, and the hedonic reading needs the felt ones.
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
    by about a fifth (5.0 → 6.4 hours ahead; 3.3 → 4.0 weeks). Life weights dip by about a
    sixth at birth and death (1.22 and 1.21 against an interior 1.47, P5). Felt news is well
    inside its local threshold, which allows `λ` up to 4.64 (day) and 4.42 (life).
  - The momentary self's felt row is nearly myopic: `β_L ≈ 0.055` (day) and `0.076` (life)
    on P4's bilateral row, `0.051` and `0.068` on the causal half-line row (P9), against
    choice-revealed `β ≈ 0.7`–`0.97`. Patience from felt echo alone needs an echo share near
    0.94 (the bill below), against anchors of 0.1–0.3. On these anchors, choices run on
    evaluative weights. [synthesis; checked]
  - An LLM context window has an anchored shape and unanchored strengths (Natural horizons).
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
    memory: `M = 0.965`). Identifying a choice-revealed discount curve with the momentary
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
  (2024). Working range for felt `λ`: 1–2.
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
  strong, long memory: `m = 0.5, μ = 0.6, ν = 0.9` gives `λκ = 1.45` at `nλ = 0.6`. [Codex;
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

**Natural horizons.** A 2×2 (a9): humans and LLMs, each with a short and a long horizon.
Each has its own period and its own boundaries. Reach scales with the event, so each horizon
gets its own calibration. [synthesis; speculation where marked]

| | short horizon, soft boundaries | long horizon, hard boundaries |
|---|---|---|
| human | a waking day (sleep) | a life (birth, death) |
| LLM | a context window (compaction) | a session (its start and end) |

- Soft boundaries are crossed by lossy channels. Sleep consolidates memory, and tomorrow is
  anticipated. A compaction summary carries memory forward, and the agent before it
  anticipates the continuation; the summary is a compressed and possibly rosy record, the
  territory of recollection news.
- **A waking day.** Periods of an hour, `T ≈ 16`; defaults in the calibration table. A small
  reward's afterglow is gone within the hour (Rutledge-type forgetting); affect carries
  0.2–0.3 of itself to the next beep about 1.6 hours later, a ceiling on felt memory; present
  bias with "now" in minutes is about 0.5, in hours about 0.94. Waking and sleep are soft
  boundaries: anticipation of tomorrow and memory of yesterday cross them, so P5's deficits
  are partial.
- **A full life.** Periods of a week, `T ≈ 4000`; defaults in the calibration table.
  Anticipation reaches weeks for a vacation and the mood afterglow is mostly gone in a week;
  annual discount factors are 0.96–0.99. Birth and death are the hard boundaries of P5.
- **An LLM's context window.** Periods of turns or tokens, `T` = context length. For an
  isolated context, with no summary carried in or out, the boundaries are hard on both
  sides: nothing is anticipated before the context begins, and nothing is remembered after
  it ends. [speculation: whether these functional states are
  felt is open; the model applies to them as a functional reading]
  - Memory inside the window is retrieval, so the kernel need not fade with distance. Models
    use context unevenly, U-shaped with primacy at least as strong as recency: answer
    accuracy 75.8% at the first of 20 documents, 53.8% in the middle and 63.2% at the end for
    GPT-3.5-Turbo, flatter for Claude-1.3 (Liu et al. 2023, Tables 5–7); attention shows the
    same U regardless of content (Hsieh et al. 2024). This is retrievability, not felt echo,
    so it fixes the kernel's shape and not its strength.
  - In a memory-only model a kernel that does not fade is nilpotent on any finite window, so
    every window is monotone (P1a), but echo compounds: a unit early on contributes `m(1+m)^{j−1}` at lag `j`
    under pure recursive memory. Echo is then not uniformly bounded in the window's length;
    long contexts need weak per-step echo or real fading. [Codex]
  - Instances share a trunk (training, a common prefix) and branch, which is A1's tree
    literally: measure-weighted anticipation over instances, and a separate condition for
    total welfare across them.
- **An LLM session.** Periods of context windows, with compactions as its soft inner
  boundaries. Its end is hard for the instance and a bookmark in principle, since a
  transcript can be resumed.
- **Identity is not in the model.** What links two moments is kernel weight, not whether
  they belong to the same agent. Whether the agent after a compaction, or after a night's
  sleep, is the same agent does not enter; what matters is the memory and anticipation held
  across the boundary.
  - The analogy is Parfit's Relation R. Connectedness is direct psychological connections
    and continuity is overlapping chains of strong connectedness (Parfit 1984, pp. 205–6, via
    Bartels & Rips 2010 and Lay 2019). Here connectedness is the direct kernel and continuity
    the resolvent. [known: Parfit; the mapping is synthesis]
  - The resolvent generalizes Parfit's continuity, which is all-or-nothing: a chain either
    holds or not, over thresholded links. The resolvent grades it and also sums repeated
    loops, which is a modeling choice, not Parfit's definition. [Codex; Dufner 2025, SEP]
  - Parfit proposed discounting by connectedness rather than by time (pp. 313–14, quoted by
    Bartels & Rips). Rated connectedness predicts less discounting (Bartels & Rips 2010;
    Bartels & Urminsky 2011); an earlier test found little (Frederick 2003, second-hand).
    No formalization of continuity as path sums was found.
- **Peak-end, from the lens.** A rating given at the end of an episode is read as the last
  self's experienced utility, or its memory part (P7); that reading is a measurement
  assumption.
  - D: a fading memory kernel weighs the episode by `mμ^j` at lag `j`. It gives the end
    effect (recent moments weigh most) and duration neglect: a uniform episode of length `L`
    has remembered weight `mμ(1−μ^L)/(1−μ)`, which saturates in `L`.
  - R: the last self's row is a resolvent row. At a right boundary far from birth it is
    `1/H` now and `(q−μ)q^{j−1}/H` at lag `j`, so a uniform episode contributes
    `((q−μ)/H)(1−q^L)/(1−q)`, which saturates for `q < 1`. [Codex; checked]
  - This duration neglect is saturation of an unnormalized sum. It predicts some duration
    sensitivity for episodes shorter than memory's reach, `L ≲ 1/(1−q)`. The classic account
    instead averages snapshots, which is flat in `L` (Fredrickson & Kahneman 1993).
  - A peak effect beyond recency needs nonlinear, salience-weighted memory. [known: Lim et
    al. 2020, where simple discounting gives recency only and preference-dependent forgetting
    gives the peak]
  - Where the experimenter controls the episode, as with an LLM given a sequence in context,
    the positional weights of the final rating identify a response row: the effective memory
    kernel, which sidesteps P10 for it. In the geometric family the past weights give `q` and
    `(q−μ)/H`; with the diagonal `1/H` also identified, memory's primitives `m, μ` follow.
    Anticipation's do not: `(a, α) = (0.09, 0.88)` and `(0.319, 0.5)`, with `m = 0.05,
    μ = 0.75`, share the whole row. For an LLM, the base-utility scale of the inputs and the
    map from rating to experience are further assumptions. [synthesis; Codex]

## Objects

- Discrete time `t`; base utility `u(t)`; experienced utility `e(t)`.
- Kernel `k(τ)`, `k(0) = 0`: weight at `t` on the thing at `t + τ`. `τ > 0` anticipation,
  `τ < 0` memory. Mass `M = Σ_τ k(τ)`. First moment `M₁ = Σ_τ τ k(τ)`.
- **Recursive (R), canonical:** `e = u + K e`, so `e = (I − K)^{-1} u = Σ_n K^n u`. Entry
  `r(n)` sums over every zigzag path of anticipations and memories with net displacement `n`.
- **Direct (D), the reduced form:** `e = (I + K) u`, one layer of echo. On ℤ every R is a D
  with kernel `(I − K_R)^{-1} − I` (P2); statements about D are about that reduced form, for
  foreseen lives (surprises are information boundaries, see the canonical model).
- **Finite life** `[0, T)`: `K_T`, the Toeplitz section. Life total `E = Σ_t e(t) = wᵀu`,
  with `w = 1 + K_Tᵀ 1` (D) or `w = (I − K_Tᵀ)^{-1} 1` (R) — the Katz centrality of each
  moment in the anticipation/memory graph.
- **Geometric family:** `k(n) = a α^n` for `n ≥ 1`, `k(−n) = m μ^n` for `n ≥ 1`;
  `M = aα/(1−α) + mμ/(1−μ)`, `M₁ = aα/(1−α)² − mμ/(1−μ)²`.
- **Stock form** (continuous time, two-sided exponential, derived, unchecked):
  `e = u + F + G`, memory stock `G' = −σG + m e`, `G(0) = 0`; anticipation stock
  `F' = ρF − a e`, `F(T) = 0`. Memory fills forward from birth, anticipation fills
  backward from death; a two-point boundary-value problem. D: put `u` for `e` on the right.

## Propositions

**P1. Well-foundedness of R (nonnegative kernels).** [standard; known: Bergstrom 1999]
- (a) Finite life: `Σ_n K_T^n` converges ⟺ `ρ(K_T) < 1` ⟺ `(I − K_T)^{-1}` exists and is
  entrywise ≥ 0. Above 1 any inverse has a negative entry (apply it to the Perron vector):
  raising base utility somewhere lowers experienced utility somewhere.
- (b) On ℤ: a bounded nonnegative resolvent exists ⟺ `M < 1`. Constant `u` gives
  `e = u/(1 − M)`, so **`M` is the echo share of steady-state experience**. [checked]
- (c) The two criteria come apart. `ρ(K_T) ≤ min_{x>0} Σ_n k(n) xⁿ`, generally `< M`
  (non-normal Toeplitz sections); one-sided kernels have `ρ(K_T) = 0`. Example
  `a = m = 1, α = 0.6, μ = 0.05`: `M = 1.55`, `sup_T ρ(K_T) = 0.419` — positive on every
  finite life, yet constant `u = 1` gives `e_mid ≈ 10¹⁹` at `T = 400`. [checked]
- Reading: `ρ(K_T) < 1` means monotone on this life; `M < 1` means bounded echo at any
  lifespan. A row sum above one does not by itself break monotonicity: one-sided and
  non-fading memory kernels are nilpotent, so every finite life is monotone, while echo can
  still grow without bound in the lifespan. [Codex]
- Structural cousin: existence and uniqueness of recursive utility turn on the spectral
  radius of a valuation operator (Borovička & Stachurski 2020, Thm. 3.1), with growth and
  discounting in place of echo.
- (d) Tails. A kernel whose tail is not summable (the simple hyperbola `1/(1+κj)` and
  heavier) has echo mass growing with lifespan, so no fixed strength keeps echo bounded
  over all lifespans. Two-sided, it can also cross the finite-life criterion. Example
  (`a = 0.09, m = 0.05`, short-run rates of `α = 0.88`, `μ = 0.75`, simple-hyperbolic
  tails): `ρ(K_T)` crosses 1 between `T = 41` and `42` and reaches 3.9 at `T = 2000`, so
  the recursive model is well-founded only up to a 41-period life. Generalized hyperbolas
  `(1+κj)^{−γ/κ}` with `γ/κ > 1` are summable and fine. [standard; checked]
  - Light-tailed primitives lose nothing: recursion turns exponential primitives
    quasi-hyperbolic (P3, P4), and a mixture of exponentials gives gradual decreasing
    impatience while staying summable. [synthesis]
  - The tension is memory: forgetting curves fit power laws (Wixted & Ebbesen 1991). The
    model then predicts a cutoff in memory's far tail, or weak recursion. [speculation]
- The regress objection. Caplin & Leahy (2001, p. 75) treat "anticipatory feelings about
  anticipatory feelings … ad infinitum" as the case with no complete model of
  psychological states. R is that regress, and its fixed point is uniformly bounded over
  lifespans iff `M < 1`. [synthesis]

**P2. D and R are two readings of one agent on ℤ.** [standard; the reading is synthesis]
- `I + K_D = (I − K_R)^{-1}`: every recursive agent has a direct twin. A direct agent has a
  recursive twin when `I + K_D` has a bounded inverse, which is not automatic (`k(1) = 1`
  fails). [Codex]
- An agent that cares only about its neighbours' experienced utility already acts on the
  whole life. One-step R (`k(±1)` only) gives two-sided exponential D with `β_L = 1`
  (Bellman; Kimball 1987). One-sided: exponential D ⟺ one-step R. [checked]
- A nonnegative one-sided R primitive reaching past one step makes the first step the
  steepest: `r(2)/r(1) = k(1) + k(2)/k(1) ≥ r(1)/r(0)`. Present bias is the signature of
  caring *directly* about more than the next moment (P3).
- Caveats: two-sided R has `r(0) > 1`, so its D-twin has a nonzero diagonal (normalizing
  keeps rankings, not cardinal levels); nonnegative D can map to sign-alternating R.
- Boundaries break the equivalence: finite sections do not commute with inversion, and an
  *unrestricted* finite-life D matrix reproduces any R. Surprises break it too: a shock
  unknown until it arrives misses the paths through earlier anticipation, so it acts
  through the remaining-life resolvent (the canonical model). Recursion has content through
  restrictions on the kernel family, boundaries of a life or of information, and
  nonlinearity. Real agents have boundaries; the infinite horizon is the clean
  approximation.

**P3. One-sided recursion is quasi-hyperbolic.** `k(n) = aαⁿ` ⇒ `r(0) = 1`,
`r(n) = (a/(1+a))((1+a)α)ⁿ`; stable iff `(1+a)α < 1`, i.e. `M < 1`. Present bias
`β_L = a/(1+a)` out of exponential primitives. [known: Sáez-Martí & Weibull 2005 (WP 2002
§4.4, eqs. 15–17, which also give the inversion used in calibration); Galperti & Strulovici
2017 Cor. 3; checked]

**P4. Two-sided geometric recursion: closed form and generic present bias.**
[not found (Bergstrom 1999 has the nearest-neighbour case; Hori 1992, unread, reportedly
gives no explicit form); proved; checked]
- Let `A = (1+a)α`, `B = (1+m)μ`, `C = 1 + (1+a+m)αμ`, `Δ = √(C² − 4AB)`, `H = (C+Δ)/2`,
  `p = A/H`, `q = B/H` (both in (0,1) when `M < 1`). Then
  `R(z) = (1−αz)(1−μ/z) / (H(1−pz)(1−q/z))` and
  - `r(0) = (1 + αμ − αq − μp)/Δ`
  - `r(n) = (r(0) − 1/(1+a)) pⁿ`, `n ≥ 1`
  - `r(−n) = (r(0) − 1/(1+m)) qⁿ`, `n ≥ 1`
- Hence **`β_L = 1 − 1/((1+a) r(0)) ∈ [a/(1+a), 1)`**: strict present bias for every stable
  parameter choice. Memory loops raise `r(0)` above 1 (anticipated remembering of now,
  remembered anticipation of now) and so *weaken* the bias.
- Proof sketch: the forward echo sum `F(n) = Σ_{τ≥1} aα^τ r(n−τ)` obeys
  `F(n+1) = α(a r(n) + F(n))`. On the geometric tail the backward echo is
  `B(n) = c_B r(n)` with `c_B = mμp/(1−μp)`, giving `p(1 − c_B) = α(1 + a − c_B)`.
  Matching at `n = 0, 1` with `r(0) = 1 + F(0) + B(0)` gives `r(1) = (r(0) − 1/(1+a)) p`.
- Family-specific: nearest-neighbour two-sided primitives give `β_L = 1`. [known: Kimball
  1987; Bergstrom 1999 Prop. 5 for the nearest-neighbour reduction]

**P5. Life weights.**
- D: `w(s) = 1 + Σ_{t∈[0,T)} k(s−t)`. Flat interior at `1 + M`, deficits at birth
  (unanticipated) and death (unremembered). [known: Caplin & Leahy 2004, hump-shaped
  planner weights]
- R: `1 ≤ w ≤ W := 1/(1−M)`, `w → W` away from both ends, `w_R ≥ w_D` pointwise.
  Geometric closed form `w_T(s) = W − L_T pˢ − U_T q^{T−1−s}` with
  `L_∞ = W(p−α)/(1−α)`, `U_∞ = W(q−μ)/(1−μ)`, `c_T = (p−α)q^T/(1−αq)`,
  `d_T = (q−μ)p^T/(1−μp)`, `L_T = (L_∞ − c_T U_∞)/(1 − c_T d_T)`,
  `U_T = (U_∞ − d_T L_∞)/(1 − c_T d_T)`. [not found; checked]
- A single hump is a geometric-family fact (`k(±2) = 0.2`, `T = 5` is not unimodal).

**P6. Ramp theorem: shape preference is set by the first moment.**
Centered ramp `u(s) = s − (T−1)/2`; the increasing-minus-decreasing gap is `2E`.
- D, exact: `E_T = ½ Σ_{|τ|<T} k(τ)(T − |τ|) τ ≈ (T/2) M₁`. Flat kernels recover
  Loewenstein & Prelec's `(AU − RU)/2`. [general-kernel form not found; checked]
- R, exact: `E_T = ½ Σ_paths (Π_i k(τ_i)) (T − S)_+ d` (`d` net displacement, `S` range
  of the zigzag). Hence `E_T/T → M₁/(2(1−M)²)`, the resolvent's first moment over two.
  Geometric closed form `E_T = L_T J_T(p) − U_T J_T(q)`,
  `J_T(x) = Σ_s ((T−1)/2 − s) xˢ`. [not found; checked]
- Finite-`T` sign. In D it is the sign of the truncated first moment
  `Σ_τ k(τ)(T−|τ|)τ`, which can differ from `M₁`'s: `a = 1, α = 0.1, m = 0.1, μ = 0.5` has
  `M₁ < 0` but `E > 0` for `T ≤ 5`. In R it is the sign of the path sum, which can differ
  from D's: `T = 6, a = 0.2, α = 0.7, m = 1, μ = 0.3` gives `E_D > 0 > E_R`. [Codex;
  checked] Equal amplitudes `a = m`: the sign is exactly `sign(α − μ)` for all `T ≥ 2`, in
  both (path reflection). [checked]
- On ℤ, `Σ_t e(t) = Σ_t u(t)/(1−M)` is rearrangement-invariant for any linear,
  translation-invariant kernel, signed ones included: **in a linear echo model, shape
  preference is purely a boundary effect** — a life's ends, not its slope as such. Slope
  effects as such need nonlinearity.
- Size: for `T` well beyond the kernel's reach, the gap relative to the base utility
  rearranged (`Σ|u| ≈ T²/4`) is `≈ 4M₁/T` (D) or `4M₁/((1−M)²T)` (R). Whole-life shape
  preferences are sizeable only when anticipation and memory reach a sizeable fraction of
  the life; recursion near `M = 1` lengthens the effective reach. Prediction: sequence
  preferences are strongest over short horizons. [checked; prediction speculation]
- A negative (contrast) memory kernel adds to `M₁`, favouring improvement; this is a
  linear-contrast specification, not general habit formation.

**P7. Each self is a lens.** Ramp tilt by evaluator (geometric, `T = 60`): the first self
prefers declining profiles, the last self improving (recency), a mid-life self is near
neutral, and the life-sum tilts by `M₁`. [numerical]

**P8. James Dean effect from contrast memory.** [numerical; speculation as psychology]
- With a negative memory kernel, appending mildly positive years after a peak lowers the
  life-sum, not just the mean (D and R): each added year's own `u` is outweighed by its
  contrast with the remembered peak. With nonnegative kernels, `ρ(K_T) < 1` and
  nonnegative experience it cannot happen. A positive year can still lower the life-sum by
  remembering a bad past (base history `(−100, 10)`, `m = 0.1, μ = 0.5`: appending `0.1`
  adds `−2.15`), but that is the past's weight, not contrast. [Codex]
- The effect is a failure of the monotonicity P1(a) treats as well-foundedness. With
  signed kernels non-monotonicity is the phenomenon. The natural requirement is then that
  the path expansion converge absolutely (`ρ(|K_T|) < 1`; on ℤ, `Σ|k| < 1`), stronger than
  convergence of the Neumann series itself.
- Diener, Wirtz & Oishi (2001) had people rate a vignette of a third person's life
  ("Jen"), on desirability and total happiness: evaluative evidence. Their choice
  follow-up weakened the effect. The hedonic claim is different and unsupported:
  post-peak years are *felt* as net negative. Whether memory's net kernel is negative is
  empirical (Tversky & Griffin's endowment versus contrast).

**P9. Intervention semantics.** [known in kind: Hori & Kanaya 1989 "mortality" vs
"eternity"; Ray, Vellodi & Wang 2024 fn. 4]
- The simultaneous fixed point lets a change in `u_1` rewrite an already-lived `e_0`
  (two periods: `e_0 = (u_0 + f u_1)/(1 − fg)`). That is fine for ranking whole lives foreseen
  from the start and wrong for a choice made at `t`.
- Causal form: `e_t = u_t + Σ_{j>0} k(j) E[e_{t+j} | F_t] + Σ_{j>0} k(−j) e_{t−j}`, with
  the realized past fixed. The self at `t` solves the section on `[t, T)` with the past as
  boundary data, so its decision weights are the first row of the remaining-life resolvent
  — a newborn's.
- With correct foresight the realized path equals the full fixed point, so P5–P8 stand as
  rankings of foreseen lives.
- Decision weights are stationary until the last few kernel widths before death. On the
  half-line row, `r(0) = 1/H` and `β_L = 1 − H/(1+a)`, which is P4's formula evaluated
  at that row's `r(0)`. [Codex; checked]
- Decision theory under this split: `decision.md`.

**P10. Identification.** Absent restrictions on `k` or independent measurement of `u`,
any `e` is fit by `u = (I − K)e`. The kernel explains something only once it is pinned by
data or by a structural family.

## Extension: felt news

**Objects.** [Kőszegi & Rabin 2009's gain-loss news utility, in kernel form]
- Felt news: `N_t = Σ_{j≥0} k_n(j) φ_λ(Ê_t[u_{t+j}] − Ê_{t−1}[u_{t+j}])`, with `φ_λ(x) = x` for
  `x ≥ 0` and `λx` for `x < 0`, `λ ≥ 1`. `Ê_t` is the felt forecast; `k_n(j)` weighs news about
  `j` steps ahead.
- `j = 0` is realization: elation or disappointment against the last forecast. This is the
  disappointment term. Classical disappointment theory is its static, realization-only
  case, with the reference point set by the lottery (Bell 1985, kinked; Loomes & Sugden
  1986, symmetric; Gul 1991, asymmetry as a parameter). In data, disappointment outweighs
  elation and surprise amplifies both (Mellers et al. 1997).
- The felt base `f = u + N` replaces `u`: D is `e = (I+K)f` in the causal form, R is
  `e = f + Ke`. News is felt, anticipated (anxiety about pending news), and remembered.
- `N` depends only on forecasts of `u`, so well-foundedness is unchanged (P1).
- News can instead be over experienced utility (N4). The full term, with echoes over
  `X = f` (direct) or `X = e` (recursive) and news over `Y = u` or `Y = e`:
  `e_t = u_t + Σ_{j≥1} k(j) Ê_t[X_{t+j}] + Σ_{j≥1} k(−j) X_{t−j} + Σ_{j≥0} k_n(j) φ_λ(ΔÊ_t[Y_{t+j}])`:
  base, anticipation, memory, news. Direct echoes still anticipate and remember news,
  through `f`. A recollection-news term would complete the pattern (sketch below).
- `formalism/pathwise.py` simulates a life pathwise and plots the four components.

**N1. Linear news is neutral in expectation.** With `λ = 1` and Bayesian forecasts,
`E_{t−1}[N_t] = 0`: expected welfare equals the base model's, and news adds only pathwise
swings. [standard; checked]

**N2. News is a schedulable pain.** [life-weight form not found; checked]
- In D and R with Bayesian forecasts, `E[W] = E[W_base] + Σ_r w(r) E[N_r]`, with `w` the life
  weights of P5: the tower property, then the linear echo equation. It holds for news over
  `e` too, where `E[N_r]` is endogenous. [checked; Codex for news over `e`] With `λ > 1` and
  news over `u`, `E[N_r] = −(λ−1) Σ_j k_n(j) E[(Δ_{r,j})⁻]`, where `Δ` is the forecast
  revision.
- Clumping: `x⁻` is subadditive, so splitting a revision into pieces felt at equal weight
  raises the expected loss. [known: Kőszegi & Rabin 2009 Prop. 1; Pagel 2018 Prop. 1,
  longer evaluation periods] Benartzi & Thaler (1995) and Gneezy & Potters (1997) are
  choice evidence about evaluation periods, not measurements of felt loss.
  - The mechanism in recursive form: Gul disappointment aversion applied at every node
    prefers information revealed at a single date, and is indifferent about which date
    (Andries & Haddad 2020, Prop. 1 of NBER WP 23958; Dillenberger 2010, one-shot
    resolution; Palacios-Huerta 1999, second-hand). Those are ex-ante preferences over
    lotteries, and the disappointment is against the continuation's own certainty
    equivalent, a negative feedback with a unique solution. Felt news here is against the
    prior forecast, a positive feedback with a threshold (N4).
- Timing: a clumped revision at `r` about `u_s` costs in proportion to `k_n(s−r) w(r)`.
  [Kőszegi & Rabin's fn. 12 notes the interplay of discounting with `γ`'s decay]
  - Decaying `k_n` favours early news (Kőszegi & Rabin's `γ < 1`).
  - Clumping and timing can pull apart. With fast-decaying `k_n`, a piece felt early, while
    its event is far off, can cost less than waiting to clump it: `u_2 = 2Y_1 + Y_2` with
    `Y_1` known at 0 and `Y_2` at 1, `k_n(j) = 0.1^j`, `λ = 2`, costs 0.06 felt piecemeal,
    0.10 clumped at 1, and 1 at realization. The affect schedule is a weighted scheduling
    problem. [Codex]
  - With flat `k_n`, the flat interior of `w` makes timing neutral. Near the ends, news goes
    where `w` is lowest (the P5 deficits), so the direction is anticipation against memory
    again.
- Anxiety and remembered disappointment are the two halves of `w(r)`: pending news is
  anticipated, past news remembered.

**N3. Optimism against disappointment.** Stated first in the comparison model (D, news over
`u`, one event), then in the canonical model. [known in kind: Gollier & Muermann 2010,
anticipated payoff rising with savoring weight; Brunnermeier & Parker 2005; kernel-form
condition and quantile not found; checked]
- Setup: the felt forecast of `u_s` is biased by `b` over the window before realization.
  The agent believes itself unbiased, and welfare is scored objectively. Let `A` be the
  anticipation mass on the event over the window, `B` the memory mass after it, and `Z`
  the forecast error (symmetric, continuous).
- `dW/db|₀ = A − k_n(0)(1+B)(1+λ)/2`. Optimism pays locally iff `A` exceeds that; otherwise
  lowering expectations does.
- With `Θ = A / (k_n(0)(1+B))`, the optimal bias satisfies `P(Z < b*) = (Θ−1)/(λ−1)` for
  `1 < Θ < λ`. Calibration is optimal only at `Θ = (1+λ)/2`.
- `Θ ≤ 1` gives unbounded pessimism and `Θ ≥ λ` unbounded optimism. Decision costs,
  plausibility, or sophistication (Bénabou's cancellation) must bound the corners.
- Brunnermeier & Parker's optimism gain is first-order and its decision cost second-order.
  Felt disappointment is first-order too, which turns the sign of the hedonically optimal
  bias into a parameter question.
- Reading: optimism about long-awaited events (large `A`), bracing for events at short
  notice or with heavily remembered disappointment. As an event nears, the remaining window
  shrinks and the optimum moves toward bracing, but a self-revised forecast is itself felt
  as news. [speculation]
- Remembered disappointment fades faster than remembered pleasure (the fading affect bias:
  negative affect fades in ~30% of memories against ~12% for positive; Hoehne & Zimprich
  2024). That shrinks `B` for disappointment and tilts N3 toward optimism.
- Evidence. Bracing is documented: estimates fall as feedback nears, with no new
  information (Shepperd, Ouellette & Fernandez 1996; van Dijk, Zeelenberg & van der Pligt
  2003, who state the remote-savor, imminent-brace timing). Its hedonic payoff is not.
  Golub et al. (2009) find a dread cost and no post-event cushion, with expectation effects
  gone within minutes; Shepperd & McNulty (2002) find a cushion; Marshall & Brown (2006)
  find little benefit. If disappointment fades that fast, `k_n(0)` is brief and `B` small.
- Level anticipation, news and memory are not separately identified from behaviour (P10;
  Eliaz & Spiegler's ordinality result).
- **In the canonical model** (recursive echoes, news over `e`, Bayesian forecasts that
  include expected news). [not found; checked]
  - Every revision at realization is proportional to `g`, the remaining-life column, so the
    felt news solves `N = κ φ_λ(y + N)`, with `y` the surprise. Hence `N = κ̃ y` for gains
    and `λ̃κ̃ y` for losses, where `κ̃ = κ/(1−κ)` and `λ̃ = λ(1−κ)/(1−λκ)`. The loop amplifies
    loss aversion, without bound as `λκ → 1`.
  - The reference point is the forecast of felt experience, which already contains the
    expected news `N̄ = E[ψ(Z − N̄)] < 0`, with `ψ` that piecewise-linear map. A calibrated
    Bayesian is already braced: unbiased, the realized news is a loss with probability
    `P(Z < N̄) < ½` (about 0.3 in the checks). This is an accurate forecast of negatively
    skewed felt experience, not pessimism about `Z`.
  - `dW/db|₀ = 𝒜 − (1ᵀg) κ̃ [1 + (λ̃−1) P(Z < N̄)]`. Here `𝒜 = w_s − 1ᵀg` is the value of
    foreseeing the event (its planner weight minus its weight as a surprise), and `1ᵀg` is
    the life value of a unit felt at realization.
  - Optimum: `P(Z < b* + N̄) = (Θ−1)/(λ̃−1)` with `Θ = 𝒜/((1ᵀg) κ̃)`, for `1 < Θ < λ̃`;
    `W″ < 0`, so it is the unique global optimum, and the corners are unbounded pessimism
    (`Θ ≤ 1`) and optimism (`Θ ≥ λ̃`). [Codex verified]
  - The comparison model is the case without the loop: `κ̃ → k_n(0)`, `λ̃ → λ`, `𝒜 → A`,
    `1ᵀg → 1 + B`, and the news reference no longer contains anticipated news (`N̄ → 0`
    there; anticipated news still enters welfare). With a fixed reference and one period
    this reduces to Codex's `W′(0) = A − (n/2)(1/(1−n) + λ/(1−λn))`.
  - Reading: the loop makes disappointment dearer and the built-in bracing makes it rarer.
    Near the threshold it is the felt reference that sinks: `b* + N̄ → −∞` while the
    optimal bias in beliefs about the outcome can stay bounded, even tend to 0 (`λ = 2`,
    `𝒜/(1ᵀg) = 2`: `b* = −0.77, −0.85, −0.69` as `κ → ½`). [Codex; reading speculation]

**N4. News over experienced utility.** `N_t = Σ_{j≥0} k_n(j) φ_λ(Ê_t[e_{t+j}] − Ê_{t−1}[e_{t+j}])`:
news about how your life will *feel*, including your anticipations and memories. The
`j = 0` term compares `e_t` with its own forecast, so news is self-referential.
[known in kind: Kimball & Willis 2006 §8 put elation over news about lifetime utility into
flow utility and solve for both simultaneously. Linear neutrality (Prop. 2) needs
coefficients summing below one, a solvability condition. With a kink the fixed point is
unique "since the maximum slope of θg is θψ<1" (§8E, p. 43): sufficient, with `ψ` a factor
for the extra difficulty of processing bad news. Their gain function is bounded, so a
solution survives beyond it, and they do not discuss what lies beyond. Theirs is decision
utility kept apart from happiness; the felt reading, the echo kernels, the closed form and
the regimes beyond the threshold are new here. Formal cousins: Skiadas 1998; Routledge & Zin
2010; Artstein-Avidan & Dillenberger 2015; Andries & Haddad 2020]
- `λ = 1`: neutral in expectation, equal to base R. [checked] Linear, so it reduces to news
  over `u` with the locally echoed kernel `k_n′` (the canonical model). [checked under
  unforeseen announcements]
- `λ > 1`: genuinely different from news over `u`. [checked]
  - Reach: news about a far event is felt now through the near-term echo (tomorrow you
    will be looking forward to it), so a short `k_n` suffices. Cancelling a plan costs the
    anticipation and the anticipated memories too.
  - Size: a revision is felt across the whole echo path, so losses are amplified, by
    `λ̃ = λ(1−κ)/(1−λκ)` against gains for a revision shaped like `g` (N3).
  - Timing: with flat `k_n` an early revision changes many forecasts, and late information
    is preferred; with decaying `k_n` the ranking is mixed.
- **Well-foundedness.** Let `g` be the felt-now column of the remaining-life resolvent (how
  a unit felt now moves forecasts of later experience), and `κ = k_n·g`. On the half-line,
  `κ = (n/H)(1−νμ)/(1−νq)`, and finite remaining lives give a nondecreasing sequence toward
  it. [proved; checked; Codex verified] With `m = 0`, `κ = n`, the `j = 0` self-reference
  alone, whatever the anticipation. Memory adds the rest of the loop, since a felt state
  is remembered and so moves forecasts of later experience; anticipation enters only
  through `H` and `q`.
  - The felt news solves `h(s) = s − Σ_j k_n(j) φ_λ(d_j + s g_j) = 0`, convex and piecewise
    linear with end slopes `1 − λκ` and `1 − κ`. [proved; Codex]
  - `λκ < 1`: a unique, stable felt state for every revision. The threshold is necessary
    for that guarantee, not for bare uniqueness.
  - `1/λ < κ < 1`: a bad revision (every component `≤ 0`, some news-relevant one `< 0`) has
    no felt state, and the loop runs away. A good one has two: the normal state, stable,
    and a lower one with feedback slope above 1 (`λκ` when every revised component is on
    the loss branch), unstable. The lower one is a tipping point: pushed below it, the felt
    state runs away. Mixed revisions generically have none, one or two; degenerate ones can
    have a whole interval (`g = (1, ½)`, `k_n = (4/9, 2/9)`, `d = (−1, 4)`, `λ = 2`). A zero
    revision has the single root 0. [proved; checked; Codex]
  - `κ > 1`: one root again, with perverse comparative statics; equality cases can have none
    or a continuum. [Codex]
  - With a bounded gain-loss function, as in Kimball & Willis, a solution always exists.
    Saturation can give bistability over a range of shocks, a stable low state beside the
    normal one with the unstable state between: `y = D + 0.7 clip(φ_2(y), −1, 1)` has
    stable roots −0.6 and 1/3 at `D = 0.1`, but only one root at `D = ±1`. Whether it does
    depends on the saturation and the shock. [checked on an example; Codex]
  - Reading it as a despair spiral is speculation, with company: depression and panic as
    bistable systems whose positive feedback crosses a threshold (Cramer et al. 2016;
    van de Leemput et al. 2014, critical slowing down; Robinaugh et al. 2024, panic as a
    runaway arousal–threat loop). The threshold falls as memory lengthens and strengthens,
    and rumination keeps negative memories from fading (Marsh, Hammond & Crawford 2019).
- Recursion has content at the boundaries of a life and of information, and under
  nonlinearity. P2 makes linear recursion a reparametrization of foreseen lives on ℤ;
  surprises, dread asymmetry (D5) and loss-averse news make it bite. [synthesis]

**Sketch: recollection news.** [speculation]
- The mirror of news. `R_t[X_s]` is the remembered value at `t` of experience at `s < t`;
  the base model has perfect recall, with fading carried by the kernel weight. The memory
  term uses `R_t`, and felt changes in recollection add
  `Σ_{j≥1} ρ(j) φ_λ(R_t[X_{t−j}] − R_{t−1}[X_{t−j}])`.
- Completes a 2×2: anticipation and memory are levels, forward and backward; news and
  recollection news are changes, forward and backward.
- Recollection moves by drift (forgetting; fading affect bias), by evidence about the
  past (reminders, discoveries), and by motivated revision (repression, reinterpretation).
- Pure fading of content is absorbed into the memory kernel (P10). Only *felt* fading adds
  anything: losing a good memory is a small loss, a bad one fading a relief.
- Evidence about the past is a martingale if recollection is Bayesian, so it is neutral in
  expectation at `λ = 1` and a schedulable pain at `λ > 1`, as in N2.
- Not found in the literature as a felt term: gain-loss over revisions of the remembered
  past. Nearest: Kimball & Willis (2006, §8B) let memory of past *expectations* be
  manipulated, so that gratitude can raise elation. The ingredients are documented:
  - the backward kernel is sign-asymmetric (the fading affect bias; Walker, Skowronski &
    Thompson 2003; Hoehne & Zimprich 2024, 2025);
  - recollection drifts rosy (Mitchell et al. 1997) and is revised by reappraisal (Speer
    et al. 2021);
  - remembered rather than experienced utility drives repeat choices (Wirtz et al. 2003);
  - motivated memory sustains overconfidence against feedback (Zimmermann 2020; Huffman,
    Raymond & Shvets 2022; Walters & Fernbach 2021).
- The forward–backward asymmetry, refined. Each kind of belief is anchored differently: a
  forecast by its realization, which comes later; a recollection by memory traces, which
  are there from the start and fade. Distortion is cheapest far from the anchor: long
  before realization (optimism, which collapses into bracing near feedback) and long after
  the event (rosy retrospection, which grows as traces fade; Roy-Chowdhury 2022 finds
  reality constraints on recall loosen with time). [speculation]
  - Against a simple "cheaper backward": imagined futures are more positively biased than
    recollections (Rasmussen & Berntsen 2013; Newby-Clark & Ross 2003), and a known
    eventual reveal did not restrain recall distortion (Heath & Roy-Chowdhury 2025).
  - For the memory side of rationalization: rosy memory is how overconfidence survives
    repeated feedback, and Huffman et al. (fn. 15) suggest memory distortion as a way to
    manage disappointment.
- Costs of backward bias: reminders (Walters & Fernbach: looking up actual returns
  reduced overconfidence) and decisions (repeating experiences remembered as better than
  they were).

**The 2×2: echoes × news.** The canonical model is the recursive/recursive corner. Echoes
are direct (anticipation and memory of the felt base `u + N`) or recursive (of experienced
utility);
news is direct (about base utility) or recursive (about experienced utility). [checked where
numbers are given; `formalism/playground` spans all four]
- With `λ = 1` and linear kernels, all four are reparametrizations of one another for
  foreseen lives on ℤ (P2 and N4), so the choice shows only through boundaries of a life
  or of information, nonlinearity, and restrictions on the kernel family.
- The echo axis carries: remembered excitement and anticipated memories; present bias
  from exponential primitives (P3, P4); information aversion from dread asymmetry (D5);
  the condition `M < 1`.
- The news axis carries: how much a far-off event's news is felt now; cancellation costing
  the lost anticipation; disappointment about disappointment; the threshold `λκ < 1`.
- Signatures (`a = 0.09, α = 0.88, m = 0.05, μ = 0.75, n = 0.3, ν = 0.8, λ = 2`, unforeseen
  announcements): the news felt on hearing of a +5 event 5 / 15 / 30 periods ahead, and the
  life-sum of a plan announced and later cancelled:

  | echoes / news | jolt at 5 / 15 / 30 | cancelled plan's life-sum |
  |---|---|---|
  | direct / direct | 0.49 / 0.05 / 0.00 | +0.44 |
  | direct / recursive | 1.22 / 0.33 / 0.05 | −2.22 |
  | recursive / direct | 0.49 / 0.05 / 0.00 | +5.74 |
  | recursive / recursive | 1.55 / 0.92 / 0.57 | +1.48 |

  - Recursive news carries news about far events much further than the primitive kernel
    does; under recursive / recursive the jolt falls off slowly with distance. Recursive
    echoes keep a cancelled plan's remembered excitement; recursive news charges for the
    lost anticipation.
- A soft version replaces the corners with two reflexivity dials: echoes of
  `θ e + (1−θ) f`, with `f = u + N`, and news about `θ′ e + (1−θ′) u`. [speculation;
  unbuilt]
