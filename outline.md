# Experience Echoes

The scaffold for the flagship post: bullets for a9 to write from, not prose. Math lives in
`formalism/` (`formalism/INDEX.md` maps every claim below to its proposition, support and
artifact); sources in `bibliography.md`.

## The post

- **Thesis.** Looking forward, looking back and the jolt of news are experiences too. Count
  them as welfare and three things follow: a moment matters by its place in a web of echoes;
  learning changes how a life feels even when it changes no decision, so a hedonic agent
  chooses what it feels by as well as what it does; and the self that looked forward to a
  choice becomes a predictor of it.
- **What it is.** Mostly a bridge. Economics and psychology have a worked-out theory of
  anticipatory, remembered and news utility, from Jevons (1871) to Kőszegi & Rabin (2009).
  LessWrong meets the same questions in its own terms (the litanies, value of information,
  picoeconomics) and, in the posts our scans found, without these sources. The post assembles
  the theory into one model, points it at LessWrong's questions, and adds a few results, each
  flagged.
- **Reading.** Hedonic: anticipation, memory and news are felt, and welfare is the life-sum of
  experienced utility. For the reader: whatever else you value, if experience counts, these
  experiences count. Nothing needs hedonism about all value, so "Not for the Sake of Happiness
  (Alone)" can stand.
- **Form.** One post of about 9.5k words, one figure per section. The technical companion
  (`formalism/`, polished) carries proofs, closed forms and checks. Follow-ups, not this post:
  decision theory by learning, shared-state critics, the LLM peak-end study (end of file).
- **Title.** Working: *Experience Echoes*; "convolutional utility" names the framework.
  Alternatives: *Convolutional Utility: Counting Anticipation and Memory*; *What Your Past
  Self Predicted*.
- **Running example.** One holiday: announced early or late, enjoyed, remembered, cancelled.
  Sections borrow other openers where they land better: the Huntington's test, P(doom), the
  bottle saved for a special occasion.
- **Tags** give provenance only; support (proved, checked, data) is in `formalism/INDEX.md`.
  *imported* (a named published result) · *standard* (textbook) · *synthesis* (known pieces,
  new assembly) · *not found* (not located in the literature passes: a candidate
  contribution, not a priority claim) · *speculation*.
- **Drafting rules.**
  - Open each section with the reader's question and the example; then the imported idea,
    credited inside the claim; then what the frame adds.
  - Put the qualifier in the headline: "learning can change welfare without changing a
    decision", not "beliefs are welfare" bare.
  - Define on first use the words LessWrong uses otherwise: *anticipation* is felt, not the
    "anticipated experiences" of "Making Beliefs Pay Rent"; *news* is a felt revision, not
    information; *valence* is not Byrnes's; *utility* is felt and summed, not a VNM
    representation of preferences (§2).
  - Say what the post brings, never that LessWrong lacks it: the scans were not exhaustive.
  - Keep agent provenance (who argued what) out of the post; it lives in the companion and
    the ledger.

## What the post imports

Status in `bibliography.md`: **FT** full text read · **WP** working version · **ABS**
abstract only · **2ND** second-hand · **scan** a LessWrong search summary, read before quoting.

| idea | source | where LessWrong meets it | § |
|---|---|---|---|
| savoring and dread change what people choose | Loewenstein 1987 (FT); Berns et al. 2006 (FT) | "Lotteries: a waste of hope" (scan); "Justified expectation of pleasant surprises" (FT) | 1 |
| anticipation and memory as felt utility, counted where felt | Jevons 1871 (no entry); Caplin & Leahy 2001 (FT), 2004 (WP); Kahneman, Wakker & Sarin 1997 (FT); Hersch & Weltman 2022 (FT) | experiencing against remembering self (lukeprog 2011, Metus 2012; scan) | 2 |
| recursive, two-sided interdependence and its stability | Bergstrom 1999 (FT) | | 2, 5 |
| the same recursion read as preference: benefit-cost on private values | Bergstrom 2006 (WP); Milgrom 1993 (2ND) | | 2 |
| discounting backward as well as forward | Ray, Vellodi & Wang 2024 (FT) | | 2 |
| momentary happiness as expectations plus prediction errors | Rutledge et al. 2014 (FT) | Byrnes, valence series (scan) | 2, 9 |
| planner weights over a life; no pure time preference | Caplin & Leahy 2004 (WP); Ramsey 1928 (FT) | "Against discount rates" (scan) | 3 |
| preferences over the shape of a life | Loewenstein & Prelec 1993 (FT); Velleman 1991 (FT); Brown 2019 (FT); Cosaert & Potoms 2024 (FT) | McAuliffe & Shriver 2022, EA Forum (scan) | 3 |
| peak-end and duration neglect | Fredrickson & Kahneman 1993 (ABS); Lim et al. 2020 (FT) | lukeprog 2011 (scan) | 3 |
| welfare scored by objective expectation of felt life; optimal expectations | Brunnermeier & Parker 2005 (FT) | Litany of Gendlin (FT); Raemon 2011 (FT) | 4 |
| truth is free in expectation when anticipation is linear | Epstein 2008 (FT); Eliaz & Spiegler 2006 (FT) | Litany of Gendlin | 4 |
| ignorable is not cost-free | Kadane, Schervish & Seidenfeld 2008 (FT); Skyrms 1990 (FT) | VOI and updatelessness (Diffractor 2018; Soto 2024; FT) | 4 |
| nonlinearity in beliefs prices information; late resolution | Kreps & Porteus 1978 (2ND) via Skiadas 1998 (FT); Eliaz & Spiegler 2006 | jimrandomh's `√p` utility of belief (FT) | 4, 5 |
| news utility, loss-averse; clumping and inattention | Kőszegi & Rabin 2009 (FT); Pagel 2018 (WP) | | 4, 5, 6 |
| felt sign asymmetries: dread over savoring, fading affect, loss aversion as a forecasting error | Dawson & Johnson 2026 (FT); Hardisty & Weber 2020 (ABS); Hoehne & Zimprich 2024 (FT); Kermer et al. 2006 (FT) | | 5, 9 |
| optimism against disappointment; bracing | Gollier & Muermann 2010 (WP); van Dijk et al. 2003 (FT); Golub et al. 2009 (FT) | | 4 |
| sophisticated self-deception cancels | Bénabou 2015 (FT); Bénabou & Tirole 2002 (WP) | "Doublethink" (FT) | 4 |
| information avoidance in the field | Oster, Shoulson & Dorsey 2013 (WP); Golman et al. 2017 (FT); Karlsson et al. 2009 (FT) | ugh fields (FT); Bostrom's reaction hazards (FT) | 4 |
| recursive present bias from exponential primitives | Sáez-Martí & Weibull 2005 (WP); Galperti & Strulovici 2017 (WP) | hyperbolic discounting from structure (twanvl 2011; scan) | 5 |
| self-referential news about utility | Kimball & Willis 2006 (WP) | | 5 |
| delegation, alerts and what consumption reveals | Andries & Haddad 2020 (WP); Pagel 2018 (WP) | "Detach the grim-o-meter" (FT); doom-coping posts (FT) | 6 |
| Newcomb as a psychological game; self-inference | Geanakoplos 1996 (FT); Bernheim & Thomadsen 2005 (WP) | Newcomb, FDT (Yudkowsky & Soares 2017; FT) | 7 |
| the savoring trap between selves | Kőszegi 2010 (FT); Caplin & Leahy 2001 | picoeconomics, successive selves (scan) | 7 |
| plans as their own commitment device | Kőszegi & Rabin 2009 (FT) | | 7 |
| stop-gradients and performative stability | Oesterheld, Treutlein, Cooper & Hudson 2023 (WP) | Treutlein 2023 (FT) | 7 |
| personal rules and self-reputation | Bénabou & Tirole 2004 (WP); Bodner & Prelec 2003 (FT) | Parfit's hitchhiker | 7 |
| caring measure; conserved measure | Greaves 2004 (2ND) | the Anthropic Trilemma (FT) | 8 |
| connectedness and continuity | Parfit 1984 (2ND); Bartels & Rips 2010 (FT) | | 8 |

## What is new

Candidates, conditional on the literature passes. None is the premise, which is old.

1. **Shape is a boundary effect** (P6). For foreseen lives under linear, stationary,
   summable echo, the shape of a life matters only through its ends. For long linear ramps
   the sign is asymptotically the kernel's first moment's, and the size its reach over the
   lifespan.
2. **Recursion's price on information** (D5; an extension result, X1). Dread outweighing
   savoring, the best-supported sign asymmetry, prices information only when you anticipate
   your own future felt states. An exact identity gives the dread penalty against a symmetric
   baseline; what a schedule of information costs is how it moves that penalty. Mortality
   information is priced even in the symmetric core.
3. **The news loop's gain** (N4). Felt news about felt experience has a unique, stable felt
   state for every revision iff its loop gain `κ < 1`, and amplifies each revision by
   `1/(1−κ)`. Without memory the gain is the news strength alone; memory adds a feedback
   route, and anticipation amplifies it.
4. **Affect policies** (D7, synthesis with close prior art). A hedonic agent picks an action
   policy and an affect policy; Good's theorem and updatelessness govern only the first, and
   the agent's own actions leak into the second.
5. **The past self as predictor** (D1, D2, D6, synthesis). How much already-felt anticipation
   a rule counts as depending on the present choice is one dial; reliability is worth the
   anticipation it earns. Exact savoring-trap stopping conditions (D3) are in the companion.
6. **The data** (§9). A new analysis of public momentary-happiness data: the echo of a task
   outcome is front-loaded and heavy-tailed; an apparent loss-averse news asymmetry is
   confounded with chosen risk; a loss's echo starts stronger than a gain's and fades
   faster.

## Sections

Word budget: 9.4k.

### 1. A holiday before it happens (~600)

- **Question.** What does a holiday do for you, and when?
- **Example.** Weeks of looking forward, a week away, an afterglow, years of remembering. Then
  the same trip cancelled the night before: the anticipation was felt, the cancellation
  hurts, some remembered excitement survives. Which of these belong in the welfare ledger?
- **Two anomalies** *imported*. Loewenstein (1987): people would pay most to delay a kiss from
  the movie star of their choice by three days, and more to avoid a shock delayed by years
  than one now. Berns et al. (2006): 9 of 32 people took a stronger shock sooner rather than
  wait. Exponential discounting gets both backwards; felt savoring and dread get both right.
- **The stakes**, previewed in LessWrong's terms.
  - If the cancellation notice is itself a harm, information has a felt price, which is a
    question for the Litany of Gendlin (§4–§6).
  - The self who looked forward to the trip predicted the self who decides whether to go:
    Newcomb inside one life (§7).
- **LessWrong anchors.** "Lotteries: a waste of hope" (Yudkowsky 2007) is the natural foil:
  its objection is where emotional investment goes, an opportunity cost the additive model
  leaves open (attention and displacement, §2); read it before quoting. "Justified expectation of pleasant surprises" (2009) is the friendliest precedent.
- **Roadmap.** The two lists above: what is imported, what is new.
- **Figure.** The holiday decomposed over time: base utility, anticipation, memory, news and
  their sum, for a trip taken and a trip cancelled (`formalism/pathwise.py`, redrawn on the
  post's example).

### 2. Count experiences (~900)

- **Question.** What exactly gets counted, and is it double counting?
- **Four things to keep apart:** an event's base utility; the experienced utility of a
  moment; the welfare of a life; the objective a self chooses by. Most confusion in this
  literature is a slide between two of them.
- **Not a VNM utility** *standard*. On LessWrong "utility" defaults to von Neumann and
  Morgenstern's: a representation of preferences over lotteries, unique up to positive
  affine maps, with no zero, and summable across times or people only with further
  structure. Experienced utility is felt, cardinal and summed, and its zero matters: a
  longer life at negative `e` is worse, and the level kinks (§5) sit at hedonic zero, which
  choices alone do not pin. Choices bear on it only through an assumption about what a self
  chooses by (patience §3, loss aversion §9).
- **The equation.** Experienced utility now is base utility now, plus felt anticipation of
  later experience, plus felt memory of earlier experience, plus felt news (the jolt when
  forecasts change):
  `e_t = u_t + Σ_{j≥1} a α^j Ê_t[e_{t+j}] + Σ_{j≥1} m μ^j e_{t−j} + news`, sums within the
  life. A temporal kernel model; in its linear, foreseen case it is base utility convolved
  with an effective two-sided kernel, hence the name. *synthesis* of imported pieces: anticipation and memory (Jevons;
  Loewenstein 1987; Caplin & Leahy 2001), two-sided recursion (Bergstrom 1999's benevolent
  utility read within one life; Ray, Vellodi & Wang 2024's backward discounting), news
  (Kőszegi & Rabin 2009; Pagel 2018's kernel; Kimball & Willis 2006 for news about utility
  itself).
- **Echoes of echoes.** You remember looking forward to the trip and look forward to
  remembering it. Caplin & Leahy (2001, p. 75) set the regress aside as having no complete
  model; it has a fixed point, bounded over all lifespans iff the echo share `M < 1`: the
  echo must be less than the whole. *standard* (Bergstrom 1999; a Neumann series), the
  echo-share reading *synthesis*. The news loop has its own condition (§5).
- **Gains and losses alike.** Every channel weighs a gain and an equal loss the same; sign
  asymmetries (dread outweighing savoring, memory by sign, loss-averse news) are an
  extension, ranked by their felt evidence (§5). The data are the reason: felt news is barely
  loss-averse where measured (§9).
- **Welfare is the life-sum** `W = Σ_t e_t`, scored by the objective expectation. *imported*:
  instant utility (Kahneman, Wakker & Sarin 1997), Caplin & Leahy's (2004) defence of
  multiple counting, Hersch & Weltman's (2022) atomism. Each echo is a real experience,
  counted once, when it is felt.
- **Additive echo is an assumption; say so here.** Echo adds to the present rather than
  displacing it. So the model endorses amplifying echoes of good states and damping bad ones
  (`∂W/∂K_ij = w_i e_j`, elementary) and has no optimum over kernels (welfare grows without
  bound as `M → 1`). Attention, saturation and displacement are the missing costs
  (`notes/displacement.md`, parked). Savoring is welfare, not a free amplifier.
- **The reinforcement-learning reading** *known in kind* (Rutledge et al. 2014; Gershman
  2026), the identification *synthesis*: felt anticipation is a critic's value over
  experienced utility, felt news its TD error, memory a decaying trace. The canonical self feels
  its own critic. Byrnes's valence series is the LessWrong neighbour; say which
  "felt anticipation" is meant.
- **Two derived objects, used from here on.**
  - The **life weight** `w(s)`: what a unit of base utility at `s` adds to the life-sum once
    every echo is counted (§3, §4, §7).
  - The **felt row**: how the momentary self weighs the rest of its life (§3, §5).
  - **Rows and columns of one operator** *standard* algebra, the reading *synthesis*. For a
    foreseen life `e = R u` with `R = (I − K)⁻¹`: the felt row is a row of `R`, the life
    weight a column sum, `W = Σ_s w(s) u_s`. Read as preference, the same recursion makes
    each row a self's utility function over the life (Bergstrom 1999 between people;
    Sáez-Martí & Weibull 2005 between selves), the momentary hedonist's objective, and with
    pure altruism benefit-cost counts base values only (Bergstrom 2006; Milgrom 1993). The
    hedonic reading sums the columns. Which object is welfare is the reading, and the two
    disagree most about time: a steeply present-weighted row against flat interior columns
    (§3).
- **Identification** *standard*: any felt path fits some base path (P10). The kernel is a
  frame until data or a structural family pin it (§9).
- **LessWrong anchors.** Experiencing against remembering self (lukeprog 2011; Metus 2012);
  "Not for the Sake of Happiness (Alone)".
- **Figure.** The echo graph: moments as nodes, anticipation and memory as weighted edges, one
  remembered-anticipation path highlighted.
- Companion: core, the canonical model, Objects, P1–P2, P9–P10.

### 3. A good moment counts more than once (~1,000)

- **Question.** If good moments echo, does it matter when they happen? Is there a reason to
  want a life that gets better?
- **Example.** The trip of a lifetime taken in the last months of a life has little life left
  to be remembered in; taken in infancy, nothing looked forward to it. Moving it within the
  middle of a life changes almost nothing: the holiday's own end is no boundary, since memory
  goes on after it.
- **Moments as centrality.** A moment's life weight is its Katz centrality in the
  anticipation and memory graph. *synthesis*; the hump-shaped planner weights are Caplin &
  Leahy's (2004, *imported*); the recursive closed form is *not found* (P5).
- **Flat interior, deficits at the ends.** Away from birth and death every moment approaches
  the same weight, `1/(1−M)`: given time-neutral aggregation, echoes add no pure time preference over
  base utility (*standard*: Ramsey 1928; "Against discount rates"). Birth is unanticipated and
  death unremembered, so the ends weigh less, about a sixth at the illustrative life
  calibration.
- **Shape is a boundary effect** *not found* (P6).
  - The class, stated once: foreseen lives, linear, stationary (translation-invariant),
    absolutely summable echo with a bounded resolvent. On an infinite line such echo leaves
    the life-sum unchanged by rearrangement, so a life's shape matters only through its
    ends, not its slope.
  - For linear ramps on lives long against the kernel's reach, rising beats falling,
    asymptotically, iff anticipation's lever arm beats memory's (the kernel's first moment
    `M₁ > 0`). Short lives have counterexamples. Endpoint pulses compare accumulated echo
    masses instead, and arbitrary profiles need the whole weight function.
    Loewenstein & Prelec (1993) have the flat-kernel case and Cosaert & Potoms (2024) the
    directions, both *imported*.
  - Size: about `4M₁/T` of the base utility rearranged (direct; a factor `(1−M)^{−2}` larger
    recursively). Whole-life shape preferences are small unless anticipation and memory reach
    across decades, and strongest over short sequences (a prediction, *speculation*).
  - The debate: take Brown's (2019) explaining-away horn openly, with Velleman (1991) as the
    foil, and answer Hersch & Weltman's (2024) "begs the question": the result is diagnostic.
    It says what linear echo can explain and what a narrative or nonlinear account must add.
- **No moment feels these weights.** Each self weighs its life through its own felt row,
  which is strongly present-weighted (`β ≈ 0.05`–`0.08` at the illustrative calibrations).
  A self can still choose by the life-sum.
  - **Patience is not felt anticipation.** Explaining measured patience by the felt row
    alone would make nearly all experience echo (`M ≈ 0.94` at `β = 0.7` and 4% a year),
    against the illustrative scenarios' 0.3. A felt-row explanation needs a very large echo
    mass; patient choice more plausibly runs on the life-sum or another evaluative objective.
    The inversion is Sáez-Martí & Weibull's (*imported*); the bill is *synthesis*.
- **Each self is a lens; peak-end.** Judging a life from its end inherits recency. A fading
  memory kernel gives the end effect, and duration neglect as saturation, with some duration
  sensitivity for episodes shorter than memory's reach, unlike averaging snapshots. A peak
  beyond recency needs salience-weighted memory (Lim et al. 2020). *synthesis* of imported
  pieces (Fredrickson & Kahneman 1993).
- **Forgotten pain.** A pain later forgotten counted in full when it was felt; it loses only
  the painful recollections it would have caused. *imported* (Lee et al. 2022; Shardlow et
  al. 2025; Parfit's amnesia case, second-hand).
- **Figure.** Life weights `w(s)`, direct against recursive, flat inside with deficits at both
  ends; inset, a rising and a falling ramp of equal total.
- Companion: core P5–P7 (peak-end with P7); `calibration.md` for the patience bill.
- To the companion: the James Dean effect (P8), P7's numbers, the ramp's exceptions.

### 4. Learning can change how life feels without changing what you do (~1,400)

- **Question.** Would you take a free, accurate test for a fatal, untreatable disease? The
  Litany of Gendlin says owning up to what is true makes nothing worse.
- **Example.** Huntington's disease: of 1,001 at-risk people untested at enrollment, under
  10% pursued predictive testing over the study's follow-up, and the untested acted like
  non-carriers (Oster, Shoulson & Dorsey, working paper; the corrigendum revises the
  actual-risk series, with less over-optimism). Holiday version: a booking that may fall through,
  with reassuring and worrying updates and nothing to do until a set date.
- **Beliefs enter welfare** *imported* (Brunnermeier & Parker 2005). Felt anticipation is a
  forecast, so what you believe changes what you feel, and welfare is scored by the objective
  expectation of the felt life.
- **In expectation the truth is free** *standard* (the tower property: Epstein 2008; Eliaz &
  Spiegler 2006; Kimball & Willis 2006), given linear echoes and news, a calibrated prior,
  actions held fixed and a lifespan the information does not move. Pathwise it is not: bad
  news hurts now. The Litany is right on average and wrong for whoever draws the bad news;
  Raemon's (2011) "Issues with the Litany of Gendlin" is the pathwise half.
  - Exception *not found*: mortality information is priced even in the linear recursive
    model, since remembered anticipation runs only in the branches where you live.
- **Ignorable is not cost-free** *imported* (Kadane, Schervish & Seidenfeld 2008). Good's
  theorem says free information never hurts a decision, because you can act as if you had not
  seen it; it says nothing about how seeing it feels. Their own examples are a mystery's ending
  and Huntington's testing. LessWrong's value-of-information and updatelessness discussions
  (Diffractor 2018; Soto 2024) are about the ignorable half.
- **What prices information is nonlinearity in beliefs** *imported* (Kreps & Porteus via
  Skiadas 1998; Eliaz & Spiegler 2006; on LessWrong, jimrandomh's `√p` utility of belief).
  The symmetric core has none, mortality aside. The sign asymmetries of §5 supply it:
  - **Dread outweighing savoring**, the best-supported: it needs recursion (§5).
  - **Loss-averse news** *imported* (Kőszegi & Rabin 2009; Pagel 2018), the least
    supported as a feeling (§9). Bad news hurts more than equal good news helps, so at equal
    effective weights news felt piecemeal costs more than news felt at once, and updates
    that end where they began still cost. News is a schedulable pain: its cost is its size
    times the life weight of the moment it is felt (the life-weighted form *not found*).
    With unequal weights clumping and earliness can pull apart (companion's
    counterexample).
- **Optimism or bracing** *imported* (Brunnermeier & Parker 2005; Gollier & Muermann 2010;
  van Dijk, Zeelenberg & van der Pligt 2003). A rosy forecast buys anticipation now and pays
  in disappointment later: optimism for long-awaited events, bracing for ones at short
  notice. With linear news the trade is linear, so the felt objective has no interior
  optimum, and what bounds belief (decisions, plausibility) sets the bias. Bracing is documented; its hedonic
  payoff is not (Golub, Gilbert & Wilson 2009).
- **In the near-Bayesian, linear-anticipation benchmark, self-deception does not pay for an
  agent who knows it is doing it** *imported* (Bénabou 2015; Bénabou & Tirole 2002).
  Censoring bad news makes good news suspect, and the two cancel. A formal cousin of "Doublethink", under near-Bayesian
  sophistication. So the escape is not choosing beliefs: §6 is about choosing what to feel by.
- **Objections.**
  - "Not for the Sake of Happiness (Alone)": the post locates a cost and recommends no false
    belief.
  - "Then avoid bad news": avoidance forgoes the decision value (Good's half), and avoidance
    that leaks later can cost more (§6). Ugh fields (Roko 2010) are the failure on the
    action side; Bostrom's psychological reaction hazards (2011) name the felt cost.
- **Figure.** The booking's news felt along a reassuring and a worrying path: welfare swings
  pathwise and averages to the life without news (the Litany's two halves). Inset: partial
  updates that end where they began, at equal effective weights free under linear news and
  charged under loss-averse news (§5).
- Companion: decision D5; core N1–N3, X4.
- To the companion: recollection news; the optimism quantile and rationalization as hedonic
  arbitrage, both needing loss-averse news (X4; a learned critic consoles itself after bad
  news at `λ = 2` and not at `λ = 1`).

### 5. Echoes of echoes: what recursion adds (~1,000)

- **Question.** Why model feelings about feelings at all?
- **For a life you foresee, one layer is enough** *standard* algebra, the reading
  *synthesis*. On an infinite line every recursive model is a direct one with a stretched
  kernel (P2). Recursion shows where foresight fails, at a life's ends and at surprises,
  under restrictions on the kernel family, and once gains and losses are weighed apart
  (below).
- **Exponential primitives become present-biased** *imported* one-sided (Sáez-Martí &
  Weibull 2005; Galperti & Strulovici 2017). Caring directly about every later self with
  geometrically fading weight, when they all do the same, gives a quasi-hyperbolic felt row;
  caring only about the next self gives plain exponential weights (P2). Memory loops weaken
  the bias (two-sided closed form *not found*, provisionally, P4). twanvl (2011) brings
  hyperbolic discounting from uncertain rates to LessWrong; felt echo is another structural
  route.
- **Surprises are information boundaries** *synthesis*. A shock nobody saw coming misses the
  earlier selves who would have anticipated it, so the recursive model answers differently
  from its foreseen reduced form, even on an infinite line.
- **When gains and losses differ: the extension** *synthesis*. The core weighs them alike;
  the evidence suggests an order, a synthesis across unlike measures (`calibration.md`):
  - dread over savoring, strongly: dread about six times savoring within persons (Dawson &
    Johnson 2026), little savoring in the lab (Hardisty & Weber 2020);
  - memory by sign, depending on lag: a loss's echo starts stronger and fades faster (§9;
    the fading affect bias, Hoehne & Zimprich 2024);
  - a small base kink, not separable from news at the offer (§9);
  - loss-averse news, mostly from choices: about 2 revealed in choices, 1.0–1.2 felt where
    measured (§9), and loss aversion as an affective forecasting error (Kermer et al. 2006).
  - The kinks of levels (base, anticipation, memory) sit at hedonic zero, which choices
    alone do not pin; news's sits at zero revision. The structurally cleanest kink has the
    weakest felt support.
- **Dread of dread prices information** *not found*, an extension result: the felt-flow
  identity and the direct/recursive contrast; the late-resolution structure is *imported*
  (Kreps & Porteus via Skiadas 1998; Epstein 2008).
  - Dread outweighing savoring, as a kernel on outcomes, leaves information timing neutral.
    Recursively you anticipate your own later felt states, which contain your later
    forecasts, so the asymmetry lands on a belief.
  - The penalty against a symmetric baseline is the dread excess times the life-weighted
    expected negative parts of felt states; an information schedule costs what it adds to
    that penalty. It bites only when some felt state can land on either side of zero;
    rumination (bad states remembered more) prices information the same way.
- **News about how life will feel feeds on itself.** *known in kind* (Kimball & Willis 2006:
  simultaneous news about lifetime utility, with a sufficient condition); the sharp threshold
  and regimes *not found*.
  - Good news about a far event is felt now, because tomorrow you will be looking forward to
    it; cancelling a plan costs the anticipation too.
  - Without memory the loop's gain `κ` is just the news strength; memory adds a feedback
    route (a felt state is remembered, so it moves forecasts of later experience), and
    anticipation amplifies it. `κ < 1` guarantees a unique, stable felt state for every
    revision, which the loop amplifies by `1/(1−κ)`, about a quarter at the illustrative
    calibrations.
  - With loss-averse news the threshold is `λκ < 1`, and for `1/λ < κ < 1` a uniformly bad
    revision has no felt state; a bounded gain-loss function can have a stable low state
    beside the normal one. A model result about the extension, not a theory of despair: the
    depression and panic bistability models are company, *speculation*.
- **Figure.** One-layer anticipation of outcomes against anticipation of felt states, with
  the feedback path drawn; inset, the sign asymmetries ranked by their felt evidence.
- Companion: core P2–P4, N4, X1–X4; decision D5.
- To the companion: the 2×2 of echoes against news, the threshold's closed form and full
  regime classification, D4; built-in bracing (any concave felt channel makes a calibrated
  Bayesian's relief more frequent than its disappointment; at `λ = 1` dread does so only
  slightly, and memory's sign depends on its lag profile).

### 6. Act on it, feel it later (~1,200)

- **Question.** Can you act on everything you know without feeling every update?
- **Example.** P(doom), revised weekly. Or the holiday booking handed to an agent who sends a
  summary each Sunday, until a refund email arrives on a Wednesday.
- **Two policies** *synthesis*; *known in kind* (Pagel 2018: the investor who ignores his
  portfolio and pays a manager; Andries & Haddad 2020: alerts and delegation).
  - A hedonic agent chooses an action policy (what it does with information) and an affect
    policy (what information its felt forecasts and news run on).
  - Good's theorem and updatelessness govern the action policy only. The affect policy is
    where information costs: Kadane, Schervish & Seidenfeld's cost-free half.
- **Which affect policy is best depends on the asymmetry.** In the symmetric core, with
  actions and the lifespan held fixed, none matters (the tower property). Against dread of
  dread, the best-supported case, feeling by the prior was best in every case checked; there
  is no theorem. Against loss-averse news it is a weighted scheduling problem that batches
  where weights are equal.
- **Actions leak into affect** *known in kind* (Andries & Haddad: observed consumption reveals
  wealth); the observation closure and pooling condition *synthesis*.
  - A self that knows its own policy reads hidden news off its actions, their results and
    even its inaction. Commitment alone does not stop the leak.
  - Batched feeling needs the whole observable history (acts, results, inaction) to stay
    uninformative until the batch. Delegation, delayed consequences and pooling can be
    combined to that end; none suffices alone in general (late consequences do not hide an
    informative act, and pooling acts does not hide informative results).
- **P(doom)** *speculation as psychology*: under dread or loss-averse news, settle a policy,
  act on it, feel the forecast in batches. Conditioning each action on the latest forecast trades its instrumental value
  against the news it leaks.
- **Not belief choice.** Beliefs stay accurate, so §4's cancellation does not bite. Whether
  affect can come apart from belief within one mind is open; attention and delegation are the
  known routes.
- **Optional aside: affect leaks into action too.** In one hidden-game actor-critic, a critic
  sharing a state with the policy carried its level into action: a critic that expected much
  kept the agent complacent, whether the level came from rosy feeling or a plain reward shift
  (`learning.md`, D8; the felt objective is not needed). Kept outside the network, the level
  stopped mattering: where affect lives in an architecture decides whether it leaks. An
  architectural example, not evidence about people.
- **LessWrong anchors.** Soares, "Detach the grim-o-meter" (2015): keep resolve, stop
  calibrating demeanor to global badness, with no schedule; "Simply locate yourself" (2015);
  Mayer (2023); TurnTrout (2022); Sabien (2023). The constraint is Ruby's: coping must not
  corrupt the beliefs action uses.
- **Objections.** "This is not looking": not looking forgoes the action's value, and a
  feasible delegated arrangement can preserve it, though leakage and incentives can force
  trade-offs. "Can a mind do this?": open; delegation is the existence proof.
- **Figure.** Information flowing to a doer and a feeler, with the leaks through actions,
  results and inaction drawn.
- Companion: decision D7; `learning.md`, D8.

### 7. Your past self is a predictor (~1,400)

- **Question.** You looked forward all week to Friday's dinner. On Friday you are tired. Does
  the week of anticipation count for anything now?
- **Example.** The dinner; the bottle saved for a special occasion that never comes.
- **Newcomb inside a life** *synthesis*; nearest prior art Bernheim & Thomadsen 2005 and
  Geanakoplos 1996 (Newcomb as a psychological game). A choice is Newcomb-like when an
  already-felt payoff, anticipation, depended on an accurate prediction of it. The past self
  is a natural predictor, not automatically a good one.
- **One dial, `J`** *synthesis*: how much of the already-felt past a decision rule counts as
  depending on the present choice.
  - `J = 0` is fixed-past choice; full dependence is advance commitment, the planner.
  - FDT reaches the planner only if past forecasts were accurate evaluations of the decision
    function on the realized input (the transparent-Newcomb condition); EDT need not.
  - `J` is one channel, not a classification of decision theories.
  - Optional aside: in a learner, `J` is a stop-gradient on the self's forecast of its own
    policy. In the tested no-news scheduling cases, detached it learns the fixed-past date,
    passed through the commitment date, and a partial weight the dates between; news adds
    equilibrium and optimization complications. *known in kind* (Oesterheld, Treutlein,
    Cooper & Hudson 2023; Treutlein 2023 on LessWrong).
- **The savoring trap** *imported* (Kőszegi 2010, crediting Loewenstein 1987 and Caplin &
  Leahy 2001); exact stopping conditions *not found*.
  - Selves who share the life-sum objective, each holding the past fixed, push a pleasure
    toward the unremembered end and hurry pains: each counts the anticipation it can still
    gain, not what earlier selves already felt. The bottle.
  - Opposite in sign to present bias's preproperation (O'Donoghue & Rabin 1999). An
    effortless pleasure under sophistication tells them apart (*speculation*; Shu & Gneezy's
    procrastinated pleasures have rival explanations).
- **Plans become reference points** *imported* (Kőszegi & Rabin 2009: the preferred
  credible plan, Def. 1, and the plan as its own commitment device, Prop. 5), adapted to
  recursive news. Deviating from what past selves predicted is felt as news; under
  loss-averse news (§5's extension) the losses within that revision can make plans sticky,
  so expectations can do a commitment device's work. Weak news keeps the trap. The model
  check's percentages wait on an archived script.
- **Reliability is worth its anticipation** *synthesis*; anticipation scaled by one's own
  forecast of follow-through is *not found*.
  - A self known to bail whenever the moment dips anticipates every plan's reward at a
    discount (exactly for a fixed reward component; anticipated costs and news move too), so
    follow-through that looks like sunk cost can pay at the policy level: Parfit's hitchhiker
    inside one life.
  - Past anticipation alone is not a reason to follow through, and the echo channel `J` does
    not by itself favour reliability in the cost-then-reward example.
  - Felt news can make selves flaky against their own interest (worked example: strong
    linear news, or weaker loss-averse news).
  - Nearest: Bénabou & Tirole's personal rules (2004), whose payoff is instrumental.
- **LessWrong anchors.** Newcomb and FDT (Yudkowsky & Soares 2017); successive selves as a
  prisoner's dilemma (picoeconomics: Crowley 2009, Alexander 2009; Wei Dai on Zvi's "How I
  lost 100 pounds using TDT"); Parfit's hitchhiker.
- **Objection.** "This is commitment devices": yes, for a causal agent with a device. FDT's
  claimed edge is reaching the planner without one, if past forecasts track the policy.
- **Figure.** One pleasure scheduled two ways, the commitment date against the fixed-past
  selves' date, with the lost memory shaded; optional inset, the learner's dial
  (`experiments/learned_expectations/scheduling_dial.png`).
- Companion: decision D1–D3, D6.

### 8. Copies (~500; cuttable to a follow-up)

- **Question.** You are about to be copied. How much should you look forward?
- **Anticipation, as a forecast of one continuing path, is measure-weighted** *synthesis*,
  assumed rather than derived. It takes the conserved-measure horn of the Anthropic Trilemma
  (Yudkowsky 2009); Greaves's caring measure (2004, second-hand) is the precedent.
- Copy-counted anticipation would let a branching future outweigh a single past without
  bound.
- Aggregation is a second axiom. Aggregated by measure as well, splitting into identical
  continuations is welfare-invisible and adds up to normality (Everett branches); branches
  with different outcomes are resolved like any uncertainty, news costs included; real copies (uploads, LLM
  instances) are extra welfare subjects, a population-ethics question the kernel does not
  settle.
- Identity is not needed: kernel weight links moments. Parfit's connectedness is the direct
  kernel and continuity, graded, the resolvent: an analogy (Parfit second-hand, via Bartels &
  Rips 2010).
- A context window as a life with hard ends, instances as the branching tree: *speculation*,
  the follow-up's teaser.
- **Figure.** A branching tree with measure on its branches.
- Companion: `selves.md`.

### 9. What the data say (~800)

- **Question.** Do echoes show up in measured happiness, and does the data pick the
  recursive model?
- **Momentary happiness**: the Great Brain Experiment (47,067 people) and Forbes & Bennett's
  two experiments. Rutledge et al.'s (2014) model *imported*; the analysis is new.
  - Echoes of task outcomes are front-loaded with a slow tail, closer to a power law than to
    the standard single exponential, in all three datasets, on held-out people.
  - About 80% of a sustained outcome stream's fitted response comes from earlier trials (the
    fitted kernel's echo share, 0.78–0.82). It is a statement about task outcomes over a
    play, not about happiness at large, and under the power law it grows with the window.
  - The recursive model fits but is not singled out: direct memory fits identically (P2),
    and a transient plus a mood, or pooling people with different kernels, also front-load.
  - Chosen risk lowers happiness. In 50/50 gambles an apparent loss-averse news asymmetry is
    the same regressor as a felt cost of the chosen gamble's spread; where probabilities vary,
    a lottery-risk regressor absorbs or reduces it. The adjusted task fits give felt news
    `λ` of roughly 1.0–1.2, which is why the core is symmetric. A certain loss moves happiness 1.2 times an equal gain, but
    that kink sits where the pre-trial forecast does, so it is not separable from news.
  - A loss's echo starts stronger and fades faster: 1.13 times a gain's one trial on, 0.94 at
    twenty, with alike echo masses over a play. Read as memory, the fading affect bias at
    the scale of trials.
  - Whether the play-long persistence belongs to the outcomes or to news (accumulated luck) is
    not identified: two near-tied fits.
  - Across plays, carryover is consistent with a slowly decaying positive afterglow: about
    45% of a play's luck after minutes and 23% after 22 minutes, with intervals that include
    zero from hours on; replay timing is the player's choice. No negative adaptation lobe was
    detected at these scales, and the pulse design constrains slow adaptation only weakly.
- **Calibration anchors** (`calibration.md`): sign asymmetries ranked by felt evidence (dread
  strongly over savoring, loss-averse news weakly), news strength 0.1–0.3, thought running
  forward about three times as often as back, a small felt echo of the weekend.
- **Figure.** Lag-response curves (single geometric, jump, power law) against the free
  kernel, with held-out error.
- Companion: `experiments/happiness/README.md`; `calibration.md`.

### 10. What survives (~600)

- **Question.** What is left if you reject the strongest assumptions?
- **Claims against what they need.**
  - Counting felt echoes as welfare: only that experience counts.
  - Life weights and the boundary result: linear, additive, stationary echo.
  - Prices on information: a sign asymmetry (dread, rumination or loss-averse news; §5),
    with actions and the lifespan held fixed (mortality information is priced regardless).
  - The past self as predictor: forecasts that track the policy.
- **Limits.** The core is symmetric and real kernels are not: dread's asymmetry has the
  strongest evidence, though its survey measure is coarse, and kernels are nonlinear beyond
  sign too; power-law forgetting threatens
  `M < 1` and `M₁`; the evidence for a past–future asymmetry is thin; identification (P10);
  whether echo adds to the present or displaces it (parked); hedonic adaptation, ruled out
  only at fast scales (parked); whether affect can separate from belief in one mind.
- **Example.** Someone knowingly chooses a less pleasant, more meaningful life: the model
  accounts for its hedonic part and does not settle the choice.
- **Figure.** The claim–assumption matrix.

## Technical companion

The `formalism/` docs, polished: `core.md` (the model, echoes P1–P10, news N1–N4),
`decision.md` (D1–D7), `selves.md` (A1–A2, horizons, identity), `calibration.md`, and the
checks and playground. `formalism/INDEX.md` is its table of contents and claim map.

## Follow-ups

- **Decision theory by learning.** Twins and altruists look alike in symmetric self-play; a
  copy signal or inferred dependence separates them; iterated games and unknown adversaries
  (`experiments/learned_expectations/`, `notes/empathy.md`).
- **Shared-state critics** (`learning.md`, D8). A critic's level reaches the policy through
  their shared state: machine learning, its own short piece.
- **LLMs.** The peak-end study (positional weights of an end-of-episode rating identify the
  effective memory kernel); context windows and sessions as lives; instances as A1's tree.
- **The Bates world** (`notes/bates.md`): its own project.
