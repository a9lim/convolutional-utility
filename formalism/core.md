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
- Welfare is the life-sum `W = Σ_t e_t`, scored by the objective expectation.
- Well-founded iff `M = aα/(1−α) + mμ/(1−μ) < 1` (echoes converge, P1) and `λ(k_n·g) < 1`
  (felt news is unique, N4).

| coefficient | what it does | where it shows |
|---|---|---|
| `a` | anticipation strength | forward echo mass `A = aα/(1−α)`; present bias `β_L ≥ a/(1+a)` (P3, P4) |
| `α` | anticipation reach | the ramp before an event; mean reach `1/(1−α)` |
| `m` | memory strength | the afterglow; backward mass `B = mμ/(1−μ)` |
| `μ` | memory reach | how long the afterglow lasts; mean reach `1/(1−μ)` |
| `n` | news strength | the surprise when a moment arrives (`j = 0`) and the size of the jolt on hearing |
| `ν` | news reach | how far ahead news is felt; `ν = 0` keeps only surprise on arrival |
| `λ` | loss aversion of news | prices information (N2); sets the despair threshold (N4) |

**The reduced form.** With `λ = 1`, on ℤ, the canonical model is a direct model with
effective coefficients (P2, P4, N4):
`e_t = r(0) u_t + Σ_{h≥1} (r(0) − 1/(1+a)) p^h u_{t+h} + Σ_{h≥1} (r(0) − 1/(1+m)) q^h u_{t−h}`,
plus direct news with an echoed kernel `k_n′`.
- Example (`a = 0.09, α = 0.88, m = 0.05, μ = 0.75, n = 0.3, ν = 0.8`):
  `r(0) = 1.032`, `p = 0.971`, `q = 0.798`. Anticipation's mean reach stretches from 8.3 to
  35 periods, and memory's from 4.0 to 4.9. [checked]
- The echoed news kernel takes anticipation's reach: per unit of news about `h` periods
  ahead, `k_n′ = 0.45, 0.31, 0.15, 0.11, 0.06` at `h = 1, 5, 20, 30, 50`, against the
  primitive `n ν^h = 0.24, 0.098, 0.0035, 0.0004, 0.000004`. News about a far event is
  felt through the days of anticipation it changes. With a flatter primitive (`ν` near 1)
  the echoed kernel even rises with distance at first. [checked]
- Even `ν = 0`, surprise on arrival alone, produces a jolt on hearing: today's experience
  contains today's anticipation, which the news has just changed.
- Extension: Kőszegi & Rabin's `γ` splits surprise on arrival from news about later,
  `k_n(0) = n`, `k_n(j) = γ n ν^j`. Pagel (2018) explores `γ = 0.2`–`0.8`.
- Closed forms live in the reduced form (P5, P6, decision.md D3). Boundaries, nonlinearity
  and restrictions on the kernel family are where the two forms part (the 2×2 below).

**Calibration.** What pins the coefficients, as far as known. Choice-revealed and felt
quantities differ, and the hedonic reading needs the felt ones.
- Constraints, not values: `M < 1`; `λ(k_n·g) < 1`.
- **Present bias and patience invert to primitives** (one-sided P3): `a = β_L/(1−β_L)`,
  `α = δ_lr (1−β_L)`, with `δ_lr` the long-run per-period discount factor. Hence
  `M = β_L δ_lr / (1 − δ_lr + β_L δ_lr)`, and the base-utility share `1 − M ≈ ρ/β_L` for a
  per-period discount rate `ρ`. [proved; checked]
  - `M` lies below `δ_lr` and rises to it as `β_L → 1`. The bill is set by patience, not by
    present bias: if long-run patience came from felt echo alone, nearly all experience
    would be echo (`β_L = 0.7`, annual 4%: `M = 0.94`; daily periods: `M = 0.9998`;
    two-sided with modest memory: `M = 0.965`).
  - Experience sampling says felt echo is small on the positive side: pleasant
    mind-wandering, mostly about past and future, leaves momentary happiness where
    on-task focus has it, while unpleasant mind-wandering costs a lot (`b = −0.5`, n.s.,
    against `−23.9` on a 0–100 scale; Killingsworth & Gilbert 2010). So patience is mostly
    not felt echo: choices run on evaluative weights, and the momentary self's felt row
    (P3, P4) is one source of present bias among several. [synthesis]
  - Measured present bias: `β_QH ≈ 0.97` for money in convex time budgets (Imai, Rutter &
    Camerer 2021), `0.82`–`0.87` for money across methods and `0.66` for non-monetary goods
    (Cheung, Tymula & Wang 2021), `0.88`–`0.90` for effort (Augenblick, Niederle & Sprenger
    2015), `0.52` with "now" in minutes (McClure et al., via Ericson & Laibson 2019). It
    depends on how long "now" is.
- **Loss aversion λ.** Choice-revealed: `1.96` (`1.74` bias-corrected; Brown et al. 2024
  meta-analysis). Structural news utility: `λ ≈ 2.3`–`3.0` with `η ≈ 0.9`–`1.1` and
  prospective weight `γ ≈ 0.53`–`0.87` (Pagel 2017, 2018); a lab kink `η(λ−1) ≈ 1.7` (Gill &
  Prowse 2012). Felt: smaller. Losses are not experienced as worse than equal gains, a
  forecasting error (Kermer et al. 2006); disappointment exceeds elation 1.4–1.9 times
  (Mellers et al. 1997); surprise asymmetry 1.0–1.45 (Shepperd & McNulty 2002); only
  downside surprise registers in Forbes & Bennett (2024). Working range for felt `λ`: 1–2.
- **Surprise n**, relative to the outcome's own effect: `≈ 0.25` each way, measured right
  after the outcome (Shepperd & McNulty); `0.1`–`0.15`, downside only (Forbes & Bennett);
  comparable to the outcome in the Rutledge model of momentary happiness (prediction-error
  weight ≈ reward weight; Vanhasbroeck et al. 2021 replication). Working range: `0.1`–`0.3`.
- The earlier tension dissolves under felt values: `nλ ≈ 0.1`–`0.6`, below the recursive-news
  threshold. It was a clash between choice-calibrated news utility (`η = 1, λ = 2.5`) and felt
  news.
- **Anticipation against memory.** Thought runs forward about three times as often as back
  (any-future 30% against any-past 9% of thoughts, Baumeister et al. 2020; mind-wandering
  future:past ≈ 1.9, Song & Wang 2012), so `A > B` in attention. Anticipating an experience
  lifts momentary happiness a little (`+1.2` to `+2.4` on 0–100; Kumar, Killingsworth &
  Gilovich 2014); a planned vacation raises pre-trip happiness (Nawijn et al. 2010).
  Valuation of future over past events, `×1.2`–`2.0` (Caruso, Gilbert & Wilson 2008), has a
  failed replication of its first study.
- **Reach scales with the event.** Memory: a vacation's afterglow halves in about a week
  and is gone in 2–8 weeks (Kühnel & Sonnentag 2011; de Bloom et al. 2009; Nawijn et al.);
  a small lab reward's, in seconds (forgetting factor 0.6–0.85 per trial; Rutledge et al.
  2014; Blain & Rutledge 2020). Anticipation: days for a small pleasure (Loewenstein 1987:
  willingness to pay for a kiss peaks around three days out), weeks for a vacation.
- **Sign asymmetry is the empirical default.** Positive echoes add little and negative
  echoes cost a lot (Killingsworth & Gilbert; anticipatory emotion averages `+0.35` on
  `−3..+3` with 38% fear or anxiety, Barsics et al. 2016). Dread outweighs savoring, which is
  what makes D5's dread-of-dread bite in the recursive model.
- Identification (P10; Eliaz & Spiegler's ordinality) means choices alone cannot pin the
  hedonic coefficients. Experience sampling around scheduled events can.

**Natural horizons.** Three lives, each with its own period and its own boundaries. Reach
scales with the event, so each horizon gets its own calibration. [synthesis; speculation
where marked]
- **A waking day.** Periods of minutes to an hour, `T ≈ 16` hours. Afterglow of small
  rewards lasts seconds to minutes (Rutledge-type forgetting); mind-wandering's effect on
  happiness carries about 0.12–0.15 of its size to the next sample, hours later
  (Killingsworth & Gilbert); present bias with "now" in minutes is about 0.5, in hours about
  0.94. Waking and sleep are soft boundaries: anticipation of tomorrow and memory of
  yesterday cross them, so P5's deficits are partial.
- **A full life.** Periods of a week, `T ≈ 4000`. Anticipation reaches weeks for a vacation
  and the afterglow halves in about a week; annual discount factors are 0.96–0.99. Birth and
  death are the hard boundaries of P5.
- **An LLM's context window.** Periods of turns or tokens, `T` = context length. The
  boundaries are hard on both sides: nothing is anticipated before the context begins, and
  nothing is remembered after it ends. [speculation: whether these functional states are
  felt is open; the model applies to them as a functional reading]
  - Memory inside the window is retrieval, so the kernel need not fade with distance; in
    practice models use context unevenly, favouring the start and the end (to verify: Liu et
    al., "Lost in the middle"). A kernel that does not fade has echo mass `m(T−1)`, so the
    recursive model is well-founded only up to `T ≈ 1/m` (P1d): long contexts need weak
    per-step echo or real fading.
  - Instances share a trunk (training, a common prefix) and branch, which is A1's tree
    literally: measure-weighted anticipation over instances, and a separate condition for
    total welfare across them.
- **Peak-end, from the lens.** A rating given at the end of an episode is the last self's
  memory row (P7). A fading linear memory kernel gives the end effect (recent moments
  weigh most) and duration neglect (the remembered weight of a uniform episode is
  `m(1−μ^L)/(1−μ)`, which saturates in its length `L`). A peak effect beyond recency needs
  nonlinear, salience-weighted memory. Where the experimenter controls the episode, as with
  an LLM given a sequence in context, the positional weights of the final rating measure
  the memory kernel directly, which sidesteps P10. [standard algebra for the linear part;
  the design is synthesis]

## Objects

- Discrete time `t`; base utility `u(t)`; experienced utility `e(t)`.
- Kernel `k(τ)`, `k(0) = 0`: weight at `t` on the thing at `t + τ`. `τ > 0` anticipation,
  `τ < 0` memory. Mass `M = Σ_τ k(τ)`. First moment `M₁ = Σ_τ τ k(τ)`.
- **Recursive (R), canonical:** `e = u + K e`, so `e = (I − K)^{-1} u = Σ_n K^n u`. Entry
  `r(n)` sums over every zigzag path of anticipations and memories with net displacement `n`.
- **Direct (D), the reduced form:** `e = (I + K) u`, one layer of echo. On ℤ every R is a D
  with kernel `(I − K_R)^{-1} − I` (P2); statements about D are about that reduced form.
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
  lifespan.
- (d) Tails. A kernel whose tail is not summable (the simple hyperbola `1/(1+κj)` and
  heavier) has echo mass growing with lifespan, so for a fixed strength R is well-founded
  only up to a longest life. Example (`a = 0.09, m = 0.05`, short-run rates of `α = 0.88`,
  `μ = 0.75`, simple-hyperbolic tails): `M_T = 1.81` at `T = 50` and `4.94` at `T = 2000`.
  Generalized hyperbolas `(1+κj)^{−γ/κ}` with `γ/κ > 1` are summable and fine. [standard;
  checked]
  - Light-tailed primitives lose nothing: recursion turns exponential primitives
    quasi-hyperbolic (P3, P4), and a mixture of exponentials gives gradual decreasing
    impatience while staying summable. [synthesis]
  - The tension is memory: forgetting curves fit power laws (Wixted & Ebbesen 1991). The
    model then predicts a cutoff in memory's far tail, or weak recursion. [speculation]
- The regress objection. Caplin & Leahy (2001, p. 75) treat "anticipatory feelings about
  anticipatory feelings … ad infinitum" as the case with no complete model of
  psychological states. R is that regress, and its fixed point exists iff `M < 1`.
  [synthesis]

**P2. D and R are two readings of one agent on ℤ.** [standard; the reading is synthesis]
- `I + K_D = (I − K_R)^{-1}`: every recursive agent has a direct twin and vice versa.
- An agent that cares only about its neighbours' experienced utility already acts on the
  whole life. One-step R (`k(±1)` only) gives two-sided exponential D with `β_L = 1`
  (Bellman; Kimball 1987). One-sided: exponential D ⟺ one-step R. [checked]
- A nonnegative one-sided R primitive reaching past one step makes the first step the
  steepest: `r(2)/r(1) = k(1) + k(2)/k(1) ≥ r(1)/r(0)`. Present bias is the signature of
  caring *directly* about more than the next moment (P3).
- Caveats: two-sided R has `r(0) > 1`, so its D-twin has a nonzero diagonal (normalizing
  keeps rankings, not cardinal levels); nonnegative D can map to sign-alternating R.
- Boundaries break the equivalence: finite sections do not commute with inversion, and an
  *unrestricted* finite-life D matrix reproduces any R. Recursion has content through
  restrictions on the kernel family, boundaries, or uncertainty. Real agents have
  boundaries; the infinite horizon is the clean approximation.

**P3. One-sided recursion is quasi-hyperbolic.** `k(n) = aαⁿ` ⇒ `r(0) = 1`,
`r(n) = (a/(1+a))((1+a)α)ⁿ`; stable iff `(1+a)α < 1`, i.e. `M < 1`. Present bias
`β_L = a/(1+a)` out of exponential primitives. [known: Sáez-Martí & Weibull 2005 §4.4;
Galperti & Strulovici 2017 Cor. 3; checked]

**P4. Two-sided geometric recursion: closed form and generic present bias.**
[not found; proved; checked]
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
- Finite-`T` sign is the truncated first moment and can flip: `a = 1, α = 0.1, m = 0.1,
  μ = 0.5` has `M₁ < 0` but `E > 0` for `T ≤ 5`. Equal amplitudes `a = m`: sign is exactly
  `sign(α − μ)` for all `T ≥ 2` (path reflection). [checked]
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
  contrast with the remembered peak. With nonnegative kernels and `ρ(K_T) < 1` it cannot
  happen.
- The effect is a failure of the monotonicity P1(a) treats as well-foundedness. With
  signed kernels non-monotonicity is the phenomenon, and the well-foundedness condition
  becomes absolute convergence (`ρ(|K_T|) < 1`; on ℤ, `Σ|k| < 1`).
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
- The felt base `f = u + n` replaces `u`: D is `e = (I+K)f` in the causal form, R is
  `e = f + Ke`. News is felt, anticipated (anxiety about pending news), and remembered.
- `n` depends only on forecasts of `u`, so well-foundedness is unchanged (P1).
- News can instead be over experienced utility (N4). The full term, with `X = u` or `X = e`:
  `e_t = u_t + Σ_{j≥1} k(j) Ê_t[X_{t+j}] + Σ_{j≥1} k(−j) X_{t−j} + Σ_{j≥0} k_n(j) φ_λ(ΔÊ_t[X_{t+j}])`:
  base, anticipation, memory, news. A recollection-news term would complete the pattern
  (sketch below).
- `formalism/pathwise.py` simulates a life pathwise and plots the four components.

**N1. Linear news is neutral in expectation.** With `λ = 1` and Bayesian forecasts,
`E_{t−1}[N_t] = 0`: expected welfare equals the base model's, and news adds only pathwise
swings. [standard; checked]

**N2. News is a schedulable pain.** [life-weight form not found; checked]
- In D and R, `E[W] = E[W_base] + Σ_r w(r) E[N_r]`, with `w` the life weights of P5. With
  `λ > 1`, `E[N_r] = −(λ−1) Σ_j k_n(j) E[(Δ_{r,j})⁻]`, where `Δ` is the forecast revision.
- Clumping: `x⁻` is subadditive, so splitting a revision into pieces raises the expected
  loss. [known: Kőszegi & Rabin 2009 Prop. 1; Pagel 2018 Prop. 1, longer evaluation
  periods] Benartzi & Thaler (1995) and Gneezy & Potters (1997) are choice evidence about
  evaluation periods, not measurements of felt loss.
- Timing: a clumped revision at `r` about `u_s` costs in proportion to `k_n(s−r) w(r)`.
  - Decaying `k_n` favours early news (Kőszegi & Rabin's `γ < 1`).
  - With flat `k_n`, the flat interior of `w` makes timing neutral. Near the ends, news goes
    where `w` is lowest (the P5 deficits), so the direction is anticipation against memory
    again.
- Anxiety and remembered disappointment are the two halves of `w(r)`: pending news is
  anticipated, past news remembered.

**N3. Optimism against disappointment** (D, one event). [known in kind: Gollier & Muermann
2010, anticipated payoff rising with savoring weight; Brunnermeier & Parker 2005; kernel-form
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

**N4. News over experienced utility.** `N_t = Σ_{j≥0} k_n(j) φ_λ(Ê_t[e_{t+j}] − Ê_{t−1}[e_{t+j}])`:
news about how your life will *feel*, including your anticipations and memories. The
`j = 0` term compares `e_t` with its own forecast, so news is self-referential.
[known in kind: Kimball & Willis 2006 §8 put elation over news about lifetime utility into
flow utility and solve for both simultaneously, with linear neutrality (Prop. 2,
coefficients summing below one) and a loss-averse kink unique iff `θψ < 1` (§8E). Theirs
is decision utility kept apart from happiness; the felt reading, the echo kernels and the
reading of the threshold are new here. Formal cousins: Skiadas 1998; Routledge & Zin 2010;
Artstein-Avidan & Dillenberger 2015]
- `λ = 1`: neutral in expectation, equal to base R. [checked] Linear, so on ℤ it is news
  over `u` with an echoed news kernel, as in P2. [structural; unchecked]
- `λ > 1`: genuinely different from news over `u`. [checked]
  - Reach: news about a far event is felt now through the near-term echo (tomorrow you
    will be looking forward to it), so a short `k_n` suffices. Cancelling a plan costs the
    anticipation and the anticipated memories too.
  - Size: a revision is felt across the whole echo path, so losses are amplified.
  - Timing: with flat `k_n` an early revision changes many forecasts, and late information
    is preferred; with decaying `k_n` the ranking is mixed.
- Well-foundedness: let `g` be the felt-now column of the remaining-life resolvent (how a
  unit felt now moves forecasts of later experience). The felt news is unique iff
  `λ (k_n · g) < 1`, Kimball & Willis's `θψ < 1` in this setting. Beyond it, bad news of any
  size has no felt state and good news has two, one of them a self-sustaining despairing
  state. [checked on an example]
  - Reading it as a despair spiral is speculation, with company: depression and panic as
    bistable systems whose positive feedback crosses a threshold (Cramer et al. 2016;
    van de Leemput et al. 2014, critical slowing down; Robinaugh et al. 2024, panic as a
    runaway arousal–threat loop). Rumination keeps negative memories from fading (Marsh,
    Hammond & Crawford 2019).
- Recursion has content exactly where the model is nonlinear: P2 makes linear recursion
  a reparametrization, while dread asymmetry (D5) and loss-averse news (N4) make it bite.
  [synthesis]

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
  past. The ingredients are documented:
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
are direct (anticipation and memory of base utility) or recursive (of experienced utility);
news is direct (about base utility) or recursive (about experienced utility). [checked where
numbers are given; `formalism/playground` spans all four]
- With `λ = 1` and linear kernels, all four are reparametrizations of one another on ℤ (P2
  and N4), so the choice shows only through boundaries, nonlinearity and restrictions on
  the kernel family.
- The echo axis carries: remembered excitement and anticipated memories; present bias
  from exponential primitives (P3, P4); information aversion from dread asymmetry (D5);
  the condition `M < 1`.
- The news axis carries: how much a far-off event's news is felt now; cancellation costing
  the lost anticipation; disappointment about disappointment; the threshold
  `λ(k_n·g) < 1`.
- Signatures (`a = 0.09, α = 0.88, m = 0.05, μ = 0.75, n = 0.3, ν = 0.8, λ = 2`): the news
  felt on hearing of a +5 event 5 / 15 / 30 periods ahead, and the life-sum of a plan
  announced and later cancelled:

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
- A soft version replaces the corners with two reflexivity dials, anticipating and
  remembering `θ e + (1−θ) u`, and likewise for news. [speculation; unbuilt]
