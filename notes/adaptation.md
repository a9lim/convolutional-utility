# Hedonic adaptation (B4)

Drafting sketch, 2026-10-15. Identities checked numerically in the session scratchpad
(`adapt.py`, `b4.py`). Tags as in core.

## Candidate models

- **EMA reference on base utility.** `e_t = u_t − h r_t`, `r_{t+1} = ρr_t + (1−ρ)u_t`;
  `h ∈ [0, 1]` the completeness of adaptation. Helson's adaptation level; habit formation
  (Constantinides 1990, Wathieu 1997, via Baucells & Bellezza). *standard*
  - Telescoping: `Σ_t e_t = (1−h) Σ_t u_t + h (r_T − r_0)/(1 − ρ)`. Welfare is a level term
    plus a net-rise term. [checked]
  - Epilogue after a life at `x`: `L` periods at `y < x` add
    `(1−h) L y − h (1 − ρ^L)(x − y)/(1 − ρ)`. One period is a net loss iff `y < h x`; a long
    enough epilogue pays once `L > h(x − y)/((1−h)(1−ρ)y)`; full adaptation never. Here the
    decline is felt as negative, unlike displacement's reductio. [checked]
  - Over a life the level term dominates unless `h` is near 1: with a year's adaptation
    time and weekly periods, the two terms weigh equally only at `h ≈ 0.99`.
- **EMA reference on felt states (recursive adaptation).** `r` tracks `e`, not `u`: the
  steady state is `u/(1 + h)`, never full; full adaptation needs the non-fading memory
  `e_t = u_t − (1−ρ) Σ_{s<t} e_s` (the recursive twin of full EMA adaptation on `u`).
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

## Level, integral, derivative

- Base utility is a level term; anticipation a forward integral (+); memory a backward
  integral, positive for afterglow and negative for adaptation; news a derivative of
  forecasts. Any linear filter decomposes this way, so the presence of all three is not
  itself deep. The pattern of signs and directions is.
- A level minus a matched backward integral is a derivative: `u_t − r_t = (r_{t+1} − r_t)/(1−ρ)`.
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
