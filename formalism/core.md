# Core model

Status tags, two independent kinds. Provenance: **[standard]** textbook math · **[known: …]**
in the literature, cited · **[known in kind: …]** a close cousin is published ·
**[synthesis]** known pieces, new assembly · **[not found]** not located in the literature
passes (see `bibliography.md`): a candidate contribution, not a priority claim ·
**[speculation]**. Support: **[proved]** proof sketch here · **[checked]**
`formalism/checks.py` verifies numerically · **[numerical]** computed, not archived as a check.
Bracketed names (**[Codex]**) record whose argument it was.

## The canonical model

Recursive echoes and recursive news: anticipation, memory and news are all about experienced
utility. In causal form, for each moment `t` of a life `[0, T)`:

```
e_t = u_t                                                        base
    + Σ_{j=1}^{T−1−t} a α^j  Ê_t[e_{t+j}]                         anticipation
    + Σ_{j=1}^{t}     m μ^j  e_{t−j}                              memory
    + Σ_{j=0}^{T−1−t} n ν^j  ( Ê_t[e_{t+j}] − Ê_{t−1}[e_{t+j}] )  news
```

- `Ê_t` is the self's forecast at `t`, with `Ê_t[e_t] = e_t`. All three channels have
  geometric primitives; recursion reshapes them.
- **Linear and sign-symmetric.** Every channel weighs a gain and an equal loss alike. Kinks
  (dread outweighing savoring, memory by sign, a base kink, loss-averse news) are the
  extension at the end of this file, X1–X4, ranked by their felt evidence.
- **Forecasts are rational:** `Ê_t` is the Bayesian expectation on the self's (affect)
  information. Future news innovations have zero conditional expectation, so forecasts
  carry no expected future news (only the echoes of news already felt), and the
  playground's and `pathwise.py`'s unforeseen announcements (off-support events, revisions of
  the model rather than Bayesian conditioning) agree with Bayesian forecasts given the same
  base forecasts. [Codex, the wording]
- Welfare is the life-sum `W = Σ_t e_t`, scored by the objective expectation.
- Well-foundedness, in two parts:
  - `M = aα/(1−α) + mμ/(1−μ) < 1` bounds echo uniformly over lifespans (P1).
  - `κ < 1`, with `κ = k_n·g`, makes the felt state at every moment unique and stable for
    every revision (N4). On the half-line `κ = (n/H)(1−νμ)/(1−νq)`, with `H, q` from P4.

| coefficient | what it does | where it shows |
|---|---|---|
| `a` | anticipation strength | forward echo mass `A = aα/(1−α)`; present bias `β_L ≥ a/(1+a)` (P3, P4) |
| `α` | anticipation reach | the ramp before an event; mean reach `1/(1−α)` |
| `m` | memory strength | the afterglow; backward mass `B = mμ/(1−μ)` |
| `μ` | memory reach | how long the afterglow lasts; mean reach `1/(1−μ)` |
| `n` | news strength | the surprise when a moment arrives (`j = 0`), the size of the jolt on hearing, and the loop gain `κ` (N4) |
| `ν` | news reach | how far ahead news is felt; `ν = 0` keeps only surprise on arrival |

**The reinforcement-learning reading.** Write `V^α_t = Ê_t[Σ_{j≥0} α^j e_{t+j}]`, a value
function over experienced utility with discount `α`. Then anticipation is `a (V^α_t − e_t)`,
and news is `(n/ν) δ_{t−1}`, with `δ_{t−1} = e_{t−1} + ν V^ν_t − V^ν_{t−1}` the TD error at
discount `ν`; memory is a trace of past experience decaying at `μ`. So the canonical self is a
learner that feels its own critic and its own TD errors. [checked; known in kind: Rutledge et al.
2014's momentary happiness, expected values plus prediction errors, exponentially
forgotten; Gershman 2026's expected prediction error; the identification is synthesis]

**The reduced form.** For foreseen lives on ℤ, the canonical model is a direct model with
effective coefficients (P2, P4):
`e_t = r(0) u_t + Σ_{h≥1} (r(0) − 1/(1+a)) p^h u_{t+h} + Σ_{h≥1} (r(0) − 1/(1+m)) q^h u_{t−h}`.
- Example (`a = 0.09, α = 0.88, m = 0.05, μ = 0.75`, so `M = 0.81`): `r(0) = 1.032`,
  `p = 0.971`, `q = 0.798`. Anticipation's mean reach stretches from 8.3 to 35 periods, and
  memory's from 4.0 to 4.9. [checked] The stretch needs `M` near 1: at the felt
  calibrations (`calibration.md`, `M ≈ 0.3`) reach stretches by 21–28%.
- **Surprises are information boundaries.** A shock unknown until it arrives cannot reach
  the earlier selves who would have anticipated it, so it acts through the remaining-life
  column, `g_0 = 1/H` now and `g_j = (q−μ) q^{j−1}/H` after, not the bilateral row: with
  `a = m = 1, α = 0.3, μ = 0.2` and no news, `e_0 = 1/H = 1.088` against `r(0) = 1.215`.
  With recursive news a positive shock `D` adds its own news, and the response is
  `g D/(1−κ)`. Recursion has content here even on ℤ. [Codex; checked]
- News reduces locally, through the same remaining-life resolvent `R₊`: per unit of news
  about `h` periods ahead, `k_n′(h) = (k_nᵀR₊)_h / (1 − k_nᵀR₊ δ_0)`. Under unforeseen
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
  boundaries of a life and of information, under restrictions on the kernel family (the 2×2
  below), and under the extension's kinks (X1–X4).

## Objects

- Discrete time `t`; base utility `u(t)`; experienced utility `e(t)`.
- **Zero is hedonic neutrality**, the level of non-experience. A shift `u + c` moves `W` by
  `c Σ_s w(s)`, so linear rankings of lives of one length ignore it; comparisons across
  lifespans (P5's boundaries, A1's death branches), P8's sign condition and the extension's
  level kinks (X1–X3) use it. News compares forecasts, so it does not, and a kink in news
  (X4) sits at zero revision of its forecasted variable, which a shift of `u` leaves in
  place while the echoes are linear.
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

## Echoes: P1–P10

**P1. Well-foundedness of R (nonnegative kernels).** [standard; known: Bergstrom 1999]
- (a) Finite life: `Σ_n K_T^n` converges ⟺ `ρ(K_T) < 1` ⟺ `(I − K_T)^{-1}` exists and is
  entrywise ≥ 0. Above 1 any inverse has a negative entry (apply it to the Perron vector):
  raising base utility somewhere lowers experienced utility somewhere.
- (b) On ℤ: a bounded nonnegative resolvent exists ⟺ `M < 1`. Constant `u` gives
  `e = u/(1 − M)`, so **`M` is the echo share of steady-state experience**. [checked]
- (c) The two criteria come apart. `ρ(K_T) ≤ min_{x>0} Σ_n k(n) xⁿ`, generally `< M`
  (non-normal Toeplitz sections); one-sided kernels have `ρ(K_T) = 0`. Example
  `a = m = 1, α = 0.6, μ = 0.05`: `M = 1.55`, `sup_T ρ(K_T) = 0.419` — positive on every
  finite life, yet constant `u = 1` gives `e_mid ≈ 10¹⁹` at `T = 400`. [synthesis: a derived
  distinction, the spectral facts being standard; checked]
- Reading: `ρ(K_T) < 1` means monotone on this life; `M < 1` means bounded echo at any
  lifespan. A row sum above one does not by itself break monotonicity: one-sided and
  non-fading memory kernels are nilpotent, so every finite life is monotone, while echo can
  still grow without bound in the lifespan. [Codex]
- Structural cousin: existence and uniqueness of recursive utility turn on the spectral
  radius of a valuation operator (Borovička & Stachurski 2020, Thm. 3.1), with growth and
  discounting in place of echo.
- (d) Tails. A kernel whose tail is not summable (the simple hyperbola `1/(1+hj)` and
  heavier) has echo mass growing with lifespan, so no fixed strength keeps echo bounded
  over all lifespans. Two-sided, it can also cross the finite-life criterion. Example
  (`a = 0.09, m = 0.05`, short-run rates of `α = 0.88`, `μ = 0.75`, simple-hyperbolic
  tails): `ρ(K_T)` crosses 1 between `T = 41` and `42` and reaches 3.9 at `T = 2000`, so
  the recursive model is well-founded only up to a 41-period life. Generalized hyperbolas
  `(1+hj)^{−ω}` with `ω > 1` are summable and fine. [standard; checked]
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
  (Bellman; Bergstrom 1999 Prop. 5; Kimball 1987, abstract only). One-sided: exponential D
  ⟺ one-step R. [known; checked]
- A nonnegative one-sided R primitive reaching past one step makes the first step the
  steepest: `r(2)/r(1) = k(1) + k(2)/k(1) ≥ r(1)/r(0)`. Present bias is the signature of
  caring *directly* about more than the next moment (P3). [not found, for nonnegative
  one-sided primitives]
- Caveats: two-sided R has `r(0) > 1`, so its D-twin has a nonzero diagonal (normalizing
  keeps rankings, not cardinal levels); nonnegative D can map to sign-alternating R.
- Boundaries break the equivalence: finite sections do not commute with inversion, and an
  *unrestricted* finite-life D matrix reproduces any R. Surprises break it too: a shock
  unknown until it arrives misses the paths through earlier anticipation, so it acts
  through the remaining-life resolvent (the canonical model). Recursion has content through
  restrictions on the kernel family, boundaries of a life or of information, and the
  extension's kinks. Real agents have boundaries; the infinite horizon is the clean
  approximation.

**P3. One-sided recursion is quasi-hyperbolic.** `k(n) = aαⁿ` ⇒ `r(0) = 1`,
`r(n) = (a/(1+a))((1+a)α)ⁿ`; stable iff `(1+a)α < 1`, i.e. `M < 1`. Present bias
`β_L = a/(1+a)` out of exponential primitives. [known: Sáez-Martí & Weibull 2005 (WP 2002
§4.4, eqs. 15–17, which also give the inversion used in calibration); Galperti & Strulovici
2017 Cor. 3; checked]

**P4. Two-sided geometric recursion: closed form and generic present bias.**
[not found, provisionally: Bergstrom 1999 has the nearest-neighbour case, and Kimball 1987
(abstract only) and Hori 1992 (unread, reportedly no explicit form) are the likeliest prior
art; proved; checked]
- Let `p̄ = (1+a)α`, `q̄ = (1+m)μ` (P3's one-sided rates), `C = 1 + (1+a+m)αμ`,
  `Δ = √(C² − 4p̄q̄)`, `H = (C+Δ)/2`, `p = p̄/H`, `q = q̄/H` (both in (0,1) when `M < 1`).
  Then
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
- A single hump is a geometric-family fact (`k(±2) = 0.2`, `T = 5` is not unimodal in R:
  1.30, 1.25, 1.52, 1.25, 1.30).

**P6. Ramp theorem: shape preference is set by the first moment.**
Centered ramp `u(s) = s − (T−1)/2`; the increasing-minus-decreasing gap is `2E`.
- D, exact: `E_T = ½ Σ_{|τ|<T} k(τ)(T − |τ|) τ ≈ (T/2) M₁`. Flat kernels recover
  Loewenstein & Prelec's `(AU − RU)/2`, and Cosaert & Potoms (2024) state the qualitative
  directions (anticipation favours improvement, memory decline). [general-kernel form not
  found; checked]
- R, exact: `E_T = ½ Σ_paths (Π_i k(τ_i)) (T − S)_+ d` (`d` net displacement, `S` range
  of the zigzag). Hence `E_T/T → M₁/(2(1−M)²)`, the resolvent's first moment over two.
  Geometric closed form `E_T = L_T J_T(p) − U_T J_T(q)`,
  `J_T(x) = Σ_s ((T−1)/2 − s) xˢ`. [not found; checked]
- Finite-`T` sign. In D it is the sign of the truncated first moment
  `Σ_τ k(τ)(T−|τ|)τ`, which can differ from `M₁`'s: `a = 1, α = 0.1, m = 0.1, μ = 0.5` has
  `M₁ < 0` but `E > 0` for `T ≤ 5` (and in R). In R it is the sign of the path sum, which can differ
  from D's: `T = 6, a = 0.2, α = 0.7, m = 1, μ = 0.3` gives `E_D > 0 > E_R`. [Codex;
  checked] Equal amplitudes `a = m`: the sign is exactly `sign(α − μ)` for all `T ≥ 2`, in
  both (path reflection). [checked]
- On ℤ, `Σ_t e(t) = Σ_t u(t)/(1−M)` is rearrangement-invariant for any linear,
  translation-invariant, absolutely summable kernel (in R, with a bounded resolvent), signed
  ones included: **in a linear echo model, shape
  preference is purely a boundary effect** — a life's ends, not its slope as such. Slope
  effects as such need nonlinearity.
- Size: for `T` well beyond the kernel's reach, the gap relative to the base utility
  rearranged (`Σ|u| ≈ T²/4`) is `≈ 4M₁/T` (D) or `4M₁/((1−M)²T)` (R). Whole-life shape
  preferences are sizeable only when anticipation and memory reach a sizeable fraction of
  the life; recursion near `M = 1` lengthens the effective reach. Prediction: sequence
  preferences are strongest over short horizons. [checked; prediction speculation]
- A negative (contrast) memory kernel adds to `M₁`, favouring improvement; this is a
  linear-contrast specification, not general habit formation.
- Ramps only. Other profiles are not ranked by `M₁`: an end pulse against a start pulse
  compares `w(T−1)` with `w(0)`, echo masses. `a = 2, α = 0.2, m = 0.05, μ = 0.8` has
  `M₁ = −0.375`, so the falling ramp wins (`T = 200`: −66.9 D, −728 R), yet the unit pulse
  at the end beats the one at the start (+0.30 D, +0.60 R), unchanged at `T = 1000`. A
  slight tilt makes both profiles strictly monotone. [Codex; checked]

**P7. Each self is a lens.** Ramp tilt by evaluator (geometric, `T = 60`): the first self
prefers declining profiles, the last self improving (recency), and the life-sum tilts by
`M₁`. Where a mid-life self falls depends on the kernel: at `a = 0.09, α = 0.88, m = 0.05,
μ = 0.75` (R), rising minus falling is −100 for the first self, +56 mid-life and +71 for
the last. [numerical]

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
    μ = 0.75`, share the whole row (to 2e-5, 0.319 being rounded). For an LLM, the base-utility scale of the inputs and the
    map from rating to experience are further assumptions. [synthesis; Codex]

**P8. James Dean effect from contrast memory.** [numerical; speculation as psychology]
- With a negative memory kernel, appending mildly positive years after a peak lowers the
  life-sum, not just the mean (D and R): each added year's own `u` is outweighed by its
  contrast with the remembered peak. With nonnegative kernels, `ρ(K_T) < 1` and
  nonnegative experience it cannot happen. A positive year can still lower the life-sum by
  remembering a bad past (base history `(−100, 10)`, `m = 0.1, μ = 0.5`: appending `0.1`
  adds `−2.15` in R, `−1.90` in D), but that is the past's weight, not contrast. [Codex]
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
  boundary data, so, if it maximizes its current experience, its decision weights are the
  first row of the remaining-life resolvent — a newborn's. A self maximizing the remaining
  life-sum uses its column sums instead (decision.md, `J = 0`).
- With correct foresight the realized path equals the full fixed point, so P5–P8 stand as
  rankings of foreseen lives.
- Decision weights are stationary until the last few kernel widths before death. On the
  half-line row, `r(0) = 1/H` and `β_L = 1 − H/(1+a)`, which is P4's formula evaluated
  at that row's `r(0)`. [Codex; checked]
- Decision theory under this split: `decision.md`.

**P10. Identification.** [standard] Absent restrictions on `k` or independent measurement of `u`,
any `e` is fit by `u = (I − K)e`. The kernel explains something only once it is pinned by
data or by a structural family.

## Felt news: N1–N4

The canonical model's news is over experienced utility (N4). N1–N3 are stated first for news
over base utility, the comparison model; N3 is then redone in the canonical model. News is
linear; loss-averse news is X4.

**Objects.** [Kőszegi & Rabin 2009's news utility, linear, in kernel form]
- Felt news: `N_t = Σ_{j≥0} k_n(j) (Ê_t[u_{t+j}] − Ê_{t−1}[u_{t+j}])`. `Ê_t` is the felt
  forecast; `k_n(j)` weighs news about `j` steps ahead.
- `j = 0` is realization: elation or disappointment against the last forecast. This is the
  disappointment term. Classical disappointment theory is its static, realization-only
  case, with the reference point set by the lottery (Bell 1985, kinked; Loomes & Sugden
  1986, symmetric; Gul 1991, asymmetry as a parameter); the kinked versions are X4.
- The felt base `f = u + N` replaces `u`: D is `e = (I+K)f` in the causal form, R is
  `e = f + Ke`. News is felt, anticipated, and remembered.
- `N` depends only on forecasts of `u`, so well-foundedness is unchanged (P1).
- News can instead be over experienced utility (N4). The full term, with echoes over
  `X = f` (direct) or `X = e` (recursive) and news over `Y = u` or `Y = e`:
  `e_t = u_t + Σ_{j≥1} k(j) Ê_t[X_{t+j}] + Σ_{j≥1} k(−j) X_{t−j} + Σ_{j≥0} k_n(j) ΔÊ_t[Y_{t+j}]`:
  base, anticipation, memory, news. Direct echoes still anticipate and remember news,
  through `f`. A recollection-news term would complete the pattern (sketch below).
- `formalism/pathwise.py` simulates a life pathwise and plots the four components.

**N1. News is neutral in expectation.** With Bayesian forecasts, `E_{t−1}[N_t] = 0`:
expected welfare equals the base model's, and news adds only pathwise swings. [standard;
checked]

**N2. News is priced through life weights.** [life-weight form not found; checked]
- In D and R with Bayesian forecasts, `E[W] = E[W_base] + Σ_r w(r) E[N_r]`, with `w` the life
  weights of P5: the tower property, then the linear echo equation. It holds for news over
  `e` too, where `E[N_r]` is endogenous. [checked; Codex for news over `e`]
- Linear news has `E[N_r] = 0` (N1), so the identity prices nothing here. It is where a
  kink's price lands: the expected news it creates, times the life weight of the moment it
  is felt (X4, news as a schedulable pain).

**N3. Optimism against disappointment.** Stated first in the comparison model (D, news over
`u`, one event), then in the canonical model. [known in kind: Gollier & Muermann 2010,
anticipated payoff rising with savoring weight; Brunnermeier & Parker 2005; kernel-form
condition not found; checked]
- Setup: the felt forecast of `u_s` is biased by `b` over the window before realization.
  The agent believes itself unbiased, and welfare is scored objectively. Let `A` be the
  anticipation mass on the event over the window, `B` the memory mass after it, and `Z`
  the forecast error (symmetric, continuous).
- `dW/db = A − k_n(0)(1+B)` at every bias: a rosy forecast buys `A` of anticipation per
  unit and pays `k_n(0)` of disappointment at realization, felt and remembered. With
  `Θ = A / (k_n(0)(1+B))`, optimism pays iff `Θ > 1` and lowering expectations iff `Θ < 1`.
- So the hedonic objective has no interior optimum: for `Θ ≠ 1` welfare grows without bound
  as the bias runs one way (optimism or pessimism), and at `Θ = 1` every bias is equally
  good. Decision costs, plausibility, or sophistication (Bénabou's cancellation) must bound
  it. Brunnermeier &
  Parker's interior optimum is that bound: their optimism gain is first-order and its
  decision cost second-order. Felt disappointment is first-order too, which turns the sign
  of the hedonically optimal bias into a parameter question. Loss-averse news (X4) adds
  curvature and an interior optimum.
- Reading: optimism about long-awaited events (large `A`), bracing for events at short
  notice or with heavily remembered disappointment. As an event nears, the remaining window
  shrinks and the optimum moves toward bracing, but a self-revised forecast is itself felt
  as news. [speculation]
- Evidence. Bracing is documented: estimates fall as feedback nears, with no new
  information (Shepperd, Ouellette & Fernandez 1996; van Dijk, Zeelenberg & van der Pligt
  2003, who state the remote-savor, imminent-brace timing). Its hedonic payoff is not.
  Golub et al. (2009) find a dread cost and no post-event cushion, with expectation effects
  gone within minutes; Shepperd & McNulty (2002) find a cushion; Marshall & Brown (2006)
  find little benefit. If disappointment fades that fast, `k_n(0)` is brief and `B` small.
- Level anticipation, news and memory are not separately identified from behaviour (P10;
  Eliaz & Spiegler's ordinality result).
- **In the canonical model** (recursive echoes, news over `e`, Bayesian forecasts). [not
  found; checked]
  - Every revision at realization is proportional to `g`, the remaining-life column, so the
    felt news solves `N = κ(y + N)`, with `y` the surprise: `N = κ̃ y`, `κ̃ = κ/(1−κ)`. The
    loop makes disappointment dearer, and elation with it.
  - `dW/db = 𝒜 − (1ᵀg) κ̃`. Here `𝒜 = w_s − 1ᵀg` is the value of foreseeing the event (its
    planner weight minus its weight as a surprise), and `1ᵀg` is the life value of a unit
    felt at realization. With `Θ = 𝒜/((1ᵀg) κ̃)`, optimism pays iff `Θ > 1`: again no
    interior optimum. The anticipated news is zero in the self's own forecasts; under a
    biased forecast the objectively expected realized news is not, and it is what the slope
    charges. [Codex]
  - The comparison model is the case without the loop: `κ̃ → k_n(0)`, `𝒜 → A`,
    `1ᵀg → 1 + B`. With a fixed reference and one period this reduces to
    `W′(0) = A − n/(1−n)`. [Codex]
  - At the felt calibrations an event mid-life gives `Θ = 1` at the day defaults (exactly
    indifferent, since there `n = A` and `ν = α`) and `0.7` (life), toward pessimism. Beliefs
    free to move run until something bounds them (plausibility, decisions, sophistication),
    and that bound sets the bias actually seen. [checked]

**N4. News over experienced utility.** `N_t = Σ_{j≥0} k_n(j) (Ê_t[e_{t+j}] − Ê_{t−1}[e_{t+j}])`:
news about how your life will *feel*, including your anticipations and memories. The
`j = 0` term compares `e_t` with its own forecast, so news is self-referential.
[known in kind: Kimball & Willis 2006 §8 put elation over news about lifetime utility into
flow utility and solve for both simultaneously; linear neutrality (Prop. 2) needs
coefficients summing below one, a solvability condition. Theirs is decision utility kept
apart from happiness; the felt reading, the echo kernels and the loop gain's closed form are
new here. Formal cousins: Skiadas 1998; Routledge & Zin 2010; Artstein-Avidan & Dillenberger
2015; Andries & Haddad 2020]
- Neutral in expectation, equal to base R. [checked] Linear, so it reduces to news over `u`
  with the locally echoed kernel `k_n′` (the canonical model). [checked under unforeseen
  announcements]
- Reach: news about a far event is felt now through the near-term echo (tomorrow you will be
  looking forward to it), so a short `k_n` suffices. Cancelling a plan costs the
  anticipation and the anticipated memories too.
- **Well-foundedness.** Let `g` be the felt-now column of the remaining-life resolvent (how
  a unit felt now moves forecasts of later experience), and `κ = k_n·g`. On the half-line,
  `κ = (n/H)(1−νμ)/(1−νq)`, and finite remaining lives give a nondecreasing sequence toward
  it. [proved; checked; Codex verified] With `m = 0`, `κ = n`, the `j = 0` self-reference
  alone, whatever the anticipation. Memory adds the rest of the loop, since a felt state
  is remembered and so moves forecasts of later experience; anticipation enters only
  through `H` and `q`.
  - The felt news solves `s = Σ_j k_n(j)(d_j + s g_j)`, so `s = k_n·d / (1 − κ)`. Stability
    is under the feedback iteration `s ← k_n·d + κ s`, with nonnegative kernels.
  - `κ < 1`: a unique, stable felt state for every revision, the revision's direct news
    amplified by `1/(1−κ)`.
  - `κ > 1`: one root, unstable and with perverse comparative statics (good news felt as
    bad). `κ = 1`: no solution when `k_n·d ≠ 0`, every `s` when `k_n·d = 0`. [Codex]
  - The threshold falls as memory lengthens and strengthens. Kinked or saturating news has
    regimes of its own around it (X4).
- Recursion has content at the boundaries of a life and of information. P2 makes linear
  recursion a reparametrization of foreseen lives on ℤ; surprises, and the extension's kinks
  (dread asymmetry, X1; rumination, X2; loss-averse news, X4), make it bite. [synthesis]

**Sketch: recollection news.** [speculation]
- The mirror of news. `R_t[X_s]` is the remembered value at `t` of experience at `s < t`;
  the base model has perfect recall, with fading carried by the kernel weight. The memory
  term uses `R_t`, and felt changes in recollection add
  `Σ_{j≥1} ρ(j) (R_t[X_{t−j}] − R_{t−1}[X_{t−j}])`.
- Completes a 2×2: anticipation and memory are levels, forward and backward; news and
  recollection news are changes, forward and backward.
- Recollection moves by drift (forgetting; fading affect bias), by evidence about the
  past (reminders, discoveries), and by motivated revision (repression, reinterpretation).
- Pure fading of content is absorbed into the memory kernel (P10). Only *felt* fading adds
  anything: losing a good memory is a small loss, a bad one fading a relief.
- Evidence about the past is a martingale if recollection is Bayesian, so it is neutral in
  expectation, as in N1, and a schedulable pain under a loss-averse kink (X4).
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
- All four are reparametrizations of one another for foreseen lives on ℤ (P2 and N4), so
  the choice shows only through boundaries of a life or of information, restrictions on the
  kernel family, and the extension's kinks.
- The echo axis carries: remembered excitement and anticipated memories; present bias
  from exponential primitives (P3, P4); information aversion from dread asymmetry (X1, D5);
  the condition `M < 1`.
- The news axis carries: how much a far-off event's news is felt now; cancellation costing
  the lost anticipation; disappointment about disappointment; the threshold `κ < 1`.
- Signatures (`a = 0.09, α = 0.88, m = 0.05, μ = 0.75, n = 0.3, ν = 0.8`, unforeseen
  announcements): the news felt on hearing of a +5 event 5 / 15 / 30 periods ahead, and the
  life-sum of a plan announced and later cancelled (the playground's "cancelled" preset:
  `+4` at 35, announced at 5, cancelled at 28, `T = 50`; `model.js` `simulate().lifeSum`;
  the jolts are all gains, so loss-averse news leaves them unchanged):

  | echoes / news | jolt at 5 / 15 / 30 | cancelled plan's life-sum |
  |---|---|---|
  | direct / direct | 0.49 / 0.05 / 0.00 | +0.73 |
  | direct / recursive | 1.22 / 0.33 / 0.05 | +0.21 |
  | recursive / direct | 0.49 / 0.05 / 0.00 | +6.02 |
  | recursive / recursive | 1.55 / 0.92 / 0.57 | +5.56 |

  - Recursive news carries news about far events much further than the primitive kernel
    does; under recursive / recursive the jolt falls off slowly with distance. Recursive
    echoes keep a cancelled plan's remembered excitement; recursive news charges for the
    lost anticipation. Loss-averse news (X4, `λ = 2`) charges the cancellation more: +0.44,
    −2.22, +5.71 and +1.48.
- A soft version replaces the corners with two reflexivity dials: echoes of
  `θ e + (1−θ) f`, with `f = u + N`, and news about `θ′ e + (1−θ′) u`. [speculation;
  unbuilt]

## Sign asymmetries: X1–X4 (extension)

The canonical model weighs a gain and an equal loss alike in every channel. Each channel can
be given a sign. Base utility, anticipation and memory are levels, so their kinks sit at
hedonic zero (Objects), which choices alone do not identify without structural assumptions
(P10): a shift of `u` moves the kink against the outcomes. Felt measurement does most of the
work. News is a change, so its kink sits at zero revision of its forecasted variable, which a
shift of `u` leaves in place while the echoes are linear. The structurally cleanest kink,
news's, has the weakest felt support. The order below is by felt evidence (`calibration.md`),
a synthesis across unlike measures, not an identified ordering of coefficients. [synthesis;
Codex on the qualifiers]

- **The extended equation.** Write `x⁻ = max(−x, 0)`. Echo strengths by sign, `a⁺, a⁻`
  forward and `m⁺, m⁻` back (with reaches `μ⁺, μ⁻` when memory fades differently by sign),
  act on the positive and negative parts of the echoed `X`; a base kink is
  `u − (λ_u − 1)u⁻`; loss-averse news is `φ_λ(x) = x − (λ−1)x⁻`, so `x` for gains and `λx`
  for losses.
- **Well-foundedness.** Each kinked echo is Lipschitz with its larger strength, and on a
  fixed Bayesian tree a conditional expectation does not expand the sup norm. So
  `L = max(a⁺, a⁻) α/(1−α) + Σ_{j≥1} max(m⁺(μ⁺)^j, m⁻(μ⁻)^j) < 1` makes the felt fixed point
  with given news forcing a sup-norm contraction: one bounded adapted felt path. Sufficient,
  not sharp. [standard argument; synthesis; Codex on the reach-aware form]
  - It does not settle the system with endogenous news. Kinked news has `λκ < 1` locally
    (X4), with `κ` from the linear resolvent, which kinked echoes change. For the joint fixed
    point, a sufficient bound is `L + 2λ sup_t Σ_j k_n(j) < 1`, since the forecast difference
    `E_t − E_{t−1}` can have sup-norm operator norm near 2; the sharp condition is open.
    [Codex]

**X1. Dread outweighs savoring** (`a⁻ > a⁺`). The best-supported asymmetry.
- Evidence. Within-person survey coefficients put dread at 6.19 times savoring (Dawson &
  Johnson 2026, UK household panel; "worse off" and "better off" are not matched in size,
  so it is not a clean ratio of strengths); they split it into the anticipated outcome's
  own asymmetry and a stronger feeling (`λσ ≈ 6` with `λ ≈ 2`, so `σ ≈ 3`). Lab studies find
  substantial dread and little savoring (Hardisty & Weber 2020). Anticipatory emotion
  averages `+0.35` on `−3..+3`, with 38% fear or anxiety (Barsics et al. 2016). Pleasant
  mind-wandering, mostly about past and future, leaves momentary happiness where on-task
  focus has it, while unpleasant mind-wandering costs a lot (Killingsworth & Gilbert 2010).
- In D, a kink on outcomes keeps anticipation linear in beliefs: the convolution splits into
  one on `u⁺` and one on `u⁻`, and information timing stays neutral. In R a self anticipates
  its own later felt states, which contain later forecasts, so the kink lands on a belief and
  prices information, with an exact identity (decision.md D5). Coarser affect filtrations
  were better in every case checked (D7).

**X2. Memory by sign** (`m⁺, m⁻`; `μ⁺, μ⁻`).
- Two documented asymmetries pull apart. Negative affect fades faster than positive, the
  fading affect bias (in ~30% of memories against ~12%; Hoehne & Zimprich 2024; Walker,
  Skowronski & Thompson 2003), so `μ⁻ < μ⁺`. Rumination keeps negative memories from fading
  (Marsh, Hammond & Crawford 2019), so `m⁻ > m⁺` near the event. The ratio of loss to gain
  echo is then a function of lag, `(m⁻/m⁺)(μ⁻/μ⁺)^j`: above one early, below one late.
  [synthesis]
- In momentary-happiness data a loss's echo starts stronger and fades faster: the ratio is
  1.13 one trial on, 1.03 at ten and 0.94 at twenty, crossing one near thirteen, with
  per-trial decay 0.942 [0.937, 0.944] for losses against 0.952 [0.949, 0.954] for gains.
  Over a play the two echo masses come out alike (ratio 1.02 [0.99, 1.05]). [data:
  `experiments/happiness/audit/sign_kernels.py`]
- Sustained losses are adapted to more slowly and less completely than gains
  (`notes/adaptation.md`, parked): a kink on the contrast lobe rather than on the echo.
- Results: rumination prices information like dread (D5). Remembered disappointment, `B` in
  N3, shrinks only if its integrated weight falls: faster fading against a stronger start
  can leave it equal, as in the data, and then N3 does not tilt. [Codex]

**X3. A base kink** (`λ_u > 1`).
- Kőszegi & Rabin put none in consumption utility: all of their loss aversion is gain-loss
  utility, which is news here.
- In momentary-happiness data a certain loss lowers happiness 1.20 [1.18, 1.23] times as
  much as an equal certain gain raises it, whether or not a cost of having gambled or
  curvature is allowed, and 1.28 [1.25, 1.31] at the outcome itself once memory is split by
  sign. In Forbes & Bennett's lotteries the ratio is 1.14–1.16, and 0.95–1.00 once the chosen
  lottery's spread is controlled; every payoff there is a lottery's. [data:
  `audit/risk_cost.py`, `audit/sign_kernels.py`, `audit/forbes_shapes_risk.py`]
- Not separable from news in that design: the kink sits at zero points, which is also about
  where a player's forecast stands before each trial, so the same asymmetry reads as
  loss-averse news when the offer is revealed. [synthesis]
- Worsening finances lower life satisfaction 2.05 times as much as improving ones raise it
  (Dawson & Johnson 2026; the categories are not matched in size).
- A base kink is a change of `u`: it moves welfare levels and prices no information, in D
  or R.

**X4. Loss-averse news** (`φ_λ`, `λ > 1`). The least-supported felt asymmetry.
- Evidence. Choice-revealed loss aversion is about 2: `1.96` (`1.74` bias-corrected; Brown
  et al. 2024 meta-analysis), and structural news utility `λ ≈ 2.3`–`3.0` (Pagel 2017, 2018).
  Felt asymmetries are smaller. Losses are not experienced as worse than equal gains, a
  forecasting error (Kermer et al. 2006); disappointment exceeds elation 1.4–1.9 times
  (Mellers et al. 1997); surprise asymmetry 1.0–1.45 (Shepperd & McNulty 2002). In
  momentary-happiness data felt news is 1.0–1.2 once a felt cost of the chosen gamble's
  spread is allowed; in 50/50 gambles the two are the same regressor. [`calibration.md`;
  data]
- **News is a schedulable pain** (extends N2). [life-weight form not found; checked]
  - With news over `u`, `E[N_r] = −(λ−1) Σ_j k_n(j) E[(Δ_{r,j})⁻]`, where `Δ` is the forecast
    revision, so a revision costs its expected loss part times `λ − 1` and the life weight
    of the moment it is felt.
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
    prior forecast, a positive feedback with a threshold (below).
  - Timing: a clumped revision at `r` about `u_s` costs in proportion to `k_n(s−r) w(r)`.
    [Kőszegi & Rabin's fn. 12 notes the interplay of discounting with `γ`'s decay]
    - Decaying `k_n` favours early news (Kőszegi & Rabin's `γ < 1`).
    - Clumping and timing can pull apart. With fast-decaying `k_n`, a piece felt early,
      while its event is far off, can cost less than waiting to clump it: `u_2 = 2Y_1 + Y_2`
      with `Y_1` known at 0 and `Y_2` at 1, `k_n(j) = 0.1^j`, `λ = 2`, costs 0.06 felt
      piecemeal, 0.10 clumped at 1, and 1 at realization. The affect schedule is a weighted
      scheduling problem. [Codex]
    - With flat `k_n`, the flat interior of `w` makes timing neutral. Near the ends, news
      goes where `w` is lowest (the P5 deficits), so the direction is anticipation against
      memory again.
  - Anxiety and remembered disappointment are the two halves of `w(r)`: pending news is
    anticipated, past news remembered.
- **An interior optimum for optimism** (extends N3, comparison model). [quantile not found;
  checked]
  - `dW/db|₀ = A − k_n(0)(1+B)(1+λ)/2`. With `Θ = A / (k_n(0)(1+B))`, the optimal bias
    satisfies `P(Z < b*) = (Θ−1)/(λ−1)` for `1 < Θ < λ`. Calibration is optimal only at
    `Θ = (1+λ)/2`; `Θ ≤ 1` gives unbounded pessimism and `Θ ≥ λ` unbounded optimism.
- **A calibrated Bayesian is already braced** (extends N3, canonical model). [not found;
  checked. Flagged: it needs `λ > 1`, the least-supported asymmetry. Whether skew from
  sign-asymmetric echoes (X1, X2), felt experience concave in the outcome, gives an analogue
  is open.]
  - The felt news at realization solves `N = κ φ_λ(y + N)`. Hence `N = κ̃ y` for gains and
    `λ̃κ̃ y` for losses, where `λ̃ = λ(1−κ)/(1−λκ) = 1 + (λ−1)/(1−λκ)`. The loop amplifies
    loss aversion, without bound as `λκ → 1`, and leaves `λ = 1` fixed; all of it for
    `λκ < 1`, where the identity is defined and the branches are the gain and loss ones.
  - The reference point is the forecast of felt experience, which already contains the
    expected news `N̄ = E[ψ(Z − N̄)] < 0`, with `ψ` that piecewise-linear map. A calibrated
    Bayesian is already braced: unbiased, the realized news is a loss with probability
    `P(Z < N̄) < ½` (about 0.3 in the checks). This is an accurate forecast of negatively
    skewed felt experience, not pessimism about `Z`.
  - `dW/db|₀ = 𝒜 − (1ᵀg) κ̃ [1 + (λ̃−1) P(Z < N̄)]`. Optimum:
    `P(Z < b* + N̄) = (Θ−1)/(λ̃−1)` with `Θ = 𝒜/((1ᵀg) κ̃)`, for `1 < Θ < λ̃`; `W″ < 0`, so it
    is the unique global optimum, and the corners are unbounded pessimism (`Θ ≤ 1`) and
    optimism (`Θ ≥ λ̃`). [Codex verified]
  - The comparison model is the case without the loop (`λ̃ → λ`, and the news reference no
    longer contains anticipated news: `N̄ → 0` there, though anticipated news still enters
    welfare). With a fixed reference and one period this reduces to Codex's
    `W′(0) = A − (n/2)(1/(1−n) + λ/(1−λn))`.
  - At `λ = 1.5` and the felt calibrations the interior band `1 < Θ < λ̃` is narrow
    (`λ̃ ≈ 1.6`–`1.8`): the day's `Θ = 1` is its lower edge, and `n = 0.1 = A/λ` puts the life
    on the optimism corner's edge (`Θ ≈ λ̃`, which side depends on rounding). [checked]
  - Reading: the loop makes disappointment dearer and the built-in bracing makes it rarer.
    Near the threshold it is the felt reference that sinks: `b* + N̄ → −∞` while the
    optimal bias in beliefs about the outcome can stay bounded, even tend to 0 (`λ = 2`,
    `𝒜/(1ᵀg) = 2`: `b* = −0.77, −0.85, −0.69` as `κ → ½`). [Codex; reading speculation]
- **The loop past its threshold** (extends N4). [known in kind: Kimball & Willis 2006 §8E,
  p. 43: with a kink the fixed point is unique "since the maximum slope of θg is θψ<1",
  sufficient, with `ψ` a factor for the extra difficulty of processing bad news. Their gain
  function is bounded, so a solution survives beyond it, and they do not discuss what lies
  beyond. The regimes are new here.]
  - Genuinely different from news over `u`: a revision is felt across the whole echo path,
    so losses are amplified by `λ̃` against gains for a revision shaped like `g`; with flat
    `k_n` an early revision changes many forecasts, and late information is preferred, while
    with decaying `k_n` the ranking is mixed. [checked]
  - The felt news solves `h(s) = s − Σ_j k_n(j) φ_λ(d_j + s g_j) = 0`, convex and piecewise
    linear with end slopes `1 − λκ` and `1 − κ`. [proved; Codex]
  - `λκ < 1`: a unique, stable felt state for every revision. The threshold is necessary
    for that guarantee, not for bare uniqueness.
  - `1/λ < κ < 1`: a bad revision (every component `≤ 0`, some news-relevant one `< 0`) has
    no felt state, and the loop runs away. A good one has two: the normal state, stable,
    and a lower one with feedback slope above 1 (`λκ` when every revised component is on
    the loss branch), unstable. The lower one is a tipping point: pushed below it, the felt
    state runs away. Mixed revisions generically have none or two (one only at tangency);
    degenerate ones can have a whole interval (`g = (1, ½)`, `k_n = (4/9, 2/9)`,
    `d = (−1, 4)`, `λ = 2`). A zero revision has the single root 0. [proved; checked; Codex]
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
- **The RL reading, kinked.** News is `(n/ν) φ_λ(δ_{t−1})` when the horizon revisions share
  a sign; a critic that kinks the aggregate TD error agrees with the per-horizon kink only
  then (`experiments/learned_expectations/`).
- **Choice** (`decision.md`): plans as reference points (D3), flaky or self-enforcing
  policies (D6), the affect schedule and the cost of leaks (D7), rationalization as hedonic
  arbitrage (D5). Recollection news at `λ > 1` is a schedulable pain too (sketch above).
