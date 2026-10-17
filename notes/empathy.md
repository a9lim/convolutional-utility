# Caring about a partner: felt empathy, twins, similarity

**Status: in progress (2026-10-16); a follow-up line, decision theory by learning, not the post.** Menu items F6 and F9, the twin dial's caveat, and inferred
dependence. Reviewed by Codex (thread `cu-empathy`); prior art read and filed (`references/INDEX.md`,
"Games: guilt, Kantian morality, similarity"). Code in `experiments/learned_expectations/`:
`partners.py`, `run_partners.py`, `run_trust.py`, `dependence.py`, `run_dependence.py`.

## Empathy with a partner who feels news

Setting: my move changes partner `j`'s payoff by `Δ = H − L` (`H` if I cooperate or honor). My
`P(cooperate) = p`; `j`'s belief about it `q`, `m = E_qπ_j`. I maximize my felt utility plus `w` times `j`'s.

- **Direct model.** `W_j = A·m + (1 + B)π_j + nψ(π_j − m)`, `ψ` with slope 1 on gains and `λ` on losses;
  `A` the anticipation mass before the outcome, `B` the memory mass after. Exactly
  `wW_j = w(1 + B + n)π_j − wn(λ−1)(m − π_j)₊ + w(A − n)m`. [checked; the form is Codex's]
  - The middle term is Battigalli & Dufwenberg's simple guilt `θ·max(0, E_jπ_j − π_j)` (2007 eq. 1;
    2009 p. 13) with **`θ = w·n·(λ−1)`**. The last term is constant only while `m` is held fixed.
  - In Khalmetski, Ockenfels & Werner's terms (2015; WP eqs. 2–3: a linear weight `α` on the partner's
    positive surprise, `β` on negative): `α = wn`, `β = wnλ`. Empathy with a loss-averse partner pins
    `β/α = λ ≥ 1`, guilt over surprise-giving: transfers at or below what the partner expects (their
    Prop. 1). They measure surprise in transfers, against a distribution over the partner's
    expectation; with the expectation uncertain, guilt is `E[(m − π_j)₊]`, not its value at the mean.
  - At `λ = 1` a fixed-reference surprise term is behaviourally just stronger altruism.
  - [synthesis; B&D motivate guilt by the partner's disappointment (2009 fn. 24); the decomposition
    and the pinned ratio were not found]
- **The interpersonal `J`.** Let `j = dq/dp`, how `j`'s forecast moves under a contemplated change of
  my policy. The marginal weight on `Δ` is
  **`1 + B + n + n(λ−1)q + j·[A − n − n(λ−1)(1 − p)]`**. [Codex; checked]
  - Calibration (`q = p`) is the forecast's value; `j` is its counterfactual dependence. Accuracy does
    not imply `j = 1` (D2). An implementation of D2's channel, a gate on a forecast derivative, not the
    same object as D2's `J`, a derivative of past experience.
  - At `j = 1` and `q = p`: `E[W_j] = (1 + A + B)E[π_j] − n(λ−1)p(1−p)Δ`. The partner's anticipation
    counts, surprise goes (a predicted policy surprises no one in expectation), and loss-averse
    uncertainty is a penalty on unpredictability; total partner welfare still favours reliably good.
  - Locally `j = 1` raises the weight iff `A > n + n(λ−1)(1 − p)`. Between pure policies (honor or
    grab), `J = 1` gains `(1 + A + B)Δ` and `J = 0` gains `(1 + B + nλ)Δ` when `j` expects honoring,
    `(1 + B + n)Δ` when `j` expects a grab: finite deviations favour `J = 1` iff `A > nλ`. The gap is the
    predictability term, which a move between two pure policies does not cross.
- **Timing.** D1's Newcomb structure needs the anticipation already felt when the choice is made: the
  trust game below. In simultaneous games (`oneshot.py`, `partners.py`) `J` is forecast dependence without
  a felt past.
- **The trust game** (`run_trust.py`, canonical model). Ann trusts at 0 and anticipates until Bob
  chooses at `s`: honor gives her 0.5, grab −0.5 (outside option 0, no event); Bob gets 0.3 or
  0.3 + `t`, felt as a sure payoff. The temptation Bob resists per unit of empathy, `t*/w`:

  | calibration | `J = 0`, Ann expects honor | `J = 0`, expects grab | `J = 1` |
  |---|---|---|---|
  | game agent's (`a 0.15, n 0.3, λ 2`) | 1.45 | 0.72 | 1.14 |
  | felt calibration (`n 0.2, λ 1.5`) | 0.75 | 0.64 | 1.02 |
  | weak news (`n 0.1`) | 0.66 | 0.58 | 1.02 |
  | no news | 0.53 | 0.53 | 1.00 |
  | linear news (`λ 1`) | 0.72 | 0.72 | 1.00 |
  | no anticipation | 2.75 | 1.44 | 1.04 |
  | stronger anticipation (`a 0.2`) | 1.12 | 0.55 | 1.18 |

  - `J = 1` resists about 1 in every calibration: a predictable policy makes Ann's life deterministic,
    and it weighs like Bob's own.
  - `J = 0` depends on what Ann expects. Between its two thresholds Bob honors iff Ann expects him to:
    guilt makes trust self-fulfilling, the mechanism by which promises work in Charness & Dufwenberg
    (2006, to verify). A `J = 1` Bob's honesty does not depend on her expectation.
  - Which is more trustworthy when trusted: `J = 0` under strong loss-averse news (the game agent's
    calibration, any anticipation horizon from 2 to 14), `J = 1` at the felt calibration, with weak or
    no news, or with stronger anticipation. "Parfit's hitchhiker between people" holds where the
    partner's anticipation outweighs her loss-weighted letdown; otherwise guilt, a `J = 0` motive, does
    more, and a `J = 1` empathizer can escape guilt by being expected to betray.
- **Canonical marginal weights** (`felt.Event`, `EVENT`, `H = 0.7, L = −0.5`; the announcement is felt
  against a zero prior, so these depend on payoff levels, not only on `Δ`):

  | `p` (= `q`) | 0⁺ | 0.25 | 0.5 | 0.75 | 1⁻ |
  |---|---|---|---|---|---|
  | `J = 0` | 1.84 | 2.10 | 2.45 | 2.95 | 3.69 |
  | `J = 1` | 1.62 | 2.12 | 2.89 | 3.27 | 5.12 |

  - `J = 0` runs from `g₁(1 + κ̃)` to `g₁(1 + κ̃λ̃)` (`κ̃ = 0.50`, `λ̃ = 4.0`, `g₁ = 1.22`): guilt is
    amplified by the news loop and scaled by how long `j` feels it, so guilt toward a partner with
    long memory is larger (F7's forgiveness as the other's kernel). Below linear in between: `j`'s felt
    forecast includes its expected disappointment (core X4's built-in bracing, under loss-averse news), so its reference sits
    below `E_qπ_j` and letdowns are smaller.
  - `J = 1` drops from 3.26 to 2.56 where Ann's announcement outlook crosses zero (`p ≈ 0.589`).
  - Slopes must be taken off the boundary: at a certain outcome the realized news sits on `ψ`'s kink.
    [checked; Codex found the `p = 0` artifact]

## Twins and altruists

- **First order, a twin is an altruist.** At symmetric profiles the twin gradient `∂₁π + w∂₂π` equals
  the gradient of `π_me + w·π_them` with the other's policy fixed. [known: Alger & Weibull 2013 §6.2:
  identical first-order conditions at interior symmetric equilibria for `α = κ`, different second-order
  ones; checked] So `run_twin.py`'s thresholds are altruism thresholds, and symmetric self-play cannot
  tell twin reasoning from other-regard.
- **Finite deviations.** A deviation the copy matches with probability `κ` is homo moralis,
  `(1−κ)π(x,y) + κπ(x,x)` (Alger & Weibull Def. 4). With mixed deviations available, all-cooperate is
  its best response iff `κ ≥ max{(T−R)/(T−P), (T−R)/(R−S)}`. [Codex; counterexample to the pure-only
  test: `R = 3, S = 0, T = 5, P = 1, κ = 0.6`, mixing at 5/6 beats both pure moves] With
  `D = R + P − S − T ≤ 0` that is the altruist's threshold; with `D > 0` homo moralis is stricter (its
  utility is convex in own play iff `D > 0`, Alger & Weibull Prop. 2; Bergstrom 1995 Prop. 2 in kind).
- **Assortment.** With a fraction `σ` of indistinguishable copies and non-copies whose mean policy is
  one's own (payoff games), the gradient is `∂₁π + σw∂₂π`: altruism at `σw`. A constructed local
  analogue of Alger & Weibull's Theorem 1 (homo hamiltonensis, `κ = σ`, evolutionarily stable up to
  behavioural equivalence, under uniqueness and richness conditions), not a test of it.
  Heterogeneous non-copies break it: the gradient is `σ[π₁ + wπ₂](p,p) + (1−σ)E[π₁(p, Y)]`. [Codex]
- **With felt utility, a twin is an empathizer at `J = 1`.** The twin's gradient through the copy runs
  through both the copy's move and its own belief about it, which by symmetry is the gradient of `w`
  times the partner's felt welfare with the partner's forecast tracking my policy. Twin reasoning
  about a copy is, to first order, empathy routed through the copy's anticipation of me; the `J = 0`
  empathizer (surprise and guilt) is a different object. In payoffs `J` is idle. [checked: 2000 random
  symmetric games at three profiles, difference ≤ 3e-15; against `J = 0`, up to 1.6]
- **Felt news makes certain profiles sticky for twins.** At `J = 1`, `j`'s uncertainty about my move is
  a first-order cost off a pure profile, so between copies both all-cooperate and all-defect are more
  often locally stable: at `w_T = 0.5`, all-cooperate in every prisoner's dilemma of `run_twin`'s
  family and all-defect in 76% (payoff twin: 73% and 58%). The scheduling learner's "deterministic
  plans are local optima", between copies.
- **The dials compose multiplicatively.** `π(x,y) + w_Eπ(y,x)` with `dy/dx = w_T` is altruism at
  `(w_T + w_E)/(1 + w_T w_E)`, up to scale. [Codex] `partners.py` routes the copy derivative through the
  partner-welfare term too.
- **What gradient `J` is.** Parameter identity, not logical similarity: two independently trained
  twin-reasoners are each other's strangers and play causally. The trainer gates the gradient on true
  identity, privileged dependence information; a learner that infers dependence from a signal would
  need a model of it.
- **Prior art for the learners.** Oesterheld, Treutlein, Grosse, Conitzer & Foerster (2023): with a
  similarity "diff" in a high-dimensional one-shot prisoner's dilemma, alternating best response from
  random initialization reached mutual defection in 26 of 26 runs; pretraining to "cooperate against
  copies, defect against random" (CCDR) gave partial cooperation in 26 of 28. The twin's gradient
  learns CCDR by itself, because its gate knows which partner is a copy.

## Experiments

Four networks per population, two populations per variant, random symmetric games; half the
objective against copies (`σ = 0.5`), half against strangers: other networks, or mirrors (the
network's own current policy under a stop-gradient: lookalikes whose play the learner treats as fixed,
though, recomputed every step, they move with its parameters). An input bit says
copy or stranger. `run_partners.py`, `partners_report.txt`, `partners.png`; checks in
`python partners.py` (no gradient leaks between networks; a copy at `w_T = 0` trains like a mirror; the twin–empathizer identity).

| variant | PD, copy | PD, stranger | stag hunt, copy | stag hunt, stranger |
|---|---|---|---|---|
| causal | 0.01 | 0.01 | 0.03 | 0.02 |
| twin 1 | 0.95 | 0.01 | 0.99 | 0.07 |
| twin 1, mirrors | 0.95 | 0.01 | 0.99 | 0.06 |
| altruist 1 | 0.95 | 0.98 | 0.99 | 1.00 |
| altruist 1, mirrors | 0.98 | 0.99 | 1.00 | 1.00 |
| twin 0.5 | 0.52 | 0.01 | 0.82 | 0.08 |
| altruist 0.5 | 0.51 | 0.51 | 0.82 | 0.83 |
| felt twin 0.5 | 0.50 | 0.00 | 0.73 | 0.00 |
| felt empathy 0.5, `J = 1` | 0.50 | 0.46 | 0.77 | 0.75 |
| felt empathy 0.5, `J = 0` | 0.43 | 0.40 | 0.70 | 0.69 |

- **The bit separates twins from altruists.** Twins cooperate with copies and defect against strangers,
  including mirrors that run their own weights: the learner's gradient gate alone drives it.
  Altruists ignore the bit. In both populations of every variant.
- **Without the bit, a twin is an altruist at `σw`.** Twin 1 at `σ = 0.5` cooperates in 0.52 of
  prisoner's dilemmas (mirrors 0.51), altruist 0.5 in 0.51; at `σ = 0.25`, 0.21 against an
  altruist 0.25's 0.21; stag hunts and every stability class agree within 0.04. Independently trained
  networks matched too, because they converge to similar policies.
- **Learned play follows local stability.** Where only all-cooperate is locally stable, learned
  cooperation is 0.92–0.99; where only all-defect is, 0.01–0.07; bistable games are where learning
  selects (prisoner's dilemmas mostly defect, stag hunts mostly stag).
- **Felt empathy.** At `J = 1` it matches the felt twin with copies (0.50 against 0.50) and extends to
  strangers (0.46 against 0.00). At `w = 0.5`, `J = 1` cooperates more than `J = 0` (prisoner's
  dilemma 0.50 against 0.43, stag hunt 0.77 against 0.70), as its stability classes predict (no
  prisoner's dilemma where only all-defect is stable, against 8% at `J = 0`): the gradient learner follows
  local slopes, where `J = 1` carries the predictability term. The trust game's finite comparison can
  go the other way. At `w = 0.25` the gap (0.19 against 0.17; stag hunt 0.39 against 0.34) is within
  run-to-run variation: rounding-level changes to the felt closed form moved felt rows by up to 0.04.
- A noisy bit (flipped with probability 0.2) gives graded conditioning (0.68 against 0.22); its gate
  uses true identity, so it is a selection experiment, not inferred dependence.

## Inferred dependence

`dependence.py`, `run_dependence.py`, `dependence_report.txt`, `dependence.png`; checks in
`python dependence.py`. Reviewed by Codex (thread `cu-empathy`).

- **The twin, uninformed.** Each match shows both seats a similarity signal `s`, `N(1, 0.5²)` from copies
  and forgers, `N(0, 0.5²)` from others. The twin's gradient is its direct gradient against the partner's
  actual play plus `w·d(s)` times the dependence gradient evaluated in the copy branch (partner = its own
  policy), `d(s)` its estimate that the partner is a copy: a Bayesian posterior under an assumed model, or
  a small head fit to identities revealed after each match. The oracle routes the dependence gradient
  through true copies only.
- **Calibrated inference is the oracle in expectation.** With `d(s) = P(copy | s)`, the expected gradients
  agree, payoff or felt. [Codex; checked: ≤ 5e-15 in three populations] The oracle's identity labels buy
  nothing in expectation. Weighting the posterior-averaged dependence gradient by `d(s)` instead agrees
  only in payoff games, where `∂₂π` does not depend on the partner's play (felt gaps up to 1.2): the
  dependence term has to be conditioned on the copy branch, not averaged over partners.
- **Populations.** Copies; mirrors (the network's current policy under a stop-gradient); frozen strangers
  and forgers (four causal networks trained in self-play and frozen, which defect in 99.5% of prisoner's
  dilemmas; forgers emit copy-like signals). "Mirrors": copies and mirrors half and half. "Strangers":
  copies and frozen strangers. "Forgers": copies 0.5, strangers 0.25, forgers 0.25. Every twin at
  `w = 1`; four seeds each; seed spread about ±0.0005 in payoff.

  | payoff in its population | causal | oracle | Bayes | learned | credulous | universal | naive |
  |---|---|---|---|---|---|---|---|
  | mirrors | 0.290 | 0.375 | 0.375 | 0.375 | 0.381 | 0.384 | |
  | strangers | 0.288 | 0.323 | 0.323 | 0.323 | 0.319 | 0.307 | |
  | forgers | 0.287 | 0.315 | 0.315 | 0.315 | 0.310 | 0.303 | 0.312 |

  Credulous: assumes 90% of partners are copies; universal: treats every partner as a copy; naive: counts
  forgers as copies.
- **Inferring dependence is as good as knowing it,** when calibrated: Bayesian and learned twins match the
  oracle in cooperation at every signal (within 0.05) and in payoff (within 0.0005), and the learned head
  recovers the posterior (0.02, 0.11, 0.50, 0.89, 0.98 against 0.02, 0.12, 0.50, 0.88, 0.98 at
  `s = −0.5 … 1.5`). The felt oracle and the felt Bayesian twin agree too (0.3073, 0.3075 at `w = 0.5`).
- **What pays is the real dependence.** At `w = 1` a twin with the right dependence ascends its actual
  payoff: a copy's play is computed from the same parameters. Mirrors are recomputed from those parameters
  as well, so they move with the twin under any parameter change; there the label "stranger" undercounts
  real dependence, and payoff rises with attributed dependence (oracle 0.375, credulous 0.381, universal
  0.384). Frozen strangers and forgers do not move with it; there payoff falls with attributed dependence,
  and credulous, naive and universal twins are exploited by forgers (payoff against them 0.229, 0.234,
  0.225 against the oracle's 0.258; prisoner's-dilemma cooperation at `s = 1.5`: 0.92, 0.91, 0.91 against
  0.68).
- So an identity label is not privileged information: it is a convention about dependence, and where it
  disagrees with the dependence that is there (mirrors), over-attribution beats it. Superrational trust
  pays among agents that move with you and is exploited by lookalikes that do not, the twin's version of
  the mimicry problem (Frank 1988, to verify; menu F4).
- **Stipulated, not tested.** The dependence gradient's Jacobian: in symmetric games with a shared signal,
  "my policy in the partner's seat" is my own policy, so no perspective-taking is tested; private signals
  would need the partner's input inferred. Calibrated felt forecasts: the simulator gives the partner's
  actual policy as my belief, and a twin with that access could read disagreement with its own policy as
  evidence against copying. Equal expected gradients need not give equal Adam trajectories.

## Open

- Dependence without identity labels (Codex's design): randomized `±ε` probes to the twin's own
  mechanism with games, signals and seeds held fixed, `d̂(s) = Σ K_s δr δy / Σ K_s δr²`. Confound test:
  independently parameterized learners sharing an external update shock co-move passively, so passive
  regression reports dependence, while private probes report about 0 for them and 1 for copies. Mirrors
  would answer probes (they share parameters). Interventions identify dependence under the declared
  intervention, not an FDT logical counterfactual.
- Heterogeneous strangers (causal learners, scripted defectors) to show the `σw` equivalence failing.
- The trust game as learners: does a `J = 0` population show expectation-dependent honesty, and do
  promises (raising Ann's `q`) move it?
- Diagnostic families: donation games, prisoner's dilemmas split by the sign of `R + P − S − T`,
  payoff offsets against the zero-prior announcement.
- Iterated play: guilt toward a partner's felt history (F7), and twins in hidden repeated games.
