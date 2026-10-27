# Next steps

The post first: `outline.md` fixes its scope (ten sections). Everything that does not
unblock a claim there is in the companion's backlog or a follow-up line. Results live in
`formalism/` and the experiment READMEs; this file lists only what is open.

## The post

Each item names the section and claim it unblocks.

1. **Figures**, one per section, in the post's notation and on its running example.
   - §1: the holiday decomposed (redraw `formalism/pathwise.py`'s figure: a trip taken, a trip
     cancelled).
   - §2: the echo graph, with one remembered-anticipation path.
   - §3: life weights `w(s)`, direct against recursive; inset, equal-total ramps.
   - §4: the booking's news along a reassuring and a worrying path, averaging to the life
     without news; inset, partial updates under linear and loss-averse news.
   - §5: one-layer against recursive anticipation, the feedback path drawn; inset, the sign
     asymmetries ranked by felt evidence.
   - §6: information to a doer and a feeler, with the leaks.
   - §7: one pleasure scheduled by commitment and by fixed-past selves, the lost memory
     shaded; optional inset `scheduling_dial.png`.
   - §8: a branching tree with measure.
   - §9: lag-response curves (geometric, jump, power law) against the free kernel, with
     held-out error (`gbe.png` shows only two shapes, and its legend's `kappa` is `k₁`).
   - §10: the claim–assumption matrix.
2. **Evidence the post's numbers rest on.**
   - §7: archive the script behind D3's credible-plan table (80 draws; a session script
     until now, its rerun dropping the draws past the threshold), or drop its percentages.
   - §5: write out what the docs only assert: P4's matching step for `r(0)` and the
     half-line `g_j` behind N4's `κ`.
3. **Priority before claiming.** §5's two-sided present bias (P4): read Kimball 1987 (*J.
   Monetary Econ.* 20(2): 301–326) and Hori 1992 (*JET* 56(2): 451–467); until then it is
   "not found, provisionally".
   Fels & Zeckhauser 2008 (*J. Risk & Uncertainty* 37(2–3): 187–197) also bears on P3–P4.
4. **Citations the post leans on that are not read in full** (PDFs to `references/inbox/`,
   gitignored, for a9's academic access where noted).
   - LessWrong sources known only from search summaries (`bibliography.md`, the second scan):
     "Lotteries: a waste of hope" (§1's foil), "Against discount rates" (§3), lukeprog and
     Metus on two selves (§2–§3), twanvl (§5), the picoeconomics posts and Wei Dai's comment
     (§7), Byrnes's valence series (§2), McAuliffe & Shriver (§3). Save and read each before
     quoting.
   - Abstract-only or second-hand, load-bearing: Fredrickson & Kahneman 1993 (§3; or cite
     through Lim et al. 2020); O'Donoghue & Rabin 1999 (§7); Kreps & Porteus 1978
     (*Econometrica* 46(1): 185–200; §4–§5, or carry the claim on Skiadas 1998 and Epstein
     2008); Greaves 2004 (§8); Parfit 1984, chs. 10–15 (§8; quoted second-hand); Wixted &
     Ebbesen 1991 (§10's power-law forgetting); Bell, Loomes & Sugden and Gul (§4, or cite
     through Abdellaoui & Bleichrodt 2007).
   - Published versions of working papers the post cites by result: Andries & Haddad 2020
     (*JPE* 128(5)); Oster, Shoulson & Dorsey 2013 and its 2016 corrigendum (§4's example);
     Bernheim & Thomadsen 2005.
   - No entry yet: Jevons 1871 and Bentham (§1–§2, only inside other entries).
5. **A reader-order review** once the figures exist: a fresh reader (Codex, or a subagent
   briefed as a LessWrong reader) on the draft in order, against the drafting rules at the
   top of `outline.md`.

## The companion

- **Open formal items the post touches.**
  - Under loss-averse news, the sharp condition for the joint Bayesian forecast fixed point
    (only the sufficient row-sum condition is known; X4). Linear news has none to find.
  - D7: a comparison theorem for coarser affect filtrations under dread or rumination (§6
    says "every case checked"); jointly implementable action and affect policies, under both
    constraints (credibility under a changed `G`, and leakage).
  - `J` for imperfect foresight: past forecasts as noisy predictions of the policy, and FDT's
    `J` as a function of predictability (§7).
  - D2 with news: the `J` identity extended by the news-forcing derivative and a stated
    reference counterfactual.
  - N3 in the canonical model with kinked echoes at `λ = 1` (dread, memory by sign): does the
    optimism trade gain an interior optimum, as loss-averse news gives one (X4)? Whether
    built-in bracing survives forecasts that are not fully Bayesian.
  - D5: the delusional optimist under felt news (unaware against sophisticated);
    rationalization given Bénabou's cancellation; recollection news formalized, with the
    backward version of N3; whether reflective consistency forces linear anticipation.
  - §8, copies: pin A1 against Armstrong's ADT text and Greaves 2004.
- **Loose ends.** Check the stock-form ODE numerically; sign-asymmetric kernels (what
  survives of P6 and D3 under X1–X2?); the larger-side echo share as the sharp condition for
  kinked echoes, or a counterexample; the soft 2×2 (reflexivity dials between direct and
  recursive echoes and news); power-law kernels beyond P1(d).
- **Polish for publication.** Agent provenance markers out of the expository text (they stay
  in git and the ledger); one notation throughout; write out X4's `Θ, λ̃, b*`.
- **Calibration gaps.** Anticipation's reach within a day; vacation anticipation (Nawijn's
  gap looks like selection); news strength, lab (prediction errors about as strong as
  rewards) against events (0.1–0.3); everything about LLM strengths.
- **More prior art** (for a9's academic access): Palacios-Huerta 1999 (*J. Risk &
  Uncertainty* 18(3): 249–269; N2); Rutledge et al. 2014's SI (parameter tables, against our
  figure reads); Houben, Van Den Noortgate & Kuppens 2015 (*Psych. Bull.*, inertia
  meta-analysis); Frederick 2003 and Elster & Loewenstein 1992 (Russell Sage chapters);
  Bénabou & Tirole 2016 (*JEP* 30(3)); Eil & Rao 2011 (*AEJ: Micro* 3(2)); Cojuharenco &
  Ryvkin 2008 (*J. Math. Psych.* 52(5)); Schreiber & Kahneman 2000 (*JEP: General*); Stone,
  Schneider & Harter 2012 (*J. Positive Psych.*); Miller 2026 (*Synthese*).
- **Citation gaps outside the post.** Janet and Lemlich 1975 (the felt clock); the notes'
  sources, to verify when distilled: adaptation's Helson, Wathieu, Parducci, Solomon &
  Corbit, Brickman & Campbell, Headey & Wearing, Lucas, Lundstrom, Diener–Lucas–Scollon
  (several "from memory"), Gohberg–Krein, Coburn; the menu's prior art (Dato et al.; Duraj &
  He; Ely, Frankel & Kamenica; Todorov et al.; Frank; Dekel, Ely & Yilankaya; Kallsen &
  Muhle-Karbe; Baurdoux & Yamazaki; Jaisson & Rosenbaum; Charness & Dufwenberg; Lipnowski &
  Mathevet; Gigerenzer & Garcia-Retamero; Ersner-Hershfield). Abstract-only or second-hand
  behind companion claims: Kimball 1987 (P2's `β_L = 1`), Hori & Kanaya (P9), Tversky &
  Griffin, the memory-asymmetry cluster (recollection sketch), Geanakoplos–Pearce–Stacchetti,
  Hardisty & Weber.

## The data (`experiments/happiness/`)

None of these blocks the post; §9 reports what is in hand.

- A test that separates recursion from its rivals: forward echoes (does a rating anticipate
  the trials left, or the play's end?), or the interaction of two outcomes (linear echo
  predicts none, saturating echo some).
- The direct felt-clock test (`audit/felt_clock.py` left it open): a fast transient plus a
  slow mood in elapsed seconds, the current trial's rating delay included, with rate
  `∝ age^−q`, against an age-specific kernel shape; calibrated on simulations with
  z-scoring, heterogeneous people and repeated draws. It separates a slower felt clock (Janet
  `q = 1`, Lemlich `q = ½`) from reactivity and persistence changing with age.
- A multi-scale reading of the heavy tail against `M < 1`.
- Whether `a < 0` is dread, the certainty effect, or curvature (it halves under power
  utility).
- Separate a base kink from loss-averse news at the offer (X3): a design whose pre-trial
  forecast is away from zero points, or the offer reveal as its own event.
- Memory by sign beyond a play: does the fading affect bias's crossing (near lag 13 trials
  here) scale with the event, as reach does?
- Slow adaptation needs step data: parked with B4 (below). The in-task steps (Keren, Jangraw)
  add no evidence of adaptation, and their injection distances are uncalibrated.
  - A recovery simulation through the actual pipeline would turn them into bounds: the null
    and alternative tails, noise resampled by person, the cross-validated comparison.
  - RestAfterWins's fall below the starting mood after a winning streak is within drift. An
    announced against an unannounced end would separate a lobe from news.
- News about later trials (Blain & Rutledge), Codex's repairs not yet made: forecasts
  propagated per horizon (revisions now persist unchanged over the trials left); recovery
  simulations to calibrate the bound; anticipation and news profiled jointly; whether one news
  strength serves both channels (the magnitude channel's ratio is 0.74 [0.29, 1.41], the win
  channel's 1.30).
- Data for the constants the task fits leave open (anticipation, news about later moments,
  memory beyond minutes, adaptation steps): candidates, access and order in
  `notes/datasets.md`.

## Follow-up lines

Independent research, not prerequisites for the post.

- **Decision theory by learning** (`experiments/learned_expectations/`, `notes/empathy.md`).
  A possible post of its own: twins and altruists look alike in symmetric self-play, and a
  copy signal or inferred dependence separates them. Canonically one event's felt welfare is
  `α·m(q) + β·m(p)`, so felt play is payoff play at scale and felt empathy is altruism at a
  `J`-set weight; what remains is belief choice, `J`, and play across events. Guilt that
  depends on expectations, sticky profiles and promises are loss-averse-news (X4) questions.
  - **Unknown adversaries** (`adversary.py`). No handshake at 3000 steps: longer training, a
    larger share of copies, partners that do not punish probing, the dependence signal or
    cheap talk (does a twin use them?). Test the twin as an altruist toward lookalikes (an
    altruist at the copies' share of cooperating partners, about 0.29). Why the batch
    baseline and a braced critic learn reciprocity later; the rosy critic's defection basin
    with its level outside (D8's mechanism or the felt objective?); co-learning partners and
    a frozen independent bank; the policy on felt utility; the separate-critic GAE arm,
    keeping the felt critic `C` (affect, discount `ν`) apart from the advantage baseline `V`
    (discount `γ`, Codex).
  - **Partners** (`notes/empathy.md`). Dependence without identity labels, from randomized
    probes against a common-cause confound (Codex's design); heterogeneous strangers to break
    the `σw` equivalence; donation games and the sign of `R + P − S − T`; guilt toward a
    partner's felt history in iterated play (F7). Under X4 only: the trust game as learners
    (expectation-dependent honesty at `J = 0`, promises).
  - **Agents not yet built.** The twin dial in hidden repeated games; reliability (D6) and
    the self-Newcomb as environments; the observer with attention as a choice (batching, N2,
    D7), dread or rumination asymmetry (information avoidance, D5) and saturating news near
    the threshold; in the game distribution, whether the affect policy prefers not to tell
    games apart early (D7). The observer in the canonical model (`run_observer.py` at `λ = 1`:
    no kink, so no frozen beliefs; does `α`'s sign decide optimism, as in the game agent?).
  - **The generalist.** Every head on one trunk across wings: does affect trained in one
    context change action in another (D8 across tasks)? After the per-task baselines.
  - **Evolving felt parameters.** Over a braced critic the heterogeneity of `λ`'s push matters
    (doubling `λ` costs 9.7 and 9.4, its mean field 3.4 and 2.6, gaps ±3): which histories, and
    is it the consolation pattern? Smaller contrasts than factor two for local gradients, and a
    bounded push-spread measure. Adaptation as a gene in a world that learns from memory,
    where the level anchors (D9) and selection may reverse. Rumination's rise under
    coevolution with felt agents, absent locally: a linked gene or a non-local optimum? Longer lifetimes, where escape speed matters less; welfare
    (felt) against fitness (payoff) of the evolved populations; observed dispositions (menu F4).
  - **Well-foundedness as a learning failure.** The canonical critic at `a = 0.3, ν = 0.8`
    (anticipation mass 1.2) diverged; map where TD on felt utility diverges against
    `M + N < 1`, and `M + λN < 1` with loss-averse news.
  - **Evidence gaps** (2026-10-15 audit): archive the twin-dial output and the
    anticipated-news comparison (the "84% of directions" figure has no script), and the
    observer's tree-solver and finite-difference checks; report the consolation gap
    stratified by round (pooled 0.33 overstates it by a quarter or so); an initialization
    ablation for credible-plan selection (only 4 of 16 draws are informative); seeds for the
    game agent's motivated-belief pattern (one run), and for X4's residual lean to risk
    dominance over the matched-temperature control (+0.014, 4 of 5 seeds).
- **Shared-state critics** (`formalism/learning.md`, D8, D9).
  - **The canonical critic's complacency**: lowering its mean level below payoffs did not
    change which seeds escape (the same two of six); without memory or news 2–4 of 6. More seeds, the critic's
    response to the last payoff by round (D8(c)'s varying part), and the alignment diagnostic
    on it.
  - **Learning from memory** (D9). Separate the anchor from Adam and clipping (a matched
    update-size control; update norms, clip factors, KL to the old self through the early
    transition); a lag sweep and importance-weighted replay; a matched schedule for the
    on-policy comparison; felt replay with more seeds, where adaptation's cost is one seed so
    far; the motivated critic under replay, where the critic's level reaches the policy
    through the state and, as the baseline, through drift with opposite signs.
  - **Two channels for optimism.** Through the policy's baseline the critic's level does
    nothing detectable at batch 2048. Next: small batches, where a baseline's level should
    matter (optimistic non-committal, pessimistic committal); and a decision rule that reads
    values directly (softmax over learned move values), the classic optimism-explores case,
    against the shared state, where a high level reads as "stay".
  - **The mechanism.** Left: why removing the critic's mean push on the state traps the
    honest critic. Codex's three-branch one-step diagnostic: clone weights and Adam state;
    policy gradient alone, plus the game-varying critic gradient, plus its per-round mean;
    round-2 stay logit on fixed first-round histories. Does the shared-state sign reverse on
    a task whose optimum is stay-heavy?
- **LLMs.** Context windows and sessions as lives; instances as A1's tree. The peak-end
  design: positional weights of an end-of-episode rating identify the effective memory kernel
  (recency and duration neglect from linear memory, peak from salience); integrate with the
  peak-end study in LLMs.
- **Death dates** (`notes/death.md`, exploring). Counterfactual lifespans in the additive
  model: the dead feel no news, so ignorance of the death date pays at the calibrations; hazard
  against the felt state of the living, and the extra well-foundedness condition it brings;
  survival optimism; the exact decision case (willingness to pay for survival by
  evaluator, sticky safety plans under loss-averse news, sudden against warned deaths);
  chosen dates (an extension pays iff the added moment feels good; the momentary self's exit
  incentive rests on a short kernel-weighted forecast and outlasts a patch through memory;
  plans to continue or to exit both stick in a band under loss-averse news, and selection by
  preference undoes it; an immortal under momentary control lives a first-passage time set by
  mood persistence, longer with long memory, shorter with remembered loss-averse jolts; under
  biphasic memory, contrast troughs after drops open exit incentives at positive levels, while
  at a matched felt mean adaptation lengthens lives). Next: dread of death as a disvalue, a
  dated hazard, afterglow and adaptation together (two memory stocks), and the exit learner
  (`experiments/learned_expectations/run_exits.py`, sketched, not run). Yaari 1965 and
  Brueckner & Fischer 1986 wait in `references/inbox/`.
- **Vicarious echoes** (`notes/vicarious.md`, exploring; menu B7). Contagion, vicarious
  anticipation and memory between people: joint well-foundedness by echo shares, welfare
  weight as centrality (Katz additively, PageRank under attention budgets; the hedonic
  reading counts sympathy where felt), news across people (the matrix loop gain; reciprocity
  makes the loop, budgets make stability size-free), grief among survivors (under loss-averse
  news a widely felt death is better foreseen; under biphasic memory an undershoot after the
  loss, then recovery). Next: delays along the graph, whether to tell
  someone of their coming misfortune (against Caplin & Leahy 2004), the prior art listed there.
- **Persons in the echo graph** (`notes/persons.md`, exploring). With vicarious kernels,
  kernel weight runs between bodies: what a moment is made of (a partner at coupling 0.2 as
  much as one's own past and future), momentary, egoistic and total hedonism as row, cluster and
  global sums, forks as Ys whose branches stay weakly connected through the trunk; a measure of
  affective integration. Over a long life, fading kernels fail the whole-person clustering
  tests: couples split into time slices unless `c ≲ 8/T²`; idealized uniform recall keeps
  persons together at every length below `c = B/4`. Next: heavy-tailed kernels between the two, and the
  commensurability test (rated overlap, future-self continuity, coupling).
- **In discussion:** the extensions menu, `notes/extensions-menu.md`.

## Parked (a9)

- **Additive or displacement echo** (`notes/displacement.md`). A positive continuation must
  not lower welfare, which leaves additive and Z. a9 wants to explore the model further
  first, especially uncertain death and other counterfactuals. Discriminating extensions:
  the menu, section G. The post states additivity as an assumption (§2) and lists the
  question among its limits (§10).
- **Hedonic adaptation, B4** (`notes/adaptation.md`). Left: the Dartmouth step test and a
  frequency-principle test in the Great Brain Experiment (does a rating track the current
  payoff's rank among recent payoffs beyond its value?).
  - The Dartmouth College Experience Study (Zenodo record 22953080) is in `data/dartmouth/`,
    every file md5-checked. Its `affect` column is the PAM picture index, not valence:
    confirm the rubric before the step test (`notes/datasets.md`). The test's design is in
    the adaptation note.
- **The C1 toy** (actions leaking into affect): the menu, C1.
- **A felt forecaster in a Bates world**, a separate project: `notes/bates.md`.
