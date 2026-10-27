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
- **News needs its own joint condition.** Mutual contagion 0.9 with contemporaneous news 0.2
  has echo radius 0.9 and a news loop of 0.2, yet a common revelation's loop
  `δe = δu + (S + nI)δe` has radius 1.1 (Codex). N4 needs a matrix of cross-person news gains
  before the whole community is well-founded. *checked*
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
  good moment counts more than once", between people; feature or reductio is a question for
  the post. *synthesis*

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

- Cross-person news gains in N4: when is a community with news well-founded?
- Others' grief inside the momentary window (death.md, chosen dates): does vicarious
  anticipation of a survivor's grief deter a momentary exit more than the exiter's own future?
  A rough count says not at the life calibration unless `V` is large: own news weighs
  `nν/(1 − ν) = 0.47`, vicarious anticipation of the next period `aαV = 0.045V`. And a chosen
  death's announcement as information design for those who feel it, given the threshold above.
- Whether to tell someone of their coming misfortune, worked, against Caplin & Leahy (2004).
- The story gate `Q` and the decay question.
- Heterogeneous kernels across people; saturation (B3) for collective low states.
