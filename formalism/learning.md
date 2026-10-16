# Learning: the critic's level

Tags as in `core.md`. The formal side of the learner experiments outside the post
(`experiments/learned_expectations/`, its follow-up lines). The post's affect-policy section may
cite it in one line (`outline.md`, §6).

**D8. A shared state carries the critic's level.** [synthesis: a specialization of the
tangent-kernel calculus (Jacot, Gabriel & Hongler 2018) and of the linear-network modes of
Saxe, McClelland & Ganguli (2014); checked. Known in kind: value and policy interfere in
shared networks (Cobbe et al. 2021); reward shifts set exploration through learned Q-values,
with the same sign (Sun et al. 2022)]
- Setting: a policy and a critic read one learned state `φ_θ(x)`. The policy's stay logit
  (within one previous action) is `z = s·φ + c_z`, the critic's value `V = v·φ + c_V`. The
  critic's targets are raised by `o`: a fixed offset, a reward shift that the policy's
  baseline removes, or a rosy felt objective (at `λ = 1` exactly an offset).
- **(a) The only route.** On a given batch the policy's loss does not depend on `o` (a
  per-round batch-mean baseline over a fixed horizon removes a reward shift exactly). So,
  setting aside optimizer-wide coupling such as global gradient clipping, `o` reaches the
  policy only through the critic's gradient on `θ`.
- **(b) The forcing.** At given parameters, data and detached targets, the `o`-part of the
  critic's gradient moves the policy at `x'` at rate `2ηo E_x[K(x', x)]` under gradient flow,
  with `K(x', x) = ∇_θ z(x')·∇_θ V(x)` the cross tangent kernel of the two heads. In a
  two-layer linear model (`φ = Wx`; `x` a constant feature plus zero-mean features), fit the
  critic alone to fixed targets by squared error, both heads frozen, `W` and `c_V` at equal
  rates. Shifting the fitted targets by `f(x) = μ + f̃(x)` (`f̃` zero-mean and representable)
  ends with the stay logit moved by
  `Δz(x) = (s·v) [μ/(1 + ‖v‖²) + f̃(x)/‖v‖²]`.
  The critic's bias takes `μ/(1 + ‖v‖²)` of the mean; the state carries the rest of the
  mean and all of the varying part. This is the endpoint of the critic's fitting only: the
  policy's own learning can undo the displacement, and bootstrapped TD targets fall outside
  it.
- **(c) The sign, in a regression surrogate.** Two outputs on whitened inputs with targets
  `V* = αr` and `z* = βr` (`r` the last payoff) have, at a balanced rank-one zero-error
  factorization (where small initialization leads), `v = (α/√σ)u` and `s = (β/√σ)u` for a
  unit `u`, `σ = √(α² + β²)`: `s·v = αβ/σ`, `‖v‖² = α²/σ`, and a constant offset gives
  `Δz = oαβ/(σ + α²)`. So when value and staying both rise with the last payoff (the game
  persists; win-stay), a high critic pushes toward staying and a low one toward switching,
  biased or not. The policy learns by REINFORCE, whose improvement direction depends on the
  history, the policy and the round, so this illustrates how positively related targets
  align the heads; it is not a theorem about the agent.
- In the GRU agent: the two heads' gradients go from unrelated at initialization to a
  cosine of 0.34–0.58 by step 150 (drifting back to −0.27–+0.05 by step 500 in three of
  four seeds), a step that raises value raises staying in every seed at every trained
  checkpoint measured (steps 150–500; none at initialization), and reward shifts of ±0.5 decide complacency (6/6 against 0/6),
  though the policy's gradient is unchanged on every batch. The prediction that follows:
  keep the critic's level outside the network (a running mean of its targets, as
  PopArt-style normalization does) and the shift stops mattering. It does: 6/6 escape at
  +0.5. [checked in `experiments/learned_expectations/`]
- Limits: Adam's momentum and gradient-dependent denominator change with the offset, so the
  kernel in (b) is only a guide to its updates. Unexplained: removing the critic's mean push
  on the state also traps the honest critic.
