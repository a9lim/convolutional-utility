# Learned expectations

Agents whose reward is their own felt utility (`formalism/core.md`), computed from their own
forecasts and realized against the world. The observer and the scheduling agent use the
canonical model, and so do the game and partners agents, through the engine's closed form
(`felt.Event`, checked against the observer's `felt.BeliefPath`); the hidden-game and evolution
agents use a direct first pass (echoes of base payoffs, news on the aggregate TD error); the
iterated agent learns on payoffs alone, with no felt utility. Even the canonical critic kinks the
aggregate TD error rather than each horizon's revision, which agree only at `λ = 1` or when the
revisions share a sign. Expected return under the true environment is then the objective
expectation of the felt life-sum: Brunnermeier & Parker's well-being, learned. Open items:
`next-steps.md`, the follow-up lines.

## Role in the project

Most of this directory is a follow-up line, not evidence for the post (`outline.md`). The
post uses three things, each as an illustration of a stated incentive, not as evidence about
people:
- the scheduling agent's gradient dial between the fixed-past and commitment dates (§7, an
  optional aside: `J` as a stop-gradient);
- the motivated critic's consolation after bad news at `λ = 2` and not at `λ = 1` (§4, one
  line at most);
- a critic's level reaching the policy through a shared state (§6, an optional aside;
  `formalism/learning.md`, D8; the felt objective is not needed for it).

The observer is illustrative only: it chooses subjective probabilities under a KL tether and
is naive about its own later revisions, which is Brunnermeier–Parker-style belief choice, not
the affect policies of D7. It and the scheduling agent's other results (which credible plan
learning selects, anticipated news) support the companion's D3 and N3. Everything else
belongs to two follow-up lines (`next-steps.md`):
decision theory by learning (games, partners, twins and altruists, iterated play, unknown
adversaries) and shared-state critics (the hidden-game agent, its critic controls, evolving
felt parameters).

## Design and prior art

- Two switches, after Oesterheld (2019): what the reward credits (felt anticipation is the
  "overseer", conditional on the forecast or not) and what the learner credits (whether
  gradients flow from anticipation rewards into the policy through its self-prediction).
- The learner's switch is known in binary form: stop-gradient gives performatively stable,
  ratifiable, CDT-like fixed points; full flow gives the optimum, EDT-like or Stackelberg
  (Oesterheld, Treutlein, Cooper & Hudson 2023; Perdomo et al. 2020; Bell et al. 2021;
  Demski's partial agency).
- A lagged self-predictor is not the graded case: it still blocks the gradient, so the
  learner's recognized `J` is 0; the lag changes only how accurate past forecasts are, the
  actual `J`. Graded `J` needs another knob: a partial gradient weight (used here), an outer
  loop's horizon (Krueger, Maharaj & Leike 2020), or forecast accuracy.
- New relative to that literature: a temporal stream of felt anticipation, memory and news;
  `J` graded inside a life-sum; belief heads that choose beliefs under a tether (not D7's
  affect filtrations, which keep beliefs accurate); the LLM-welfare angle.

## Code

One engine, one games module and one agent class; each wing is an environment, an objective and a
trainer on top of them, with a runner per experiment.

- `felt.py`, the felt engine: kernels and resolvents; `news_root`, the exact felt news of a
  revision; `Event`, one event with a held belief in closed form, batched (the game, partners,
  dependence and trust agents); `BeliefPath`, the event under any belief path (the observer);
  `rounds_direct` and `rounds_canonical`, felt utility per round from a critic (the rounds agents);
  `kl`; the calibrations `LIFE`, `EVENT` and `ROUNDS`. `python felt.py` checks `Event` against
  `BeliefPath` (1e-15), `news_root` against a damped iteration, and `rounds_canonical` against its
  fixed point.
- `games.py`: random bimatrix games and their analysis (equilibria, classes, risk dominance); the
  one-shot agents' symmetric families (prisoner's dilemmas with `2R > T + S` and stag hunts with hare
  risk-dominant, by rejection); the iterated agent's four families, assigned by rank alone, in each
  player's own labels.
- `agents.py`: `Agent`, named trunks (tanh MLPs or a GRU) read by named heads. A layout says which
  trunk each head reads, so whether heads share a representation is configuration (D8): heads on one
  trunk shape each other through it, a head on its own trunk cannot, and a detached head reads its
  trunk without training it. `tie(x, w)` is the `J` dial.
- Wings: `observer.py`, `scheduling.py` (tabular), `oneshot.py` (the game agent), `partners.py`,
  `dependence.py`, `rounds.py` (the hidden-game and iterated agents: one environment, one trainer),
  `adversary.py` (unknown adversaries, on `rounds.py`).

Run from the repo root, e.g. `python experiments/learned_expectations/run_observer.py`.

## Single-self agents

### The observer

An event is announced at 0 and resolves at `s`. At each `t < s` the self holds a subjective
probability `q_t` of the high outcome and forecasts its felt life rationally given `q_t`.
Changing a belief revises forecasts, so it is felt as news. Realization is news against the
last belief. Forecasts are rational given the current belief and naive about the self's own
later revisions: at each `t` it expects to keep `q_t` until `s`. The objective is the
objective expected life-sum minus a cost of self-deception, `Σ_t KL(q_t ‖ p) / τ`; without
it, beliefs at the felt calibrations run to N3's corners.

- `felt.BeliefPath`: the model in closed form (core N3, canonical), differentiable in the belief
  path. Checked against an independent Bayesian tree solver at `q = p` (welfare to 1e-10) and
  against finite differences (gradient to 3e-10).
- `observer.py`: a numerical reference optimizer (multistart Adam plus the best step path; no
  certificate of global optimality), and the learned observer.
- `run_observer.py`: reference-optimal belief paths at the life calibration for three kinds of
  event and four tethers; writes `observer_paths.png`.
- `learn_observer.py`: one network that maps an event's features to a belief path, trained on
  felt welfare across random events and compared with the reference optimum on held-out events
  (writes its weights to `observer_net.pt`, not versioned).

The objective has a kink wherever two consecutive beliefs agree (a zero revision, priced at
`λ` on one side), so optimal beliefs are sticky and smooth optimizers stall on them; the
reference optimizer uses Adam with a decaying rate from several starts, including the best
step-shaped path.

### The scheduling agent (`decision.md`, D3)

One pleasure, announced at 0, to be taken in `[0, T)`. A tabular stopping policy; felt
utility is the canonical model, its forecasts Bayesian under a self-model of the same policy,
so they include anticipated news. Every world (the date it is taken) is solved exactly: the
felt fixed point is piecewise linear, solved by iterating on the signs of the news terms.
`python scheduling.py` checks it against an independent damped iteration (6e-12), finite
differences (1e-9) and the reduced form on deterministic plans (7e-12).

- The `J` dial is a gradient setting: the self-model enters as `π.detach() + w (π − π.detach())`.
  At `w = 0` past selves' forecasts carry no gradient, and gradient ascent on the life-sum gives
  each self its fixed-past incentive: causal decision theory. At `w = 1` the gradient includes
  how the policy shaped past anticipation: the commitment planner.
- Each self's gradient is divided by its reach probability and its sigmoid slope, so it follows
  that self's incentive conditional on being there; otherwise off-path selves and saturated
  logits stall learning short of the equilibrium.
- `scheduling.py` (model, learner, exact benchmarks); `run_scheduling.py` (a sweep against the
  exact fixed-past and commitment dates, and the dial; writes `scheduling_dial.png`);
  `run_selection.py` (which credible plan learning selects under loss-averse news).

## Single-self results

- **Observer** (chosen beliefs under a tether, not D7's affect filtration). Optimal beliefs
  at the life calibration stay calibrated far from the event, brace as it nears, and freeze
  over the last few periods; optimism never pays there. A
  network trained on felt welfare captures a median 71% of the reference optimizer's gain on
  ten held-out events (one training run; the reference has no optimality certificate).
- **Scheduling: a gradient dial reproduces the fixed-past and commitment benchmarks.** Over
  30 draws, `w = 0` learns the subgame-perfect fixed-past date in every draw without news and 90% with linear news
  (the misses sit right after the announcement: two unconverged, one a second equilibrium);
  `w = 1` learns the commitment date in every draw. Intermediate `w` gives a staircase from
  the trap to commitment (`scheduling_dial.png`, `scheduling_report.txt`).
- **Which credible plan does learning select?** With loss-averse news (`n = 0.3, λ = 2`),
  16 draws, all with several credible plans: fixed-past learning always lands on a credible
  plan, the earliest one in 96%, and the preferred one only when that is the earliest (75%).
  Only 4 draws separate the two: the earliest wins in 3, every seed, and seeds vary in 1.
  A likely mechanism, untested: uncertainty about one's own timing is felt as loss-averse news, so
  resolving it early pays. The planner (`w = 1`) reaches commitment 73% (median shortfall
  0%): a stochastic policy's own randomness is felt as news, so deterministic plans are local
  optima even for the planner (`selection_report.txt`).
- **Anticipated news.** Deterministic plans carry none, so it moves no credible plan and not
  the commitment optimum; it acts on the learning path. Against forecasts that leave it out
  (certainty-equivalent), fixed-past learning picks the same date in every draw and seed.
  Those forecasts are rosier than rational ones, and in these draws loss-averse news
  outweighs anticipation, so rational bracing makes one's own randomness cheaper: the
  first-order cost of randomizing away from a plan is lower in 84% of directions (median 1.6
  against 2.5; no archived script), and the planner reaches commitment more often (73%
  against 60%, the earlier code's `selection_report.txt` at git `fd60c6c`; 16 draws, not
  significant).
## Follow-up agents

### The game agent

Random 2×2 games, one network for both roles, simultaneous gradient self-play. Each game is
the observer's event: moves at the announcement, revealed at `s`, my payoff set by the
other's move; my belief about it is chosen under the KL tether. Felt welfare in closed form,
batched (`felt.Event`, checked against `felt.BeliefPath` to 1e-15).

- Variants (`oneshot.py`; the belief head reads the action's trunk, or its own with
  `separate_belief`): expected payoffs (the Nash baseline); felt with calibrated beliefs;
  felt with free beliefs (tethered belief choice); felt with action coupled to belief (a soft
  best response to one's own belief).
- `run_games.py`: equilibrium play by game class, equilibrium selection, motivated beliefs, and
  linear probes for game class on the hidden layer; writes `games_report.txt` and `games.png`.
- `run_twin.py`: the `J` dial in symmetric games, where the other player is a copy of one's own
  policy. `w = 0` (the other's policy held fixed) against `w = 1` (gradient through the twin),
  and the graded dial on prisoner's dilemmas against its analytic thresholds.

### The hidden-game agent

Repeated rounds (10) of an unknown random 2×2 game against a self-play partner. A GRU sees
only past moves and its own realized payoffs; an action head and a critic, the forecast of
discounted payoffs to come. Felt utility per round reads the critic as anticipation and its
TD error as news (core, the RL reading; direct version, news over base payoffs). The policy
learns by REINFORCE against the batch mean, so the critic reaches it only through the state
they share.

- Variants: payoffs only; felt with an honest (TD-only) critic; felt with a motivated critic,
  which also ascends felt utility, tethered by its TD loss. Critic controls: a fixed per-round
  offset in the TD loss, expectile TD, a canonical critic that forecasts felt utility itself,
  rewards shifted for the learners only, a critic detached from the shared state, and the
  critic as the policy's baseline.
- `rounds.py` (the `Hidden` source, `hidden_layout`, rollout and trainer); `run_repeated.py` (the
  variants over seeds; `repeated_report.txt`, `repeated.png`); `run_braced.py` (what the critic's
  level does, eighteen critics over seeds; `braced_report.txt`, `braced.png`); `run_alignment.py` (value
  and staying share a direction in the state; `alignment_report.txt`); `run_channels.py` (the
  critic's level through the state, through the policy's baseline, or both;
  `channels_report.txt`); `run_evolve.py` (heritable felt parameters under selection on
  lifetime payoff; `evolve_report.txt`, `evolve.png`).

### The iterated-games agent

A different known game every round with the same partner: each round draws a prisoner's
dilemma, chicken, stag hunt or harmony game with fresh payoffs, shown to both players in
their own randomly ordered action labels, so the cooperative move must be read off the
matrix. A GRU carries the history (each past game, both moves, my payoff); a head reads the
state and the current game and gives the move and a critic (honest, its level kept outside
the network at the TD loss's mean target over all learners' episodes, D8). Self-play with
shared weights, REINFORCE on rewards-to-go; objective selfish (my payoffs) or team (both
players'). With mixed partners, half of each batch is played against scripted partners
(always cooperate, always defect, tit for tat, coin flip).
`rounds.py` (the `Iterated` source, `iterated_layout`, scripted partners); `run_iterated.py`
(writes `iterated_report.txt`, `iterated.png`); `run_baselines.py` (the
policy gradient's noise by baseline, batch mean against groups of episodes sharing their context;
`baselines_report.txt`).

### The unknown-adversary agent

The iterated agent against a partner drawn per episode and never revealed: a copy (the same network,
both seats learning), a past self (a frozen snapshot from earlier in training, a league), or one of
eight scripts (always cooperate, always defect, tit for tat, coin flip, grim, win-stay lose-shift,
suspicious and generous tit for tat); three more scripts are held out for evaluation (alternate,
tit for two tats, an extortionate reactive strategy). Horizons fixed (10 rounds), geometric
(continuation 0.9, capped at 30) or uniform (5–15), the clock running against the public cap.
Objectives selfish, twin (plus the partner's payoff only when it is a true copy: dependence gated on
an identity the agent does not see) or altruist (plus the partner's payoff always), weighted copies
1/4, past selves 1/4, scripts 1/2. Dr. GRPO-style groups of 4 episodes share horizon, games, labels and
partner, with leave-one-out baselines; the critic honest with its level outside, or motivated, rosy or
braced, on the shared state. `adversary.py`; `run_adversary.py` (`adversary_report.txt`,
`adversary.png`; per partner, a probe for its identity on the state, and cross-play among the final
agents).

### The partners agent

Caring about a partner, and twins against altruists (`notes/empathy.md`). A population of independently
initialized networks plays random symmetric 2×2 games, each the game agent's event; each network's
objective mixes matches against a copy of itself (weight `σ`) and against strangers: other networks, or
mirrors, its own current policy under a stop-gradient (lookalikes whose play the learner treats as
fixed). An
input bit says copy or stranger (optionally noisy, or absent). Beliefs calibrated. Three dials: `w_T`,
the gradient through a copy's policy (the twin); `w_E`, the weight on the partner's payoff (altruism) or
felt welfare (empathy); `J`, the gradient through the partner's forecast of my policy.

- `partners.py` (model, trainer, local-stability slopes; `python partners.py` checks that no gradient
  leaks between networks, that a copy at `w_T = 0` trains like a mirror, and the
  twin–empathizer identity); `run_partners.py` (the variants against the analytic stability classes;
  `partners_report.txt`, `partners.png`); `run_trust.py` (a trust game with felt empathy and the
  interpersonal `J`, analytic; `trust_report.txt`).
- Inferred dependence: a twin told only a noisy similarity signal adds its dependence gradient, evaluated
  in the copy branch, at its estimate `d(s)` that the partner is a copy (a Bayesian posterior under an
  assumed model, or a head on its own trunk fit to identities revealed after each match), against the
  identity oracle.
  Strangers and forgers (strangers with copy-like signals) are frozen causal networks from a shared bank.
  `dependence.py` (`python dependence.py` checks that the calibrated twin's expected gradient is the
  oracle's, payoff and felt); `run_dependence.py` (`dependence_report.txt`, `dependence.png`).

## Follow-up results

### Decision theory by learning

- **Games.** One network plays random 2×2 games at 87–96% equilibrium play (prisoner's-dilemma-like
  games lowest), and a linear probe recovers game class from its hidden layer at 81–89% against
  71% from raw payoffs (highest with free beliefs): it tells games apart, felt or not (the
  payoff-only agent: 82.5%; one run). Felt utility shifts equilibrium selection toward risk dominance: 97.4% against
  93.4% over five seeds, higher in every seed. Motivated beliefs appear almost only in cyclic
  games, where outcomes are uncertain, as optimism about the other's move, strongly only when
  action is coupled to belief (`q − p` +0.27 against +0.02 free; single training run;
  `games_report.txt`, `games.png`).
- **The twin dial.** In symmetric games, `w = 0` defects in prisoner's dilemmas and hunts hare;
  `w = 1` cooperates and hunts stag. Graded `w` matches the analytic thresholds game by game:
  all-cooperate is stable iff `w ≥ (T−R)/(R−S)`, all-defect iff `w ≤ (P−S)/(T−P)` (known in
  kind: stop-gradients and performative stability, Oesterheld et al. 2023). These are also the
  altruism thresholds: at symmetric profiles the twin's gradient is an altruist's at weight `w`
  (Alger & Weibull 2013 §6.2), so symmetric self-play cannot tell twin reasoning from other-regard.
- **Twins against altruists, told who is a copy.** With an input bit saying copy or stranger, twins
  (`w_T = 1`) cooperate with copies in 0.95 of prisoner's dilemmas and with strangers in 0.01, even
  with mirrors that run their own weights; altruists (`w_E = 1`) cooperate with both (0.98,
  0.99). Without the bit, a twin among a share `σ` of copies plays as an altruist at `σw`: 0.52 against
  0.51 at `σ = 0.5`, 0.21 against 0.21 at 0.25, class by class. Learned play follows the analytic local
  stability of all-cooperate and all-defect: 0.92–0.99 cooperation where only the first is stable,
  0.01–0.07 where only the second (2 populations × 4 networks per variant; `partners_report.txt`).
  Oesterheld et al. (2023) needed pretraining to get this split from naive learners; the twin's gate
  on true identity supplies it.
- **Felt empathy.** With felt utility, a twin is an empathizer whose partner's forecast tracks its
  policy (`J = 1`), exactly at symmetric profiles; the felt twin and that empathizer play alike with
  copies (0.50, 0.50) and differ with strangers (0.00 against 0.46). Felt news makes pure profiles
  sticky between copies. In the trust game, the temptation an empathizer resists is about its empathy
  weight at `J = 1` in every calibration; at `J = 0` it depends on what the partner expects (guilt makes
  trust self-fulfilling), and exceeds `J = 1`'s under the game agent's strong loss-averse news (1.45
  against 1.14 per unit of empathy), not at the felt calibration (0.75 against 1.02).
- **Inferred dependence is as good as knowing it, when calibrated.** Told only a noisy similarity signal,
  Bayesian and learned twins match the identity oracle in cooperation at every signal and in payoff (within
  0.0005, 4 seeds), as their equal expected gradients predict; the learned head recovers the posterior.
  Miscalibration is what matters, and its sign depends on the real dependence: among mirrors, which move
  with the twin's parameters, payoff rises with attributed dependence (0.375 calibrated, 0.381 credulous,
  0.384 treating everyone as a copy); among frozen strangers and forgers it falls (forgers: 0.315, 0.310,
  0.303), and over-attributing twins are exploited by forgers (0.225–0.234 against them, the oracle 0.258).
  An identity label is a convention about dependence, and it loses where it disagrees with the dependence
  that is there.
- **Iterated randomized games: strategy needs someone to strategize against.** Selfish
  learners trained only against themselves play each game as if it were one-shot: defect in
  the prisoner's dilemma (99%), cooperate in harmony, and in stag hunts coordinate on one
  equilibrium per game (same move 93%) without regard to history; the one-round control plays
  the same. Nothing depends on the partner's last move, the round, or who the partner is. Team
  learners cooperate everywhere. Trained against a mix of partners, the agent learns to
  strategize across games (4 seeds, `iterated_report.txt`):
  - reciprocity across different games: after the partner cooperated in a different game it
    cooperates in a prisoner's dilemma 37% of the time, after a defection 6% (stag hunt 83%
    against 53%);
  - reading the partner: against always-defect, cooperation in prisoner's dilemmas falls from
    39% to 4% after one round; against tit for tat it rises to about 70% and holds until the
    last rounds; against an unconditional cooperator it rises and then is exploited, down to
    9% by round 10;
  - an end game: prisoner's dilemma cooperation 32% in rounds 1–9, 5% in round 10;
  - reciprocity carries back into self-play (prisoner's dilemma 29%, stag hunt 75%, from 1% and
    51%), and appears late in training, after about 1,500 steps of near-total defection.
  - Three times longer training (9000 steps, 4 seeds) does not raise self-play cooperation
    (prisoner's dilemma 0.24–0.31) but sharpens the end game: against tit for tat, about
    0.6–0.7 through round 9, then 0.07 in round 10 (0.27 at 3000 steps).
- **Unknown adversaries: the horizon sets the end game, and twins find no handshake** (4 seeds per
  variant, `adversary_report.txt`, `adversary.png`).
  - Against copies, past selves and eight scripts, selfish learners reciprocate across games: in
    prisoner's dilemmas they cooperate with every reciprocating partner (copies, past selves, tit
    for tat, grim, win-stay lose-shift: 0.73–0.75 on the fixed horizon, about 1.00 on the geometric),
    defect against always-defect from round 3 (0.99, 0.33, 0.06), and exploit unconditional
    cooperators only in the end game (a reading, untested: they look like reciprocators until
    probed, and grim punishes probing). Self-play 0.73 (the four-script iterated agent: 0.29). Held
    out, tit for two tats is met as a reciprocator, alternation as a defector, an extortionate
    reactive strategy in between (0.52–0.59).
  - The hazard sets the end game. Against tit for tat over the last five rounds: fixed horizon
    0.92, 0.74, 0.48, 0.27, 0.15; uniform on 5–15, 0.96 to 0.83; geometric, flat at 1.00.
  - Selfish learners defect until about step 1,250, as the iterated agent does; twins and altruists
    cooperate from the start. With group baselines reciprocity was in place by step 1,500 in every
    seed (cooperation with the step-1,500 self 0.85–0.98), with the batch baseline in none
    (0.31–0.36).
  - Twins cooperate with copies, past selves and reciprocating scripts alike (fixed horizon: 0.91,
    0.91, 0.86–0.92), and their dependence shows only in the end game, extended to all of them
    (round 10: 0.77 against copies, 0.76 against tit for tat; selfish 0.09). Partner identity is
    equally decodable from every honest agent's state (0.38–0.39 after five rounds, chance 0.10):
    against a cooperator, copies and reciprocators look alike, and telling them apart takes
    deviations that reciprocators punish. A twin that cannot tell copies apart spends its
    dependence on their lookalikes, as the partners agent's twin without a signal plays as an
    altruist at `σw` (synthesis; the matching altruist is untested).
  - Cross-play, fixed horizon (the row agent's payoff): selfish earns most against every column
    (0.359 against selfish, 0.409 against twins, 0.443 against altruists), twins are exploited in
    the end game, altruists cooperate with everyone, always-defect included. On the geometric
    horizon all nine pairings cooperate fully.
  - A rosy critic makes a defector, not a sucker. With the motivated critic at `a = 0.3` on the
    shared state, prisoner's dilemma cooperation stays at 0.10–0.19 against every partner, copies
    and tit for tat included (self-play payoff 0.27 against 0.40): stuck in the early defection
    basin, as the hidden-game agent stays complacent (D8). Its state tells partners apart better
    (0.55 after five rounds): defection draws distinct replies. A braced critic (`a = 0.02`) ends
    where the honest one does, later (cooperation with the step-1,500 self 0.33).
- **Gradient noise by baseline** (mixed partners, one training run, `baselines_report.txt`). At equal
  episode budget, groups of 4 episodes sharing their game sequence and partner type, with a leave-one-out
  group baseline (Dr. GRPO's estimator: no std or length normalization), cut the policy gradient's noise
  1.5–2.3× against the per-round batch mean once learning starts. Larger groups lose it to fewer distinct
  contexts (64: 2–3× noisier than the batch mean), and GRPO's std normalization is 6–7× noisier. What
  remains is within-context: one move's credit against nine rounds of sampled play.

### Shared-state critics and felt learners

- **Hidden games: two policies.** Training first reaches a complacent policy: after a loss in
  round 1 it switches only about 45% of the time, never after a gain (about 0.21 per round
  late). It then usually escapes to win-stay, lose-shift at zero (switch after 99% of losses,
  about 10% of gains), which explores and learns the game (about 0.30). One honest seed stays
  complacent for 9000 steps.
- **A high critic keeps the agent complacent.** The policy never reads the critic, yet the
  critic's level decides the escape, through the state they share. A free critic is rosy when
  anticipation outweighs chronic disappointment (`aν > nλ(1−ν)`) and braced otherwise: honest
  critics escape in 7/8 seeds (steps 250–1250), braced ones in 8/8 (by step 750), rosy ones in
  0/8 (`braced_report.txt`, `braced.png`).
  - It is the level, not the bias. An honest critic of rewards shifted by +0.5 (a shift the
    state does not see and the policy's baseline removes, so only the critic's numbers move)
    stays complacent in 6/6 seeds, like a rosy one; shifted by −0.5 it escapes in 6/6 at step
    500, like a braced one. Fixed offsets and expectile critics agree: below realized payoffs
    16/16 escape by step 750, however deep; well above, 0/8; mildly above, slowly. Neither loss
    aversion nor the felt objective is needed (at `λ = 1` the motivated critic's gradients
    equal a fixed offset's exactly; Codex). Detached from the state, a rosy critic escapes 2/4.
  - Kept outside the network (a running mean of the targets, as PopArt-style normalization
    does), the level stops mattering: the +0.5 critic escapes in 6/6, as D8 predicts.
  - Mechanism (`formalism/learning.md`, D8): once learning starts, the critic's value and
    the policy's stay logit share a direction in the state (gradient cosine 0.34–0.58 at step 150, about
    0 at initialization, drifting back toward 0 or below by step 500 in three of four seeds),
    and a step that raises value raises staying after losses and gains alike in every seed at
    every trained checkpoint (`alignment_report.txt`). A critic that must output
    high numbers keeps telling the policy things are fine. Open: removing the per-round mean of
    the critic's push on the state also stops the honest critic from escaping (0/4), though
    its mean residual is small and fluctuates in sign.
  - The canonical critic, honest about felt utility, sits above payoffs at `λ = 1` (its target
    includes echoes) and escapes in 1/4; at `λ = 2` in 1/8, late.
- **Through the decision rule instead.** With the critic as the policy's baseline and kept off
  the state, its level makes no detectable difference (honest 3/6, rosy 1/6, braced 2/6;
  `channels_report.txt`): a baseline's level leaves the expected gradient unchanged and acts
  only through sampling noise (Chung et al. 2021), which batches of 2048 games average away.
  With an undiscounted critic, whose honest values are higher, the shared-state channel keeps
  its order at lower rates (braced 3/6, honest 1/6, rosy 0/6).
- **Felt utility as the policy's reward** leaves the escape rate unchanged at `a = 0.3` (3/4
  seeds, as for payoffs); at weak anticipation it escapes 1/4, and a motivated, braced critic
  restores 4/4 (`repeated_report.txt`, 4 seeds each). Escaped agents' states tell game classes
  apart better (linear probe 41–45% balanced accuracy by round 10, chance 25%; complacent 34%).
- **Which ways of feeling survive?** Populations of learners born untrained, with heritable
  `(a, n, λ)`, selected on lifetime payoff over ten generations (weights not inherited; 3 runs
  per variant, 240 learners each). Whether affect shapes only the critic or also the policy's
  reward, selection runs against anticipation and for felt news, with no detectable selection
  on loss aversion: lifetime payoff (×1000) per s.d. of log `a` −4.4 and −5.4, of log `n` +4.0
  and +3.4, of log `(λ − 1)` +0.1 and −0.2 (pooled s.e. 0.8 each, which treat learners as
  independent despite shared games and ancestry; run-level uncertainty is larger, with 3 runs
  per variant); a neutral control shows none (all within one s.e.). Only anticipation moves
  the population: final `a` 0.025 and 0.038 against the neutral control's 0.134. Final `n`
  (0.10, 0.17) sits near the founders' median 0.1, inside the neutral control's drift (IQR
  0.017–0.25), so selection for news shows within generations, not above drift. Populations
  recover the 10% of lifetime payoff their founders' affect cost. Critics trained at the
  final medians sit slightly below payoffs (−0.03 to −0.13; a 3-seed, 1000-step check in the
  2026-10-15 review) against +0.79 at the founders' median: selection removes the rosy push
  and leaves critics roughly honest, which escape complacency as braced ones do (7/8 against
  8/8, D8). Loss aversion adds bracing before outcomes and consolation after them, which
  may be why it is not selected. Fitness is payoff over a short lifetime, mostly escape
  speed, and the report ran with 1200 steps, 10 generations and 3 runs, not the script's
  defaults (`evolve_report.txt`).
- **Consolation.** At `λ = 2` the motivated critic braces before outcomes and consoles itself
  after bad ones: just after a negative TD error it sits 0.18 below realized payoffs, after a
  positive one 0.51 below. At `λ = 1` the gap vanishes (0.33 against 0.29), as the critic's
  first-order condition predicts (`decision.md`, D5, rationalization).
