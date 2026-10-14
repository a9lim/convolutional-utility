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
utility is the canonical model with linear news, its forecasts rational under a self-model of
the same policy, so every world (the date it is taken) is solved exactly.

- The `J` dial is a gradient setting: the self-model enters as `π.detach() + w (π − π.detach())`.
  At `w = 0` past selves' forecasts carry no gradient, and gradient ascent on the life-sum gives
  each self its fixed-past incentive: causal decision theory. At `w = 1` the gradient includes
  how the policy shaped past anticipation: the commitment planner.
- Each self's gradient is divided by its reach probability and its sigmoid slope, so it follows
  that self's incentive conditional on being there; otherwise off-path selves and saturated
  logits stall learning short of the equilibrium.
- `scheduling.py` (model, learner, exact benchmarks); `run_scheduling.py` (a sweep against the
  exact fixed-past and commitment dates, and the dial; writes `scheduling_dial.png`).

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
TD error as news (core, the RL reading; direct version, news over base payoffs).
Variants: payoffs only; felt with an honest (TD-only) critic; felt with a motivated critic,
which also ascends felt utility, tethered by its TD loss. `repeated.py`, `run_repeated.py`
(writes `repeated_report.txt` and `repeated.png`).

## Results so far

- **Observer.** Optimal beliefs at the life calibration stay calibrated far from the event,
  brace as it nears, and freeze over the last few periods; optimism never pays there. A
  network trained on felt welfare captures a median 71% of the exact gain on held-out events.
- **Scheduling: the `J` dial reproduces the decision theories.** Over 30 draws, `w = 0` learns
  the subgame-perfect fixed-past date in every draw without news and 90% with linear news
  (the misses sit right after the announcement: two unconverged, one a second equilibrium);
  `w = 1` learns the commitment date in every draw. Intermediate `w` gives a staircase from
  the trap to commitment (`scheduling_dial.png`, `scheduling_report.txt`).
- **Which credible plan does learning select?** With loss-averse news (`n = 0.3, λ = 2`,
  forecasts certainty-equivalent in news), 16 draws, all with several credible plans:
  fixed-past learning always lands on a credible plan, and on the earliest one, not the
  preferred one (it matches the preferred plan only when that is the earliest, 75%). A
  likely mechanism: uncertainty about one's own timing is felt as loss-averse news, so
  resolving it early pays. The planner (`w = 1`) reaches commitment 60% (median shortfall
  0%): a stochastic policy's own randomness is felt as news, so deterministic plans are local
  optima even for the planner (`selection_report.txt`).
- **Games.** One network plays random 2×2 games at 91–96% equilibrium play, and a linear probe
  recovers game class from its hidden layer at 88% against 71% from raw payoffs: it tells
  games apart. Felt utility shifts equilibrium selection toward risk dominance (97% against
  92%). Motivated beliefs appear almost only in cyclic games, where outcomes are uncertain,
  as optimism about the other's move (`games_report.txt`, `games.png`).
- **The twin dial.** In symmetric games, `w = 0` defects in prisoner's dilemmas and hunts hare;
  `w = 1` cooperates and hunts stag. Graded `w` matches the analytic thresholds game by game:
  all-cooperate is stable iff `w ≥ (T−R)/(R−S)`, all-defect iff `w ≤ (P−S)/(T−P)` (known in
  kind: stop-gradients and performative stability, Oesterheld et al. 2023).
- **Hidden games.** Payoff per round rises from 0.00 to 0.21 within an episode as the agent
  learns the game. Felt utility leaves play unchanged; a critic free to ascend felt utility is
  rosy when anticipation outweighs chronic disappointment (`aν > nλ(1−ν)`: forecasts about 2×
  realized) and braced otherwise (`a = 0.05`: −2.4 at round 1, relaxing to −0.1): affect
  decoupled from action (D7). A surprise: the braced critic raises payoffs to 0.31 (two seeds);
  the ablation puts the gain in the critic's felt objective acting on the shared state, not in
  the felt reward. Mechanism open (`repeated_report.txt`, `repeated.png`).
