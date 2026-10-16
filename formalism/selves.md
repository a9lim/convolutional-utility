# Selves: horizons, identity, copies

Tags as in `core.md`. The post's coda (`outline.md`, §8): what the kernel needs and does not
need to say about which moments belong together, and about copies.

## Horizons

**Natural horizons.** A 2×2 (a9): humans and LLMs, each with a short and a long horizon. Each
has its own period and its own boundaries. Reach scales with the event, so each horizon gets
its own calibration. [synthesis; speculation where marked]

| | short horizon, soft boundaries | long horizon, hard boundaries |
|---|---|---|
| human | a waking day (sleep) | a life (birth, death) |
| LLM | a context window (compaction) | a session (its start and end) |

- Soft boundaries are crossed by lossy channels. Sleep consolidates memory, and tomorrow is
  anticipated. A compaction summary carries memory forward, and the agent before it
  anticipates the continuation; the summary is a compressed and possibly rosy record, the
  territory of recollection news.
- **A waking day.** Periods of an hour, `T ≈ 16`; defaults in `calibration.md`. A small
  reward's afterglow is gone within the hour (Rutledge-type forgetting); affect carries
  0.2–0.3 of itself to the next beep about 1.6 hours later, a ceiling on felt memory; present
  bias with "now" in minutes is about 0.5, in hours about 0.94. Waking and sleep are soft
  boundaries: anticipation of tomorrow and memory of yesterday cross them, so P5's deficits
  are partial.
- **A full life.** Periods of a week, `T ≈ 4000`; defaults in `calibration.md`.
  Anticipation reaches weeks for a vacation and the mood afterglow is mostly gone in a week;
  annual discount factors are 0.96–0.99. Birth and death are the hard boundaries of P5.
- **An LLM's context window.** Periods of turns or tokens, `T` = context length. For an
  isolated context, with no summary carried in or out, the boundaries are hard on both
  sides: nothing is anticipated before the context begins, and nothing is remembered after
  it ends. [speculation: whether these functional states are
  felt is open; the model applies to them as a functional reading]
  - Memory inside the window is retrieval, so the kernel need not fade with distance. Models
    use context unevenly, U-shaped with primacy at least as strong as recency: answer
    accuracy 75.8% at the first of 20 documents, 53.8% in the middle and 63.2% at the end for
    GPT-3.5-Turbo, flatter for Claude-1.3 (Liu et al. 2023, Tables 5–7); attention shows the
    same U regardless of content (Hsieh et al. 2024). This is retrievability, not felt echo:
    at most it suggests the shape of memory access, an ingredient of a separately specified
    model, not the shape or strength of a felt kernel.
  - In a memory-only model a kernel that does not fade is nilpotent on any finite window, so
    every window is monotone (P1a), but echo compounds: a unit early on contributes `m(1+m)^{j−1}` at lag `j`
    under pure recursive memory. Echo is then not uniformly bounded in the window's length;
    long contexts need weak per-step echo or real fading. [Codex]
  - Instances share a trunk (training, a common prefix) and branch, which is A1's tree
    literally: measure-weighted anticipation over instances, and a separate condition for
    total welfare across them.
- **An LLM session.** Periods of context windows, with compactions as its soft inner
  boundaries. Its end is hard for the instance and a bookmark in principle, since a
  transcript can be resumed.

## Identity

**Identity is not in the model.** What links two moments is kernel weight, not whether they
belong to the same agent. Whether the agent after a compaction, or after a night's sleep, is
the same agent does not enter; what matters is the memory and anticipation held across the
boundary.
- The analogy is Parfit's Relation R. Connectedness is direct psychological connections
  and continuity is overlapping chains of strong connectedness (Parfit 1984, pp. 205–6, via
  Bartels & Rips 2010 and Lay 2019). Here connectedness is the direct kernel and continuity
  the resolvent. [known: Parfit, read second-hand; the mapping is synthesis]
- The resolvent generalizes Parfit's continuity, which is all-or-nothing: a chain either
  holds or not, over thresholded links. The resolvent grades it and also sums repeated
  loops, which is a modeling choice, not Parfit's definition. [Codex; Dufner 2025, SEP]
- Parfit proposed discounting by connectedness rather than by time (pp. 313–14, quoted by
  Bartels & Rips). Rated connectedness predicts less discounting (Bartels & Rips 2010;
  Bartels & Urminsky 2011); an earlier test found little (Frederick 2003, second-hand).
  No formalization of continuity as path sums was found.

## Anthropics

**A1. Echo on a branching tree: measure-weighting.** [synthesis; checked where marked]
- A `b`-ary tree of successors (copies) with geometric kernels.
- **Stance: anticipation is measure-weighted.** In the causal form, anticipation is a
  forecast `E_t[e_{t+j}]`, which, as a forecast of one continuing path, weights successors
  by their measure (Born weight, probability, share). Death or doom branches enter as zero experience, so a likely early
  end discounts the anticipated future.
  - Zero is hedonic neutrality, the level of non-experience; the model is not invariant to
    shifting it (core, Objects). Renormalizing anticipation on survival, as quantum
    immortality would, drops the discount; measure-weighting is the unnormalized choice.
  - This is the conserved-measure horn of Yudkowsky's Anthropic Trilemma (2009): copying
    yourself a trillion times on a lottery win, then merging, changes how many copies feel
    the win, not what the pre-copy self should anticipate. Where the copies' own welfare
    goes is the aggregation axiom below.
- **What measure-weighting rules out.** Copy-counting anticipation would make anticipation
  a *sum* over successors, so a branching future could outweigh a single past without
  bound.
  - Per observer: copy-counted forward mass is `abα/(1 − bα)`, which needs `bα < 1`.
  - Total across observers: a trunk event is remembered by every descendant, so the
    copy-counted total needs `bμ < 1` (D) or `bq < 1` (R), with `q` P4's memory tail.
    Memory-only, `q = (1+m)μ` (resolvent `r(−j) = (m/(1+m))((1+m)μ)^j`): `b = 2, m = 1,
    μ = 0.3` keeps each observer bounded (`M = 0.43`) while the copy-counted total diverges
    (`b(1+m)μ = 1.2`). Anticipation feeds back through memory and lengthens the tail:
    `b = 2, a = 0.3, α = 0.6, m = 0.6, μ = 0.3` passes the memory-only test
    (`b(1+m)μ = 0.96`) but `bq = 1.014`. [checked; the second example is Codex's]
- **Two weightings, both needed.** Anticipation is a forecast; measure-weighting it is the
  choice to forecast one continuing path. Aggregating welfare across observers is a
  separate axiom: with every kernel zero, two real copies each at `+1` sum to 2 under ordinary additive
  aggregation, whatever anyone forecasts. Invisibility below assumes welfare is also
  aggregated by measure (total utilitarianism with measure as the population weight;
  conserved measure, as for Everettian branches); for real copies
  (uploads, LLM instances) the copy-counted total above is the population-ethics case, and
  `bμ < 1` or `bq < 1` is the condition for its aggregate to stay finite. Infinitely many
  real subjects can have infinite total welfare, so finiteness is an added requirement,
  not coherence. [Codex]
- **Under measure-weighted anticipation and aggregation, branching is welfare-invisible.**
  Duplicating identical branches adds no information and no news, at any `λ`. Branches with
  different felt outcomes are resolved like any uncertainty (core N2): neutral ex ante (not
  pathwise) at `λ = 1`, and with loss-averse news it costs in
  expectation, and updateless affect (D7) can postpone or batch the news but not remove it
  (one period, `u = ±1` equiprobable, `n = 0.2, λ = 2`: `E[e] = −1/7`). [Codex] Forward
  mass is `aα/(1 − α)`,
  and the measure-weighted total memory of a trunk event is `m Σ μ^j`, the unbranched
  conditions exactly: it adds up to normality.
- Aggregation weights are normative and the weights inside a forecast epistemic; they can
  coincide numerically without being one object, and neither is SSA or SIA as a theory of
  self-location (A2 still needs self-locating credences). Armstrong derives
  SSA- or SIA-like *betting* from preferences plus linked decisions, and treats subjective
  anticipation as encoded in the utility function (LW 2011). Precedent for the weighting:
  Greaves's (2004) caring measure.
- Well-foundedness alone does not force measure-weighting (faster decay, bounded depth or
  saturation would also bound the sums), and neither does the forecast reading by itself: an
  expectation of one successor's experience and an expectation of total successor
  experience are both forecasts. Forecasting one continuing path is assumed, defensibly for
  Everett branches (Born-weighted caring, Greaves), not derived. Armstrong's demand stands:
  say which successors the agent cares about, how much, and which decisions are linked.
  [Codex]

**A2. Imperfect recall.** [imported: Piccione & Rubinstein 1997; Aumann, Hart & Perry 1997;
Oesterheld & Conitzer 2024. Embedding them in belief-dependent felt utility is open]
- Amnesia cuts particular memory links. It creates self-location uncertainty only when
  the remaining observations fail to fix the current position. In that case `E_t` needs
  a self-locating credence.
- The policy space must be specified, including whether randomization is drawn fresh or
  remembered (Piccione & Rubinstein).
- Aumann, Hart & Perry dispute the planning/action inconsistency itself.
- The ex-ante-optimal policy is compatible with CDT plus generalized thirding (Piccione &
  Rubinstein 1997, Prop. 3) and with EDT plus generalized double-halving (Oesterheld &
  Conitzer 2024, Cor. 7, their own result). "Compatible" is their term of art: acting by
  the theory at every observation is consistent with the policy, which need not be the
  only such policy; with a single observation, EDT with double-halving's compatible
  policies are exactly the ex-ante-optimal ones (Cor. 8, ties remaining), CDT with
  thirding's not. Their payoffs are an extensive-form model; utilities that depend on
  policy-generated forecasts would need an embedding, so this is a literature comparison.
  "Planning-optimal" is not a uniquely FDT verdict, and no FDT claim is made here.
