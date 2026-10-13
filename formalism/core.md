# Core model

Status tags: **[standard]** textbook math · **[known: …]** in the literature, cited ·
**[not found]** not located in the lit pass (see `bibliography.md`), so possibly new ·
**[checked]** `formalism/checks.py` verifies numerically · **[proved]** proof sketch here.

## Objects

- Discrete time `t`; base utility `u(t)`; experienced utility `e(t)`.
- Kernel `k(τ)`, `k(0) = 0`: weight at `t` on the thing at `t + τ`. `τ > 0` anticipation,
  `τ < 0` memory. Mass `M = Σ_τ k(τ)`. First moment `μ₁ = Σ_τ τ k(τ)`.
- **Direct (D):** `e = (I + K) u`. One layer of echo.
- **Recursive (R):** `e = u + K e`, so `e = (I − K)^{-1} u = Σ_n K^n u`. Entry `r(n)` sums
  over every zigzag path of anticipations and memories with net displacement `n`.
- **Finite life** `[0, T)`: `K_T`, the Toeplitz section. Life total `E = Σ_t e(t) = wᵀu`,
  with `w = 1 + K_Tᵀ 1` (D) or `w = (I − K_Tᵀ)^{-1} 1` (R) — the Katz centrality of each
  moment in the anticipation/memory graph.
- **Geometric family:** `k(n) = a β^n` for `n ≥ 1`, `k(−n) = m α^n` for `n ≥ 1`;
  `M = aβ/(1−β) + mα/(1−α)`, `μ₁ = aβ/(1−β)² − mα/(1−α)²`.
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
  `a = m = 1, β = 0.6, α = 0.05`: `M = 1.55`, `sup_T ρ(K_T) = 0.419` — positive on every
  finite life, yet constant `u = 1` gives `e_mid ≈ 10¹⁹` at `T = 400`. [checked]
- Reading: `ρ(K_T) < 1` means monotone on this life; `M < 1` means bounded echo at any
  lifespan.
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

**P3. One-sided recursion is quasi-hyperbolic.** `k(n) = aβⁿ` ⇒ `r(0) = 1`,
`r(n) = (a/(1+a))((1+a)β)ⁿ`; stable iff `(1+a)β < 1`, i.e. `M < 1`. Present bias
`β_L = a/(1+a)` out of exponential primitives. [known: Sáez-Martí & Weibull 2005 §4.4;
Galperti & Strulovici 2017 Cor. 3; checked]

**P4. Two-sided geometric recursion: closed form and generic present bias.**
[not found; proved; checked]
- Let `A = (1+a)β`, `B = (1+m)α`, `C = 1 + (1+a+m)βα`, `Δ = √(C² − 4AB)`, `H = (C+Δ)/2`,
  `p = A/H`, `q = B/H` (both in (0,1) when `M < 1`). Then
  `R(z) = (1−βz)(1−α/z) / (H(1−pz)(1−q/z))` and
  - `r(0) = (1 + βα − βq − αp)/Δ`
  - `r(n) = (r(0) − 1/(1+a)) pⁿ`, `n ≥ 1`
  - `r(−n) = (r(0) − 1/(1+m)) qⁿ`, `n ≥ 1`
- Hence **`β_L = 1 − 1/((1+a) r(0)) ∈ [a/(1+a), 1)`**: strict present bias for every stable
  parameter choice. Memory loops raise `r(0)` above 1 (anticipated remembering of now,
  remembered anticipation of now) and so *weaken* the bias.
- Proof sketch: the forward echo sum `F(n) = Σ_{τ≥1} aβ^τ r(n−τ)` obeys
  `F(n+1) = β(a r(n) + F(n))`. On the geometric tail the backward echo is
  `B(n) = c_B r(n)` with `c_B = mαp/(1−αp)`, giving `p(1 − c_B) = β(1 + a − c_B)`.
  Matching at `n = 0, 1` with `r(0) = 1 + F(0) + B(0)` gives `r(1) = (r(0) − 1/(1+a)) p`.
- Family-specific: nearest-neighbour two-sided primitives give `β_L = 1`. [known: Kimball
  1987; Bergstrom 1999 Prop. 5 for the nearest-neighbour reduction]

**P5. Life weights.**
- D: `w(s) = 1 + Σ_{t∈[0,T)} k(s−t)`. Flat interior at `1 + M`, deficits at birth
  (unanticipated) and death (unremembered). [known: Caplin & Leahy 2004, hump-shaped
  planner weights]
- R: `1 ≤ w ≤ W := 1/(1−M)`, `w → W` away from both ends, `w_R ≥ w_D` pointwise.
  Geometric closed form `w_T(s) = W − L_T pˢ − U_T q^{T−1−s}` with
  `L_∞ = W(p−β)/(1−β)`, `U_∞ = W(q−α)/(1−α)`, `c_T = (p−β)q^T/(1−βq)`,
  `d_T = (q−α)p^T/(1−αp)`, `L_T = (L_∞ − c_T U_∞)/(1 − c_T d_T)`,
  `U_T = (U_∞ − d_T L_∞)/(1 − c_T d_T)`. [not found; checked]
- A single hump is a geometric-family fact (`k(±2) = 0.2`, `T = 5` is not unimodal).

**P6. Ramp theorem: shape preference is set by the first moment.**
Centered ramp `u(s) = s − (T−1)/2`; the increasing-minus-decreasing gap is `2E`.
- D, exact: `E_T = ½ Σ_{|τ|<T} k(τ)(T − |τ|) τ ≈ (T/2) μ₁`. Flat kernels recover
  Loewenstein & Prelec's `(AU − RU)/2`. [general-kernel form not found; checked]
- R, exact: `E_T = ½ Σ_paths (Π_i k(τ_i)) (T − S)_+ d` (`d` net displacement, `S` range
  of the zigzag). Hence `E_T/T → μ₁/(2(1−M)²)`, the resolvent's first moment over two.
  Geometric closed form `E_T = L_T J_T(p) − U_T J_T(q)`,
  `J_T(x) = Σ_s ((T−1)/2 − s) xˢ`. [not found; checked]
- Finite-`T` sign is the truncated first moment and can flip: `a = 1, β = 0.1, m = 0.1,
  α = 0.5` has `μ₁ < 0` but `E > 0` for `T ≤ 5`. Equal amplitudes `a = m`: sign is exactly
  `sign(β − α)` for all `T ≥ 2` (path reflection). [checked]
- On ℤ, `Σ_t e(t) = Σ_t u(t)/(1−M)` is rearrangement-invariant for any linear,
  translation-invariant kernel, signed ones included: **in a linear echo model, shape
  preference is purely a boundary effect** — a life's ends, not its slope as such. Slope
  effects as such need nonlinearity.
- Size: for `T` well beyond the kernel's reach, the gap relative to the base utility
  rearranged (`Σ|u| ≈ T²/4`) is `≈ 4μ₁/T` (D) or `4μ₁/((1−M)²T)` (R). Whole-life shape
  preferences are sizeable only when anticipation and memory reach a sizeable fraction of
  the life; recursion near `M = 1` lengthens the effective reach. Prediction: sequence
  preferences are strongest over short horizons. [checked; prediction speculation]
- A negative (contrast) memory kernel adds to `μ₁`, favouring improvement; this is a
  linear-contrast specification, not general habit formation.

**P7. Each self is a lens.** Ramp tilt by evaluator (geometric, `T = 60`): the first self
prefers declining profiles, the last self improving (recency), a mid-life self is near
neutral, and the life-sum tilts by `μ₁`. [numerical]

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
- Felt news: `n_t = Σ_{j≥0} ν(j) μ(Ê_t[u_{t+j}] − Ê_{t−1}[u_{t+j}])`, with `μ(x) = x` for
  `x ≥ 0` and `λx` for `x < 0`, `λ ≥ 1`. `Ê_t` is the felt forecast; `ν(j)` weighs news about
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
  `e_t = u_t + Σ_{j≥1} k(j) Ê_t[X_{t+j}] + Σ_{j≥1} k(−j) X_{t−j} + Σ_{j≥0} ν(j) μ(ΔÊ_t[X_{t+j}])`:
  base, anticipation, memory, news. A recollection-news term would complete the pattern
  (sketch below).
- `formalism/pathwise.py` simulates a life pathwise and plots the four components.

**N1. Linear news is neutral in expectation.** With `λ = 1` and Bayesian forecasts,
`E_{t−1}[n_t] = 0`: expected welfare equals the base model's, and news adds only pathwise
swings. [standard; checked]

**N2. News is a schedulable pain.** [life-weight form not found; checked]
- In D and R, `E[W] = E[W_base] + Σ_r w(r) E[n_r]`, with `w` the life weights of P5. With
  `λ > 1`, `E[n_r] = −(λ−1) Σ_j ν(j) E[(Δ_{r,j})⁻]`, where `Δ` is the forecast revision.
- Clumping: `x⁻` is subadditive, so splitting a revision into pieces raises the expected
  loss. [known: Kőszegi & Rabin 2009 Prop. 1; Pagel 2018 Prop. 1, longer evaluation
  periods] Benartzi & Thaler (1995) and Gneezy & Potters (1997) are choice evidence about
  evaluation periods, not measurements of felt loss.
- Timing: a clumped revision at `r` about `u_s` costs in proportion to `ν(s−r) w(r)`.
  - Decaying `ν` favours early news (Kőszegi & Rabin's `γ < 1`).
  - With flat `ν`, the flat interior of `w` makes timing neutral. Near the ends, news goes
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
- `dW/db|₀ = A − ν(0)(1+B)(1+λ)/2`. Optimism pays locally iff `A` exceeds that; otherwise
  lowering expectations does.
- With `Θ = A / (ν(0)(1+B))`, the optimal bias satisfies `P(Z < b*) = (Θ−1)/(λ−1)` for
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
- Evidence. Bracing is documented: estimates fall as feedback nears, with no new
  information (Shepperd, Ouellette & Fernandez 1996; van Dijk, Zeelenberg & van der Pligt
  2003, who state the remote-savor, imminent-brace timing). Its hedonic payoff is not.
  Golub et al. (2009) find a dread cost and no post-event cushion, with expectation effects
  gone within minutes; Shepperd & McNulty (2002) find a cushion; Marshall & Brown (2006)
  find little benefit. If disappointment fades that fast, `ν(0)` is brief and `B` small.
- Level anticipation, news and memory are not separately identified from behaviour (P10;
  Eliaz & Spiegler's ordinality result).

**N4. News over experienced utility.** `n_t = Σ_{j≥0} ν(j) μ(Ê_t[e_{t+j}] − Ê_{t−1}[e_{t+j}])`:
news about how your life will *feel*, including your anticipations and memories. The
`j = 0` term compares `e_t` with its own forecast, so news is self-referential.
- `λ = 1`: neutral in expectation, equal to base R. [checked] Linear, so on ℤ it is news
  over `u` with an echoed news kernel, as in P2. [structural; unchecked]
- `λ > 1`: genuinely different from news over `u`. [checked]
  - Reach: news about a far event is felt now through the near-term echo (tomorrow you
    will be looking forward to it), so a short `ν` suffices. Cancelling a plan costs the
    anticipation and the anticipated memories too.
  - Size: a revision is felt across the whole echo path, so losses are amplified.
  - Timing: with flat `ν` an early revision changes many forecasts, and late information
    is preferred; with decaying `ν` the ranking is mixed.
- Well-foundedness: let `g` be the felt-now column of the remaining-life resolvent (how a
  unit felt now moves forecasts of later experience). The felt news is unique iff
  `λ (ν · g) < 1`. Beyond it, bad news has no felt state and good news has two, one of them
  a self-sustaining despairing state. [checked on an example; reading as rumination or a
  despair spiral is speculation]
- Recursion has content exactly where the model is nonlinear: P2 makes linear recursion
  a reparametrization, while dread asymmetry (D5) and loss-averse news (N4) make it bite.
  [synthesis]

**Sketch: recollection news.** [speculation]
- The mirror of news. `R_t[X_s]` is the remembered value at `t` of experience at `s < t`;
  the base model has perfect recall, with fading carried by the kernel weight. The memory
  term uses `R_t`, and felt changes in recollection add
  `Σ_{j≥1} ρ(j) μ(R_t[X_{t−j}] − R_{t−1}[X_{t−j}])`.
- Completes a 2×2: anticipation and memory are levels, forward and backward; news and
  recollection news are changes, forward and backward.
- Recollection moves by drift (forgetting; fading affect bias), by evidence about the
  past (reminders, discoveries), and by motivated revision (repression, reinterpretation).
- Pure fading of content is absorbed into the memory kernel (P10). Only *felt* fading adds
  anything: losing a good memory is a small loss, a bad one fading a relief.
- Evidence about the past is a martingale if recollection is Bayesian, so it is neutral in
  expectation at `λ = 1` and a schedulable pain at `λ > 1`, as in N2.
- The forward–backward asymmetry: every forecast meets its realization, but a recollection
  meets only reminders. A rosy bias in memory earns the memory level term with no
  realization bill; its costs are reminders and decisions (repeating experiences
  remembered as better than they were). Hedonically motivated distortion should therefore
  be cheaper backward than forward, which is where rationalization may mostly live.
  [prior art to check: rosy retrospection, the fading affect bias, remembered versus
  experienced utility in repeat choices]
