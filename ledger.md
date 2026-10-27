# Ledger

Periodically compacted; full entries stay in git history (the last uncompacted version is
at `22c5c4f`).

## Standing decisions

- **Reading** (a9): hedonic. Anticipation and memory are felt; welfare is the objective
  expectation of the felt life-sum.
- **Model** (a9): recursive echoes with recursive news is canonical, the direct form its
  reduced form for foreseen lives; forecasts are rational. Notation: every kernel is Latin
  strength times Greek reach (`a α^j`, `m μ^j`, `n ν^j`, adaptation `c γ^j`); first moment
  `M₁`, gain-loss `φ_λ` (extension), felt news `N_t`, the jump kernel's lag-1 weight `k₁`,
  P4's rates `p̄, q̄`.
- **Symmetric core** (a9, 2026-10-17): the canonical model is linear and sign-symmetric
  (`λ = 1`). Sign asymmetries are the extension X1–X4, ranked by felt evidence: dread over
  savoring, memory by sign, a base kink, loss-averse news (a synthesis across unlike
  measures). Felt news `λ` is roughly 1.0–1.2 in the happiness data once chosen risk is
  costed, and λ ≈ 2 is a choice quantity; the cleanest
  kink structurally (news's, at zero revision) is the least supported as a feeling. Built-in
  bracing survives at `λ = 1` (any concave felt channel braces), but echo kinks brace only
  slightly at the felt calibrations and memory's sign depends on its lag profile, so it left
  the post for the companion.
- **Post** (a9; restructured 2026-10-16 at a9's request): one flagship post, working title
  *Experience Echoes*, ten sections around a running holiday example (`outline.md`), with
  the formalism as technical companion. Mostly a bridge: imported ideas credited inside the
  claim, a few candidate contributions tagged *not found*, never "ours" by default. The
  learner wing outside three illustrations, the LLM peak-end study and the Bates world are
  follow-ups.
- **Tags**: provenance (standard, known, known in kind, synthesis, not found, speculation) and
  support (proved, checked, numerical) are independent; the outline carries provenance only,
  `formalism/INDEX.md` maps each claim to its support.
- **Decision theory**: `J` is one channel (fixed-past choice against advance commitment),
  not a classification of decision theories (Codex, 2026-10-13). The choice side adopts
  Kőszegi & Rabin's preferred credible plan, credited.
- **Anthropics**: measure-weighted anticipation, assumed (the conserved-measure horn);
  aggregation is a separate axiom. Sleeping Beauty cut.
- **Learners** (a9): the observer's beliefs are tethered by a KL cost of self-deception. The
  calibrations follow the symmetric core (`λ = 1`); loss-averse news is the override `felt.X4`,
  and runners whose reports rest on it pin it explicitly (2026-10-17).
- **Horizons** (a9): a waking day, a life, an LLM context window and session (a9's wife
  studies the peak-end effect in LLMs).
- **Parked by a9**: the Bates world, as its own project; additive against displacement echo (only additive and Z survive);
  hedonic adaptation (biphasic memory chosen); the C1 toy.

## Lessons

- Learned-agent comparisons need seeds: the "braced critic raises payoffs" result compared
  braced runs against one honest seed stuck on a plateau.
- A critic level kept outside the network must track the TD loss's own weighting. The
  iterated agent's level followed self-play only, so with mixed partners the head carried a
  mean push of −0.29 on the shared state (−0.5 in rounds 1–2). Fixed, it is 0.00; prisoner's
  dilemma cooperation went from 0.35 to 0.29, with the qualitative results unchanged.
- Refactoring learners: record bitwise fingerprints first (short runs, objectives, gradients,
  rollouts) and keep the arithmetic in the same order, so reports are rerun only where the
  numerics change on purpose.
- Claims made in chat get checked before they reach the docs. Wrong first: dread pricing
  information in the direct model, CDT/FDT as the mortality/eternity split, "no adaptation
  at task scales", conservation taming copy-counted anthropics, asymmetric updating from the
  Bates flow band (a shifted symmetric band), Bayesian forecasts adding dread there (they
  lower the reference); and on 2026-10-27: sudden death beating any warning for the pair, a
  wait as long as the patch filtering it, stickiness needing a plan, the band closing at
  `λ = 1` (only for matched kernels), an attention budget as displacement, welfare following
  connectedness alone, and "drops, not levels".
- Fresh-eyes rounds (three so far) found overreaching headlines and no sinking hole; the
  linear backbone stands.
- A felt-against-payoff comparison needs matched temperature: a fixed entropy bonus against a
  rescaled reward moved equilibrium selection by 2.6 of the 4 points once credited to felt
  utility. Linear felt utility is payoffs at scale, so the matched payoff agent is the control.
- Learners: Adam stalls on saturated sigmoids (fixed by preconditioning each self's
  gradient by reach and slope); population-based training confounds selection with
  inherited weights, so evolution is generational (born untrained).
- Read the full text of a paper before designing on it. An extraction of Marek & Ryabinin's
  §4–§6 missed §3, whose offline runs had the sign my replay prediction got wrong.
- Literature agents: a control-character cleanup once touched 15 reference files (restored by
  re-extraction, spot-checked byte for byte); one agent died on an API filter error and
  needed a leaner brief.

## Codex threads

`conv-utility-premise` (premise, first decision draft, round 3), `braced-critic` (D8),
`cu-fresh-review`, `cu-extensions` (Bates), `cu-round2-core`, `cu-round2-ext` (the menu),
`cu-displacement`, `cu-disc-ext` (menu G), `cu-games-ext` (menu F), `cu-c1-leakage` (D7's
leakage bullets), `cu-framework`, `cu-empathy`, `cu-restructure` (the post's architecture and
triage), `cu-novelty-audit` (attribution, row by row), `bracing-review` (concave bracing),
`adaptation-replay` (the felt reference, replay, score centering, the invasion controls),
`cu-death` (death dates, chosen dates, the exit in equilibrium, biphasic exits), `cu-vicarious`
(vicarious echoes, news across people, grief), `cu-persons` (persons in the echo graph,
clustering). Job replies under `~/.gaslamp/jobs/`; the premise reply, source of P4–P6's
closed forms, is `cx-20261012-230641-77eb/reply.md`.

## Blocked sources, not circumvented

Dorsey 2015 (KU 403); SSRN and Chicago journals (Cloudflare); JET, JPET and JME closed
copies; Slote (lending only); AEA PDFs; Eil & Rao; Bénabou & Tirole 2016; Good 1967; Buchak
2010; philsci-archive; Philosophers' Imprint; the old LessWrong wiki. Academic-access
requests: `next-steps.md`, the post's citations and the companion's prior art.

## Log

- **2026-10-12.** Premise check: literature verification, Codex's first adversarial pass
  (finite-section spectral radius is not the mass; the ramp sign claim needed
  qualification).
- **2026-10-13.** Hedonic reading; decision theory and anthropics; felt news and the
  canonical model; calibration; the playground; the pre-writing lookover (Codex round 3);
  the observer and the first learners.
- **2026-10-14.** Anticipated news solved exactly; the braced critic deflated to "the
  critic's level, through the shared state", then D8; evolution; the happiness fits and
  their audit; first fresh-eyes review; the Bates results.
- **2026-10-15.** Second fresh-eyes review and the extensions menu; displacement and
  adaptation worked and parked; the happiness data rule out only fast adaptation.
- **2026-10-15 (evening).** C1 discussed and absorbed into D7: actions, their results and
  inaction leak into affect, so commitment alone does not make batched affect feasible
  (Andries & Haddad have the consumption case). Codex (`cu-c1-leakage`) cut the overreach:
  the four "escapes" became one conditional-independence condition, "rules do not leak"
  fails on consequences (D6), batched decisions became a conjecture, and my "linear in `q`"
  hand check is convex quadratic (now in `checks.py`). Docs consolidated: core.md reordered
  (model, objects, echoes, news, calibration, horizons), next-steps.md cut to open items,
  the Bates results and the learner design moved to `notes/bates.md` and the learner README,
  ledger compacted.
- **2026-10-16.** Learner-arm walkthrough. Iterated's outside critic level fixed (lesson
  above); Dr. GRPO-style group baselines measured. The learner arm consolidated into a
  framework (one felt engine, one games module, agents of named trunks and heads with sharing as
  configuration, the hidden-game and iterated agents merged into `rounds.py`): 73 of 79
  fingerprints bitwise identical to the old code, the rest from two intended changes (the
  hidden-game level follows both seats; the detached critic is computed per round), so braced
  and channels were rerun. Codex reviewed it (`cu-framework`): latent issues fixed, design
  notes for unknown adversaries in `next-steps.md`. Unknown adversaries, first run: the hazard
  sets the end game; twins found no handshake and spent their dependence on lookalikes; a rosy
  critic made a defector, not a sucker.
- **2026-10-16 (evening).** Audit and rework for the post, at a9's request (which supersedes
  the parked restructure). Codex read the repo independently twice: structure and audience
  (`cu-restructure`) and attribution row by row (`cu-novelty-audit`); both agreed with my own
  read. Findings: the outline sold machinery before a problem and front-loaded the canonical
  model; the import was implicit, so imported results (Bergstrom Prop. 5, Kőszegi's trap,
  Bénabou's cancellation, Kőszegi–Rabin's credible plans) read as ours in places; headlines
  dropped their qualifiers ("memory feeds the loop and anticipation does not", the ramp's
  "iff", "Doublethink as a theorem", "the `J` dial reproduces the decision theories", "luck's
  afterglow lasts days", "`k₁ > γ` at any noise level"); the plan put an open-ended learner
  program ahead of the post. Done: `outline.md` rewritten (thesis, import table with source
  status, candidate contributions, ten sections each with question, example, credit,
  LessWrong anchor, objection, figure); `README.md` a landing page; the companion split
  (`calibration.md`, `selves.md`, `learning.md` out of core and decision, peak-end beside P7)
  with tags fixed and a claim map in `formalism/INDEX.md`; `next-steps.md` reordered (the post,
  the companion, the data, follow-up lines, parked); the learner README split into what the
  post uses and the follow-ups; the §1 figure regenerated (it showed the old notation).
  Codex then verified the rework (`cu-restructure`, third round) and caught my own slips: I
  had credited present bias to caring about the next self (one-step caring is exponential,
  P2), set a life-weight example at a holiday's end (memory runs on; the boundary is the
  life's), and dropped conditions from the bracing (symmetric errors), threshold
  (`1/λ < κ < 1`), shape (the linear stationary class), risk (confounded, not decided) and
  carryover (intervals include zero from hours on) claims. All fixed; checks pass (45).
- **2026-10-17 (evening).** The learner arm moved to the symmetric core, at a9's request.
  Canonically one event's felt welfare is `α·m(q) + β·m(p)` (Codex verified the closed form),
  so the felt game, twin and empathy agents reduce to payoff ones and the trust game's
  expectation-dependent guilt is X4's; the same `α` decides whether optimism pays and whether
  `J = 1` cares more (Codex: a corollary of linearity; the empathy reduction holds toward a
  fixed partner policy or at `J = 1`, a counterexample now in the checks). `BeliefPath`
  crashed at `λ = 1` (its branch test read slopes, equal there), so the observer had never
  run canonically. The matched-temperature control moved most of felt utility's lean to risk
  dominance onto the entropy bonus (lesson above). Evolution got sign ratios centred on 1;
  Codex's design review added paired invasions, which show selection on dread and `λ`
  following the critic's level. Runners whose reports rest on `λ > 1` pin it; reruns that
  kept their configuration reproduced their reports exactly.
- **2026-10-18.** a9 asked to test biphasic memory's adaptation in the learners, and brought
  Marek & Ryabinin's score centering (arXiv 2609.20807) to fold in. Built a felt reference
  across episodes, replay from 100-step-old memories with score centering, and adaptation as
  a fourth invasion gene with mean-field controls (`run_adaptation.py`, `run_invasion.py`;
  the critic-level session card folded in). Codex's design review caught the canonical
  reference subtracted after the solve instead of inside it, the first batch replayed 101
  times during warm-up, reward shifts reaching the critic in the replay arms, and a
  three-point level curve that could not carry an "only through the level" claim; all
  replaced before the runs that count. My prediction for replay was the wrong sign: I
  expected the drift toward the old policy to slow learning, and it is what keeps the
  replaying learner learning (Codex's analytic-anchor control: sufficient in this grid). The
  paper's §3 already shows that sign offline; I had read it through an extraction that
  skipped §3, and found it only when archiving the full text (lesson above).
  The invasion rerun reproduced every earlier arm exactly. Results: README, `learning.md` D9,
  the adaptation note.
- **2026-10-18 (later).** a9 asked what the Bates world looks like with the martingale as base
  utility. The flow reading (`notes/bates.md`): a move is news about every remaining moment,
  realization tethers the felt display through the arrival kink, and the band is linear in
  `σ`. Codex (`cu-extensions`) verified the band by smooth fit and the loop multiplier, and
  corrected three of my chat claims: the lopsided band is a constant offset, not asymmetric
  updating; a display that varies by horizon makes welfare unbounded (its counterexample);
  Bayesian forecasts lower the news cost rather than adding dread. The terminal reading's DP,
  never archived, is rebuilt in `notes/bates.py` beside the flow checks.
- **2026-10-27.** a9's questions on death dates, chosen deaths and vicarious feelings grew
  three notes. `death.md` gained chosen dates (the planner's increment rule; the momentary
  self's exit rule, its plan equilibria, preference selection, the Markov exit with and
  without memory in `notes/exit.py`, and biphasic memory's contrast troughs); `vicarious.md`
  (contagion, vicarious anticipation and memory: joint stability, news across people, Katz
  against PageRank weights, grief among survivors, with and without adaptation) and
  `persons.md` (what a moment is made of, forks, and why fading-memory persons fail whole-life
  clustering) are new. Codex reviewed every round and withdrew several first claims (lessons
  above); Gemini verified the prior art bibliographically. The exit learner
  (`experiments/learned_expectations/exits.py`, `run_exits.py`) is sketched with predictions
  written, not run. Parked for a later session: the two-stock Markov exit, the learner run,
  and the notes' Open items.
