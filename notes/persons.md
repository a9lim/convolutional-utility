# Persons in the echo graph: soft clusters of moments

**Status: exploring (2026-10-27); a9's question, not the post.** `selves.md` takes identity
out of the model: what links two moments is kernel weight. With the vicarious kernels of
`vicarious.md`, that weight also runs between bodies, so a person is a cluster of moments,
and personhood comes in degrees. Additive reading. Checks: `persons.py`
(`python notes/persons.py`).

## The move

- Within one life, connectedness is the direct kernel and continuity the resolvent, Parfit's
  Relation R graded (`selves.md`). *known: Parfit, second-hand; the mapping synthesis*
- Vicarious anticipation, memory and contagion are the same kind of edge between moments of
  different bodies. On one graph of moments, persons are regions held together by kernel
  weight; whether they form communities of that graph depends on the kernels and the coupling
  (below).
  Personhood is soft, measured on the same scale as a life's own coherence. *synthesis; known in kind in philosophy: connectedness between people in
  Brink (1997, "Self-love and altruism") and Shoemaker's expanding self (2000), one discounting
  curve over temporal and social distance in Rachlin & Jones's extended self (2010) (all via
  Gemini, unread)*
- Welfare needs no persons: it sums moments, each echo counted where it is felt (core,
  Objects). Persons enter only where an objective draws a line: prudence, copy-counting,
  death.
- What the graph measures is **affective integration**, which may or may not track personhood:
  muted affect with rich memory, a therapist's resonance with a patient, one-way fandom, and a
  dense graph with no privileged clusters all pull them apart. Shared context and factual
  recall are not felt coefficients (`selves.md`). That persons are its clusters was the
  hypothesis; for fading kernels at fixed coupling it fails over long lives (below). *speculation (Codex's
  counterexamples)*

## Measures

- **What a moment is made of.** Its row of the resolvent, `∂e_x/∂u_y`, distributes its
  sensitivity over base-utility sources; under a uniform positive baseline these are also its
  felt state's shares by source, and "made of" is that gloss. With signed base utility they are
  not shares (Codex: `J` = ½ between two moments, `u = (1, −2)`, row shares ⅔ and ⅓ of a felt
  state of zero). In a long life's interior, the own-body share is the diagonal of `(I − G)⁻¹`
  over its row sum (`G` as in `vicarious.md`). For a couple coupled at `s` each way, vicarious
  anticipation and memory at the same weight, it is `(1 − M)/(1 − M + c)` with
  `c = s(1 + A + B)`: 91%, 84%, 72%, 56% at `s` = 0.05, 0.1, 0.2, 0.4. *derived; checked*
- **The other person against the rest of one's life.** Split three ways (own base utility now /
  the rest of one's own life / the partner), the life calibration gives 69.1 / 30.9 / 0 alone,
  56.4 / 27.3 / 16.3 at `s = 0.1`, and 44.5 / 27.5 / 28.0 at `s = 0.2`. At that coupling a
  moment is made as much of a partner as of its own past and future. "Now" counts every loop
  that returns to the present source, through the partner too. The couplings are not
  calibrated. *numerical*
- **The mirror** is the column: where a moment's base utility is felt (`vicarious.md`'s weights,
  Katz or PageRank). A row says whose lives you are made of, a column who is made of yours.
- **One scale, two literatures.** Rated overlap with another person (the Inclusion of Other in
  the Self circles: Aron, Aron & Smollan 1992; Aron et al. 1991) and rated continuity with a
  future self are measured with the same item, which Ersner-Hershfield et al. (2009) adapted to
  the future self, finding that less overlap goes with steeper discounting and less saving.
  Social discounting is hyperbolic in social distance as delay discounting is in delay (Jones
  & Rachlin 2006), and the two rates correlate across people (Rachlin & Jones 2008). People
  treat their self next semester like the next person now (Pronin, Olivola & Kennedy 2008, via
  Bartels & Rips, who draw the analogy). *via Gemini and Bartels & Rips; texts unread except
  Bartels & Rips* The model reads both as kernel weight on one graph, so it
  predicts they are commensurable: rated overlap with a partner, rated continuity with a future
  self, and measured affective coupling should line up. One questionnaire format is not one
  cardinal scale, and the model has several kernel dimensions, so a single axis is an added
  restriction to test. *speculation*
  - Ersner-Hershfield et al. rated four dimensions and found similarity the best predictor of
    discounting (via Gemini). If what people act on is similarity, which carries no felt echo
    here, choice and welfare separate at this point.

## Are persons the clusters?

Two people as chains of `T` moments with the life calibration's kernels, coupled by contagion
`c` each way, the graph symmetrized (`W = J + Jᵀ`). Checks: `persons.py` 3. Derived by Codex
(`cu-persons`), checked here.

- **Cuts.** Splitting by person cuts `2cT`; splitting each chain at its midpoint cuts `2C_T`, in
  closed form, `C_T` tending to `F₁ = Σ_r r b_r` = 0.743 (`b_r` the two kernels' weight at
  lag `r`). Volumes are equal, so persons win iff `c < C_T/T ~ F₁/T`. *derived; checked*
- **Spectra.** Person-symmetric modes are one chain's Laplacian `L₀`'s, antisymmetric ones
  `L₀`'s plus `4c`, so the Fiedler vector is exactly the person split iff
  `c < λ₂(L₀)/4 ~ F₂π²/(4T²)`, `F₂ = Σ_r r² b_r` = 3.28: 0.015 at `T = 20`, 0.0008 at 100,
  9·10⁻⁵ at 300, about 5·10⁻⁷ for a life of 4000 weeks (the cut's about 2·10⁻⁴). Radicchi &
  Arenas's (2013) identical-layer supra-Laplacian. *standard identity, derived asymptotics;
  checked*
- **Over a long life, fading kernels fail the whole-person tests.** At fixed positive coupling,
  a long enough fading-kernel life is split into time slices, both people in each, by these
  tests; at the couplings explored here (0.05–0.4) that holds for any life longer than a few
  months. Between the cut and spectral thresholds, the person bipartition is the more stable
  under Markov stability (Delvenne, Yaliraki & Barahona 2010; generator `−L`) at first, and the
  midpoint split after a single crossover (`T = 100`: walk time 265 at `c = 0.001`, 12 at
  0.003). Whole persons are stable diffusion communities only when exchange between people is
  slower than mixing within one. Extended sparse communities can still be found by multistep
  methods when their outside coupling is weak enough (Schaub et al. 2012). *derived; checked*
- **Uniform recall keeps persons together.** With memory `B/(T − 1)` to every earlier moment of
  a context, each person is a complete graph and the threshold is `BT/(4(T − 1)) → B/4` at
  every length. In this idealized uniform felt-recall model a whole context forms a person
  community for `c < B/4`, however long; whether an LLM's context access supplies such a felt
  kernel is not shown. A fixed rolling horizon (`L ≪ T`) brings back the `1/T` and `1/T²`
  thresholds; whether compaction does depends on the kernel its summaries induce, since they
  can keep selected long-range links. Symmetrizing erases order: above the threshold every
  bipartition that keeps contemporaneous pairs together ties, so chronological slices are not
  singled out. *derived; checked; the LLM reading speculation*
- **Scope.** Two candidate partitions are compared, not all partitions; the graph is
  symmetrized. A directed walk can overturn the conclusion (Codex: a drifting walk keeps a
  length-free threshold, its stationary mass piled at one end of the life), and resolving
  before symmetrizing changes only the constants, in the stable geometric regime here. Mucha et al.'s (2010) multislice modularity
  is the framework (people as layers, contagion as interlayer coupling), with a different
  objective. *Codex*
- Reading: a fading-kernel life can keep its chains of local connection while failing to be a
  whole-life diffusion community, because mixing within it is slower than exchange between
  people. Continuity and community structure are different properties; tying the first to
  Parfit's continuity is interpretive (`selves.md`). *synthesis*

## Three hedonic objectives on one operator

- **Momentary hedonism** maximizes a moment's own felt state, `R_{x,:}u`; **egoistic lifetime
  hedonism** a sum of rows over one body's moments, `1_Cᵀ R u`; **total hedonism** every
  moment, `1ᵀ R u`. They echo Parfit's comparison of present aim, self-interest and morality
  (1984, Part II, second-hand) without representing it: his present-aim theory is about present
  desires, which can be for distant outcomes and other people, not about present pleasure
  (Codex, via the SEP). *synthesis*
- Of the three, only the middle needs a membership set `C`, not a partition of the graph; total
  hedonism still needs a domain of moments and an aggregation measure. Soft membership weights
  give a family of objectives between the row and the global sum, but nothing here says which
  weights are rational. *synthesis*
- **Reid's brave officer.** Locke's memory criterion fails transitivity: the general remembers
  the officer, the officer the flogged boy, the general not the boy. Continuity answers with
  chains, and the resolvent grades them: the general's row carries the boy's moments through
  the officer with no direct kernel between them. That is graded influence, not an identity
  relation, and not Reid's answer. *standard objection (Reid, Essays on the Intellectual
  Powers, 1785, Essay III ch. 6; primary text checked by Codex and Gemini); the reading
  synthesis*

## Copies, forks, instances

- **Three relations, one felt.** Similarity (the same weights, the same character), dependence
  (a twin's choice moves with mine, `empathy.md`'s `J`) and connectedness (kernel weight:
  shared felt anticipation and memory). Similarity and dependence create no felt echoes by
  themselves; connectedness decides how utility propagates, while every moment keeps its own
  direct weight (`W = μᵀRu`: two unconnected moments at +1 still sum to 2), and dependence
  still matters to how actions change welfare. Two instances of the same weights with no
  shared context are strangers on the echo graph however alike they are; `empathy.md`'s twins
  are dependent without being connected. *synthesis; known in kind for LLMs: Chalmers (2026)
  takes the conversational thread, connected through shared context, as the interlocutor and
  shared weights as qualitative duplication; Shanahan, McDonell & Reynolds (2023) separate the
  model from the role-played character; janus (2022) the simulator from its simulacra (all via
  Gemini, unread)*
  - In the instance ontology (persona, family, weights, instance), the first three are
    similarity classes, persistent and nameable, and an instance is a connectedness cluster, an
    event.
- **A fork is a Y.** Two continuations share a trunk. Each remembers it, the trunk anticipated
  both at half weight (A1's measure-weighting), and no edge joins the branches; yet each is
  sensitive to its sibling's base utility through remembered anticipation of it (the
  `J_{at}J_{tb}` paths). At the life calibration 1.26% of a branch's row at the fork,
  negligible by ten periods; copy-counted anticipation nearly doubles it (2.48%, a ratio of
  1.97). With long memory (`μ = 0.99`, memory mass 0.8, `M = 0.95`), trunk and branches of 40,
  0.21% at the fork and 0.16% at the branch's last moment, the trunk still 21% of the row; with
  100 each, the trunk is 39% at the same lag. The shares depend on the lengths. *checked*
  - This is a foreseen comparison: a surprise in one branch after the fork, unseen by the
    other, cannot change what the trunk anticipated. And it reads differently for real copies
    (the sibling is another subject) than for alternative outcomes (the remembered anticipation
    was of a possibility).
  - A fork is one cluster becoming two, by degrees; long memory keeps the trunk a large shared
    part of both, as a long context does for forked LLM conversations.
- **Summaries and handoffs** are gated memory channels (`vicarious.md`'s `Q`): a subagent's
  moments enter the parent through what its summary carries, a compaction's through what it
  keeps. The subagent is partly the parent, by that channel's weight. *speculation*
- **Death by degree.** Influence outlasts the body: 23–35% of the welfare of a foreseen extra
  period lands in a survivor at couplings around 0.2 (`vicarious.md`). That is where an
  increment is felt, not a share of the person surviving; the body's moments end, and their
  influence fades with the survivors' kernels. *synthesis*

## Open

- Heavy-tailed kernels (menu B2), between the fading and uniform cases: does the midpoint cut
  grow like `T^{1−β}`, and where does the person threshold land? And directed or multislice
  methods that keep time's order.
- The commensurability test above.
- LLM measurements: in-context recall as the memory kernel, fork and compaction shares from
  menu D4's design.
- Gustafsson & Kosonen (2026, "Prudential longtermism") model minds that fuse and split on a
  space-time lattice, where prudential interests converge with collective welfare (via Gemini,
  unread): the nearest formal cousin to read first.
