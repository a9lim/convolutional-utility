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
