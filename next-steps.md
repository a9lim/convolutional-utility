# Next steps

Plan (a9): one flagship post covering the model and the whole framework (a life, beliefs,
choices, selves); the LLM peak-end study is a follow-up. Ordered by dependency. Results live
in `formalism/` and the experiment READMEs; this file lists only what is open.

## The post

1. **Learned expectations** (`experiments/learned_expectations/`).
   - **Two channels for optimism.** Through the policy's baseline the critic's level does
     nothing detectable at batch 2048. Next: small batches, where a baseline's level should
     matter (optimistic non-committal, pessimistic committal); and a decision rule that reads
     values directly (softmax over learned move values), the classic optimism-explores case,
     against the shared state, where a high level reads as "stay".
   - **The mechanism (D8).** Left: why removing the critic's mean push on the state traps the
     honest critic. Codex's three-branch one-step diagnostic: clone weights and Adam state;
     policy gradient alone, plus the game-varying critic gradient, plus its per-round mean;
     round-2 stay logit on fixed first-round histories.
   - **Seeds.** The game agent's motivated-belief pattern is still one run.
   - **Iterated games.** Partner populations of learners rather than scripts; felt-utility
     variants (does a rosy critic make a sucker?).
   - **Evolving felt parameters.** Is `λ`'s neutrality the consolation term undoing its
     bracing (evolve `λ` with `n` fixed, and with consolation removed)? Longer lifetimes,
     where escape speed matters less; welfare (felt) against fitness (payoff) of the evolved
     populations; run-level uncertainty.
   - **Well-foundedness as a learning failure.** The canonical critic at `a = 0.3, ν = 0.8`
     (anticipation mass 1.2) diverged; map where TD on felt utility diverges against
     `M + λN < 1`.
   - **Partners** (`notes/empathy.md`, in progress). A learner that infers dependence from a
     similarity signal rather than a gate on true identity; heterogeneous strangers to break the
     `σw` equivalence; the trust game as learners (expectation-dependent honesty at `J = 0`,
     promises); donation games and the sign of `R + P − S − T`; guilt toward a partner's felt
     history in iterated play (F7).
   - **Agents not yet built.** The twin dial in hidden repeated games (cooperation in hidden
     prisoner's dilemmas); reliability (D6) and the self-Newcomb as environments; the
     observer with attention as a choice (batching, N2, D7), dread or rumination asymmetry
     (information avoidance, D5) and saturating news near the threshold; in the game
     distribution, whether the affect policy prefers not to tell games apart early (D7).
   - **Evidence gaps** (2026-10-15 audit): archive the twin-dial output and the
     anticipated-news comparison (the "84% of directions" figure has no script); report the
     consolation gap stratified by round (pooled 0.33 overstates it by a quarter or so); an
     initialization ablation for credible-plan selection (only 4 of 16 draws are
     informative); does the shared-state sign reverse on a task whose optimum is
     stay-heavy?
2. **Fit to momentary-happiness data** (`experiments/happiness/`).
   - A test that separates recursion from its rivals: forward echoes (does a rating
     anticipate the trials left, or the play's end?), or the interaction of two outcomes
     (linear echo predicts none, saturating echo some).
   - The direct felt-clock test (`audit/felt_clock.py` left it open): a fast transient plus a
     slow mood in elapsed seconds, the current trial's rating delay included, with rate
     `∝ age^−q`, against an age-specific kernel shape; calibrated on simulations with
     z-scoring, heterogeneous people and repeated draws. It separates a slower felt clock
     (Janet `q = 1`, Lemlich `q = ½`) from reactivity and persistence changing with age.
   - A multi-scale reading of the heavy tail against `M < 1`.
   - Whether `a < 0` is dread, the certainty effect, or curvature (it halves under power
     utility).
   - Slow adaptation needs step data: parked with B4 (below).
3. **Structure** `outline.md` around the spine (experience echoes; acts: a life, beliefs,
   choices; coda: selves), and the technical companion. Parked by a9 until the contents
   settle. Inputs from the second review:
   - **Hook and order.** Two reviewers independently found "experience echoes" the
     economist's way in. Candidate lead: beliefs are welfare and affect policies (the
     P(doom) example), then the past self as predictor; Act I shrinks. The answer to "why
     recursion?" should be its unique payoffs: dread-of-dread pricing information (D5), the
     news threshold (N4), surprises as information boundaries.
   - **Scope.** The reception reviewer's triage within one post: model 1.5k words, beliefs
     and affect 3k, past self 2k, anthropics 1k, limits 0.5k; James Dean, recollection news,
     rationalization, the 2×2, bistability, identity and context windows to the companion;
     the data as a paragraph, the learners as one figure (the `J` dial). The abstract
     features data and learners; the outline body has neither.
4. **Figures:** the Disneyland decomposition; primitive against effective kernels; `w(s)`
   profiles; the 2×2 signatures; the threshold's regimes and its closed form against memory
   reach; built-in bracing; a ramp-sign phase diagram in `(α, μ)`; the savoring trap.
5. **Open formal items the post touches:**
   - the sharp condition for the joint Bayesian forecast fixed point (only the sufficient
     row-sum condition is known);
   - N3 in the canonical model with sign-asymmetric memory of disappointment (the fading
     affect bias); whether built-in bracing survives forecasts that are not fully Bayesian;
   - `J` for imperfect foresight: past forecasts as noisy predictions of the policy, and
     FDT's `J` as a function of predictability;
   - D7: a comparison theorem for coarser affect filtrations under dread or rumination;
     whether fixed-past selves over-check; jointly implementable action and affect policies,
     under both constraints (credibility under a changed `G`, and leakage, whose toy is
     parked below);
   - D2 with news: the `J` identity extended by the news-forcing derivative and a stated
     reference counterfactual;
   - D5: the delusional optimist under felt news (unaware against sophisticated);
     rationalization given Bénabou's cancellation; recollection news formalized, with the
     backward version of N3; whether reflective consistency forces linear anticipation;
   - the LessWrong objections ("Not for the Sake of Happiness (Alone)", "Doublethink");
   - the coda: pin A1 against Armstrong's ADT text and Greaves 2004.
6. **Calibration gaps:** anticipation's reach within a day; vacation anticipation (Nawijn's
   gap looks like selection); news strength, lab (prediction errors about as strong as
   rewards) against events (0.1–0.3); everything about LLM strengths.
7. **Prior art for a9's academic access** (PDFs to `references/inbox/`, gitignored; I extract
   and file them):
   - Could change a claimed result: Hori 1992 (*JET* 56(2): 451–467; P4); Fels &
     Zeckhauser 2008 (*J. Risk & Uncertainty* 37(2–3): 187–197; P3, P4); Kreps & Porteus
     1978 (*Econometrica* 46(1): 185–200; D5's structure); Palacios-Huerta 1999 (*J. Risk &
     Uncertainty* 18(3): 249–269; N2); Andries & Haddad 2020 published (*JPE* 128(5); we
     have the 2017 WP).
   - Quotes and calibration: Parfit 1984, chs. 10–15 (we quote pp. 205–6, 313–14
     second-hand); Rutledge et al. 2014's SI (parameter tables, against our figure reads);
     Houben, Van Den Noortgate & Kuppens 2015 (*Psych. Bull.*, inertia meta-analysis);
     Frederick 2003 and Elster & Loewenstein 1992 (both Russell Sage chapters).
   - If decision theory joins the post: Bénabou & Tirole 2016 (*JEP* 30(3)); Eil & Rao 2011
     (*AEJ: Micro* 3(2)); Bernheim & Thomadsen 2005 published (we have the 2004 draft).
   - Nice to have: Cojuharenco & Ryvkin 2008 (*J. Math. Psych.* 52(5)); Schreiber &
     Kahneman 2000 (*JEP: General*); Stone, Schneider & Harter 2012 (*J. Positive Psych.*);
     Miller 2026 (*Synthese*).
8. **Citation gaps** (bibliography audit, 2026-10-15). Cited in core or decision docs with
   no entry: Bellman and Jevons/Bentham (only inside other entries), Janet and Lemlich 1975
   (the felt clock). Cited in notes, to verify when distilled: adaptation's Helson,
   Wathieu, Parducci, Solomon & Corbit, Brickman & Campbell, Headey & Wearing, Lucas,
   Lundstrom, Diener–Lucas–Scollon (several "from memory"), Gohberg–Krein, Coburn; the
   menu's prior art (Dato et al.; Duraj & He; Ely, Frankel & Kamenica; Todorov et al.;
   Frank; Dekel, Ely & Yilankaya; Kallsen & Muhle-Karbe; Baurdoux & Yamazaki; Jaisson &
   Rosenbaum; Charness & Dufwenberg; Lipnowski & Mathevet; Gigerenzer & Garcia-Retamero;
   Ersner-Hershfield). Load-bearing claims on abstract-only or second-hand entries:
   Kimball 1987 (P2's `β_L = 1`), Hori & Kanaya (P9), Wixted & Ebbesen (power-law
   forgetting), Bell, Loomes & Sugden and Gul (disappointment), Tversky & Griffin,
   the memory-asymmetry cluster (recollection sketch), Fredrickson & Kahneman,
   Geanakoplos–Pearce–Stacchetti, O'Donoghue & Rabin, Hardisty & Weber.

## Formal loose ends

- Write out what the docs only assert: P4's matching step for `r(0)`, the half-line `g_j`
  behind N4's `κ`, and N3-canonical's `Θ, λ̃, b*`.
- Archive the D3 news table's script (80 draws; currently a session script).
- Check the stock-form ODE numerically.
- Sign-asymmetric kernels: what survives of P6 and D3?
- The soft 2×2: reflexivity dials between direct and recursive echoes and news.
- Power-law kernels beyond P1(d).

## In discussion

- The extensions menu, `notes/extensions-menu.md`.

## Parked (a9)

- **Additive or displacement echo** (`notes/displacement.md`). A positive continuation must
  not lower welfare, which leaves additive and Z. a9 wants to explore the model further
  first, especially uncertain death and other counterfactuals. Discriminating extensions:
  the menu, section G.
- **Hedonic adaptation, B4** (`notes/adaptation.md`). Left: the Dartmouth step test and a
  frequency-principle test in the Great Brain Experiment (does a rating track the current
  payoff's rank among recent payoffs beyond its value?).
  - Dartmouth download, parked mid-way for memory pressure: approved for the Dartmouth
    College Experience Study, Zenodo record 22953080 (v2.0.0 of concept 17348144). Only
    `0040_nepal_codebook_2.csv` is in `data/dartmouth/` (md5 checked). Still to fetch and
    md5-check: `0040_nepal_ts.tsv` (25,205,478 bytes, `3edfef152aa9f0af348f8466ef9ef6e2`)
    and `0040_nepal_codebook.csv` (`c739cf843dc0eb4975fc63e59c3b8c72`), from
    `https://zenodo.org/api/records/22953080/files/<name>/content`. The test's design is in
    the note.
- **The C1 toy** (actions leaking into affect): the menu, C1.
- **A felt forecaster in a Bates world**, a separate project: `notes/bates.md`.

## Follow-up: LLMs

- Context windows and sessions as lives; instances as A1's tree.
- The peak-end design: positional weights of an end-of-episode rating identify the
  effective memory kernel; recency and duration neglect from linear memory, peak from
  salience. Integrate with the peak-end study in LLMs.
