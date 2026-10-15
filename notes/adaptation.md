# Hedonic adaptation (B4)

Drafting sketch, 2026-10-15. Identities checked numerically in the session scratchpad
(`adapt.py`, `b4.py`). Tags as in core.

## Candidate models

- **EMA reference on base utility.** `e_t = u_t − h r_t`, `r_{t+1} = γr_t + (1−γ)u_t`;
  `h ∈ [0, 1]` the completeness of adaptation. Helson's adaptation level; habit formation
  (Constantinides 1990, Wathieu 1997, via Baucells & Bellezza). *standard*
  - Telescoping: `Σ_t e_t = (1−h) Σ_t u_t + h (r_T − r_0)/(1 − γ)`. Welfare is a level term
    plus a net-rise term. [checked]
  - Epilogue after a life at `x`: `L` periods at `y < x` add
    `(1−h) L y − h (1 − γ^L)(x − y)/(1 − γ)`. One period is a net loss iff `y < h x`; a long
    enough epilogue pays once `L > h(x − y)/((1−h)(1−γ)y)`; full adaptation never. Here the
    decline is felt as negative, unlike displacement's reductio. [checked]
  - Over a life the level term dominates unless `h` is near 1: with a year's adaptation
    time and weekly periods, the two terms weigh equally only at `h ≈ 0.99`.
- **EMA reference on felt states (recursive adaptation).** `r` tracks `e`, not `u`: the
  steady state is `u/(1 + h)`, never full; full adaptation needs the non-fading memory
  `e_t = u_t − (1−γ) Σ_{s<t} e_s` (the recursive twin of full EMA adaptation on `u`).
  Adapting to felt states adapts to anticipation and memory too; Baucells & Bellezza let
  anticipation move the reference ("conceptual consumption"). The direct/recursive axis
  again, now deciding completeness. [checked] *synthesis*
- **Biphasic memory.** One signed memory kernel: fast positive afterglow, slow negative
  adaptation (a difference of exponentials). The past lifts briefly, then becomes the bar;
  net mass decides assimilation against contrast (Tversky & Griffin's endowment and
  contrast). Subsumes the EMA model; needs a stability criterion for signed kernels (the
  symbol `1 − K̂(z)` without zeros in the disk, not `M < 1`). *synthesis*
- **Forward reference (expectations).** Kőszegi & Rabin; Blain & Rutledge 2020 (momentary
  happiness tracks learning, not reward). Already in the model as felt news. Backward and
  forward references part on announced permanent changes: the forward one adapts at the
  announcement (a jolt, then nothing), the backward one after the change (contrast that
  fades). *standard in kind*
- **Asymmetric adaptation.** Faster or more complete for gains than losses (unemployment,
  disability and widowhood adapt slowly or partly; Lucas and colleagues, from memory). The
  telescoping breaks and volatility costs on its own: a backward analogue of `λ`.
  *synthesis*
- **Range-frequency.** Parducci: felt value is an outcome's range position and percentile
  in its recent context, not its distance from the mean. Negatively skewed lives (frequent
  highs, rare lows) are best, and a rare extreme low can raise everyday happiness by
  stretching the range. Nonlinear, and a genuinely different rival. *known; the kernel form
  would be synthesis*
- **Multi-timescale and power-law adaptation.** A mixture of EMAs, or a fractional
  derivative of order `h`: adaptation that never quite finishes, matching the heavy tails
  in the happiness data; the order interpolates level (`h = 0`) to change (`h = 1`).
  Neural precedent: fractional differentiation by neocortical neurons (Lundstrom et al.
  2008, from memory). *synthesis*
- **Opponent process.** Solomon & Corbit 1974: the opposing process strengthens with
  repetition (tolerance and withdrawal); a nonlinear gain on adaptation. Ties to scheduling
  (D3) and saturating echo (B3). *known*
- **Set point.** `e = s + (u − r)`: felt level reverts to a personal set point, not to zero
  (Brickman & Campbell; Headey & Wearing; Diener, Lucas & Scollon 2006, from memory). It
  separates the adaptation level from the hedonic zero that A1 and D5 use. *known; the
  consequence for the zero is synthesis*

## With the other terms

- **Adapting to base, echoes on the adapted base** (`e = R(u − h r)`, `r` the EMA of `u`):
  by parts, `W = (1−h) Σ w_t u_t + h [w_{T−1} r_T − w_0 r_0 − Σ_t (w_t − w_{t−1}) r_t]/(1−γ)`,
  with `w` the life weights. The interior is flat, so up to edge corrections where `w`
  ramps (P5's deficits), the net-rise term is multiplied by the interior weight:
  `≈ (1−h) Σ w u + h W̄ (r_T − r_0)/(1−γ)`, `W̄ = 1/(1−M)` additive, 1 under Z (555.50
  exact against 555.01 in a 300-period check). [checked]
- **Adapting to felt states, with echoes** (`e = u + Ke − h r`, `r` the EMA of `e`):
  `W = [Σ_t (u + Ke)_t + h (r_T − r_0)/(1−γ)]/(1 + h)`, exactly. The level term keeps
  weight `1/(1+h)` however strong adaptation is. [checked]
- **Linear news** adds `Σ_r w_r N_r` (N2); with flat `ν` it telescopes to the total forecast
  revision, a second change channel; zero in expectation at `λ = 1`.
- What breaks the telescoping: the loss kink, asymmetric adaptation, saturation.

## Biphasic memory in the canonical model

Notation (a9): adaptation is `c γ^j`, Latin strength and Greek reach, with mass `h = cγ/(1−γ)`.
`γ` collides with the jump kernel's decay in the happiness README and with Pagel's `γ` in
core; one of those should be renamed when this reaches core.

- **The equation.** Memory becomes one signed kernel, afterglow minus adaptation:
  ```
  e_t = u_t + Σ_{j≥1} a α^j Ê_t[e_{t+j}] + Σ_{j≥1} (m μ^j − c γ^j) e_{t−j}
            + Σ_{j≥0} n ν^j φ_λ(Ê_t[e_{t+j}] − Ê_{t−1}[e_{t+j}])
  ```
  The new term is `−h r_t`, with `r_t = (1−γ) Σ_{j≥1} γ^{j−1} e_{t−j}` the EMA of felt
  states and `h = cγ/(1−γ)` its mass, the completeness of adaptation. Biphasic when
  afterglow is faster (`μ < γ`) and stronger at lag 1 (`mμ > cγ`): positive below lag
  `ln(m/c)/ln(γ/μ)`, negative after. Masses: `A = aα/(1−α)`, `B = mμ/(1−μ) − h` (net, may be
  negative), `M = A + B`.
- **Total utility.** `W = wᵀ(u + N)`, `w = (I − K_Tᵀ)^{-1} 1` with the signed kernel. Exactly,
  `W = [Σ_t X_t + h (r_T − r_0)/(1−γ)]/(1 + h)`, with `X_t = e_t + h r_t` everything but
  adaptation (base, anticipation, afterglow, news): the level shrunk by `1/(1+h)` plus
  `h/(1+h)` of the felt reference's net rise. Steady state `e = u/(1 − A − mμ/(1−μ) + h)`.
  [checked]
- **At the life calibration with `h = ½` and a year's adaptation** (`γ = 1 − 1/52`): `M =
  −0.18`, interior weight 0.85, birth 0.71, the last year 1.14, death 1.20. Adaptation more
  than cancels echo inflation (exactly at `h = A + mμ/(1−μ)`), and P5's death deficit
  reverses: the last moments are never used as a bar. Adaptation adds `h/(1−γ)` to `M₁`
  (26 weeks here), favouring rising lives. [checked]
- **Well-foundedness for signed kernels.** Replace `M < 1` by: `1 − K(z)` has no zeros on
  the unit circle and winding number zero (Wiener for the bilateral resolvent;
  Gohberg–Krein and Coburn for half-line sections, which the causal form uses). For
  nonnegative kernels this is `M < 1`. Necessary checks: `θ = 0` gives `M < 1`; `θ = π`
  bounds overcorrection, `h(1−γ)/(1+γ) < 1 + aα/(1+α) + mμ/(1+μ)`. Pure felt adaptation is
  stable iff `h < (1+γ)/(1−γ)`, failing by oscillating overshoot. The two endpoints are not
  sufficient: in random draws `|1 − K|` is smallest strictly inside `(0, π)` 18% of the
  time. *standard; the application synthesis*
- Monotonicity is lost, as P8 says of signed kernels: here that is the phenomenon.
- For the parked question: adapting to felt states can cancel echo inflation without
  displacement. Savoring raises the bar.

## Adapting to felt states, in more detail

- The reference tracks how things felt, so you adapt to your own anticipation, afterglow and
  news as well as to circumstances. Formally a negative recursive memory kernel of mass `−h`
  on `e`; with afterglow, biphasic recursive memory.
- Incomplete by construction: steady state `X/(1+h)`; full adaptation needs the memory
  that never fades. A structural reason for the incomplete adaptation set-point studies
  report (speculation).
- Predictions that separate it from adapting to base: long anticipation raises the
  reference, so a long-savored event is felt against an elevated bar (Baucells & Bellezza's
  conceptual consumption moves the reference); savoring practices wane as their echo becomes
  baseline; a stream of good news stops lifting you (a news treadmill).

## The forward reference, in more detail

- `e_t = u_t − h_f Ê_{t−1}[u_t] + …`: the reference is what you expected for now. Under
  rational expectations `E[e_t] = (1 − h_f) E[u_t]`, and surprises are felt in full.
- Kőszegi–Rabin is not forward adaptation of levels: consumption utility plus gain-loss
  feels a predictable `u` fully. Forward adaptation replaces part of the level term.
- Separating backward from forward: an announced permanent change is absorbed at the
  announcement (forward: a jolt, then the new level at `1 − h_f`) or after it arrives
  (backward: a contrast transient that fades). Predictable cycles: forward adaptation
  shrinks their amplitude to `1 − h_f` without transients; fast backward adaptation shows
  contrast at the transitions.
- The week, from core's calibration (Helliwell & Wang): weekends are felt higher though
  perfectly predictable, Monday is no worse than midweek, Sunday shows no dip. So a level
  term exists (full forward adaptation is out), and backward adaptation is slow against a
  week (no contrast at the transitions).

## a9's spitball: base utility only through news

- Remove `u_t`; let it enter only as the realization term. As written, with the `j = 0`
  term over `e`, nothing exogenous enters and `e ≡ 0` is the unique felt state below the
  N4 threshold. The working version puts `u` there: `n φ_λ(u_t − Ê_{t−1}[u_t])`, with news
  about later periods over `u` or `e`. This is full forward adaptation.
- Forward telescoping: with linear news and flat `ν`, `Σ_t N_t = Σ_s (u_s − Ê_{−1}[u_s])`,
  the total surprise against the expectations at birth: the mirror of the backward "how far
  the reference rose". A foreseen life is felt only through its birth announcement.
- Consequences: under rational expectations expected welfare is 0 at `λ = 1` and negative
  above it, whatever the outcomes; sure outcomes are all equally good once expected, so
  choice of more over less runs only through surprising oneself (`J = 0` feels a better
  deviation as good news, the planner does not). This is why Kőszegi & Rabin keep
  consumption utility. The weekend effect refutes it as a complete model.
- Partial versions are the interesting space: level, backward and forward adaptation with
  weights `1 − h_b − h_f`, `h_b`, `h_f`, each change channel telescoping when linear.

## Level, integral, derivative

- Base utility is a level term; anticipation a forward integral (+); memory a backward
  integral, positive for afterglow and negative for adaptation; news a derivative of
  forecasts. Any linear filter decomposes this way, so the presence of all three is not
  itself deep. The pattern of signs and directions is.
- A level minus a matched backward integral is a derivative: `u_t − r_t = (r_{t+1} − r_t)/(1−γ)`.
  Full adaptation turns the level term into the derivative of the reference, which is why
  welfare telescopes. Adaptation is to realized experience what news is to forecasts: both
  are change channels, and both telescope in the life-sum when linear (linear news to the
  total forecast revision, as in the Bates note). Only their nonlinearities (the loss kink,
  asymmetric adaptation) make paths matter. *synthesis; checked*
- The RL reading completes: centered reward (adaptation is reward centering, subtracting a
  running average of past reward; Naik, Wan, Tomar & Sutton 2024), value (anticipation),
  TD error (news). Causality fixes the directions: a reference can only average the past,
  a value is about the future, an error compares them. Reward centering also removes the
  sensitivity to reward level that D8 found in the shared-state critic, so adaptation may
  be the felt trace of what a learner needs to learn well. *synthesis; the evolutionary
  reading speculative*

## Tested on the happiness data (2026-10-15)

- Within a play (Great Brain Experiment) and within a block (Forbes & Bennett), kernels
  allowed a slow negative tail stay positive: the biphasic fit collapses to the jump
  kernel, and a hyperbola minus an exponential helps only by flattening the positive tail
  (−0.026% held-out error in the Great Brain Experiment; +0.06% and −0.09% in Forbes &
  Bennett's experiments).
- Between plays the afterglow of luck is positive and heavy-tailed in wall-clock time: 45%
  of the end-of-play effect at 4 minutes, 23% at 22 minutes, 10% at 10 hours, 6% at 2.4
  days, −2% [−16, 11] at 38 days (power law, exponent about 0.3). Between Forbes & Bennett
  blocks, minutes apart, it carries nearly in full (88% and 137%, noisy).
- Caveat: the gap is chosen, and unlucky players replay sooner (65% against 42% within 10
  minutes, bottom and top fifth of luck); selection on mood would inflate short-gap
  carryover, not create or hide a negative lobe.
- What this rules out is only fast adaptation. An impulse test is nearly blind to slow
  adaptation: after a pulse of length `δ` an EMA reference with time constant `τ` leaves a
  lobe `−h(1 − e^{−δ/τ}) e^{−g/τ}` at gap `g`, at most about `(δ/g)/e` over all `τ`. For a
  5-minute play, even at `h = 1`: 27% at 4 minutes, 7.6% at 22, 0.3% at 10 hours, under
  0.1% beyond; the intervals are ±10–20%. And a positive afterglow can mask a lobe. Slow
  adaptation shows in step responses (sustained changes), where the lobe accumulates to
  `−h`, and in welfare, where its integrated mass counts in full (the telescoping). So
  biphasic memory with a slow adaptation lobe is untouched by these data. Scripts: `experiments/happiness/audit/`
  (`biphasic.py`, `carryover.py`).
