# Vicarious echoes: feeling other people's anticipation and memory

**Status: exploring (2026-10-27); a9's question, menu B7, not the post.** The felt counterpart
of `empathy.md`. There a partner's welfare enters my objective with a weight `w`, a
preference; here other people's felt states enter my felt state, an experience, counted in
welfare under the hedonic reading. Additive reading, linear unless stated. Checks:
`vicarious.py` (`python notes/vicarious.py`). Reviewed by Codex (thread `cu-vicarious`), whose
corrections and counterexamples are folded in.

## Setup

- People share a time axis. Person `i`'s felt state adds to its own canonical echoes:
  - **contagion** `S_ik e_{k,t}`: feeling what `k` feels now;
  - **vicarious anticipation** `V_ik Σ_{j≥1} aα^j Ê_t[e_{k,t+j}]`: my anticipation kernel over
    `k`'s forecast felt states (dreading what will happen to you);
  - **vicarious memory** `R_ik Σ_{j≥1} mμ^j e_{k,t−j}`: my memory kernel over `k`'s past felt
    states. As written it reads `k`'s actual past whether or not it was told, aged from the
    event; a story needs an access gate (below).
- All three act on felt states, so echoes compound across people: I catch your reminiscence,
  which holds your memory, which may hold me. Each felt echo is counted once, where it is felt
  (core, Objects). News is over one's own felt states, which carry the vicarious terms, so
  grief is the survivor's revision of its own forecasts.
- **Known in kind.** Bergstrom (1999) writes the recursion between people and motivates it by
  pleasure in others' happiness (p. 71), reading the two-sided version as remembered and
  anticipated happiness within one person (p. 83); his formal analysis is of preferences.
  Bolle, Okhrin & Vogel (2009) model interdependent happiness, through comparison rather than
  contagion. New here is the person × time construction with news, mortality and the welfare
  accounting. *synthesis*

## Joint well-foundedness

- **Echoes, by row sums.** If every person's total echo share
  `M + Σ_k S_ik + A Σ_k V_ik + B Σ_k R_ik ≤ q < 1`, the echo operator has sup norm at most
  `q` and the community's echoes are well-founded at every lifespan, with dead person-moments
  removed too; infinitely many people need the uniform margin `q`. *standard: Bergstrom's
  dominant diagonal on the person × time graph, P1's bound; checked on random draws*
- **Stable separately, unstable jointly.** Contagion alone is a Kronecker sum on a common
  person × time domain, `ρ(I ⊗ K + S ⊗ I) = ρ(K) + ρ(S)` for nonnegative matrices; unequal
  lifespans break the exact structure. Two people at `M = 0.6` (alone `ρ < 0.6` at every length,
  an interior felt state of 2.5), contagion 0.45 each way: `ρ` is 0.81 at `T = 5` and 0.997 at
  `T = 20`, where the interior felt state is 471, and past 1 by `T = 80`, where no convergent
  nonnegative resolvent remains (an algebraic solution can still exist). *standard*
  - A collective despair threshold, a pair or group spiralling where neither member would
    alone, is a reading: the linear model amplifies good states as much as bad and has no
    process in time. *speculation*
  - Prior art to read: emotional contagion (Hatfield, Cacioppo & Rapson 1994); co-rumination,
    which goes with both closer friendships and more depression and anxiety (Rose 2002).
    *bibliographic details verified (Codex, Gemini); texts unread*
- **News across people** (Codex, `cu-vicarious`). A unit forcing felt now by `k` moves `i`'s
  forecasts at horizon `j` by `G_j[i, k]`, a column of the community's remaining-life
  resolvent; felt news solves `s = b + Ks` with `K = Σ_j nν^j G_j`, N4's `κ` as a matrix.
  *derived; checked*
  - Linear news: stable for every revision iff `ρ(K) < 1`. Loss-averse news, kinked per person
    and horizon: `ρ(λK) < 1` is sufficient and necessary for that guarantee, and with
    `ρ(K) < 1 ≤ λρ(K)` a strict all-loss revision has no felt state at all. A particular mixed
    revision can still have a stable root above the threshold (Codex's two-period
    counterexample); its test is the Jacobian `Σ_j nν^j D_j G_j`, `D_j` the slopes in use.
  - **Modes.** When `S, V, R` are simultaneously diagonalizable, each eigenmode is one person
    with `a, m, n` scaled by `(1 + v_θ)/(1 − s_θ)`, `(1 + r_θ)/(1 − s_θ)`, `1/(1 − s_θ)` and the
    rates unchanged: `κ_θ = n/((1 − s_θ)H_θ) · (1 − νμ)/(1 − νq_θ)`. Under pure contagion
    `ρ(K) = f(ρ(S))` on any graph. *derived; checked against the full resolvent*
  - Mutual contagion 0.9 with contemporaneous news 0.2 and no temporal echo: `K = n(I − S)⁻¹`,
    `ρ(K) = 2` (the unreduced loop `S + nI` has radius 1.1), although echoes alone (0.9) and
    each person's news (0.2) are stable.
- **Reciprocity, not reach, makes the loop.** One-way ties (fans who feel a hub) are triangular:
  every diagonal block is a single person, so no one's loop changes, however large the
  response. A reciprocal star has `ρ(S) = (Σ_f s_hf s_fh)^{1/2}`, so fixed ties cross the news
  threshold as the crowd grows: at the life calibration, the hub feeling each fan at 0.05 and
  each fan the hub at 0.4, `λ = 2`, is stable with 11 fans (`λρ(K)` = 0.994) and not with 12
  (1.053), while echoes stay well-founded (`M + ρ(S)` = 0.81). The hub's own diagonal gain
  misses it; the instability runs through the fans' reactions. *derived (Codex); checked*
  - Reading: a public figure who feels the crowd that feels them can be destabilized by many
    weak ties. *speculation*
- **Attention budgets make stability size-free.** If every person's social rows sum to fixed
  budgets (`S1 = σ1`, `V1 = v1`, `R1 = r1`), the constant vector is invariant and
  `ρ(K) = κ(a(1 + v)/(1 − σ), m(1 + r)/(1 − σ), n/(1 − σ))` whatever the size and topology:
  0.346 at `σ = 0.3` for stars of 1, 3 and 8 fans. Normalization alone is not safety, since an
  unsafe budget stays unsafe at every size. *derived (Codex); checked*

## Whose moments count

- In a long life's interior, a foreseen unit of `k`'s base utility adds `1ᵀ(I − G)⁻¹ e_k` to
  welfare, `G = MI + S + AV + BR` in person space: summing the response over time gives
  `x = e_k + Gx`. A column sum, Katz centrality between people (§3's moments as centrality, one
  level up); felt levels are the rows, `(I − G)⁻¹ 1`. An unforeseen shock adds news and
  information boundaries. *standard; checked against the person × time resolvent*
- **Being felt raises a moment's weight; feeling another's good raises one's level.** Ten fans
  feel a hub at contagion 0.1, vicarious anticipation and memory 0.05: a unit of the hub's base
  utility adds 3.99, a fan's 1.47 (1.47 alone); a fan's felt level is 1.72 against the hub's
  1.47. With the hub feeling each fan at 0.01 (fans at 0.05): 2.77 against 1.52. Feeling
  another's suffering lowers one's level the same way. *numerical*
- **The hedonic reading counts sympathy where it is felt.** That is not the same as adding
  altruistic willingness to pay, which also carries others' costs and can mismeasure benefits
  if summed naively (Bergstrom 2006's point, read in the 2004 working paper, against counting
  sympathetic benefits while neglecting sympathetic costs; Milgrom 1993 secondhand). Under the
  life-sum, the weight of a person's base utility rises with how widely they are felt: a loved
  person's suffering costs more than a stranger's equal suffering, by the dread and grief it
  causes in others. Equal concern for persons, unequal weight on their base utility. §3's "a
  good moment counts more than once", between people. a9 reads it as a feature: a beloved
  figure's hardship draws more reaction than a stranger's. *synthesis*
- **Additive or budgeted feeling: Katz or PageRank.** Additive ties, each with its own weight,
  give the column sums above, Katz centrality. If each person instead feels others with a fixed
  share `σ` of attention spread by a row-stochastic `P`, welfare weights are PageRank with
  damping `σ/(1 − M)` and uniform teleport, `w = N/((1 − M)(1 − d)) PR`, and every felt level
  under equal base utility is `1/(1 − M − σ)`: for uniform base utility a budget moves where
  welfare is felt, not how much. This needs everyone to feel someone; a sink breaks it (Codex:
  `M = 0`, `σ = ½`, one person feeling the other, levels 1.5 and 1, weights 1 and 1.5).
  *standard identity; the reading synthesis; checked*
  - A budget is not displacement. Budgeted social echo still adds to base utility and
    amplifies it; full displacement, `e = (1 − M − σ)u + Ge`, keeps equal-base levels at 1, with
    welfare weights of the same PageRank shape. Centrality does not tell the readings apart
    (Codex).
- **A celebrity.** A thousand fans each give 0.3 of their attention to others, a fifth of that
  to one celebrity and the rest to a friend; the celebrity feels its own circle of ten. A unit
  of the celebrity's base utility adds 236 to welfare, a fan's 2.3. Fans who follow ten
  celebrities split the fifth: 29; a hundred: 8.8. Additively the celebrity keeps 236, and a
  fan following ten has a row sum past one, yet the completed graph (each celebrity with its own
  circle, fans feeling all of them) is block triangular, so `ρ(S)` stays 0.3 and the community is
  well-founded at any number of celebrities. What grows is the fan's felt level: 2.64, 5.88,
  16.7 at 1, 10, 40 celebrities (Codex). A budget keeps parasocial feeling from inflating the
  fan, not from diverging. *numerical; checked*
- **Public reaction.** A hardship revealed now for a hub, a unit drop four periods ahead, linear
  news: twenty fans feeling the hub at 0.1 together feel 3.6 times its own felt news (−0.33
  against −0.093; news terms only, not the whole change in felt state). If the hub feels its fans too, at a budget of 0.3, its own news is 10% worse
  (−0.102): the crowd's grief, reflected. The reaction a9 points to is the news part of the
  column. *numerical*

## The two examples

- **Dreading what will happen to someone else** is vicarious anticipation. Their bad moment's
  welfare cost includes my dread of it, and, if they know, their own dread, which I also
  anticipate: the column again.
  - Whether to tell them: telling turns their surprise into dread and adds my anticipation of
    that dread, while news about horizon `j` weighs `ν^j`, so telling early saves news and
    costs anticipation. death.md's knowing criterion with a vicarious term. Prior art: Caplin &
    Leahy (2004), a concerned expert choosing what to disclose to an anxious patient
    (*bibliographic details via Gemini, unread*). *speculation, not worked*
- **Enjoying someone's memory as they tell it** is one of two operators. Contagion: I catch
  their felt state now, mostly their reminiscence. Vicarious memory: their felt past enters my
  memory.
  - They separate by content, not persistence. Contagion scales with the teller's current felt
    state, vicarious memory with the remembered one: a joyful memory told by someone now
    grieving gives the listener the teller's mixed state under contagion and the old joy under
    vicarious memory. Contagion persists too, since the listener remembers having felt it.
  - A story needs a gate: `Σ_{s<t} R_ik mμ^{t−s} Q_ik(t, s) ẽ^i_{k,s}`, with `Q` whether `i`
    has access to `k`'s moment `s` and `ẽ` the representation received. Decay from the event
    (as written) or from the telling is then a modelling choice, and an empirical one: a
    friend's joy from a decade ago against yesterday's, vividness held fixed. *speculation*
  - Prior art: capitalization, telling others of good events raises the teller's affect beyond
    the event (Langston 1994; Gable, Reis, Impett & Asher 2004); the listener's side, which is
    the question here, in Conoley et al. (2015: celebrating others' good news raised the
    listener's positive emotion in a diary study) and Peters, Reis & Gable (2018, interpersonal
    and iterative capitalization); "vicarious savoring" in Bryant & Veroff (2007).
    *bibliographic details and abstracts verified (Codex, Gemini); texts unread*

## Grief: a death date among survivors

Person 0 dies uniformly on 16–30 of a 30-period life (death.md's case); survivors live to 30,
learn what person 0 learns and the death when it happens. Life calibration, `u = 1` for all.
"Foreseen from birth" is revelation at 0 against the prior; a death at 30 falls outside the
survivors' scored interval. `cells()`' partitions checked by Codex (nesting, adaptedness,
per-time news).

- **A survivor's own news has zero mean** at `λ = 1`: alive in every branch, its forecasts
  are a martingale whose revisions are all felt, so `E[N_{1,t}] = 0` at every `t` and every
  warning. This is the survivor's own news term, not all of grief: what it feels of the dying
  and their deprivation remain. *standard; checked*
- **One-way contagion is linear.** A survivor's baseline does not depend on the death, and the
  news kink is positively homogeneous, so each survivor's response is `s` times a fixed one and
  survivors who do not feel each other add (Codex). The sudden-minus-foreseen gap for the
  dying and those who feel them is
  - at `λ = 1`, `0.682 + 0.996 Σs`: survivors catch the dying self's relief, and ignorance pays
    more the more the dying are felt;
  - at `λ = 2`, `0.684 − 0.486 Σs`: **foreknowledge wins once the total contagion toward the
    dying exceeds 1.41.** One survivor at 0.2 leaves sudden death ahead (+0.59); eight at 0.2
    reverse it (−0.09); with one survivor at 2 the pair prefers a 13-period warning, a
    16-period one, and revelation at birth to a sudden death, rising in that order (+0.06,
    +0.20, +0.29).
  - A widely felt death is better foreseen, a solitary one better sudden, when news is loss
    averse. *derived; checked*
- **The survivor's own loss-averse news** (`λ = 2`, contagion 0.2): −0.001 with revelation at birth,
  −0.11 with four periods' warning, −0.22 with one, −0.20 sudden. Long warnings are cheaper,
  but a one-period warning costs a little more than sudden death, so Fels's timing comparison
  (2015, Obs. 5) is context, not a theorem here. *numerical*
- **What the survivor's welfare is made of** (`λ = 2`, against revelation at birth, each part
  through its own echoes, Codex's decomposition): sudden, +0.20 caught from the dying and −0.30 own news;
  one period's warning −0.16 and −0.32; four periods −0.10 and −0.16. Own news is the larger
  part each time; what it catches is why sudden beats a short warning for it. Among the
  couplings tried at 0.2 (contagion, adding vicarious anticipation or memory, contagion both
  ways) the survivor ranks revelation at birth first, then sudden, four periods, one period.
  *numerical*
- **Survivors share the deprivation.** One more foreseen period for person 0 (death at 100 to
  101, survivor to 200), accounted by where experience changes (`ΔW = e_new(1 + 1ᵀHb)`, as in
  death.md): uncoupled, 83% is the new moment's own felt state and none reaches the survivor;
  with contagion 0.2 the survivor gets 23% (adding vicarious anticipation, 34%; vicarious
  memory, 35%). With vicarious memory the survivors remember the life after it ends; the extra
  experience is theirs, the dead acquire none. *numerical*
- **Grief under biphasic memory** (`vicarious.py` 6; adaptation as in `adaptation.md`, own memory
  only, the same `h` for both people). The survivor's reference was built on the shared level and
  sits above its new one, so its felt state undershoots and recovers as the reference adapts
  down. Reviewed by Codex (`cu-vicarious`). *checked*
  - **The mechanism needs no foreknowledge** (Codex): with `e_t = X_t − h r_t` and `r` the EMA of
    felt states, a permanent downward step in `X` gives `e_t = e_after + (e_death − e_after)
    [g − h(1 − g)]^t`, starting below the new level whenever `h > 0`. *derived*
  - Foreseen, contagion 0.5, `h = ½` with a primitive mean lag of a year: from 1.21 to 0.63 three
    weeks after the death, settling at 0.85, within 10% of the step after 58 weeks (a calibration
    result, not a recovery-time prediction); without adaptation, from 2.56 down to 1.47 and
    flat. The step shrinks with adaptation (−30% against −42%), as `s/(d + s)` with
    `d = 1 − A − B₊ + h`: both the survivor's amplification and the deceased's adapted level
    fall. *checked*
  - Sudden (death uniform on 41–50 of 100, adaptation over about 15 periods, contagion 0.5), in
    the branch dying at 45: a shock, then slow recovery (0.51 at the death, 0.68 three periods
    later, 0.81 after fifteen, toward the steady state 0.85) against a shock and a fast return
    without adaptation (1.28, then 1.48). At `λ = 2` the shock deepens (0.24). The undershoot
    survives a survivor horizon of 240 and deaths moved to 141–150 (Codex). Survivor welfare,
    sudden minus foreseen: +0.13 at `λ = 1`, −0.04 at `λ = 2`, out of about 107. *checked*
  - What biphasic memory adds is the slow undershoot from the negative lobe; the positive-memory
    model already has a shock and a fast recovery.
  - Signed memory changes the stability test: linear news needs `ρ(K) < 1` in moduli, and the
    loss-averse bound becomes `ρ(λH) < 1` with `H = Σ_j nν^j |G_j|`, absolute responses summed
    over horizons (sufficient; Codex's two-period counterexample has `λK = 0.96` and an unstable
    root). The calibrations here pass with room (`H` 0.25 and 0.23, so 0.50 and 0.47 at
    `λ = 2`). *derived (Codex); checked by Codex*
  - It resembles one bereavement trajectory, an undershoot then recovery toward a lower level,
    but longitudinal studies find heterogeneous trajectories (Bonanno et al. 2002: resilience
    the largest group, 46%, common grief 11%, chronic 16%, assessed at six and eighteen months),
    life satisfaction recovering over years, partly (Lucas, Clark, Georgellis & Diener 2003),
    and complete adaptation to widowhood not rejected in another panel (Clark, Diener, Georgellis
    & Lucas 2008). Their measures do not identify this kernel or its recovery time. *synthesis;
    papers checked by Codex; texts unread here*
- Lindemann (1944) named anticipatory grief; a historical lead, not support for any ranking
  here. *bibliographic details verified; text unread*

## Relation to `empathy.md`

- A self maximizing its own felt state with vicarious anticipation `V` of a partner weighs the
  partner's felt states at `V aα^j`, horizon by horizon: an empathizer with a decaying `w`.
  The `J` question carries over: whether my policy moves the forecast I vicariously
  anticipate. *synthesis, not checked*
- `empathy.md` asks how caring changes choices; this note asks what a coupled community's
  welfare is. Under the hedonic reading only the second adds welfare.

## Open

- Delays along the graph: information reaching fans at their distance from the hub, and
  whether a cascade's felt news depends on its path under loss aversion.
- Others' grief inside the momentary window (death.md, chosen dates): does vicarious
  anticipation of a survivor's grief deter a momentary exit more than the exiter's own future?
  A rough count says not at the life calibration unless `V` is large: own news weighs
  `nν/(1 − ν) = 0.47`, vicarious anticipation of the next period `aαV = 0.045V`. And a chosen
  death's announcement as information design for those who feel it, given the threshold above.
- Whether to tell someone of their coming misfortune, worked, against Caplin & Leahy (2004).
- The story gate `Q` and the decay question.
- Heterogeneous kernels across people; saturation (B3) for collective low states.
