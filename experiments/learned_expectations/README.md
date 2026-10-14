# Learned expectations

Agents whose reward is their own felt utility (the canonical model, `formalism/core.md`),
computed from their own forecasts and realized against the world. Expected return under
the true environment is then the objective expectation of the felt life-sum: Brunnermeier &
Parker's well-being, learned. Plan and prior art: `next-steps.md`, "Extension (a9)".

## The observer

An event is announced at 0 and resolves at `s`. At each `t < s` the self holds a subjective
probability `q_t` of the high outcome and forecasts its felt life rationally given `q_t`.
Changing a belief revises forecasts, so it is felt as news. Realization is news against the
last belief. The objective is the objective expected life-sum minus a cost of self-deception,
`Σ_t KL(q_t ‖ p) / τ`; without it, beliefs at the felt calibrations run to N3's corners.

- `observer.py`: the model in closed form (core N3, canonical), differentiable in the belief
  path, and the exact optimizer. Checked against an independent Bayesian tree solver at
  `q = p` (welfare to 1e-10) and against finite differences (gradient to 3e-10).
- `run_observer.py`: exact optimal belief paths at the life calibration for three kinds of
  event and four tethers; writes `observer_paths.png`.
- `learn_observer.py`: one network that maps an event's features to a belief path, trained on
  felt welfare across random events and compared with the exact optimum on held-out events.

The objective has a kink wherever two consecutive beliefs agree (a zero revision, priced at
`λ` on one side), so optimal beliefs are sticky and smooth optimizers stall on them; the
exact optimizer uses Adam with a decaying rate from several starts, including the best
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
  `channels_report.txt`).

## Results so far

- **Observer.** Optimal beliefs at the life calibration stay calibrated far from the event,
  brace as it nears, and freeze over the last few periods; optimism never pays there. A
  network trained on felt welfare captures a median 71% of the exact gain on held-out events.
- **Scheduling: the `J` dial reproduces the decision theories.** Over 30 draws, `w = 0` learns
  the subgame-perfect fixed-past date in every draw without news and 90% with linear news
  (the misses sit right after the announcement: two unconverged, one a second equilibrium);
  `w = 1` learns the commitment date in every draw. Intermediate `w` gives a staircase from
  the trap to commitment (`scheduling_dial.png`, `scheduling_report.txt`).
- **Which credible plan does learning select?** With loss-averse news (`n = 0.3, λ = 2`),
  16 draws, all with several credible plans: fixed-past learning always lands on a credible
  plan, the earliest one in 96%, and the preferred one only when that is the earliest (75%).
  A likely mechanism: uncertainty about one's own timing is felt as loss-averse news, so
  resolving it early pays. The planner (`w = 1`) reaches commitment 73% (median shortfall
  0%): a stochastic policy's own randomness is felt as news, so deterministic plans are local
  optima even for the planner (`selection_report.txt`).
- **Anticipated news.** Deterministic plans carry none, so it moves no credible plan and not
  the commitment optimum; it acts on the learning path. Against forecasts that leave it out
  (certainty-equivalent), fixed-past learning picks the same date in every draw and seed.
  Those forecasts are rosier than rational ones, and in these draws loss-averse news
  outweighs anticipation, so rational bracing makes one's own randomness cheaper: the
  first-order cost of randomizing away from a plan is lower in 84% of directions (median 1.6
  against 2.5), and the planner reaches commitment more often (73% against 60%).
- **Games.** One network plays random 2×2 games at 91–96% equilibrium play, and a linear probe
  recovers game class from its hidden layer at 88% against 71% from raw payoffs: it tells
  games apart. Felt utility shifts equilibrium selection toward risk dominance (97% against
  92%). Motivated beliefs appear almost only in cyclic games, where outcomes are uncertain,
  as optimism about the other's move (`games_report.txt`, `games.png`).
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
    0 at initialization), and a step that raises value raises staying after losses and gains
    alike in every seed and checkpoint (`alignment_report.txt`). A critic that must output
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
- **Consolation.** At `λ = 2` the motivated critic braces before outcomes and consoles itself
  after bad ones: just after a negative TD error it sits 0.18 below realized payoffs, after a
  positive one 0.51 below. At `λ = 1` the gap vanishes (0.33 against 0.29), as the critic's
  first-order condition predicts (decision.md D5, rationalization).
