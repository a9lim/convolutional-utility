# Learned expectations

Agents whose reward is their own felt utility (`formalism/core.md`), computed from their own
forecasts and realized against the world. The observer and the scheduling agent use the
canonical model, and so does the game agent, through `felt.py`'s closed form (checked
against `observer.py`); the hidden-game and evolution agents use a direct first pass (echoes
of base payoffs, news on the aggregate TD error); the iterated agent learns on payoffs
alone, with no felt utility. Even the canonical critic kinks the aggregate TD error rather
than each horizon's revision, which agree only at `λ = 1` or when the revisions share a
sign. Expected return under the true environment is then the objective expectation of the
felt life-sum: Brunnermeier & Parker's well-being, learned. Open items: `next-steps.md`,
item 1.

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
  `J` graded inside a life-sum; belief and affect heads (D7's two filtrations); the
  LLM-welfare angle.

## The observer

An event is announced at 0 and resolves at `s`. At each `t < s` the self holds a subjective
probability `q_t` of the high outcome and forecasts its felt life rationally given `q_t`.
Changing a belief revises forecasts, so it is felt as news. Realization is news against the
last belief. Forecasts are rational given the current belief and naive about the self's own
later revisions: at each `t` it expects to keep `q_t` until `s`. The objective is the
objective expected life-sum minus a cost of self-deception, `Σ_t KL(q_t ‖ p) / τ`; without
it, beliefs at the felt calibrations run to N3's corners.

- `observer.py`: the model in closed form (core N3, canonical), differentiable in the belief
  path, and a numerical reference optimizer (multistart Adam plus the best step path; no
  certificate of global optimality). Checked against an independent Bayesian tree solver at
  `q = p` (welfare to 1e-10) and against finite differences (gradient to 3e-10).
- `run_observer.py`: reference-optimal belief paths at the life calibration for three kinds of
  event and four tethers; writes `observer_paths.png`.
- `learn_observer.py`: one network that maps an event's features to a belief path, trained on
  felt welfare across random events and compared with the reference optimum on held-out events.

The objective has a kink wherever two consecutive beliefs agree (a zero revision, priced at
`λ` on one side), so optimal beliefs are sticky and smooth optimizers stall on them; the
reference optimizer uses Adam with a decaying rate from several starts, including the best
step-shaped path.

Run from the repo root, e.g. `python experiments/learned_expectations/run_observer.py`.

## The scheduling agent (decision.md D3)

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

## The game agent

Random 2×2 games, one network for both roles, simultaneous gradient self-play. Each game is
the observer's event: moves at the announcement, revealed at `s`, my payoff set by the
other's move; my belief about it is chosen under the KL tether. Felt welfare in closed form,
batched (`felt.py`, checked against `observer.py` to 2e-15).

- Variants (`games.py`): expected payoffs (the Nash baseline); felt with calibrated beliefs;
  felt with free beliefs (D7's decoupled affect); felt with action coupled to belief (a soft
  best response to one's own belief).
- `run_games.py`: equilibrium play by game class, equilibrium selection, motivated beliefs, and
  linear probes for game class on the hidden layer; writes `games_report.txt` and `games.png`.
- `run_twin.py`: the `J` dial in symmetric games, where the other player is a copy of one's own
  policy. `w = 0` (the other's policy held fixed) against `w = 1` (gradient through the twin),
  and the graded dial on prisoner's dilemmas against its analytic thresholds.

## The hidden-game agent

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
- `repeated.py` (agent, felt utility, trainer); `run_repeated.py` (the variants over seeds;
  `repeated_report.txt`, `repeated.png`); `run_braced.py` (what the critic's level does,
  sixteen critics over seeds; `braced_report.txt`, `braced.png`); `run_alignment.py` (value
  and staying share a direction in the state; `alignment_report.txt`); `run_channels.py` (the
  critic's level through the state, through the policy's baseline, or both;
  `channels_report.txt`); `run_evolve.py` (heritable felt parameters under selection on
  lifetime payoff; `evolve_report.txt`, `evolve.png`).

## The iterated-games agent

A different known game every round with the same partner: each round draws a prisoner's
dilemma, chicken, stag hunt or harmony game with fresh payoffs, shown to both players in
their own randomly ordered action labels, so the cooperative move must be read off the
matrix. A GRU carries the history (each past game, both moves, my payoff); a head reads the
state and the current game and gives the move and a critic (honest, its level kept outside
the network, D8). Self-play with shared weights, REINFORCE on rewards-to-go; objective
selfish (my payoffs) or team (both players'). With mixed partners, half of each batch is
played against scripted partners (always cooperate, always defect, tit for tat, coin flip).
`iterated.py`; `run_iterated.py` (writes `iterated_report.txt`, `iterated.png`).

## Results so far

- **Observer.** Optimal beliefs at the life calibration stay calibrated far from the event,
  brace as it nears, and freeze over the last few periods; optimism never pays there. A
  network trained on felt welfare captures a median 71% of the reference optimizer's gain on
  ten held-out events (one training run; the reference has no optimality certificate).
- **Scheduling: the `J` dial reproduces the decision theories.** Over 30 draws, `w = 0` learns
  the subgame-perfect fixed-past date in every draw without news and 90% with linear news
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
  kind: stop-gradients and performative stability, Oesterheld et al. 2023).
- **Hidden games: two policies.** Training first reaches a complacent policy: after a loss in
  round 1 it switches only about 45% of the time, never after a gain (about 0.21 per round
  late). It then usually escapes to win-stay, lose-shift at zero (switch after 99% of losses,
  about 10% of gains), which explores and learns the game (about 0.30). One honest seed stays
  complacent for 9000 steps.
- **A high critic keeps the agent complacent.** The policy never reads the critic, yet the
  critic's level decides the escape, through the state they share. A free critic is rosy when
  anticipation outweighs chronic disappointment (`aν > nλ(1−ν)`) and braced otherwise: honest
  critics escape in 7/8 seeds (steps 250–1500), braced ones in 8/8 (by step 750), rosy ones in
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
  - Mechanism (decision.md D8): once learning starts, the critic's value and the policy's
    stay logit share a direction in the state (gradient cosine 0.34–0.58 at step 150, about
    0 at initialization, drifting back toward 0 or below by step 500 in three of four seeds),
    and a step that raises value raises staying after losses and gains alike in every seed at
    every trained checkpoint (`alignment_report.txt`). A critic that must output
    high numbers keeps telling the policy things are fine. Open: removing the per-round mean of
    the critic's push on the state also stops the honest critic from escaping (0/4), though
    its mean residual is small and fluctuates in sign.
  - The canonical critic, honest about felt utility, sits above payoffs at `λ = 1` (its target
    includes echoes) and escapes in 1/4; at `λ = 2` in 3/8, late.
- **Through the decision rule instead.** With the critic as the policy's baseline and kept off
  the state, its level makes no detectable difference (honest 3/6, rosy 2/6, braced 3/6;
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
- **Iterated randomized games: strategy needs someone to strategize against.** Selfish
  learners trained only against themselves play each game as if it were one-shot: defect in
  the prisoner's dilemma (99%), cooperate in harmony, and in stag hunts coordinate on one
  equilibrium per game (same move 94%) without regard to history; the one-round control plays
  the same. Nothing depends on the partner's last move, the round, or who the partner is. Team
  learners cooperate everywhere. Trained against a mix of partners, the agent learns to
  strategize across games (4 seeds, `iterated_report.txt`):
  - reciprocity across different games: after the partner cooperated in a different game it
    cooperates in a prisoner's dilemma 43% of the time, after a defection 6% (stag hunt 86%
    against 54%);
  - reading the partner: against always-defect, cooperation in prisoner's dilemmas falls from
    43% to 4% after one round; against tit for tat it rises to about 75% and holds until the
    last rounds; against an unconditional cooperator it rises and then is exploited, down to
    11% by round 10;
  - an end game: prisoner's dilemma cooperation 38% in rounds 1–9, 9% in round 10;
  - reciprocity carries back into self-play (prisoner's dilemma 35%, stag hunt 78%, from 1% and
    50%), and appears late in training, after about 1,500 steps of near-total defection.
  - Three times longer training (4 seeds; output not archived) does not raise self-play
    cooperation (prisoner's dilemma 0.22–0.38) but sharpens the end game: against tit for
    tat, about 0.7 through round 9, then 0.06–0.12 in round 10.
- **Consolation.** At `λ = 2` the motivated critic braces before outcomes and consoles itself
  after bad ones: just after a negative TD error it sits 0.18 below realized payoffs, after a
  positive one 0.51 below. At `λ = 1` the gap vanishes (0.33 against 0.29), as the critic's
  first-order condition predicts (decision.md D5, rationalization).
