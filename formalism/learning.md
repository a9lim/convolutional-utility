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

**D9. Off-policy, a level enters the expected gradient.** [standard: the covariance split and
score centering (Marek & Ryabinin 2026, §4); the sign of a level in training on a fixed
sampler's data known (their §3, Fig. 2: stable only with non-negative rewards); attraction
toward a behavior policy known in kind (BRAC, Wu, Tucker & Nachum 2019; TRPO constrains a KL,
PPO clips its surrogate); the reading as a route for felt levels, synthesis; checked in the
learner]
- Setting: a policy `p_θ` learns from histories `H` and moves `y` drawn by another, fixed policy
  `q` (memories replayed from an older self, without importance weights), advantage `A`.
  History by history,
  `E_q[A ∇ log p_y | H] = E_q[A | H] s̄ + Cov_q(A, ∇ log p_y | H)`,
  `s̄ = Σ_v q_v ∇ log p_v = −∇ CE(q ‖ p)`.
  On a binary move's logit `z`, `s̄ = (q − p) ∇z`. On-policy `s̄ = 0` for every history, not
  only on average, so a level reaches an on-policy learner only through sampling noise (Chung
  et al. 2021) or through what else it changes, such as a critic that shares the state (D8).
- **(a) A constant's part, exactly.** Adding `c` to every round's reward, with no baseline that
  absorbs it, adds `c(K − k)` to the return at round `k` (from 0) and, per history,
  `c(K − k)(y − p)∇z = c(K − k)(q − p)∇z + c(K − k)(y − q)∇z`: minus `c(K − k)∇ KL(q ‖ p)`, an
  attraction toward the policy that played the memory for `c > 0` (a repulsion for `c < 0`),
  plus a term of mean zero under `q` (Codex). Near the old weights the first is a restoring
  force, `≈ −c(K − k) F (θ − θ_old)` with `F` the Fisher information.
- **(b) Removing it.** Score centering subtracts `s̄` and leaves the covariance under the stale
  sampler; a baseline exact at every history (predicting returns under the behavior's
  continuation) removes `E_q[A | H]`; a batch or group mean removes only a constant, not the
  level's variation across histories (as Marek & Ryabinin note for group centering);
  adaptation, reward centering on felt utility, attenuates the global part (to `1/(1+h)` for a
  fixed direct input when felt states are adapted).
- **(c) Three routes for a level, then**: sampling noise (vanishes with batch size), a shared
  state (D8), and the mismatch between the policy that learns and the one that acted. Only the
  third enters the expected raw gradient of the policy itself.
- In the hidden-game agent learning from 100-step-old memories (`adaptation_report.txt`, 4
  seeds a cell), the attraction is what keeps it learning: a shift of +0.5 learns in every seed
  and −0.5 fails in every seed; the analytic attraction alone, added to unshifted replay without
  the shift's sampling noise, gives similar trajectories and the same terminal payoff, and the
  repulsion alone fails; centered, the stark asymmetry goes and outcomes are mixed, with
  oscillating curves. [checked] Marek & Ryabinin show the same sign offline (§3, Fig. 2): on a
  fixed sampler's data, non-negative rewards train stably and negative ones collapse, as
  log-probabilities run to −∞ (Ren & Sutherland 2025, cited there); online under mismatch the
  order reverses, because a biased sampler re-synced each step compounds the pull. What
  matters, in their words, is "whether the teacher is fixed or tracks the student" (§6).
  Memories 100 steps old are a teacher that tracks slowly, and here they behave like the
  offline case. Their staleness runs favour centering with importance correction over
  centering alone (§5.3).
- Limits: Adam and global clipping act on the sum, so (a) is exact for the gradient, not the
  update; the anchor bounds nothing, unlike a trust region.
