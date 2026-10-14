# Next steps

Plan (a9): one flagship post covering the model and the whole framework (a life, beliefs,
choices, selves); the LLM peak-end study is a follow-up. Ordered by dependency.

## The post

1. **Learned expectations** (`experiments/learned_expectations/`): built the observer, the
   scheduling agent (the `J` dial reproduces fixed-past and commitment play; exact rational
   forecasts with anticipated news), the game agent (random 2×2 games; the twin dial
   reproduces causal against evidential play) and the hidden-game agent (a felt critic: a rosy
   critic keeps it complacent through the shared state). Next:
   - **Two channels for optimism.** Built (`run_channels.py`): with the critic as the policy's
     baseline its level does nothing detectable at batch 2048, as Chung et al.'s theory
     predicts. Next: the same at small batches, where a baseline's level should matter
     (optimistic non-committal, pessimistic committal), and a decision rule that reads values
     directly (softmax over learned move values), the classic optimism-explores case, against
     the shared state, where a high level reads as "stay".
   - **The mechanism, finished.** Codex's three-branch one-step diagnostic near the plateau:
     clone weights and Adam state, apply the policy gradient alone, plus the game-varying
     critic gradient, plus its per-round mean; read the round-2 stay logit on fixed first-round
     histories. Explains why the honest critic needs its mean push to escape. A small theorem:
     under gradient flow a critic offset moves the policy at a rate set by the cross-kernel of
     value and policy gradients.
   - **Seeds for the game agent.** Equilibrium selection toward risk dominance (97% against 92%)
     and the motivated-belief pattern are single training runs; rerun over seeds.
   - **Evolving felt parameters.** Heritable `(a, m, n, λ)` in a population playing hidden
     games, selected on payoffs: does selection favor bracing? (Known in kind: the indirect
     evolutionary approach, Güth & Yaari; Dekel, Ely & Yilankaya 2007.)
   - **Well-foundedness as a learning failure.** The canonical critic at `a = 0.3, ν = 0.8`
     (anticipation mass 1.2) diverged; map where TD on felt utility diverges against
     `M + λN < 1`.
   - The twin dial in hidden repeated games (cooperation in hidden prisoner's dilemmas);
     reliability (D6) as an agent.
2. **Fit to momentary-happiness data.** Rutledge et al. 2014 model happiness as decaying sums
   of rewards, expected values and prediction errors: the direct model with linear news.
   If their data are available: does the recursive model fit better, and is `λ > 1` on
   prediction errors?
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
     whether fixed-past selves over-check; jointly implementable action and affect policies;
   - D2 with news: the `J` identity extended by the news-forcing derivative and a stated
     reference counterfactual;
   - D3: which credible plan learning selects (the agent extension);
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
- **Observer** (built): random events, the agent chooses only its beliefs, tethered by
  `KL(q ‖ p)/τ`. Still to add: attention as a choice (batching, N2, D7); dread or rumination
  asymmetry (information avoidance, D5); saturating news near the threshold.
- **Agent:** actor-critic whose critics are its felt anticipation and news (core, the RL
  reading). Environments in order: scheduling, reliability, self-Newcomb, then a
  distribution of two-player games (a9: does it learn to tell them apart?), with the payoff
  matrix given or to be inferred; the affect policy may prefer not to tell them apart early
  (D7).
  - Two switches, after Oesterheld (2019): what the reward credits (felt anticipation is
    the "overseer", conditional on the forecast or not) and what the learner credits
    (whether gradients flow from anticipation rewards into the policy through its
    self-prediction).
  - The learner's switch is known in binary form: stop-gradient gives performatively
    stable, ratifiable, CDT-like fixed points; full flow gives the optimum, EDT-like or
    Stackelberg (Oesterheld, Treutlein, Cooper & Hudson 2023; Perdomo et al. 2020; Bell et
    al. 2021; Demski's partial agency).
  - A lagged self-predictor is not the graded case: it still blocks the gradient, so the
    learner's recognized `J` is 0; the lag changes only how accurate past forecasts are,
    the actual `J`. Graded `J` needs another knob: a partial gradient weight, an outer
    loop's horizon (Krueger, Maharaj & Leike 2020), or forecast accuracy.
  - New relative to that literature: a temporal stream of felt anticipation, memory and
    news; `J` graded inside a life-sum; belief and affect heads (D7's two filtrations); the
    LLM-welfare angle.

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
