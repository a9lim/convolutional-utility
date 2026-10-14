# Next steps

Plan (a9): one flagship post covering the model and the whole framework (a life, beliefs,
choices, selves); the LLM peak-end study is a follow-up. Ordered by dependency.

## The post

1. **Decision-theory audit** (in progress): D1–D7 and A1–A2 under the canonical model
   (recursive echoes and news, rational forecasts). A self's own deviation from a forecast
   plan revises forecasts, so it is felt as news; plans become reference points, as in
   Kőszegi–Rabin personal equilibrium. Re-derive D2's dial with news, D3's stopping
   conditions, D4, D6 with both channels, A1 under loss-averse news; Codex round 4.
2. **Observer model** (the extension below), once the audit raises no open questions.
3. **Structure** `outline.md` around the spine (experience echoes; acts: a life, beliefs,
   choices; coda: selves), and the technical companion.
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
     whether fixed-past selves over-check;
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

## Extension (a9): learned expectations

- Train an agent whose reward is its own felt utility, computed from its own forecasts and
  realized against the world: Brunnermeier & Parker's well-being, learned. Expected return
  under the true environment is exactly the objective expectation of the felt life-sum.
- Observer version: random events, the agent only forecasts. Predictions to test: N3's
  bias quantile and its timing (optimism far off, bracing near); batching when attention
  is a choice (N2, D7); information avoidance under dread or rumination asymmetry (D5);
  behaviour near the threshold, with saturating news.
- Agent version: games and Newcomb-like setups. Whether gradients flow from anticipation
  rewards into the policy through its own self-prediction is D2's `J`: a stop-gradient is
  fixed-past (CDT-like), full flow is commitment, a lagged self-predictor is the graded
  case. Check prior art: Demski, "Partial agency" and "The parable of Predict-O-Matic"
  (LW 2019); Perdomo et al. 2020, performative stability against optimality; Krueger,
  Maharaj & Leike 2020, auto-induced distributional shift.
- Separate belief and affect heads give D7's two filtrations; tying them adds decision
  costs. Relevance to LLM welfare and honesty: rewards that depend on a model's own
  expectations select for motivated expectations unless affect is kept apart from belief.

## Follow-up: LLMs

- Context windows and sessions as lives; instances as A1's tree.
- The peak-end design: positional weights of an end-of-episode rating identify the
  effective memory kernel; recency and duration neglect from linear memory, peak from
  salience. Integrate with the peak-end study in LLMs.

## Formal loose ends

- Check the stock-form ODE numerically.
- Sign-asymmetric kernels: what survives of P6 and D3?
- The soft 2×2: reflexivity dials between direct and recursive echoes and news.
- Power-law kernels beyond P1(d).
