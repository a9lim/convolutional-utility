# Next steps

Plan (a9): publish the model as a standalone post first; decision theory and the LLM
peak-end study make follow-up posts. Ordered by dependency.

## Post 1: the model

1. **Canonical audit.** Re-derive or re-check the headline results under the canonical model
   (recursive echoes, recursive news `n·ν^j`), not just the reduced form:
   - P5, P6 for foreseen lives (news vanishes under perfect foresight, so they should
     carry over; confirm);
   - N3 under news over `e`; the despair threshold `λ(k_n·g)` analytically;
   - D5's dread-of-dread analytically (when does the felt forecast straddle the kink?) and
     its size.
2. **Codex review** (gaslamp, thread `conv-utility-premise`): the canonical model, the
   reduced form, N1–N4, dread-of-dread, the present-bias inversion and echo-share bill, the
   horizons and the Parfit mapping. The last review predates all of these.
3. **Close prior-art gaps** that could hit the claimed results:
   - Bernheim & Thomadsen 2005, "Memory and anticipation" (paywalled; library copy) — the
     nearest prior art for D1;
   - Hori 1992 (many-generation two-way altruism) — does it contain core P4?
   - read closely: Kimball & Willis 2006 §8, Sommervoll 2010, Cosaert & Potoms 2024 (any
     first-moment or ramp results?);
   - Fels & Zeckhauser 2008; the JPET version of Bergstrom 1999 §5; Elster & Loewenstein
     1992 (library copy); Dorsey 2015 full text;
   - D5: Bénabou & Tirole 2016 and Eil & Rao 2011 full texts (blocked so far); Kőszegi &
     Rabin 2009 §§III–IV; Rutledge 2014 full text; Halabi et al. 2022.
4. **Calibrate:** one default parameter set per natural horizon (a waking day, a life, a
   context window, a session) from the felt anchors (felt `λ` 1–2, `n` 0.1–0.3, `A > B`,
   reach scaling with event size, dread > savoring). Settle how the post treats the
   echo-share bill (patience is mostly not felt echo).
5. **Structure Post 1** in `outline.md`: the canonical equation and coefficients;
   well-foundedness; the reduced form (recursion stretches reach, quasi-hyperbolic from
   exponential primitives, the echo-share bill); centrality and shape; news and
   information (truth free in expectation, dread-of-dread, news as a schedulable pain,
   optimism against disappointment); identity (Parfit). Keep decision theory and anthropics
   to a pointer.
6. **Figures for Post 1:** the Disneyland decomposition; primitive against effective
   kernels; `w(s)` profiles; the 2×2 signatures; the despair threshold; a ramp-sign phase
   diagram in `(α, μ)`.

## Post 2: decision theory and beliefs

- Self-Newcomb (D1), the savoring trap (D3: the recursive analogue of the stopping
  conditions and the `α < μ` case; read Kőszegi 2010 §3.2 closely), reliability (D6 worked
  example with both channels), affect policies (D7: the batching rule; whether fixed-past
  selves over-check).
- Make `J` concrete for imperfect foresight: past forecasts as noisy predictions of the
  policy, and FDT's `J` as a function of predictability.
- Beliefs as welfare (D5): the delusional optimist under felt news (unaware against
  sophisticated); rationalization given Bénabou's cancellation; recollection news
  formalized, with the backward version of N3; whether reflective consistency forces linear
  anticipation; the LessWrong objections ("Not for the Sake of Happiness (Alone)",
  "Doublethink").
- Anthropics coda: pin A1 against Armstrong's ADT text and Greaves 2004.

## Post 3: LLMs

- Context windows and sessions as lives; instances as A1's tree.
- The peak-end design: positional weights of an end-of-episode rating as a direct
  measurement of the memory kernel; recency and duration neglect from linear memory,
  peak from salience; verify Liu et al. on positional use of context. Integrate with the
  peak-end study in LLMs.

## Formal loose ends

- Check the stock-form ODE numerically.
- Sign-asymmetric kernels: what survives of P6 and D3?
- The soft 2×2: reflexivity dials between direct and recursive echoes and news.
- Power-law kernels beyond P1(d).
