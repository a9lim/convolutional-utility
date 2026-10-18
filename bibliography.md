# Bibliography

Status: **FT** full text read · **WP** full text of a working/author version (published
text may differ) · **ABS** abstract or publisher record only · **ABS+** abstract plus part
of the text (a scan or excerpt) · **2ND** primary unread, described via the secondary
named. Files are in `references/`. First verification pass 2026-10-12 (two literature
agents plus Codex; spot-read by Claude where marked).

## Direct precursors of the premise

- **Bergstrom, T. (1999).** Systems of benevolent utility functions. *J. Public Economic
  Theory* 1(1): 71–100. doi:10.1111/1097-3923.00004. **FT** (typeset accepted version,
  eScholarship; and CREST WP 87-4, 1987) ·
  `papers/bergstrom-1999-systems-of-benevolent-utility-functions-jpet.txt`,
  `papers/bergstrom-1987-systems-benevolent-utility-interdependence.txt`
  - `U = u + AU`; nonnegative inverse ⟺ `I − A` dominant diagonal (M-matrix). On ℤ the
    Neumann series gives the unique *bounded* nonnegative inverse.
  - Prop. 5: nearest-neighbour two-sided `U_t = u_t + aU_{t−1} + bU_{t+1}` is well-behaved
    iff `a + b < 1`, and reduces to two-sided geometric weights on `u` (bounded root).
  - The conclusion sketches the *intrapersonal* reading: happiness depends on
    consumption, expected next-period happiness, and remembered past happiness. A finite
    life is called essential to the story. No results follow. In the JPET version the
    reading moves into §5 (p. 83, "a simple model of memory and anticipation for a single
    person"), extending Kimball's hall of mirrors to remembered pleasures and anticipated
    delights; fn. 7 says finite life and nonstationarity matter.
  - JPET Lemmas 2–4: the nearest-neighbour factorization `(I−A) = (1/(1+αβ))(I−αJ⁻¹)(I−βJ)`,
    and the forward discount rate rises with the backward weight. §6.1 (p. 86): one-sided
    altruism fits anticipated but not recollected happiness. Nearest-neighbour only, no
    geometric kernel: P4 is not pre-empted.
- **Caplin, A. & Leahy, J. (2004).** The social discount rate. *J. Political Economy*
  112(6): 1257–1268. doi:10.1086/424740. **WP** (NBER w7983) ·
  `papers/caplin-2000-the-social-discount-rate-nber-w7983.txt`
  - The direct two-sided model (D): each self discounts the past and the future.
  - A planner's weights on felicity are hump-shaped with equal rates, and rising when
    there is no memory. The planner is more patient than the selves (Prop. 1).
  - §4.6 is the explicit Jevonian defence: felicity is experienced several times
    (anticipated, enjoyed, remembered), so counting it several times is no error.
- **Ray, D., Vellodi, N. & Wang, R. (2024).** Past and future: backward and forward
  discounting. *JEEA* 22(2): 837–875. doi:10.1093/jeea/jvad036. **FT** (Claude) ·
  `papers/ray-2024-past-and-future-backward-forward-discounting.txt`
  - Felicity discounts consumption backward (rate `b`) and forward (rate `f`). Overall
    utility weights future selves' felicities, with a privileged "retirement self":
    one level of anticipated-remembered.
  - Effective discounting is non-geometric and time-inconsistent. Local impatience falls
    toward the retirement age, can turn negative, and jumps at retirement (Prop. 1);
    they match this to age profiles in Harrison et al. 2002 and Read & Read 2004.
  - Fn. 4 avoids weighting past selves: "if we deviate from a plan, will those selves
    feel the change?" — the intervention problem (core P9).
  - §5.2: the planner is more patient than the agents (after Caplin & Leahy).
- **Hersch, G. & Weltman, D. (2022).** A new well-being atomism. *PPR* 107(1): 3–23.
  doi:10.1111/phpr.12900. **FT** · `papers/hersch-weltman-2022-a-new-well-being-atomism.txt`
  - Comprehensive momentary well-being = discrete + retrospective (a function of
    earlier times) + expectational (expected future discrete well-being). Lifetime
    well-being sums these. This is model D in words, with a hedonic reading.
  - Expectations may be actual, rational or possible, so anticipation need not track
    the realized future.
- **Cosaert, S. & Potoms, T. (2024).** Intertemporal consumption with anticipating,
  remembering, and experiencing selves. *Int. Economic Review* 65(3): 1283–1322.
  doi:10.1111/iere.12705. **FT** (open access, read closely) ·
  `papers/cosaert-2024-anticipating-remembering-experiencing-selves.txt`
  - Direct, one layer: `V = ω_A U^A + ω_R U^R + U^E`, with accumulation factors
    `D_A = β_A^{t−τ+1}`, `D_R = β_R^{T−t+1}`, `β ≥ 1` (p. 9), not decay kernels.
  - Not estimated: `β_A, β_R` are grid-searched on [1, 1.2] in a revealed-preference
    rationalizability test (fn. 23: the gains in fit come between 1 and 1.2), on Spanish
    household data, quarterly, four quarters, 2,052 households. No calibration anchors.
  - Anticipation favours increasing profiles, memory decreasing ones (pp. 3, 5); no
    first-moment link, no closed forms. Cites Chapman (1996) and Castillo et al. (2022):
    more prefer improving sequences as the array shrinks (p. 8), support for P6's
    short-horizon prediction.
- **Knight, J. & Gunatilaka, R. (2014).** Memory and anticipation: new empirical support
  for an old theory of the utility function. Oxford Econ. DP 721. **FT** ·
  `papers/knight-2014-memory-and-anticipation-new-empirical-support-for-an-old-theory-of-the-utility-function-oxford-dp721.txt`
  - Tests the Bentham and Jevons utility of memory and anticipation with subjective
    well-being regressions on past and expected income.
- **Elster, J. & Loewenstein, G. (1992).** Utility from memory and anticipation. In
  Loewenstein & Elster (eds.), *Choice over Time*, Russell Sage, 213–234. **2ND**
  (Loewenstein & Prelec 1993; Shardlow et al. 2025)
  - Memory and anticipation each have a consumption effect and a contrast effect.
    Stronger backward contrast favours improvement.

- **Sommervoll, D. E. (2010).** Self-delusion in the pursuit of happiness. Statistics
  Norway DP 604. **WP** · `papers/sommervoll-2010-self-delusion-in-the-pursuit-of-happiness-ssb-dp604.txt`
  - Discounted utility with memories and anticipations. Notes that anticipations of
    memories and memories of anticipations exist, but models first order only (§2, p. 6).
  - Ex. 2.4 (p. 9): one-step anticipation leaves the first period unanticipated, P5's
    birth deficit; Thm 2.1 (p. 8) derives time inconsistency from it. Deterministic, no
    news: nothing on sequences (P6), and its optimal self-delusion has no disappointment
    cost (Thm 3.3), unlike N3.

## Recursion and altruism math

- **Sáez-Martí, M. & Weibull, J. (2005).** Discounting and altruism to future
  decision-makers. *J. Economic Theory* 122(2): 254–266. doi:10.1016/j.jet.2004.06.003.
  **WP** (IFN WP 575, 2002) · `papers/saez-marti-2002-discounting-and-future-selves-wp575.txt`
  - Altruism toward future selves' *total* utility ↔ discounting of consumption utility,
    `f = 1 + f* ∗ f`.
  - §4.4: quasi-hyperbolic `βδ^t` ↔ exponential altruism weights, which is core P3.
    Exponential discounting ↔ one-period altruism.
  - Eqs. 15–17: `f(t) = βδ^t` gives `f*(t) = β(1−β)^{t−1}δ^t`, so `β* = β/(1−β)`,
    `δ* = (1−β)δ`: `calibration.md`'s inversion, exactly. Their example (Angeletos et al.'s
    `β = 0.55, δ = 0.96`) gives `β* = 1.22, δ* = 0.43`. One-sided only.
  - A nonnegative `f` need not give a nonnegative `f*`; the negative case is called
    "spite". The working paper states no convergence condition.
- **Galperti, S. & Strulovici, B. (2017).** A theory of intergenerational altruism.
  *Econometrica* 85(4): 1175–1218. doi:10.3982/ECTA13937. **WP** (Jan 2017 preprint) ·
  `papers/galperti-2017-a-theory-of-intergenerational-altruism-preprint.txt`
  - Axiomatizes pure altruism toward future generations' total utility. Present bias
    follows (Prop. 2). Its footnote: a subset of the results appeared as "From
    Anticipations to Present Bias: A Theory of Forward-Looking Preferences" (2014 WP), the
    single-agent anticipation framing, so P3's credit covers anticipation too.
  - Cor. 3: linear `G` gives `βδ^t` with `β = γ/(1+γ)`, `δ = (1+γ)α`, on
    `γ < (1−α)/α` — our `M < 1`.
  - §4.5, "a first step" (p. 27): finite two-sided systems, solvable iff `αα̂ < 1` for two
    generations and `αα̂ < 1/3` for three (`det(I−K) = (1+αα̂)(1−3αα̂)`, an instance of
    P1(a)). No general-`T` closed form, no roots `p, q`, no life weights: P4 and P5 are
    not pre-empted.
  - Credits Fels & Zeckhauser (2008, *J. Risk & Uncertainty* 37(2–3): 187–197; paywalled,
    unread; one-sided, an aggregator linear in future generations' well-being, per G&S
    p. 19) for the
    linear equivalence.
- **Kimball, M. (1987).** Making sense of two-sided altruism. *J. Monetary Economics*
  20(2): 301–326. doi:10.1016/0304-3932(87)90018-3. **ABS** (2ND: Bergstrom 1999)
  - Two-sided intergenerational recursion, solved as a difference equation whose
    bounded solution uses the smaller root. Not the source of P4 or P6.
- **Hori, H. & Kanaya, S. (1989).** Utility functionals with nonpaternalistic
  intergenerational altruism. *JET* 49(2): 241–265. doi:10.1016/0022-0531(89)90080-X.
  **2ND** (Bergstrom 1999; Galperti & Strulovici; Codex)
  - Existence and uniqueness for two-way altruism. Distinguishes "mortality" solutions
    (ancestors' utility held fixed) from "eternity" solutions (re-evaluated
    counterfactually), the semantics in core P9.
  - Hori (1992), *JET* 56(2): 451–467, doi:10.1016/0022-0531(92)90092-V, extends this to
    altruism over many generations. Paywalled, unread. Bergstrom (1999, fn. 6) reports that
    Hori could not find the utility functions in explicit form and gives a system of
    equations instead, so P4's closed form is probably not there.
- **Ray, D. (1987).** Nonpaternalistic intergenerational altruism. *JET* 41(1): 112–132.
  **2ND** (Ray, Vellodi & Wang 2024; Galperti & Strulovici)
  - Poses representing utility-over-utility altruism in consumption form.
- **Heifetz, A., Minelli, E. & Polemarchakis, H. (2023).** Affective interdependence and
  welfare. arXiv:2305.10165. **WP** · `papers/heifetz-2023-affective-interdependence-and-welfare.txt`
  - A P-matrix suffices for Pareto-optimal affective equilibria. A resolvent with negative
    entries can still admit positive welfare weights, though equal weights may fail.
- **Borovička, J. & Stachurski, J. (2020).** Necessary and sufficient conditions for
  existence and uniqueness of recursive utilities. *J. Finance* 75(3). **WP**
  (arXiv:1710.06526) ·
  `papers/borovicka-2019-necessary-and-sufficient-conditions-for-existence-and-uniqueness-of-recursive-utilities-arxiv.txt`
  - Recursive utility can be "vacuous": no finite solution exists when the spectral
    radius of a valuation operator reaches one (Thm. 3.1). P1's threshold form, with
    growth and discounting in place of echo.
- **Shinotsuka, T. (2002).** Interdependent utility functions in an intergenerational
  context. Seminar paper. **WP** (partial) ·
  `papers/shinotsuka-2002-interdependent-utility-functions-intergenerational.txt`
  - Lattice-theoretic existence under boundedness and monotonicity. Example 1: no
    monotone representation when `αβ > 1`.

## Anticipatory and memory utility, sequences

- **Loewenstein, G. (1987).** Anticipation and the valuation of delayed consumption.
  *Economic Journal* 97(387): 666–684. doi:10.2307/2232929. **FT** ·
  `papers/loewenstein-1987-anticipation-and-valuation-of-delayed-consumption.txt`
  - A one-sided exponential anticipation kernel on future consumption utility, scaled by
    "imaginability" and discounted on top. Savoring motivates delay, dread motivates
    getting it over with. A reverse time inconsistency. Cites Wolf (1970) on utility from
    memory. Direct, not recursive.
- **Loewenstein, G. & Prelec, D. (1993).** Preferences for sequences of outcomes.
  *Psychological Review* 100(1): 91–108. doi:10.1037/0033-295X.100.1.91. **FT** ·
  `papers/loewenstein-1993-preferences-for-sequences-of-outcomes.txt`
  - `AU = Σ(t−1)u_t`, `RU = Σ(n−t)u_t`, improvement `= (AU − RU)/2`. This is the flat-kernel
    case of core P6. The weight on improvement is a free parameter, not derived.
- **Baucells, M. & Bellezza, S. (2017).** Temporal profiles of instant utility during
  anticipation, event, and recall. *Management Science* 63(3): 729–748.
  doi:10.1287/mnsc.2015.2362. **WP** (2016 articles-in-advance) ·
  `papers/baucells-2016-temporal-profiles-of-instant-utility-aer.txt`
  - Single-event instant utility with an adaptive reference point. Anticipation and
    recall decay at different rates. Anticipation is U-shaped, and there is an optimal
    anticipation length. Total utility is `∫u`; not recursive.
- **Gilboa, I., Postlewaite, A. & Samuelson, L. (2016).** Memorable consumption. *JET* 165:
  414–455. doi:10.1016/j.jet.2016.05.004. **WP** (PIER 16-003) ·
  `papers/gilboa-2016-memorable-consumption-wp.txt`
  - A backward exponential kernel on memorable consumption above a customary level;
    habit formation is nested. §5.1.5 leaves anticipation out because it makes a game
    among selves.
- **Minardi, S. & Savochkin, A. (2023).** Time for memorable consumption (axiomatic memory
  utility; anticipation excluded). **WP** · `papers/minardi-2023-time-for-memorable-consumption.txt`
  - Citation details still to pin down.
- **Caplin, A. & Leahy, J. (2001).** Psychological expected utility theory and anticipatory
  feelings. *QJE* 116(1): 55–79. doi:10.1162/003355301556347. **FT** (third-party copy of
  the published article) · `papers/caplin-2001-psychological-expected-utility-theory-and-anticipatory-feelings.txt`
  - Prizes are psychological states; anticipation without memory (fn. 8, p. 63).
    Period-1 utility depends on the period-2 policy, so plans are time-inconsistent
    (pp. 64–66); Kreps–Porteus is the consistent special case.
  - Information preferences are motivated qualitatively (blunters and monitors; BRCA
    testing, p. 60), with no concave/convex theorem.
  - p. 75: rejecting the substitution axiom is valid only if there can be no complete model
    of psychological states, as with anticipatory feelings about anticipatory feelings ad
    infinitum. Core P1 is a complete model of that regress when `M < 1`.
- **Brunnermeier, M. & Parker, J. (2005).** Optimal expectations. *AER* 95(4): 1092–1118.
  doi:10.1257/0002828054825493. **FT** (author copy, AER pagination; proofs unread) ·
  `papers/brunnermeier-2005-optimal-expectations.txt`
  - Felicity = memory utility + current flow + anticipatory utility (§I.A, p. 1095), with
    a memory discount separate from the future discount; only `δ = 1/β` keeps rankings
    time-invariant (p. 1098). Formally the direct model with exponential kernels.
  - Well-being is the objective expectation of average felicity (Def. 1, p. 1096).
    Beliefs are chosen once, then updated by Bayes, by agents unaware of the distortion
    (p. 1097).
  - Small optimism: first-order anticipatory gain, second-order decision cost (p. 1093).
    Optimists are surprised downward on average (Prop. 4). Later resolution can be
    preferred because information removes the ability to distort (pp. 1108–09).
  - The nearest prior art for D5's optimist. No felt disappointment term.
- **Kimball, M. & Willis, R. (2006).** Utility and happiness. U. Michigan WP. **WP** (§8
  read by the literature agent; pins checked) · `papers/kimball-2006-utility-and-happiness-*.txt`
  - Affect = baseline mood + elation, elation an increasing function of current and past
    news about lifetime utility (p. 29).
  - §8: putting elation in the utility function means solving simultaneously for elation
    and lifetime utility (p. 38). Prop. 2 (p. 39): under rational expectations, adding a
    linear function of lifetime-utility news with coefficients summing below one leaves
    preferences unchanged.
  - Prop. 2's "sum below one" is the solvability condition: `v*_t = v_t/(1−θb_0)` (p. 39).
  - §8E (pp. 42–45): elation with slope 1 for good news and `ψ > 1` for bad, `ψ` a factor
    "to represent the additional difficulty of processing bad news". The fixed point is
    unique "since the maximum slope of θg is θψ<1" (p. 43): sufficient, not iff. The kink
    is sharpened by `(1−ψθ)^{-1}`, "formally like a Keynesian multiplier" (p. 45). Core
    N4's threshold, in a scalar problem without echo or a horizon kernel.
  - `g` is bounded (asymptotes `±γ/ρ`, p. 43), so a solution survives past the threshold;
    nothing is said about what lies beyond.
  - §8B (p. 40): memory of past expectations can be manipulated ("gratitude"), a precursor
    of core's recollection sketch; lowering expectations has no effect on lifetime utility
    far from death.
- **Kimball, M. & Willis, R. (2023).** Utility and happiness. NBER WP 31707. **WP** ·
  `papers/kimball-2023-utility-and-happiness-nber-w31707.txt`
  - Later version; the same condition `θψ < 1` (PDF p. 44).
  - §8B (p. 40): imperfect memory of past expectations "may provide an opening for gaming
    the system".
  - Their utility is a decision construct, kept apart from happiness. The prior art for
    core N4.
- **Frederick, S., Loewenstein, G. & O'Donoghue, T. (2002).** Time discounting and time
  preference: a critical review. *JEL* 40(2): 351–401. doi:10.1257/002205102320161311.
  **FT** · `papers/frederick-2002-time-discounting-and-time-preference-review.txt`
  - §5.2.3 sets out Loewenstein's anticipation model. Notes the sign effect (dread >
    savoring) and the preference for improving sequences (§4.2.4). No memory section.
- **Constantinides, G. (1990).** Habit formation. *JPE* 98(3): 519–543. doi:10.1086/261693.
  **FT** (not saved)
  - Utility over `c − x`, where `x` is an exponentially weighted sum of past consumption.
    The canonical negative backward kernel, with linear-contrast caveats.

## Welfare: planners, time-neutrality, double counting

- **Kahneman, D., Wakker, P. & Sarin, R. (1997).** Back to Bentham? Explorations of
  experienced utility. *QJE* 112(2): 375–405. doi:10.1162/003355397555235. **FT** ·
  `papers/kahneman-1997-back-to-bentham.txt`
  - Total utility = time-neutral integral of instant utility. Effects of anticipation and
    of previous consumption must already be inside instant utility (Axiom 3, a
    "sufficient statistic"). This is the rationale for summing `e` with echoes included.
- **Kahneman, D. (2000).** Experienced utility and objective happiness: a moment-based
  approach. In *Choices, Values, and Frames*, ch. 37. **FT** ·
  `papers/kahneman-2000-moment-based-approach-experienced-utility.txt`
  - Contrasts time-neutral total utility with discounted decision utility. Global
    retrospective judgments are treated as errors.
- **Ramsey, F. P. (1928).** A mathematical theory of saving. *Economic Journal* 38(152):
  543–559. doi:10.2307/2224098. **FT** · `papers/ramsey-1928-mathematical-theory-of-saving.txt`
  - Discounting later enjoyments is "ethically indefensible", a weakness of imagination.
    Enjoyments at different times are assumed separable and additive.
- **Bernheim, B. D. (1989).** Intergenerational altruism, dynastic equilibria and social
  welfare. *REStud* 56(1): 119–128. **WP** (NBER w2288, other title) ·
  `papers/bernheim-1987-intergenerational-altruism-and-social-welfare-nber-w2288.txt`
  - A planner over total utilities is dynamically inconsistent unless it honours the dead.
    Its felicity discount tends to max(planner, individual), paralleling Caplin & Leahy
    Prop. 4.
- **Bergstrom, T. (2006).** Benefit-cost in a benevolent society. *AER* 96(1): 339–351.
  doi:10.1257/000282806776157623. **WP** (2004) ·
  `papers/bergstrom-2004-benefit-cost-in-a-benevolent-society-wp.txt`
  - At distributionally efficient allocations, use private values and do not add
    altruistic valuations. This treats base `v` as welfare and `U` as preference, the
    opposite of the Jevonian reading.
- **Milgrom, P. (1993).** Is sympathy an economic value? In Hausman (ed.), *Contingent
  Valuation: A Critical Assessment*. **2ND** (Bergstrom 2006)
  - Benefits are the sum of private valuations; sympathy is not added.

## Philosophy: the shape of a life

- **Velleman, J. D. (1991).** Well-being and time. *Pacific Phil. Quarterly* 72(1): 48–77.
  doi:10.1111/j.1468-0114.1991.tb00410.x. **FT** · `papers/velleman-1991-well-being-and-time.txt`
  - Uphill and downhill lives with equal sums of momentary well-being differ, and
    well-being is non-additive. He explains the difference by narrative meaning
    (retrospective significance), not by timing.
  - Behind his veil, timing alone gives indifference.
  - Explicitly sets aside C. I. Lewis's claim that events are coloured by recollection
    and anticipation of other events. This is the strongest foil to our account.
- **Slote, M. (1982).** Goods and lives. *Pacific Phil. Quarterly* 63: 311–326 (rpt. in
  *Goods and Virtues*, 1983). **2ND** (Velleman)
  - A time preference for goods that come late in life.
- **Dorsey, D. (2015).** The significance of a life's shape. *Ethics* 125(2): 303–330.
  doi:10.1086/678373. **FT** (KU ScholarWorks) ·
  `papers/dorsey-2015-the-significance-of-a-lifes-shape.txt`
  - An ecumenical shape-of-a-life hypothesis with a relational (narrative) view: relations
    between events can enter synchronic welfare (pp. 310–313, 327–329). No anticipation or
    memory anywhere in the body.
  - The Instrumental View, nearest to ours (shape causes felt unhappiness, p. 308), is set
    aside by stipulation: shape itself "has no instrumental effects" (p. 309). Such
    explanations may be true but are not "of themselves sufficient" (p. 310).
- **Brown, J. L. D. (2019).** Additive value and the shape of a life. *Ethics* 130(1):
  92–101. doi:10.1086/704345. **FT** · `papers/brown-2019-additive-value-and-the-shape-of-a-life.txt`
  - Dilemma: once relational value is built into momentary value, the equal-sums case
    changes and the shape hypothesis is explained away. Our model takes that horn
    openly.
- **Glasgow, J. (2013).** The shape of a life and the value of loss and gain. *Phil.
  Studies* 162(3): 665–682. doi:10.1007/s11098-011-9788-0. **ABS**
  - Momentary losses are themselves bad and gains good.
- **Hersch, G. & Weltman, D. (2024).** It's not the slope that matters. *J. Moral
  Philosophy* 22(1–2). doi:10.1163/17455243-20244139. **FT** ·
  `papers/hersch-weltman-2024-not-the-slope-that-matters.txt`
  - Memory salience and future-regarding routes give the upward life "more area at the
    moments of looking back". They argue such routes cannot support the *slope*
    hypothesis without begging the question. The closest philosophical treatment of our
    mechanism, informal.
- **Kauppinen, A. (2012).** Meaningfulness and time. *PPR* 84(2): 345–377.
  doi:10.1111/j.1933-1592.2010.00490.x. **FT** · `papers/kauppinen-2012-meaningfulness-and-time.txt`
  - Puts the hedonist reply as order effects incorporated into moment-utilities (citing
    Feldman 2004 and Kahneman 2000). Lists those who think order matters beyond regret and
    anticipation.
- **Campbell, S. M. (2015).** When the shape of a life matters. *ETMP* 18(3): 565–575.
  doi:10.1007/s10677-014-9540-x. **FT** · `papers/campbell-2015-when-the-shape-of-a-life-matters.txt`
  - Distinguishes first-order from synchronic shape; under hedonism they coincide.
- **Portmore, D. (2007).** Welfare, achievement, and self-sacrifice. *JESP* 2(2): 1–29.
  doi:10.26556/jesp.v2i2.22. **FT** · `papers/portmore-2008-welfare-achievement-and-self-sacrifice.txt`
  - Fn. 32 reports Feldman: shape matters only if noticed and enjoyed (attitudinal
    hedonism).
- **Feldman, F. (2004).** *Pleasure and the Good Life*, ch. 6. OUP. **2ND** (Portmore;
  Kauppinen)

## Philosophy and experimental philosophy: time biases

- **Parfit, D. (1984).** *Reasons and Persons*, ch. 8. OUP. **2ND** (Dougherty 2011; Lee
  et al. 2022)
  - The "my past or future operations" case. People prefer the longer painful operation
    to lie in the past. The section number is still to confirm.
- **Dougherty, T. (2011).** On whether to prefer pain to pass. *Ethics* 121(3): 521–537.
  doi:10.1086/658896. **FT** · `papers/dougherty-2011-on-whether-to-prefer-pain-to-pass.txt`
  - Pain pump: a risk-averse, future-biased agent can be exploited across amnesia
    pills.
  - Fn. 21 doubts that anticipation and memory differ in phenomenology, which is our
    mechanism.
- **Sullivan, M. (2018).** *Time Biases*. OUP. **2ND** (Campbell NDPR review; Lee et al.
  2022; Shardlow et al. 2025)
  - Temporal neutrality: both near-bias and future-bias are irrational. Anticipates that
    memories carry value.
- **Greene, P., Latham, A., Miller, K. & Norton, J. (2021).** On preferring that overall,
  things are worse: future-bias and unequal payoffs. *PPR* 105(1): 181–194.
  doi:10.1111/phpr.12819. **FT** · `papers/greene-2021-future-bias-and-unequal-payoffs.txt`
  - Negative future-bias survives a 10:1 payoff difference; positive future-bias does
    not. A sign asymmetry.
- **Greene, P. et al. (2022).** Bias towards the future. *Philosophy Compass* 17(8):
  e12859. doi:10.1111/phc3.12859. **FT** · `papers/greene-2022-bias-towards-the-future.txt`
  - Survey, including Latham et al. (2021, *Synthese*): past pain is discounted but not to
    zero.
- **Lee, R. et al. (2020).** Pain in the past and pleasure in the future. *Cognitive
  Science* 44(9): e12887. doi:10.1111/cogs.12887. **FT** ·
  `papers/lee-2020-pain-in-the-past-pleasure-in-the-future.txt`
  - Future bias appears from age 7 and is abandoned when the past quantity is larger.
- **Lee, R. et al. (2022).** Past-future preferences for hedonic goods and the utility of
  experiential memories. *Phil. Psychology* 35(8): 1181–1211.
  doi:10.1080/09515089.2022.2038784. **FT** ·
  `papers/lee-2022-past-future-preferences-utility-of-experiential-memories.txt`
  - Under amnesia most choose the Parfit option. When memories will return there is no
    clear preference; memory utility explains part of the bias.
- **Shardlow, J. et al. (2025).** Discounting past experience and the utility of memory.
  *Synthese* 205(4): 166. doi:10.1007/s11229-025-04992-x. **FT** ·
  `papers/shardlow-2025-discounting-past-experience-utility-of-memory.txt`
  - Measures the relative weights on primary versus recollective and anticipatory
    experience. Large individual differences: about a third prefer 10 never-remembered
    hours of pain to 1 remembered hour. The nearest thing to empirical kernel weights.
- **Caruso, E., Latham, A. & Miller, K. (2025).** Is future bias just a manifestation of
  the temporal value asymmetry? *Phil. Psychology* 38(8): 3441–3480.
  doi:10.1080/09515089.2024.2360673. **FT** ·
  `papers/caruso-2025-is-future-bias-a-manifestation-of-the-temporal-value-asymmetry.txt`
  - Finds no temporal value asymmetry. Cites Halabi et al. (2022, *J. Econ. Psych.*,
    unread) as a failed replication of Caruso et al. 2008.
- **Callender, C. (2021).** The normative standard for future discounting. *Australasian
  Phil. Review* 5(3): 227–253. **FT** (skim) ·
  `papers/callender-2021-normative-standard-for-future-discounting.txt`
- **Luper, S. (2026).** Death. *Stanford Encyclopedia of Philosophy*, §5.2 (Lucretius'
  symmetry argument). **FT** · `web/luper-2026-sep-death.md`

## Personal identity and connectedness (`selves.md`, Identity)

- **Parfit, D. (1984).** *Reasons and Persons*, chs. 10–15. OUP. **2ND** (Bartels & Rips
  2010; Lay 2019; Dufner 2025)
  - Connectedness is "the holding of particular direct psychological connections";
    continuity is "overlapping chains of strong connectedness" (pp. 205–6, via Bartels &
    Rips p. 50). Strong connectedness is a threshold: at least half the direct connections
    that hold over a day in nearly every actual life (p. 206, via Lay p. 127).
    Connectedness "admits of degree"; continuity, as the SEP reads it, is all-or-nothing.
  - Discounting by connectedness, not time: "This is a discount rate, not with respect to
    time itself, but with respect to [connectedness]" (pp. 313–14, quoted by Bartels &
    Rips p. 67, their bracket).
- **Bartels, D. & Rips, L. (2010).** Psychological connectedness and intertemporal choice.
  *JEP: General* 139(1): 49–69. doi:10.1037/a0018062. **FT** ·
  `papers/bartels-2010-psychological-connectedness-and-intertemporal-choice.txt`
  - Five studies: greater rated connectedness goes with less discounting. Discounting as a
    two-dimensional function `u(P, t)` of connectedness and time (p. 50). Reports that
    Frederick's (2003) direct test found "mainly null effects" (p. 51).
- **Bartels, D. & Urminsky, O. (2011).** On intertemporal selfishness. *J. Consumer Research*
  38(1): 182–198. doi:10.1086/658339. **WP** (author draft, Nov 2010; and the CogSci 2010
  precursor) · `papers/bartels-2010-on-intertemporal-selfishness-jcr-forthcoming-draft.txt`,
  `papers/bartels-2010-impatience-as-intertemporal-egoism-cogsci-proceedings.txt`
  - Connectedness as the share of defining features believed to persist, one scalar
    between two dates; "connectedness and stability of identity" used interchangeably
    (p. 8). Continuity is not separated out.
- **Frederick, S. (2003).** Time preference and personal identity. In Loewenstein, Read &
  Baumeister (eds.), *Time and Decision*, Russell Sage. **2ND** (Bartels & Rips) —
  negligible correlations between rated similarity of selves and discounting.
- **Lay, C. (2019).** Why Parfit's psychological criterion does not work as a personal
  identity theory (and how it could). *Argumenta* 5(1): 125–138. **FT** ·
  `papers/lay-2019-why-parfits-psychological-criterion-does-not-work-as-a-personal-identity-theory.txt`
  - Quotes Parfit's definitions of strong connectedness and continuity (p. 127).
- **Dufner, A. (2025).** Personal identity and ethics. *Stanford Encyclopedia of
  Philosophy*. **FT** · `web/dufner-2025-sep-personal-identity-and-ethics.md`
  - Continuity is "an overlapping chain of direct connections" and "must be understood as
    an all-or-nothing relation" (§2). Parfit "left open how much relative weight continuity
    and connectedness should have" (§5).
- **Olson, E. (2002; rev. 2023).** Personal identity. *SEP*. **FT** ·
  `web/olson-2002-sep-personal-identity.md`
- Not found: a formalization of continuity as path sums over connections. The nearest
  formal relatives are the chain-sum altruism models above (Sáez-Martí & Weibull; Galperti
  & Strulovici; Ray, Vellodi & Wang). Lead, unread (bot-checked): Miller (2026, *Synthese*),
  degree-theoretic conativism.

## Psychology

- Caruso, Gilbert & Wilson (2008), future events valued more than equivalent past ones:
  full entry under Calibration anchors.
- **Van Boven, L. & Ashworth, L. (2007).** Looking forward, looking back: anticipation is
  more evocative than retrospection. *JEP: General* 136(2): 289–300.
  doi:10.1037/0096-3445.136.2.289. **ABS** ·
  `papers/van-boven-2007-looking-forward-looking-back-anticipation-is-more-evocative-than-retrospection-abs.txt`
  - Five experiments. Anticipation is more emotionally intense, mediated by mental
    simulation. The expected-versus-remembered gap is slight.
- **Tversky, A. & Griffin, D. (1991).** Endowment and contrast in judgments of
  well-being. In Strack, Argyle & Schwarz (eds.), *Subjective Well-Being*, 101–118. **2ND**
  (Griffin & Gonzalez 2013, `papers/griffin-gonzalez-2013-endowment-contrast-model.*`)
  - Satisfaction = salience-weighted endowment from memory + current endowment +
    relatedness × contrast. Satisfaction and choice come apart.
- **Diener, E., Wirtz, D. & Oishi, S. (2001).** End effects of rated life quality: the
  James Dean effect. *Psychological Science* 12(2): 124–128. doi:10.1111/1467-9280.00321.
  **FT** (third-party copy of the published article) ·
  `papers/diener-2001-end-effects-of-rated-life-quality-james-dean-effect.txt`
  - Vignettes of a fictitious third person ("Jen") who dies suddenly, rated for
    desirability and for total happiness (9-point scales; p. 125).
  - Adding five mildly pleasant years lowers the rating of a very happy life (about 6.1
    to 5.4); five mildly unhappy years raise a depressed one (2.4 to 3.0). Age at death
    has no effect: duration neglect. Studies 1–2, N = 115 and 55.
  - Years added in the middle behave like none; at the end they lower the rating (Study 3,
    N = 34, flagged as small).
  - A choice follow-up weakened the effect (p. 127, no numbers). Evaluative evidence, so
    it bears on the evaluative reading, not on felt experience.
- **Fredrickson, B. & Kahneman, D. (1993).** Duration neglect in retrospective
  evaluations of affective episodes. *JPSP* 65(1): 45–55. doi:10.1037/0022-3514.65.1.45.
  **ABS**
- **Kahneman, D. et al. (1993).** When more pain is preferred to less. *Psychological
  Science* 4(6): 401–405. doi:10.1111/j.1467-9280.1993.tb00589.x. **ABS**
- **Ariely, D. (1998).** Combining experiences over time. *J. Behav. Decision Making*
  11(1): 19–45. **FT** (skim) · `papers/ariely-1998-combining-experiences-over-time.txt`
  - Retrospective pain is driven by the end and by the trend over the second half.
- **Ariely, D. & Carmon, Z. (2000).** Gestalt characteristics of experiences. *JBDM*
  13(2): 191–201. **ABS**
- **Hsee, C., Abelson, R. & Salovey, P. (1991).** The relative weighting of position and
  velocity in satisfaction. *Psychological Science* 2(4): 263–267.
  doi:10.1111/j.1467-9280.1991.tb00146.x. **ABS**
- **Lim, S., Yoon, S., Kwon, J., Kralik, J. & Jeong, J. (2020).** Retrospective evaluation of
  sequential events and the influence of preference-dependent working memory. *Frontiers
  in Computational Neuroscience* 14: 65. doi:10.3389/fncom.2020.00065. **FT** (CC BY) ·
  `papers/lim-2020-retrospective-evaluation-of-sequential-events-and-preference-dependent-working-memory.txt`
  - "Simple discounting" `y(t) = Σ r^{t−k} x_k` (eq. 22) is the average at `r = 1` and the
    end at `r = 0`; it cannot give peaks, whose weights would have to exceed recent ones.
    A preference-dependent forgetting rate `r(x_k)` (eq. 23) lets the peak count: core's
    "peak needs salience-weighted memory". They never derive duration neglect, and in
    their fits averaging beats peak-end.
- Fredrickson & Kahneman's evaluations are a *normalized* average of snapshots, flat in
  duration; core's fading sum is unnormalized and saturates. Abstract level, closed:
  Baumgartner, Sujan & Padgett (1997, *JMR*), results not solely recency; Schreiber &
  Kahneman (2000, *JEP: General*), judgment by prototype; Ariely & Zauberman (2000),
  segmentation; Cojuharenco & Ryvkin (2008, *J. Math. Psych.* 52(5)), peak-end and
  average rankings converge, worth a library copy.
- **Cheung, W.-Y. et al. (2020).** Anticipated nostalgia: looking forward to looking back.
  *Cognition and Emotion* 34(3): 511–525. doi:10.1080/02699931.2019.1649247. **FT** (not
  saved)
  - Anticipated nostalgia is mostly positive and tied to savouring. It predicts later
    nostalgia and wellbeing. Empirical footing for the recursive "anticipated
    remembering" term.
- **Batcho, K. & Shikh, S. (2016).** Anticipatory nostalgia. *Personality and Individual
  Differences* 98: 75–84. doi:10.1016/j.paid.2016.03.088. **2ND** (Batcho 2020)
  - "Missing the present before it's gone" goes with sadness and worry, so the recursive
    term can be negative.
- **Wixted, J. & Ebbesen, E. (1991).** On the form of forgetting. *Psychological Science*
  2(6): 409–415. doi:10.1111/j.1467-9280.1991.tb00175.x. **ABS**
  - Forgetting fits a power law better than an exponential. Heavy tails put `M` and
    `μ₁` at risk.
- **Bryant, F. & Veroff, J. (2007).** *Savoring*. Erlbaum. **2ND** (Bryant 2021,
  `papers/bryant-2021-progress-and-future-directions-on-savoring.txt`)
  - Three temporal modes: anticipation, the moment, reminiscence.

## Decision theory: anticipation, commitment, personal equilibrium

- **Kőszegi, B. (2010).** Utility from anticipation and personal equilibrium. *Economic
  Theory* 44(3): 415–444. doi:10.1007/s00199-009-0465-x. **FT** (§§1–6) ·
  `papers/koszegi-2010-utility-from-anticipation-and-personal-equilibrium.txt`
  - Personal equilibrium (Def. 1): each self maximizes, and beliefs match later
    behaviour. Self 2 takes the realized anticipation as given.
  - §3.2 and Example 2: selves with identical utility functions fail to carry out self
    1's favourite plan, and both lose. This is D3's mechanism; he credits Loewenstein
    1987 and Caplin & Leahy 2001.
  - §6.1: a one-player, multi-self psychological equilibrium. Fn. 22 links it to
    Hori–Kanaya and Bergstrom.
  - Example 1 (p. 423): both "expect z, choose z" and "expect z′, choose z′" are personal
    equilibria; the sole value of commitment there is changing one's own expectations
    (pp. 425–26). Thm. 2 (p. 431): with anticipation linear in beliefs, information
    neutrality iff disappointment neutrality. No recursion, memory or felt news on
    deviations.
- **Kőszegi, B. & Rabin, M. (2006).** A model of reference-dependent preferences. *QJE*
  121(4): 1133–1165. doi:10.1162/qjec.121.4.1133. **FT** (skim) ·
  `papers/koszegi-2006-a-model-of-reference-dependent-preferences.txt`
  - Personal equilibrium (Def. 1) and preferred personal equilibrium (Def. 2).
- **Kőszegi, B. & Rabin, M. (2007).** Reference-dependent risk attitudes. *AER* 97(4):
  1047–1073. doi:10.1257/aer.97.4.1047. **FT** (skim) ·
  `papers/koszegi-2007-reference-dependent-risk-attitudes.txt`
  - UPE and PPE (Defs. 1–2): the person does not internalize the choice's effect on
    expectations.
  - CPE (Def. 3) is for choices committed long before outcomes, so it is a matter of
    commitment timing.
- **Yudkowsky, E. & Soares, N. (2017).** Functional decision theory: a new theory of
  instrumental rationality. arXiv:1710.05060. **FT** ·
  `papers/yudkowsky-2017-functional-decision-theory.txt`
  - Subjunctive dependence means intervening on the decision function, not the token
    (§3).
  - Transparent Newcomb is equivalent to Parfit's hitchhiker: FDT pays and one-boxes
    (§4). The observed input is handled by choosing the intervention node (§6).
  - The claim that information is never negatively valued is instrumental.
- **Geanakoplos, J., Pearce, D. & Stacchetti, E. (1989).** Psychological games and
  sequential rationality. *GEB* 1(1): 60–79. doi:10.1016/0899-8256(89)90005-5.
  **ABS+** (scan, pp. 60–62) · `papers/geanakoplos-1989-psychological-games-and-sequential-rationality.pdf`
  - Payoffs depend on beliefs, and equilibrium beliefs are correct. Backward induction
    fails in general.
- **Geanakoplos, J. (1996).** The hangman's paradox and Newcomb's paradox as
  psychological games. Cowles DP 1128. **FT** ·
  `papers/geanakoplos-1996-hangmans-paradox-and-newcombs-paradox-as-psychological-games.txt`
  - In Newcomb, psychological Nash holds the predictor's belief fixed, so it two-boxes.
    The hanging-paradox unraveling is a cousin of D3's dread unraveling.
- **Battigalli, P. & Dufwenberg, M. (2009).** Dynamic psychological games. *JET* 144(1):
  1–35. doi:10.1016/j.jet.2008.01.004. **FT** (skim) ·
  `papers/battigalli-2009-dynamic-psychological-games.txt`
  - With own-plan dependence, the one-shot-deviation principle fails. Subsumes Caplin &
    Leahy and Kőszegi–Rabin.
- **Bernheim, B. D. & Thomadsen, R. (2005).** Memory and anticipation. *Economic Journal*
  115(503): 271–304. doi:10.1111/j.1468-0297.2005.00989.x. **WP** (author draft, July 2004,
  via Wayback of Bernheim's Stanford page) ·
  `papers/bernheim-2004-memory-and-anticipation-author-draft-july2004.txt`
  - Model (draft pp. 4–5): choose at 0, feel anticipation `V = E[U | I_1]` at 1, receive
    `U` at 2; period-0 preferences `V + δU`. One layer, no recursion; memory is only
    informational (Piccione–Rubinstein consistency). With perfect recall anticipation
    drops out of choice; forgetting breaks iterated expectations (p. 5).
  - Newcomb (§4.1, Thm. 1, p. 10): the chooser forgets `δ` but recalls the action (p. 9), so
    the action later signals the prediction. One-boxing for any `δ < (a−b)/b = 999`;
    perfect memory leaves only two-boxing; an all-two-box equilibrium always exists.
  - The felt anticipation comes *after* the choice and depends on it causally, through
    self-inference: the prediction is "a fait accompli" (p. 8). D1's structure, an
    already-felt anticipation that depends on a prediction of the later procedure, is not
    there. Partial prior art for D1; for its third bullet, here memory is what creates the
    dependence.
  - Anticipatory emotions plus imperfect memory make seemingly dominated strategies
    rational. Gives a resolution of Newcomb needing only a small weight on anticipation,
    and near-certain cooperation in the Prisoner's Dilemma (Thm. 2, a forgotten common
    signal; the authors are "somewhat skeptical" about lab fit, p. 19).
- **Bodner, R. & Prelec, D. (2003).** Self-signaling and diagnostic utility in everyday
  decision making. In Brocas & Carrillo (eds.), *The Psychology of Economic Decisions*,
  vol. 1. **FT** · `papers/bodner-2003-self-signaling-and-diagnostic-utility.txt`
  - EDT-flavoured diagnostic utility. Discusses Newcomb experiments and naive versus
    sophisticated selves. Diagnostic utility is intrinsic, a hedonic value of self-image
    (Remark 2 separates it from instrumental self-signaling).
- **O'Donoghue, T. & Rabin, M. (1999).** Doing it now or later. *AER* 89(1): 103–124.
  doi:10.1257/aer.89.1.103. **ABS**
  - Present bias procrastinates immediate costs and preproperates immediate rewards.
    Sophistication worsens preproperation.
- **Strotz, R. (1956).** Myopia and inconsistency in dynamic utility maximization. *RES*
  23(3): 165–180. **Pollak, R. (1968)** *RES* 35(2): 201–208. **Peleg, B. & Yaari, M.
  (1973)** *RES* 40(3): 391–401. **2ND** (Frederick et al. 2002)
  - Consistent planning among selves; the existence of consistent plans.
- **McClennen, E. (1990).** *Rationality and Dynamic Choice*. CUP. **2ND** (SEP "Decision
  Theory" §6.1)
  - Resolute choice.
- **Kreps, D. & Porteus, E. (1978).** Temporal resolution of uncertainty and dynamic
  choice theory. *Econometrica* 46(1): 185–200. **2ND** (Golman et al. 2017; Kőszegi
  2010)
  - Preferences over when uncertainty resolves.
- **Golman, R., Hagmann, D. & Loewenstein, G. (2017).** Information avoidance. *JEL* 55(1):
  96–135. doi:10.1257/jel.20151245. **FT** (skim) · `papers/golman-2017-information-avoidance.txt`
  - Anticipatory utility licenses avoiding free, useful information.

## Timing of pleasures and pains

- **Shu, S. & Gneezy, A. (2010).** Procrastination of enjoyable experiences. *J. Marketing
  Research* 47(5): 933–944. doi:10.1509/jmkr.47.5.933. **FT** ·
  `papers/shu-2010-procrastination-of-enjoyable-experiences.txt`
  - Landmarks and gift cards go unused when the window is long. Their mechanism is
    effort-cost discounting plus overpredicted free time, and deadlines cure it.
    Distinct from Loewenstein's savoring.
- **Berns, G. et al. (2006).** Neurobiological substrates of dread. *Science* 312(5774):
  754–758. doi:10.1126/science.1123721. **FT** (PMC) · `papers/berns-2006-neurobiological-substrates-of-dread.txt`
  - n = 32; most hurry shocks, and 9 "extreme dreaders" accept more voltage to avoid
    waiting.
- **Kivetz, R. & Keinan, A. (2006).** Repenting hyperopia. *J. Consumer Research* 33(2):
  273–282. doi:10.1086/506308. **WP** · `papers/keinan-2006-repenting-hyperopia-wp.txt`
  - Regret over virtuous choices grows with distance. The mechanism is regret, not
    anticipation.
- **Kivetz, R. & Simonson, I. (2002).** Self-control for the righteous. *JCR* 29(2):
  199–217. doi:10.1086/341571. **ABS**
  - Consumers precommit to indulgence.
- **Hardisty, D. & Weber, E. (2020).** *J. Consumer Psychology* 30(4): 598–613. **ABS**
  (via the literature agent; title to confirm)
  - Waiting is itself disliked, so net savoring is weak.
- **Dawson, C. & Johnson, S. (2026).** Asymmetric anticipatory emotions. *Cognitive
  Science* 50(1): e70160. **FT** · `papers/dawson-2026-asymmetric-anticipatory-emotions.txt`
  - Dread outweighs savoring in survey estimates.

## Value of information and beliefs as welfare (D5, D7; core N1–N3)

### Economics

Brunnermeier & Parker 2005 and Caplin & Leahy 2001 are under anticipatory utility above.

- **Epstein, L. (2008).** Living with risk. *RES* 75(4): 1121–1141.
  doi:10.1111/j.1467-937X.2008.00504.x. **FT** (abstract and intro) ·
  `papers/epstein-2008-living-with-risk.txt`
  - Expected-utility agents are indifferent to when risk resolves (p. 1121): D5's "truth
    is free in expectation" in one line. His axioms allow seeking information when good
    news is likely and avoiding it when bad is likely. Anticipatory feelings imply a
    demand for commitment (p. 1122).
- **Eliaz, K. & Spiegler, R. (2006).** Can anticipatory feelings explain anomalous choices
  of information sources? *GEB* 56(1): 87–104. doi:10.1016/j.geb.2005.06.004. **FT** ·
  `papers/eliaz-2006-anticipatory-feelings-anomalous-information-sources.txt`
  - Prop. 1 (p. 96): `u(z)` and `u(z) − Σcᵢzᵢ` give the same information choices, using
    only iterated expectations. Information choices cannot reveal which beliefs are good.
  - Props. 2–3 (pp. 98–99): Bayesian belief-utility cannot make information attitudes
    reverse with the prior (seek when good news is likely, avoid when bad is).
  - Remark 1 (p. 100): two states, concave `u` gives information aversion, convex gives
    seeking; "not an original result".
  - Escapes: non-expected utility; prior-dependent utility, which they criticise for an
    infinite regress and lost identifiability (p. 102); non-Bayesian updating, which they
    favour.
- **Kőszegi, B. & Rabin, M. (2009).** Reference-dependent consumption plans. *AER* 99(3):
  909–936. doi:10.1257/aer.99.3.909. **FT** (§§I–II closely) ·
  `papers/koszegi-2009-reference-dependent-consumption-plans.txt`
  - Consumption utility plus loss-averse gain-loss over changes in rational beliefs, with
    prospective weight `γ` (p. 910). Information tastes are derived, not assumed.
  - Fully revealing signals: early information preferred iff `γ < 1`, indifference iff
    `γ = 1` (pp. 917–19, Prop. 2).
  - Clumping (Props. 1, 3, 4): collapsing signals helps, a weak early signal hurts;
    learning everything at once is weakly best (p. 919). Avoidance is of *partial*
    information. Props. 1–4 are in §II and proved for binary outcomes with linear `μ`.
  - Fn. 12 (p. 915): some results hold only if discounting is not too fast relative to
    `γ`'s decay, the germ of N2's `k_n(s−r) w(r)`. Fn. 23: at `λ = 1` the model is
    observationally β–δ with `β = (1+γη)/(1+η)`, `δ = 1`, a cousin of P3.
  - §IV, eq. 5 (p. 924): raising consumption above the plan is a contemporaneous gain and a
    prospective loss, the news of one's own deviation. Def. 1: the preferred personal
    equilibrium is the best credible plan, by backward recursion. Prop. 5: it is the equal
    split iff `γ ≥ 1/λ`, the plan its own commitment device; below, consumption tilts to
    the present. "This beliefs-based time inconsistency arises even though preferences in
    our model are time consistent" (p. 925). The canonical model's choice side with echoes
    removed (decision.md, setup). `γλ` is a different product from N4's `λκ`.
- **Pagel, M. (2018).** A news-utility theory for inattention and delegation in portfolio
  choice. *Econometrica* 86(2): 491–522. doi:10.3982/ECTA14417. **WP** (intro, §§3.1,
  4.1–4.2) · `papers/pagel-2018-news-utility-theory-inattention-delegation-portfolio-choice-wp.txt`
  - Loss-averse news utility under rational expectations makes looking a first-order
    loss: inattention, delegation, and an ostrich effect after adverse signals (pp. 3–6).
  - News about `t+τ` is weighted `γβ^τ` (eqs. 9–10, p. 15): the canonical model's
    `k_n(j) = γ n ν^j` with `ν = β`. Explores `γ = 0.2` against `0.8` (fn. 26, Fig. 2).
- **Andries, M. & Haddad, V. (2020).** Information aversion. *JPE* 128(5): 1901–1939.
  **WP** (NBER w23958, 2017) · `papers/andries-2017-information-aversion-nber-w23958.txt`
  - Gul disappointment aversion applied recursively, inside an Epstein–Zin recursion
    (Def. 1, eq. 2): "receiving fragmented information multiplies the scope for
    disappointment" (p. 2).
  - Prop. 1 (p. 7): prefers information revealed at a single date, and is indifferent
    about which date. The recursive form of N2's clumping and D7's batching.
  - Alerts after sharp drops raise welfare (Prop. 5); delegation cannot always shield the
    agent, since observed consumption reveals wealth (pp. 23–24): D7's coarse affect
    filtration, formally.
  - Ex-ante and time-consistent; disappointment is against the continuation's own
    certainty equivalent, a negative feedback with a unique solution. Felt news (N4) is
    against the prior forecast.
- **Dillenberger, D. (2010).** Preferences for one-shot resolution of uncertainty and
  Allais-type behavior. *Econometrica* 78(6): 1973–2004. **WP** (PIER 09-033) ·
  `papers/dillenberger-2009-preferences-for-one-shot-resolution-of-uncertainty-and-allais-type-behavior-penn-wp09-033.txt`
  - Recursive certainty-equivalent evaluation (after Segal 1990): a preference for
    one-shot resolution is equivalent to negative certainty independence, Allais-type
    behaviour, and "can be interpreted as dynamic disappointment aversion" (p. 23).
    Partial information is disliked; finer staging drives value toward the worst prize
    (Prop. 6). No felt flow.
- **Palacios-Huerta, I. (1999).** The aversion to the sequential resolution of
  uncertainty. *J. Risk & Uncertainty* 18(3): 249–269. **2ND** (Artstein-Avidan &
  Dillenberger) — Gul folded back through the tree prefers resolution all at once, by
  example.
- Kreps–Porteus, the structure behind D5's recursion: a concave aggregator over
  continuation values prefers late resolution (Skiadas 1998, Prop. 1, below; Epstein 2008,
  eq. 5.2). Caplin & Leahy (2001, fn. 12, p. 68) note that Kreps–Porteus leaves the
  assignment of utility across periods open.
- **Kőszegi, B. (2003).** Health anxiety and patient behavior. *J. Health Economics* 22(6):
  1073–1084. doi:10.1016/j.jhealeco.2003.06.002. **FT** ·
  `papers/koszegi-2003-health-anxiety-and-patient-behavior.txt`
  - One-shot anticipatory utility `u(E[·|information])`; concave `u` is information-averse
    (p. 1076). No recursion.
- **Caplin, A. & Eliaz, K. (2003).** AIDS policy and psychology: a mechanism-design
  approach. *RAND J. Economics* 34(4): 631–646. **FT** (copy on a co-author's page) ·
  `papers/caplin-2003-aids-policy-and-psychology-a-mechanism-design-approach.txt`
  - A convex anxiety cost of beliefs, "no more than a special case" of Kreps–Porteus
    (pp. 635–36), giving a preference for late resolution.
- **Schweizer, N. & Szech, N. (2018).** Optimal revelation of life-changing information.
  *Management Science* 64(11). **WP** (KIT, 2017) ·
  `papers/schweizer-2017-optimal-revelation-of-life-changing-information-kit-wp.txt`
  - Concave anticipatory utility of beliefs; information is "a gamble over anticipated
    utility outcomes" (p. 3). One-shot.
- **Bénabou, R. & Tirole, J. (2002).** Self-confidence and personal motivation. *QJE*
  117(3): 871–915. doi:10.1162/003355302760193913. **WP** (2001; intro, §§I, IV, V.B) ·
  `papers/benabou-2002-self-confidence-and-personal-motivation-wp.txt`
  - Three motives for confidence: hedonic, signalling, motivation; Bayesian agents with
    endogenous memory.
  - §IV: self-deception spoils good news with self-doubt; with free repression, partial
    recall never beats full recall.
  - §V.B: concave hedonic utility of self-image gives information avoidance, convex gives
    seeking.
- **Bénabou, R. & Tirole, J. (2004).** Willpower and personal rules. *JPE* 112(4):
  848–886. doi:10.1086/421167. **WP** (2003; §§1–3) ·
  `papers/benabou-2004-willpower-and-personal-rules-wp.txt`
  - Self-reputation over willpower with imperfect recall: lapses are precedents and
    evidence about type (pp. 2–3, 10–11). Confidence raises self-control and ex-ante
    welfare (Prop. 1); over-rigid rules produce compulsion. The payoff is instrumental.
- **Bénabou, R. & Tirole, J. (2016).** Mindful economics: the production, consumption, and
  value of beliefs. *JEP* 30(3): 141–164. doi:10.1257/jep.30.3.141. **ABS** (full text
  blocked)
- **Bénabou, R. (2015).** The economics of motivated beliefs. *Revue d'économie politique*
  125(5): 665–685. doi:10.3917/redp.255.0665. **FT** ·
  `papers/benabou-2015-the-economics-of-motivated-beliefs.txt`
  - Affective plus instrumental demand for beliefs; anticipatory flow `s·E[U₂]`
    (pp. 671–73). With distorted information, iterated expectations fail (fn. 8).
  - p. 677: for a near-Bayesian agent with anticipation linear in beliefs, the gain from
    censoring bad news and the loss from self-doubt cancel, leaving only costs. Fn. 16:
    linear is the benchmark; concave favours coarser posteriors, convex more dispersed;
    the shape is empirical.
  - Asymmetric updating and information avoidance as predictions (pp. 674–75), citing
    Möbius et al., Eil & Rao, Oster et al., Karlsson et al.

### Field and lab evidence

- **Oster, E., Shoulson, I. & Dorsey, E. R. (2013).** Optimal expectations and limited
  medical testing: evidence from Huntington disease. *AER* 103(2): 804–830.
  doi:10.1257/aer.103.2.804. **WP** (NBER w17629, 2011; intro, §§4–6) ·
  `papers/oster-2011-optimal-expectations-and-limited-medical-testing-nber-w17629.txt`
  - Under 10% of 1,001 at-risk people test; untested people report risk well below
    clinical risk and act like non-carriers. Model: Brunnermeier–Parker with linear
    anticipation; testing destroys the option to hold chosen beliefs (Prop. 3).
  - Corrigendum (*AER* 106(6): 1562–65, 2016; **ABS**): corrected risk series shows less
    over-optimism, concentrated at advanced symptoms. The AER sample may differ from the WP.
- **Karlsson, N., Loewenstein, G. & Seppi, D. (2009).** The ostrich effect: selective
  attention to information. *J. Risk and Uncertainty* 38(2): 95–115.
  doi:10.1007/s11166-009-9060-6. **FT** (OCR) ·
  `papers/karlsson-2009-the-ostrich-effect-selective-attention-to-information.txt`
  - Attend after good preliminary news, avoid after bad (Prop. 1, p. 101). Aggregate
    login data, Sweden and Vanguard: modest effects (pp. 104–08).
- **Sicherman, N., Loewenstein, G., Seppi, D. & Utkus, S. (2016).** Financial attention.
  *RFS* 29(4): 863–897. doi:10.1093/rfs/hhv073. **FT** · `papers/sicherman-2016-financial-attention.txt`
  - Individual-level: logins fall 9.5% after market declines; the trait is stable.
- **Gherzi, S., Egan, D., Stewart, N., Haisley, E. & Ayton, P. (2014).** The meerkat
  effect: personality and market returns affect investors' portfolio monitoring
  behaviour. *JEBO* 107: 512–526. doi:10.1016/j.jebo.2014.07.013. **WP** (accepted
  manuscript) · `papers/gherzi-2014-the-meerkat-effect-portfolio-monitoring-am.txt`
  - 617 clients: monitoring rises after both up and down days. No ostrich effect.
- **Falk, A. & Zimmermann, F. (2016).** Beliefs and utility: experimental evidence on
  preferences for information. IZA DP 10172. **WP** ·
  `papers/falk-2016-beliefs-and-utility-preferences-for-information-iza-dp10172.txt`
  - Real electric shocks, N = 376. 76% prefer sooner information, distraction shifts
    people later, ~90% prefer clumped to piecemeal, priors don't matter. Table 2 sets out
    each model's predictions; Brunnermeier–Parker's later-information prediction fails.
- **Eil, D. & Rao, J. (2011).** The good news-bad news effect: asymmetric processing of
  objective information about yourself. *AEJ: Micro* 3(2): 114–138.
  doi:10.1257/mic.3.2.114. **ABS** (full text blocked)
  - Near-Bayesian on good news; on bad news, signal strength ignored and new information
    avoided.
- **Sharot, T., Korn, C. & Dolan, R. (2011).** How unrealistic optimism is maintained in
  the face of reality. *Nature Neuroscience* 14(11): 1475–1479. doi:10.1038/nn.2949.
  **FT** (behavioural results) ·
  `papers/sharot-2011-how-unrealistic-optimism-is-maintained-in-the-face-of-reality.txt`
  - Larger updates to desirable than to undesirable information about life events.
  - Contested, via the literature agent (**ABS**): Shah et al. 2016 (*Cognitive
    Psychology* 90) and Harris & Hahn 2011 (*Psych. Review* 118) argue statistical
    artifact; Garrett & Sharot 2017 reply. Möbius et al. 2022 (*Mgmt Sci* 68) find
    asymmetry plus conservatism; Coutts 2019 and Barron 2021 (*Exp. Econ.*) find no
    valence asymmetry beyond conservatism.

### Disappointment, bracing and evaluation periods (core N1–N3)

- **Bell, D. (1985).** Disappointment in decision making under uncertainty. *Operations
  Research* 33(1): 1–27. doi:10.1287/opre.33.1.1. **ABS** (form via Abdellaoui &
  Bleichrodt 2007; Mellers et al. 1997) ·
  `papers/bell-1985-disappointment-in-decision-making-under-uncertainty-abs.txt`
  - Linear, kinked disappointment/elation term against the lottery's mean; disappointment
    aversion (`d > e`) is allowed, not forced.
- **Loomes, G. & Sugden, R. (1986).** Disappointment and dynamic consistency in choice
  under uncertainty. *RES* 53(2): 271–282. doi:10.2307/2297651. **ABS** (form via
  Abdellaoui & Bleichrodt 2007; Chauveau & Nalpas WP) ·
  `papers/loomes-1986-disappointment-and-dynamic-consistency-in-choice-under-uncertainty-abs.txt`
  - `u(w) + D(u(w) − E[u])`, `D` odd-symmetric: no built-in asymmetry.
- **Gul, F. (1991).** A theory of disappointment aversion. *Econometrica* 59(3): 667–686.
  doi:10.2307/2938223. **ABS** (form via Abdellaoui & Bleichrodt 2007) ·
  `papers/gul-1991-a-theory-of-disappointment-aversion-abs.txt`
  - Outcomes below the certainty equivalent reweighted by `β`; asymmetry is a parameter.
    A choice theory with a static reference point.
- **Abdellaoui, M. & Bleichrodt, H. (2007).** Eliciting Gul's theory of disappointment
  aversion by the tradeoff method. *J. Economic Psychology* 28(6): 631–645.
  doi:10.1016/j.joep.2007.07.009. **FT** ·
  `papers/abdellaoui-2007-eliciting-guls-theory-of-disappointment-aversion-by-the-tradeoff-method.txt`
  - The secondary source for the Bell, Loomes–Sugden and Gul forms above (pp. 634, 642–43).
- **Mellers, B., Schwartz, A., Ho, K. & Ritov, I. (1997).** Decision affect theory:
  emotional reactions to the outcomes of risky options. *Psychological Science* 8(6):
  423–429. doi:10.1111/j.1467-9280.1997.tb00455.x. **FT** (poor OCR) ·
  `papers/mellers-1997-decision-affect-theory-emotional-reactions-to-outcomes-of-risky-options.txt`
  - Felt reactions to outcomes: surprise amplifies both elation and disappointment
    (p. 425); disappointment exceeds elation in the fits (pp. 427–28).
- **Gollier, C. & Muermann, A. (2010).** Optimal choice and beliefs with ex ante savoring
  and ex post disappointment. *Management Science* 56(8): 1272–1284.
  doi:10.1287/mnsc.1100.1185. **WP** (CFS 2006/28) ·
  `papers/gollier-2006-optimal-choice-and-beliefs-with-ex-ante-savoring-and-ex-post-disappointment-cfs-wp.txt`
  - Anticipated payoff chosen to trade savoring against disappointment; Prop. 1: it rises
    with the intensity of anticipatory feelings. The formal precedent for core N3.
- **van Dijk, W., Zeelenberg, M. & van der Pligt, J. (2003).** Blessed are those who expect
  nothing: lowering expectations as a way of avoiding disappointment. *J. Economic
  Psychology* 24(4): 505–516. doi:10.1016/S0167-4870(02)00211-8. **FT** ·
  `papers/van-dijk-2003-blessed-are-those-who-expect-nothing.txt`
  - Estimates fall only when feedback is self-relevant and imminent (n = 80, p. 512).
    States the timing logic, savor when remote and brace when imminent (p. 508, citing an
    unpublished Loewenstein & Linville 1986). Felt disappointment not measured.
- **Shepperd, J., Ouellette, J. & Fernandez, J. (1996).** Abandoning unrealistic optimism:
  performance estimates and the temporal proximity of self-relevant feedback. *JPSP*
  70(4): 844–855. doi:10.1037/0022-3514.70.4.844. **FT** ·
  `papers/shepperd-1996-abandoning-unrealistic-optimism-performance-estimates-and-temporal-proximity-of-feedback.txt`
  - Estimates fall just before feedback with no new information (Study 2). Effects are
    small; few cite avoiding disappointment as the reason.
- **Sweeny, K., Carroll, P. & Shepperd, J. (2006).** Is optimism always best? *Current
  Directions in Psychological Science* 15(6): 302–306. doi:10.1111/j.1467-8721.2006.00457.x.
  **FT** · `papers/sweeny-2006-is-optimism-always-best-future-outlooks-and-preparedness.txt`
  - Review: optimism yields as feedback nears, as stakes rise, and as bad outcomes become
    easy to imagine; the affective payoffs are flagged as needing confirmation.
- **Shepperd, J. & McNulty, J. (2002).** The affective consequences of expected and
  unexpected outcomes. *Psychological Science* 13(1): 85–88. doi:10.1111/1467-9280.00416.
  **FT** · `papers/shepperd-2002-the-affective-consequences-of-expected-and-unexpected-outcomes.txt`
  - Expectations cushion bad news and amplify good, symmetrically, but expectations were
    supplied as base rates.
- **Golub, S., Gilbert, D. & Wilson, T. (2009).** Anticipating one's troubles: the costs
  and benefits of negative expectations. *Emotion* 9(2): 277–281. doi:10.1037/a0014716.
  **FT** · `papers/golub-2009-anticipating-ones-troubles-the-costs-and-benefits-of-negative-expectations.txt`
  - Negative expectations cost dread beforehand and gave no measurable cushion afterwards;
    expectation effects gone within minutes. Table 1 is the savoring/dread versus
    cushion/amplification matrix.
- Also saved at abstract level: Shepperd, Findley-Klein, Kwavnick, Walker & Perez (2000),
  bracing for loss, *JPSP* 78(4) (**FT**, intro and discussion); Taylor & Shepperd (1998),
  *PSPB* 24(9); Marshall & Brown (2006), *Cognition & Emotion* 20(1), little benefit of low
  expectancies; Sweeny & Shepperd (2010), *Emotion* 10(5); Norem & Cantor (1986), *JPSP*
  51(6), defensive pessimism as anxiety management (all **ABS**).
- **Benartzi, S. & Thaler, R. (1995).** Myopic loss aversion and the equity premium
  puzzle. *QJE* 110(1): 73–92. doi:10.2307/2118511. **WP** (NBER w4369) ·
  `papers/benartzi-1993-myopic-loss-aversion-and-the-equity-premium-puzzle-nber-w4369.txt`
  - Loss-averse investors take more risk when they evaluate rarely; the residual premium
    is "the price of excessive vigilance" (WP p. 16). A valuation model, not felt affect.
- **Gneezy, U. & Potters, J. (1997).** An experiment on risk taking and evaluation periods.
  *QJE* 112(2): 631–645. doi:10.1162/003355397555217. **FT** ·
  `papers/gneezy-1997-an-experiment-on-risk-taking-and-evaluation-periods.txt`
  - Less frequent feedback raises betting (67% vs 51%), already in round 1, before any loss
    is experienced (p. 639); the low-frequency arm also changes information.

### LessWrong on feeling versus acting (D7; all `web/`, **FT**)

- **Soares, N. (2015).** Detach the grim-o-meter. *Minding Our Way* / LessWrong.
  - Stop calibrating the grim-o-meter against the state of the world; it is built for
    local occasions. Resolve stays.
- **Soares, N. (2015).** Simply locate yourself.
  - Treat bad news as information about where you ended up, not as the world going wrong.
    The nearest informal precedent for updateless affect.
- **Mayer (2023).** Being at peace with doom. Silences the emotional components while
  reasoning stays aimed at preventing doom; not self-deception.
- **TurnTrout (2022).** Emotionally confronting a probably-doomed world. Feelings are not
  beliefs.
- **Sabien, D. (2023).** A way to be okay. The emotional victory condition is best effort,
  not outcome.
- Noted, not saved: Ruby, "A quick guide to confronting doom" (coping must keep you in
  touch with reality); Yudkowsky, "MIRI announces new Death With Dignity strategy" (2022);
  Soares, "Dark, not colorless".

### Philosophy and decision theory

- **Good, I. J. (1967).** On the principle of total evidence. *BJPS* 17(4): 319–321.
  **2ND** (Skyrms 1990; Ahmed & Salow 2019; closed)
  - Free evidence has nonnegative expected value for a Bayesian expected-utility maximizer.
- **Skyrms, B. (1990).** The value of knowledge. *Minnesota Studies in the Philosophy of
  Science* 14: 245–266. **FT** · `papers/skyrms-1990-the-value-of-knowledge.txt`
  - Good's tacit assumptions (pp. 246–247). Information is "really free" only if utility
    is independent of the experimental result (p. 256). The theorem fails for Jeffrey
    EDT (p. 255).
- **Kadane, J., Schervish, M. & Seidenfeld, T. (2008).** Is ignorance bliss? *J.
  Philosophy* 105(1): 5–36. **FT** · `papers/kadane-schervish-seidenfeld-2008-is-ignorance-bliss.txt`
  - Utility can depend on the knowledge base, anticipated experiences included (§II).
  - §III.2: information is *decision-theoretically ignorable* if every rule available
    without it stays available, and *cost-free* if ignoring it also leaves utility
    unchanged (eq. 13). The taxi driver who offers to reveal the mystery's ending (Ex. 12)
    and Huntington's testing (Ex. 16) are ignorable but not cost-free.
  - The nearest prior art for D5's instrumental/intrinsic split.
- **Ahmed, A. & Salow, B. (2019).** Don't look now. *BJPS* 70(2): 327–350. **WP** (author
  draft; pages differ) · `papers/ahmed-salow-2019-dont-look-now.txt`
  - Failures of Good's theorem from non-partitional observation and from independence
    violations (fn. 21 lists disappointment and anticipated-utility theories). Neither is
    belief-dependent welfare.
- **Buchak, L. (2010).** Instrumental rationality, epistemic rationality, and
  evidence-gathering. *Phil. Perspectives* 24: 85–120. **ABS** ·
  `papers/buchak-2010-instrumental-rationality-epistemic-rationality-and-evidence-gathering.txt`
  - Risk-weighted agents can refuse free evidence. Sets aside desires to be in particular
    epistemic states as a separate case.
- **Bostrom, N. (2011).** Information hazards: a typology of potential harms from
  knowledge. *Review of Contemporary Philosophy* 10: 44–79. **FT** (author PDF; manuscript
  pages) · `papers/bostrom-2011-information-hazards.txt`
  - *Psychological reaction hazard*: information lowers well-being through sadness or
    disappointment (p. 19). *Belief-constituted value hazard*: a component of well-being
    depends constitutively on epistemic states (pp. 19–21).

### LessWrong and the Alignment Forum, updatelessness and information (all `web/`, **FT**)

- **Diffractor (2018).** VOI is only nonnegative when information is uncorrelated with
  future action.
  - The ignore-the-observation proof fails when the probability of an observation depends
    on the policy (XOR blackmail, Parfit's hitchhiker, transparent Newcomb). cousin_it's
    reply: UDT's value of information stays nonnegative.
- **Soto, M. (2024).** Updatelessness doesn't solve most problems.
  - A trade-off between learning and strategicness: reason not to learn a logical fact
    before a logical counterfactual mugging. Soto disavows "scared of information"; the
    prior must decide ex ante what actions may depend on. Comments by Yudkowsky
    (updatelessness keeps information from harming you) are saved with it.
- **Demski, A. (2019).** Conceptual problems with UDT and policy selection.
  - UDT wants to decide how to use information before looking; thinking longer is a kind
    of updating.
- **Kokotajlo, D. (2019).** The commitment races problem.
  - Agents gain collectively from learning before committing, and individually from
    committing early.
- **Garrabrant, S. (2016).** Updatelessness and son of X. Logical updatelessness.
- All hazards here run through action or bargaining position. None is felt.

### LessWrong on truth, comfort and anticipation (all `web/`, **FT**)

- **LessWrong wiki.** Litany of Gendlin; Litany of Tarski. Gendlin's is credited to Eugene
  Gendlin (book and page unverified); Tarski's is Yudkowsky's naming (2007).
- **Raemon (2011).** Issues with the Litany of Gendlin.
  - The emotional reaction to a truth is part of reality, so some truths cost something
    to learn. Informal; comment thread saved.
- **HonoreDB, jimrandomh et al. (2011).** Utility-of-belief thread under "Making beliefs
  pay rent".
  - jimrandomh: concave utility of belief (`√p`) makes learning worth −0.244 and Joe
    "plugs his ears"; convex (`p²`) makes it worth +2/9. The closest LessWrong precedent
    for D5's Jensen point.
  - HonoreDB: a reflectively consistent UDT agent's utility of belief must be linear in
    `p`. Contested in the thread; the author later called the proof holey.
- **Yudkowsky, E. (2007).** Doublethink (choosing to be biased). The main
  anti-self-deception norm: you cannot choose bias knowingly.
- **Yudkowsky, E. (2007).** Not for the sake of happiness (alone). Rejects reducing value
  to happiness: the counter-position the hedonic reading must answer.
- **Yudkowsky, E. (2009).** Justified expectation of pleasant surprises.
  - A pleasant surprise beats being told in advance; vague hope has value. A hunch, no
    data. The nearest LessWrong statement that anticipation itself matters.
- **Dai, W. (2009).** Anticipation vs. faith: at what cost rationality?
  - Anticipation's experiences valued for their own sake; UDT works without anticipation.
    Mixes hedonic and Armstrong-style subjective anticipation.
- **Roko (2010).** Ugh fields. Hedonic avoidance of thinking about a problem, as a costly
  conditioned pathology.
- **Sotala, K. (2011).** Strategic ignorance and plausible deniability. Reputational, not
  hedonic.
- Not found on LessWrong or the Alignment Forum: a treatment of information as
  intrinsically costly through felt anticipation in a decision-theoretic setting, or of
  memory as utility in one. The literature agent's search relied on web search, so
  coverage is not exhaustive.

### LessWrong, EA Forum and blogs: the second scan

Searched 2026-10-14 (GreaterWrong and site searches); pages fetched as model summaries and
not saved, so read before quoting. Verdict: scattered informal precedents, no unified
welfare treatment. No post found mentioning Kőszegi–Rabin, Caplin–Leahy, Loewenstein's
anticipation work or psychological games; ACX and Overcoming Bias archives were not
searchable.

- **Yudkowsky, E. (2007).** Lotteries: a waste of hope. Hope as misallocated emotional
  energy; commenters, Hanson among them, defend its value. The best-known LessWrong
  treatment of anticipation as a good, and the natural foil.
- **Hanson, R. (2008).** The hope premium. *Overcoming Bias*. Seen only as a search
  summary (hope is priced); unverified.
- **Metus (2012).** Expected utility and utility after time. Experiencing against
  remembering self as an aggregation puzzle; comments cite peak-end. The nearest welfare
  framing of Kahneman's two selves on LessWrong.
- **lukeprog (2011).** Review of *Thinking, Fast and Slow*. Lists two selves, peak-end and
  duration neglect as under-discussed.
- **Galef, J. (2011).** Life extension versus replacement. In comments, Grognor argues
  memories have utility in themselves and DanielLC rejects it: the only memory-as-utility
  exchange found.
- **Zvi (2011).** How I lost 100 pounds using TDT. Wei Dai's comment: a hyperbolic
  discounter's successive selves play a prisoner's dilemma, so TDT applies. With
  **Crowley, P. (2009)**, Akrasia, hyperbolic discounting, and picoeconomics, and **Alexander,
  S. (2009)**, Applied picoeconomics (Ainslie's successive selves): the within-a-life
  Newcomb and PD framing, without felt anticipation (D1–D3).
- **twanvl (2011).** [LINK] Hyperbolic discounting is rational (Farmer & Geanakoplos:
  hyperbolic curves from uncertain rates). Present bias from structure is familiar, from
  felt echo not. With **Yudkowsky (2008)**, Against discount rates: no pure time preference
  (P5's flat interior).
- **McAuliffe, W. & Shriver, A. (2022).** Does the trajectory of pain matter? EA Forum
  (Rethink Priorities). Sequence and peak-end in welfare; anticipation treated as a
  confound. The nearest EA treatment of a life's shape.
- **Zvi (2023).** AI: practical advice for the worried. Dread of a bleak future spoils
  present fun: anticipation in present welfare, for the P(doom) example (D7).
- **Byrnes, S. (2023).** Valence series. Separates valence, a forward-looking,
  value-like signal, from hedonic tone; readers will ask which "felt anticipation" is. Also
  a terminology collision: "Making beliefs pay rent (in anticipated experiences)" uses
  anticipation epistemically.
- Missing outside LessWrong, flagged by the scan, unread: **Ainslie, G. (2001)**,
  *Breakdown of Will*; **Ainslie, G. (2003)**, Uncertainty as wealth (anticipation as
  consumption, premature satiation; possibly the nearest neighbour of D3's savoring trap).

## Recollection, recursive news and rumination (core N4 and the recollection sketch)

### Recursive gain-loss

- **Skiadas, C. (1998).** Recursive utility and preferences for information. *Economic
  Theory* 12(2): 293–312. doi:10.1007/s001990050222. **FT** ·
  `papers/skiadas-1998-recursive-utility-and-preferences-for-information.txt`
  - `V_t = f(c_t, E[V_t | F_{t−1}], E[V_{t+1} | F_t])`, decreasing in the prior expectation
    of `V_t` itself: disappointment over a utility index that contains it (pp. 303–304).
    Unique by monotonicity; no loss-aversion kink.
- **Routledge, B. & Zin, S. (2010).** Generalized disappointment aversion and asset
  prices. *J. Finance* 65(4): 1303–1332. doi:10.1111/j.1540-6261.2010.01571.x. **WP** (NBER
  w10107) · `papers/routledge-2003-generalized-disappointment-aversion-and-asset-prices-nber-w10107.txt`
  - The disappointment threshold sits on a recursive utility index (eq. 16); an ex-ante
    risk preference, not a felt flow.
- **Artstein-Avidan, S. & Dillenberger, D. (2015).** Dynamic disappointment aversion. **WP**
  · `papers/artstein-avidan-2015-dynamic-disappointment-aversion-wp.txt`
  - Gul applied at every node: splitting resolution into stages lowers value ("I prefer to
    wait and hear only the final result").

### Recollection and motivated memory

- **Mitchell, T., Thompson, L., Peterson, E. & Cronk, R. (1997).** Temporal adjustments in
  the evaluation of events: the "rosy view". *J. Experimental Social Psychology* 33(4):
  421–448. doi:10.1006/jesp.1997.1333. **ABS** ·
  `papers/mitchell-1997-temporal-adjustments-in-the-evaluation-of-events-the-rosy-view-abs.txt`
  - Three field studies (a Europe trip, Thanksgiving, a bike trip): expectations and later
    recollection both exceeded experience.
- **Walker, W. R., Vogl, R. & Thompson, C. (1997).** Autobiographical memory:
  unpleasantness fades faster than pleasantness over time. *Applied Cognitive Psychology*
  11(5): 399–413. **ABS** · `papers/walker-1997-autobiographical-memory-unpleasantness-fades-faster-than-pleasantness-abs.txt`
- **Walker, W. R., Skowronski, J. & Thompson, C. (2003).** Life is pleasant—and memory helps
  to keep it that way! *Review of General Psychology* 7(2): 203–210.
  doi:10.1037/1089-2680.7.2.203. **ABS** · `papers/walker-2003-life-is-pleasant-and-memory-helps-to-keep-it-that-way-abs.txt`
  - The fading affect bias; dysphoria disrupts it.
- **Sedikides, C. & Skowronski, J. (2020).** In human memory, good can be stronger than
  bad. *Current Directions* 29(1): 86–91. doi:10.1177/0963721419896363. **ABS** ·
  `papers/sedikides-2020-in-human-memory-good-can-be-stronger-than-bad-abs.txt`
- **Hoehne, S. & Zimprich, D. (2024).** Predicting the likelihood and amount of fading:
  fixed, flourishing, flexible affect. *Memory & Cognition* 52(4): 872–893.
  doi:10.3758/s13421-023-01507-2. **FT** ·
  `papers/hoehne-2024-predicting-the-likelihood-and-amount-of-fading-fixed-flourishing-flexible-affect.txt`
  - 1,748 memories: negative affect fades in 30% against 12% for positive; positive
    flourishes in 34% against 10%; valence flips negative-to-positive 13% against 4%.
- **Hoehne, S. & Zimprich, D. (2025).** Evidence for a fading affect bias in subjectively
  assessed affect changes. *Frontiers in Psychology* 16: 1608751.
  doi:10.3389/fpsyg.2025.1608751. **FT** ·
  `papers/hoehne-2025-evidence-for-a-fading-affect-bias-in-subjectively-assessed-affect-changes.txt`
  - 12,314 memories; the fading affect bias holds in directly reported change.
- **Walker, W. R., Yancu, C. & Skowronski, J. (2014).** Trait anxiety reduces affective
  fading for both positive and negative autobiographical memories. *Advances in Cognitive
  Psychology* 10(3): 81–89. doi:10.5709/acp-0159-0. **FT** ·
  `papers/walker-2014-trait-anxiety-reduces-affective-fading-for-both-positive-and-negative-autobiographical-memories.txt`
- **Marsh, C., Hammond, M. & Crawford, M. (2019).** Thinking about negative life events as
  a mediator between depression and fading affect bias. *PLoS ONE* 14(1): e0211147.
  doi:10.1371/journal.pone.0211147. **FT** ·
  `papers/marsh-2019-thinking-about-negative-life-events-mediator-depression-fading-affect-bias.txt`
  - More thinking about a negative memory means less fading; reminders preserve negative
    affect.
- **Devitt, A. & Schacter, D. (2018).** An optimistic outlook creates a rosy past.
  *Psychological Science* 29(6): 936–946. doi:10.1177/0956797617753936. **FT** (author
  manuscript) · `papers/devitt-2018-an-optimistic-outlook-creates-a-rosy-past.txt`
  - Positive simulation beforehand makes an event remembered more favourably.
- **Rasmussen, A. & Berntsen, D. (2013).** The reality of the past versus the ideality of
  the future. *Memory & Cognition* 41(2): 187–200. doi:10.3758/s13421-012-0260-y. **ABS** ·
  `papers/rasmussen-2013-the-reality-of-the-past-versus-the-ideality-of-the-future-abs.txt`
  - Imagined futures are more positively biased; the past is constrained by what happened.
- **Newby-Clark, I. & Ross, M. (2003).** Conceiving the past and future. *PSPB* 29(7):
  807–818. doi:10.1177/0146167203029007001. **ABS** ·
  `papers/newby-clark-2003-conceiving-the-past-and-future-abs.txt`
- **Wilson, A. & Ross, M. (2001).** From chump to champ. *JPSP* 80(4): 572–584.
  doi:10.1037/0022-3514.80.4.572. **ABS** ·
  `papers/wilson-2001-from-chump-to-champ-peoples-appraisals-of-their-earlier-and-present-selves-abs.txt`
- **Wirtz, D., Kruger, J., Scollon, C. & Diener, E. (2003).** What to do on spring break?
  *Psychological Science* 14(5): 520–524. doi:10.1111/1467-9280.03455. **ABS** (open copy
  behind a bot check) · `papers/wirtz-2003-what-to-do-on-spring-break-abs.txt`
  - Remembered, not on-line or anticipated, experience predicted the desire to repeat.
- **Speer, M., Ibrahim, S., Schiller, D. & Delgado, M. (2021).** Finding positive meaning
  in memories of negative events adaptively updates memory. *Nature Communications* 12:
  6601. doi:10.1038/s41467-021-26906-4. **FT** ·
  `papers/speer-2021-finding-positive-meaning-in-memories-of-negative-events-adaptively-updates-memory.txt`
  - Reappraisal changes a memory's later affect, after a reminder and a 24-hour delay.
- **Roy-Chowdhury, V. (2022).** Self-confidence and motivated memory loss. Cambridge CWPE
  2213. **WP** · `papers/roy-chowdhury-2022-self-confidence-and-motivated-memory-loss-wp.txt`
  - Reality constraints on recall loosen with time since the information; most of the
    later positive recall bias is tied to decay.
- **Heath, R. & Roy-Chowdhury, V. (2025).** Recall distortion and past choices. *JEBO* 240:
  107302. **WP** · `papers/heath-2025-recall-distortion-and-past-choices-wp.txt`
  - Recall favours past choices; distortion was the same whether the truth would be
    revealed or not.
- **Huffman, D., Raymond, C. & Shvets, J. (2022).** Persistent overconfidence and biased
  memory: evidence from managers. *AER* 112(10): 3141–3175. **WP** (IZA DP 16283) ·
  `papers/huffman-2023-persistent-overconfidence-and-biased-memory-evidence-from-managers-iza-dp16283.txt`
  - Rosy memory of feedback sustains overconfidence (p. 3); fn. 15: memory distortion as a
    way to manage disappointment.
- **Walters, D. & Fernbach, P. (2021).** Investor memory of past performance is positively
  biased. *PNAS* 118(36): e2026680118. **FT** ·
  `papers/walters-2021-investor-memory-of-past-performance-is-positively-biased.txt`
  - Recalled returns exceed actual; looking them up reduces overconfidence and trading.
- **Amelio, A. & Zimmermann, F. (2023).** Motivated memory in economics: a review. *Games*
  14(1): 15. **WP** (ECONtribute DP 213) ·
  `papers/amelio-2022-motivated-memory-in-economics-a-review-econtribute-dp213.txt`
  - Announcing a later recall test or raising stakes reduces motivated memory (p. 18).
- Abstract level: Zimmermann (2020), *AER* 110(2), positive feedback persists and negative
  fades; Chew, Huang & Zhao (2020), *JPE* 128(10), motivated false memory; Greenwald (1980),
  *Am. Psychologist* 35(7), the totalitarian ego; Kunda (1990), *Psych. Bull.* 108(3),
  motivated reasoning. Also saved: Eyster, Li & Ridout, ex post rationalization (arXiv
  2107.07491, **WP**); Thomas & König (2018), *Frontiers* 9: 760 (**FT**).

### Meta-emotion, rumination and bistability

- Abstract level: Mayer & Gaschke (1988), *JPSP* 55(1), meta-experience of mood; Gottman,
  Katz & Hooven (1996), *J. Family Psychology* 10(3), meta-emotion; Nolen-Hoeksema (1991),
  *J. Abnormal Psychology* 100(4), response styles.
- **Nolen-Hoeksema, S., Wisco, B. & Lyubomirsky, S. (2008).** Rethinking rumination.
  *Perspectives on Psychological Science* 3(5): 400–424. **FT** ·
  `papers/nolen-hoeksema-2008-rethinking-rumination.txt`
  - Rumination pulls up negative memories (p. 402) and can tip into self-perpetuating
    episodes (p. 404).
- **Watkins, E. (2008).** Constructive and unconstructive repetitive thought. *Psych.
  Bull.* 134(2): 163–206. **FT** (author manuscript) ·
  `papers/watkins-2008-constructive-and-unconstructive-repetitive-thought.txt`
  - A vicious cycle of mood and thought; the amplification could run for positive mood too.
- **Cramer, A. et al. (2016).** Major depression as a complex dynamic system. *PLoS ONE*
  11(12): e0167490. **FT** · `papers/cramer-2016-major-depression-as-a-complex-dynamic-system.txt`
  - Strong connectivity gives two attractors, tipping points and hysteresis.
- **van de Leemput, I. et al. (2014).** Critical slowing down as early warning for the
  onset and termination of depression. *PNAS* 111(1): 87–92. **FT** ·
  `papers/van-de-leemput-2014-critical-slowing-down-as-early-warning-for-depression.txt`
- **Kuppens, P., Allen, N. & Sheeber, L. (2010).** Emotional inertia and psychological
  maladjustment. *Psychological Science* 21(7): 984–991. **FT** (accepted manuscript) ·
  `papers/kuppens-2010-emotional-inertia-and-psychological-maladjustment.txt`
- **Robinaugh, D. et al. (2024).** A network theory of panic disorder. *Psych. Review*
  131(6): 1482–1508. **WP** (preprint) ·
  `papers/robinaugh-2019-network-theory-of-panic-disorder-computational-model-preprint.txt`
  - An arousal–threat loop whose strength crosses into a second, runaway stable state.
- **Hosseinichimeh, N. et al. (2018).** Feedback mechanisms among depression, rumination
  and stressors in adolescents. *PLoS ONE* 13(9): e0204389. **FT** ·
  `papers/hosseinichimeh-2018-feedback-mechanisms-among-depression-rumination-and-stressors-in-adolescents.txt`

## Calibration anchors (`calibration.md`)

### Loss aversion

- **Brown, A., Imai, T., Vieider, F. & Camerer, C. (2024).** Meta-analysis of empirical
  estimates of loss aversion. *JEL* 62(2): 485–516. doi:10.1257/jel.20221698. **WP** (2022) ·
  `papers/brown-2024-meta-analysis-of-empirical-estimates-of-loss-aversion-wp.txt`
  - Mean `λ = 1.955` [1.82, 2.11] (Table 5); bias-corrected 1.74. Only 9 of 522 estimates use
    a Kőszegi–Rabin reference point.
- **Pagel, M. (2017).** Expectations-based reference-dependent life-cycle consumption.
  *REStud* 84(2): 885–934. doi:10.1093/restud/rdx003. **WP** ·
  `papers/pagel-2017-expectations-based-reference-dependent-life-cycle-consumption-wp.txt`
  - Structural estimates, annual periods. Table 1 (p. 30): `η = 0.97`, `λ = 2.33`,
    `γ = 0.59`, `θ = 0.77`, `β = 0.97`; the text (p. 29) says `η = 1.1`, `λ = 2.4`,
    `γ = 0.53`. Core uses the table.
- **Pagel (2018)**, already above: Table 1 estimates `η = 0.87`, `λ = 3.03`, `γ = 0.87` from
  life-cycle portfolio shares; plausible lab range `η ≈ 1`, `λ ∈ [2, 3]`, `γ ≈ 0.8` (p. 40).
- **Pagel, M. (2016).** Expectations-based reference-dependent preferences and asset
  pricing. *JEEA* 14(2): 468–514. doi:10.1111/jeea.12137. **WP** ·
  `papers/pagel-2016-expectations-based-reference-dependent-preferences-and-asset-pricing-wp.txt`
  - Calibration only: `η = 1`, `λ = 2.6`–`3.4`, `γ = 0.7`.
- **Gill, D. & Prowse, V. (2012).** A structural analysis of disappointment aversion in a real
  effort competition. *AER* 102(1): 469–503. doi:10.1257/aer.102.1.469. **WP** (IZA DP 4536) ·
  `papers/gill-2012-a-structural-analysis-of-disappointment-aversion-in-a-real-effort-competition-iza-dp4536.txt`
  - Kink `η(λ−1) ≈ 1.72` on average, with large heterogeneity; the reference point adjusts
    almost instantly.
- **Kermer, D., Driver-Linn, E., Wilson, T. & Gilbert, D. (2006).** Loss aversion is an
  affective forecasting error. *Psychological Science* 17(8): 649–653.
  doi:10.1111/j.1467-9280.2006.01760.x. **FT** ·
  `papers/kermer-2006-loss-aversion-is-an-affective-forecasting-error.txt`
  - Forecasters predicted losses would hurt more than gains please; experiencers showed no
    asymmetry (Study 1), and losers were happier than they predicted (Study 2, d = 1.18).
- Abstract level: McGraw, Larsen, Kahneman & Schkade (2010), *Psych. Sci.* 21(10),
  judged-feelings loss aversion only under direct comparison; Harinck et al. (2007),
  *Psych. Sci.* 18(12), gains loom larger for small amounts.

### Present bias and patience

- **Imai, T., Rutter, T. & Camerer, C. (2021).** Meta-analysis of present-bias estimation
  using convex time budgets. *Economic Journal* 131(636): 1788–1814. doi:10.1093/ej/ueaa115.
  **FT** (with online appendix) ·
  `papers/imai-2021-meta-analysis-of-present-bias-estimation-using-convex-time-budgets.txt`
  - `β = 0.97` for money, `0.88` for effort (Table 5); "now" within the day raises `β` by
    about 0.05.
- **Cheung, S., Tymula, A. & Wang, X. (2021).** Quasi-hyperbolic present bias: a
  meta-analysis. IZA DP 14625. **WP** ·
  `papers/cheung-2021-quasi-hyperbolic-present-bias-a-meta-analysis-iza-dp14625.txt`
  - Money `0.82` (0.84–0.87 corrected); non-monetary `0.66`; convex time budgets alone 0.98.
- **Augenblick, N., Niederle, M. & Sprenger, C. (2015).** Working over time. *QJE* 130(3):
  1067–1115. doi:10.1093/qje/qjv020. **WP** (NBER w18734) ·
  `papers/augenblick-2015-working-over-time-dynamic-inconsistency-in-real-effort-tasks-nber-w18734.txt`
  - Money `β ≈ 0.97`–`0.99`; effort `≈ 0.88`–`0.90`; daily `δ ≈ 1`.
- **Cohen, J., Ericson, K., Laibson, D. & White, J. (2020).** Measuring time preferences.
  *JEL* 58(2): 299–347. doi:10.1257/jel.20191074. **WP** (NBER w22455) ·
  `papers/cohen-2020-measuring-time-preferences-nber-w22455.txt`
- **Ericson, K. & Laibson, D. (2019).** Intertemporal choice. *Handbook of Behavioral
  Economics* 2: 1–67. doi:10.1016/bs.hesbe.2018.12.001. **WP** (NBER w25358) ·
  `papers/ericson-2019-intertemporal-choice-nber-w25358.txt`
  - "How soon is now?" (§4.1): McClure et al.'s juice `β = 0.52` with "now" in minutes.
- Abstract level: Matoušek, Havránek & Iršová (2022), *Exp. Econ.* 25(1), mean experimental
  annual discount rate 0.33 after correcting for publication bias.

### Anticipation, memory and the content of thought

- **Killingsworth, M. & Gilbert, D. (2010).** A wandering mind is an unhappy mind. *Science*
  330: 932. doi:10.1126/science.1192439. **FT** (with supplement) ·
  `papers/killingsworth-2010-a-wandering-mind-is-an-unhappy-mind.txt`
  - Mind-wandering in 46.9% of samples. Against on-task focus: overall `b = −8.79`, pleasant
    topics n.s., unpleasant `−23.9` (0–100 scale).
- **Baumeister, R., Hofmann, W., Summerville, A., Reiss, P. & Vohs, K. (2020).** Everyday
  thoughts in time. *PSPB* 46(12): 1631–1648. doi:10.1177/0146167220908411. **WP** (preprint) ·
  `papers/baumeister-2020-everyday-thoughts-in-time-preprint.txt`
  - Any-future 29.6% against any-past 9.0% of thoughts; the present is happiest, the past
    least pleasant.
- **Song, X. & Wang, X. (2012).** Mind wandering in Chinese daily lives. *PLoS ONE* 7(9):
  e44423. **FT** · `papers/song-2012-mind-wandering-in-chinese-daily-lives-an-experience-sampling-study.txt`
  - Mind-wandering orientation: future 40.5%, past 21.5%.
- **D'Argembeau, A., Renaud, O. & Van der Linden, M. (2011).** Frequency, characteristics
  and functions of future-oriented thoughts in daily life. *Applied Cognitive Psychology*
  25(1): 96–103. **FT** · `papers/dargembeau-2011-frequency-characteristics-and-functions-of-future-oriented-thoughts-in-daily-life.txt`
  - About 59 future thoughts a day, mostly within a week.
- **Barsics, C., Van der Linden, M. & D'Argembeau, A. (2016).** Frequency, characteristics
  and perceived functions of emotional future thinking in daily life. *QJEP* 69(2):
  217–233. **WP** · `papers/barsics-2016-frequency-characteristics-and-perceived-functions-of-emotional-future-thinking-in-daily-life-author-version.txt`
  - Anticipatory emotion averages +0.35 on −3..+3; 49% involve joy, 38% fear or anxiety.
- **Stawarczyk, D. et al. (2011).** Mind-wandering: phenomenology and function. *Acta
  Psychologica* 136: 370–381. **WP** · `papers/stawarczyk-2011-mind-wandering-phenomenology-and-function-as-assessed-with-a-novel-experience-sampling-method-author-version.txt`
  - Future-oriented task-unrelated thought dominates (the prospective bias).
- **Kumar, A., Killingsworth, M. & Gilovich, T. (2014).** Waiting for merlot. *Psychological
  Science* 25(10): 1924–1931. doi:10.1177/0956797614546556. **FT** ·
  `papers/kumar-2014-waiting-for-merlot-anticipatory-consumption-of-experiential-and-material-purchases.txt`
  - Thinking about an upcoming experiential purchase: +2.4 (+1.2 within person) on 0–100;
    material purchases +0.3 (Study 2).
- **Bryson, A. & MacKerron, G. (2017).** Are you happy while you work? *Economic Journal*
  127(599): 106–125. doi:10.1111/ecoj.12269. **WP** (CEP DP 1187, 2013) ·
  `papers/bryson-2013-are-you-happy-while-you-work-lse-cep-dp1187.txt`
  - Mappiness, within person (Table 2): theatre, dance or concert +9.3, museum +8.8, sport
    +8.1, intimacy +14.2 on 0–100. Against Kumar et al., anticipation is 0.13–0.26 of
    the experience while thinking about it (a cross-study ratio).
- **Nawijn, J., Marchand, M., Veenhoven, R. & Vingerhoets, A. (2010).** Vacationers happier,
  but most not happier after a holiday. *Applied Research in Quality of Life* 5(1): 35–47.
  doi:10.1007/s11482-009-9091-9. **FT** (author version) ·
  `papers/nawijn-2010-vacationers-happier-but-most-not-happier-after-a-holiday.txt`
  - Higher pre-trip happiness for vacationers; after the trip, only very relaxed trips
    raise it, back to baseline within 8 weeks.
  - The pre-trip gap does not ramp across waves (weeks 11, 19, 27) and matches the
    post-trip gap (read from Fig. 1): selection, more than anticipation. Pre-trip/on-trip
    ratio unidentified.
- **Kühnel, J. & Sonnentag, S. (2011).** How long do you benefit from vacation? *J.
  Organizational Behavior* 32(1): 125–143. doi:10.1002/job.699. **FT** ·
  `papers/kuhnel-2011-how-long-do-you-benefit-from-vacation-a-closer-look-at-the-fade-out-of-vacation-effects.txt`
  - The post-vacation boost halves in about a week and is gone by week 4. Table 2:
    exhaustion 2.95 / 1.55 / 2.43 / 2.88 before, the first day back, 2 weeks, 4 weeks;
    engagement 3.06 / 3.45 / 3.20 / 3.11. About a third remains at two weeks; these behave
    like recovery stocks.
- **de Bloom, J. et al. (2010).** Effects of vacation from work on health and well-being:
  lots of fun, quickly gone. *Work & Stress* 24(2): 196–216.
  doi:10.1080/02678373.2010.493385. **FT** ·
  `papers/de-bloom-2010-effects-of-vacation-from-work-on-health-and-well-being-lots-of-fun-quickly-gone.txt`
  - Nine-day ski trip, n = 96, mood on 1–10 (Table 2): 7.28 before, 8.27 during, 7.41 a
    week after, 7.28 at two weeks. 13% of the mood gain remains after a week. Baseline two
    weeks before, so anticipation is not measured.
- **de Bloom, J. et al. (2009).** Do we recover from vacation? Meta-analysis. *J.
  Occupational Health* 51(1): 13–25. doi:10.1539/joh.k8004. **FT** ·
  `papers/de-bloom-2009-do-we-recover-from-vacation-meta-analysis-of-vacation-effects-on-health-and-well-being.txt`
  - Vacation effect d = +0.43, fade-out d = −0.38 within 2–4 weeks.
- **Caruso, E., Gilbert, D. & Wilson, T. (2008).** A wrinkle in time. *Psychological Science*
  19(8): 796–801. doi:10.1111/j.1467-9280.2008.02159.x. **FT** ·
  `papers/caruso-2008-a-wrinkle-in-time-asymmetric-valuation-of-past-and-future-events.txt`
  - Future events valued 1.2–2.0 times past ones; Study 1 failed to replicate (Halabi et
    al. 2022, reported in Caruso et al. 2025).
- Abstract level: Van Boven & Ashworth (2007), anticipation more evocative than
  retrospection; Finnbogadóttir & Berntsen (2013), *Consciousness & Cognition* 22(1),
  involuntary future projections as frequent as memories and more positive.

### Surprise and momentary happiness

- **Rutledge, R., Skandali, N., Dayan, P. & Dolan, R. (2014).** A computational and neural
  model of momentary subjective well-being. *PNAS* 111(33): 12252–12257.
  doi:10.1073/pnas.1407535111. **FT** (author-hosted PDF, main text) ·
  `papers/rutledge-2014-a-computational-and-neural-model-of-momentary-subjective-well-being.txt`
  - Happiness = weighted, exponentially forgotten sums of certain rewards, expected values
    and prediction errors; forgetting factor `γ = 0.61 ± 0.30` (SD), trials of roughly
    7–12 s, rated every 2–3 trials.
  - Weights per £ on 0–100, read from Fig. 2A: certain reward 9.6, expected value 6.3,
    prediction error 12.9; the text gives only EV < RPE (t(25) = 4.3). Replications and
    the smartphone sample: EV/CR 0.46–0.65, RPE/CR 1.1–1.3. A model splitting expected
    value by timing: reward +10.4, EV at choice +3.35, EV at outcome −8.1. [figure reads]
  - Data: the Great Brain Experiment smartphone task, deposited by Rutledge (Zenodo 4421847,
    mirror of Dryad doi:10.5061/dryad.prr4xgxkk; CC0): 47,067 participants, 91,058 plays,
    1.1M ratings. Fitted in `experiments/happiness/` (local copy in `data/`, gitignored).
- **Vanhasbroeck, N. et al. (2021).** Testing a computational model of subjective
  well-being: a replication. *Cognition & Emotion*. doi:10.1080/02699931.2021.1891863. **WP** ·
  `papers/vanhasbroeck-2021-testing-a-computational-model-of-subjective-well-being-replication-of-rutledge-2014-author-version.txt`
  - Weights per €: certain reward 0.14, expected value 0.06, prediction error 0.15;
    `γ = 0.81`.
- **Blain, B. & Rutledge, R. (2020).** Momentary subjective well-being depends on learning
  and not reward. *eLife* 9: e57977. doi:10.7554/eLife.57977. **FT** ·
  `papers/blain-2020-momentary-subjective-well-being-depends-on-learning-and-not-reward.txt`
  - Happiness tracks probability prediction errors, how surprised one is, not reward size;
    forgetting factor about 0.6.
- **Forbes, L. & Bennett, D. (2024).** The effect of reward prediction errors on subjective
  affect depends on outcome valence and decision context. *Emotion* 24(3): 894–911.
  doi:10.1037/emo0001310. **WP** (accepted manuscript) ·
  `papers/forbes-2024-the-effect-of-reward-prediction-errors-on-subjective-affect-depends-on-outcome-valence-and-decision-context-accepted-manuscript.txt`
  - With the outcome controlled, only negative prediction errors register, at about a
    tenth of the outcome's effect.
- Abstract level: Rutledge et al. (2015), *J. Neuroscience* 35(27), dopamine and momentary
  well-being.

### Emotional inertia (ceilings on felt memory)

- **Kuppens, Allen & Sheeber (2010)**, above (rumination and bistability): Table 1, affect autocorrelation
  between beeps (10 a day, about 1.6 h apart, n = 79): happy .30, excited .33, relaxed
  .27, satisfied .29, angry .20, anxious .22, depressed .22, sad .27.
- **Kuppens, P., Oravecz, Z. & Tuerlinckx, F. (2010).** Feelings change. *JPSP* 99(6):
  1042–1060. doi:10.1037/a0020962. **FT** ·
  `papers/kuppens-2010-feelings-change-accounting-for-individual-differences-in-the-temporal-dynamics-of-affect.txt`
- **Vansteelandt, K. & Verbeke, G. (2016).** A mixed model to disentangle variance and
  serial autocorrelation in affective instability using ecological momentary assessment
  data. *Multivariate Behavioral Research* 51(4): 446–465. **FT** ·
  `papers/vansteelandt-2016-a-mixed-model-to-disentangle-variance-and-serial-autocorrelation-in-affective-instability-ema.txt`
  - Exponential serial correlation of valence: 0.61 at one hour, half-life about 1.4 h
    (eating-disorder patients, n = 58).
- **Brose, A., Schmiedek, F., Koval, P. & Kuppens, P. (2015).** Emotional inertia
  contributes to depressive symptoms beyond perseverative thinking. *Cognition & Emotion*
  29(3): 527–538. **FT** ·
  `papers/brose-2015-emotional-inertia-contributes-to-depressive-symptoms-beyond-perseverative-thinking.txt`
  - Day-to-day autoregression of negative affect .34 (Table 1).
- Autocorrelation also contains slowly moving base utility, so these bound felt memory
  from above. Houben, Van Den Noortgate & Kuppens (2015, *Psych. Bull.*), the meta-analysis,
  closed.

### The week as a natural experiment

- **Helliwell, J. & Wang, S. (2014).** Weekends and subjective well-being. *Social Indicators
  Research* 116(2): 389–407. **WP** (NBER w17180, 2011) ·
  `papers/helliwell-2011-weekends-and-subjective-well-being-nber-w17180.txt`
  - Gallup, N ≈ 527,000, emotions "yesterday", coefficients against Monday (Table 3):
    Friday / Saturday / Sunday happiness .015 / .031 / .033, enjoyment .021 / .054 /
    .059, laughter .021 / .039 / .037, worry −.016 / −.073 / −.074. No Blue Monday
    (Tuesday to Thursday +.001 to +.002) and no Sunday dip.
  - The day before a midweek holiday shows no lift (Table 4: happiness −.011, s.e. .007).
- **Weigelt, O., Siestrup, K. & Prem, R. (2021).** Continuity in transition. *J.
  Organizational Behavior* 42(5): 567–586. **FT** (hybrid OA) ·
  `papers/weigelt-2021-continuity-in-transition-recovery-and-day-of-week-perspectives-employee-energy.txt`
  - Vitality on 1–5 (Table 2): Thursday to Friday +0.26; Sunday to Monday −0.31 and −0.19
    in two samples. An energy stock, more recovery than echo.
- Abstract level: Stone, Schneider & Harter (2012, *J. Positive Psych.*), Friday better,
  Monday no worse than Tuesday to Thursday; Ryan, Bernstein & Brown (2010, *JSCP*), better
  mood from Friday evening to Sunday afternoon.

### LLM context windows (`selves.md`, Horizons)

- **Liu, N. et al. (2024).** Lost in the middle: how language models use long contexts.
  *TACL* 12: 157–173. arXiv:2307.03172. **FT** ·
  `papers/liu-2023-lost-in-the-middle-how-language-models-use-long-contexts.txt`
  - Accuracy by the answer's position is U-shaped, primacy at least as strong as recency
    (Tables 5–7): GPT-3.5-Turbo with 20 documents 75.8% first, 53.8% middle, 63.2% last
    (closed-book 56.1%); Claude-1.3 59.9 / 55.9 / 60.1 (closed-book 48.3%).
- **Hsieh, C.-Y. et al. (2024).** Found in the middle: calibrating positional attention bias
  improves long context utilization. arXiv:2406.16008. **WP** ·
  `papers/hsieh-2024-found-in-the-middle-calibrating-positional-attention-bias-improves-long-context-utilization.txt`
  - Attention by document position is U-shaped even with content shuffled (Fig. 4):
    intrinsic positional bias.
- **Guo, X. & Vosoughi, S. (2024).** Serial position effects of large language models.
  arXiv:2406.15981. **WP** · `papers/guo-2024-serial-position-effects-of-large-language-models.txt`
  - Primacy dominates, recency weaker, in classification-style tasks.
- **Wu, X., Wang, Y., Jegelka, S. & Jadbabaie, A. (2025).** On the emergence of position
  bias in transformers. arXiv:2502.01951. **WP** ·
  `papers/wu-2025-on-the-emergence-of-position-bias-in-transformers.txt`
  - Causal masking favours early tokens and relative positional decay favours recent ones.

## Decision theory by learning (`experiments/learned_expectations/`; D2, D7)

- **Oesterheld, C., Treutlein, J., Cooper, E. & Hudson, R. (2023).** Incentivizing honest
  performative predictions with proper scoring rules. *UAI 2023*. arXiv:2305.17601. **WP**
  (appendix passages) ·
  `papers/oesterheld-2023-incentivizing-honest-performative-predictions-with-proper-scoring-rules.txt`
  - App. C: a predictor that treats the outcome as influenced causally by its report, but
    only acausally by the report's effect, has performatively stable equilibria;
    performative optimality "would correspond to an agent using evidential epistemic
    decision theory". App. D.2: repeated gradient descent is gradient descent on a
    stop-gradient objective; meta-learning would prefer the objective without it.
  - Pre-empts the binary half of the extension's claim: stop-gradient is stable and
    CDT-like, full flow is optimal and EDT-like.
- **Treutlein, J. (2023).** Stop-gradients lead to fixed point predictions. LessWrong. **FT**
  · `web/treutlein-2023-stop-gradients-lead-to-fixed-point-predictions.md`
- **Perdomo, J., Zrnic, T., Mendler-Dünner, C. & Hardt, M. (2020).** Performative
  prediction. *ICML*, PMLR 119: 7599–7609. arXiv:2002.06673. **FT** ·
  `papers/perdomo-2020-performative-prediction.txt`
  - Performative optimality (Def. 2.1) against stability (Def. 2.3), a fixed point of
    repeated risk minimization; neither implies the other (p. 3); the optimum is the
    Stackelberg equilibrium, the leader committing first (§5.1).
- **Demski, A. (2019).** Partial agency; The parable of Predict-O-Matic; Random thoughts on
  Predict-O-Matic; Defining myopia; The credit assignment problem (and 2020, 2025 sequels).
  LessWrong. **FT** · `web/demski-2019-*.md`, `web/demski-2020-*.md`, `web/demski-2025-*.md`
  - Nash as `argmax_a f(a, a*)`, "sending the gradient through the first argument but not
    the second"; "Causal decision theory is more 'partial' and evidential decision theory
    is less so"; partial agency is what selection incentivizes by default.
- **Demski, A. (2017).** Mixed-strategy ratifiability implies CDT=EDT. **FT** ·
  `web/demski-2017-mixed-strategy-ratifiability-implies-cdt-edt.md` — enough self-knowledge
  screens off the correlation channel.
- **Mennen, A. (2018).** When wishful thinking works. **FT** ·
  `web/mennen-2018-when-wishful-thinking-works.md` — believe the fixed point with the
  highest expected utility.
- **Krueger, D., Maharaj, T. & Leike, J. (2020).** Hidden incentives for auto-induced
  distributional shift. arXiv:2009.09153. **WP** ·
  `papers/krueger-2020-hidden-incentives-for-auto-induced-distributional-shift.txt`
  - A myopic inner loop hides the incentive to influence one's own inputs; population-based
    training reveals it. Q-learning at `γ = 0` against its own past action learns the
    self-correlation channel in a third of runs.
- **Bell, J., Linsefors, L., Oesterheld, C. & Skalse, J. (2021).** Reinforcement learning in
  Newcomblike environments. *NeurIPS* 34: 22146–22157. **FT** ·
  `papers/bell-2021-reinforcement-learning-in-newcomblike-environments.txt`
  - Rewards may depend on the policy, not just the action. A value-based learner cannot
    converge to a policy that is not ratifiable; learners valuing policies directly
    behave evidentially.
- **Oesterheld, C. (2018).** Doing what has worked well in the past leads to evidential
  decision theory. **FT** ·
  `papers/oesterheld-2018-doing-what-has-worked-well-in-the-past-leads-to-evidential-decision-theory.txt`
- **Oesterheld, C. (2019).** Approval-directed agency and the decision theory of
  Newcomb-like problems. *Synthese*. **FT** (CC BY) ·
  `papers/oesterheld-2019-approval-directed-agency-and-the-decision-theory-of-newcomb-like-problems.txt`
  - Two decision theories interact: the overseer's (in the reward) and the agent's. In the
    extension, felt anticipation plays the overseer.
- **Everitt, T., Leike, J. & Hutter, M. (2015).** Sequential extensions of causal and
  evidential decision theory. arXiv:1506.07359. **WP** ·
  `papers/everitt-2015-sequential-extensions-of-causal-and-evidential-decision-theory.txt`
  — causal, action-evidential and policy-evidential sequential agents.
- **Everitt, T. et al. (2021).** Reward tampering problems and solutions in reinforcement
  learning. arXiv:1908.04734. **WP** ·
  `papers/everitt-2021-reward-tampering-problems-and-solutions-in-reinforcement-learning.txt`
  — belief-based rewards (§4.3); agents that do or do not model their future selves'
  use of a changed model.
- **Gershman, S. (2026).** Subjective functions. arXiv:2512.15948. **WP** ·
  `papers/gershman-2026-subjective-functions.txt`
  - Expected prediction error as reward, with the value estimate frozen ("similar to the
    logic of target networks"); predicts avoidance of information gathering where value
    estimates run optimistic. Theory only.
- **Iigaya, K. et al. (2020).** The value of what's to come. *Science Advances*. **FT**
  (CC BY) ·
  `papers/iigaya-2020-the-value-of-whats-to-come-neural-mechanisms-coupling-prediction-error-and-the-utility-of-anticipation.txt`
  — anticipatory utility and advance-information seeking in humans (fMRI and model).
- Not found: an agent trained on felt utility built from its own forecasts, or emergent
  optimism or information avoidance in trained agents.

- **Chung, W., Thomas, V., Machado, M. C. & Le Roux, N. (2021).** Beyond variance reduction:
  understanding the true impact of baselines on policy optimization. *ICML*, PMLR 139:
  1999–2009. arXiv:2008.13773. **FT** (arXiv v3) ·
  `papers/chung-2021-beyond-variance-reduction-understanding-the-true-impact-of-baselines-on-policy-optimization.txt`
  - Baselines matter beyond variance: with sampled-action updates, a baseline below the
    min-variance one is *committal* (most sampled actions reinforced, premature
    near-determinism; Prop. 1–2, 2-arm bandit), one above it non-committal (sampled actions
    pushed down, exploration kept). Absent under the true gradient; needs sampling noise
    with on-policy coupling (§2.1, §4). Theory for bandits; MDPs empirical, tabular, exact
    `Q^π` (§5). The decision-rule channel for a critic's optimism, against the
    shared-state channel in the hidden-game agent.

## Shared representations and the critic's level (D8)

- **Jacot, A., Gabriel, F. & Hongler, C. (2018).** Neural tangent kernel: convergence and
  generalization in neural networks. *NeurIPS* 31. arXiv:1806.07572. **FT** ·
  `papers/jacot-2018-neural-tangent-kernel-convergence-and-generalization-in-neural-networks.txt`
  - Under gradient descent the network function follows the kernel gradient of the
    functional cost, with the tangent kernel `∇_θ f · ∇_θ f`. D8's cross tangent kernel is
    the two-head version.
- **Saxe, A. M., McClelland, J. L. & Ganguli, S. (2014).** Exact solutions to the nonlinear
  dynamics of learning in deep linear neural networks. *ICLR*. arXiv:1312.6120. **FT** ·
  `papers/saxe-2014-exact-solutions-to-the-nonlinear-dynamics-of-learning-in-deep-linear-neural-networks.txt`
  - Deep linear networks learn input–output modes one by one from small initialization,
    toward balanced factorizations: D8(c)'s rank-one surrogate.
- **Sun, H., Han, L., Yang, R., Ma, X., Guo, J. & Zhou, B. (2022).** Exploit reward shifting
  in value-based deep-RL: optimistic curiosity-based exploration and conservative
  exploitation via linear reward shaping. *NeurIPS*. arXiv:2209.07288 (as "Optimistic
  curiosity exploration and conservative exploitation with linear reward shaping"). **FT** ·
  `papers/sun-2022-exploit-reward-shifting-in-value-based-deep-rl.txt`
  - A reward shift equals a change of Q-initialization under function approximation (§4.1);
    a positive shift is conservative, a negative one exploratory, through the argmax over
    rarely visited actions (§4.3). Same sign as D8, different channel: value-based, the
    decision rule reads the values; D8's policy never reads the critic.
- **Schaul, T., Borsa, D., Modayil, J. & Pascanu, R. (2019).** Ray interference: a source of
  plateaus in deep reinforcement learning. arXiv:1904.11455. **FT** ·
  `papers/schaul-2019-ray-interference-a-source-of-plateaus-in-deep-reinforcement-learning.txt`
  - Negative interference between components under shared function approximation, with
    on-policy coupling of learning and data, produces plateaus (pp. 1–2). The nearest
    analogue of the complacent plateau; no critic involved.
- **Cobbe, K., Hilton, J., Klimov, O. & Schulman, J. (2021).** Phasic policy gradient. *ICML*.
  arXiv:2009.04416. **FT** (v1) · `papers/cobbe-2021-phasic-policy-gradient.txt`
  - Policy and value objectives interfere in a shared network (p. 2); nothing on the
    value's level or sign.
- **Hessel, M., Soyer, H., Espeholt, L., Czarnecki, W., Schmitt, S. & van Hasselt, H.
  (2019).** Multi-task deep reinforcement learning with PopArt. *AAAI*. arXiv:1809.04474.
  **FT** · `papers/hessel-2019-multi-task-deep-reinforcement-learning-with-popart.txt`
  - Value and policy updates both use normalized returns, so shared-parameter updates are
    invariant to a return's scale and offset (p. 3, eqs. 5–9). D8 predicts such
    normalization removes the level's forcing. Also van Hasselt et al. (2016), the
    value-only original · `papers/van-hasselt-2016-learning-values-across-many-orders-of-magnitude.txt`
- **Naik, A., Wan, Y., Tomar, M. & Sutton, R. S. (2024).** Reward centering. *RLC*.
  arXiv:2405.09999. **FT** · `papers/naik-2024-reward-centering.txt` — constant reward shifts
  degrade discounted value learning; centering removes it; the actor's update is unchanged
  by centering (p. 22).
- Also read: Rashid et al. 2020 (optimistic initialization fails in deep Q-learning because
  generalization erases it; a reward offset did little in their maze, p. 8); Du et al. 2018
  (auxiliary/main gradient cosine on shared parameters, the alignment diagnostic's
  precedent); Garcin et al. 2025 (ICLR; even decoupled, the critic shapes what data the
  policy collects); Wan, Korenkevych & Zhu 2025 (a ±100 reward offset breaks most deep RL
  in continuing tasks, PPO included, §2.4); Andrychowicz et al. 2021 (value normalization
  and separate networks matter in on-policy RL, §3.2–3.3). Texts in `papers/`.
- **Marek, M. & Ryabinin, M. (2026).** Score centering stabilizes off-policy reinforcement
  learning. arXiv:2609.20807. **FT** (arXiv v1) ·
  `papers/marek-2026-score-centering-stabilizes-off-policy-reinforcement-learning.txt`
  - Off-policy the policy gradient splits, conditional on the prefix, as `E_q[R] s̄ + Cov_q(R, s)`,
    `s̄ = E_q[∇ log p]` (§4, eq. 3): "drift" sees rewards only through their mean and, for a
    positive mean, distils the trainer toward the sampler (`s̄` is minus the gradient of the
    cross-entropy to it); on-policy it vanishes. Score centering subtracts `s̄` (eq. 4; loss
    form eq. 11, top-k head with the tail modelled by the trainer, eqs. 6–8; with importance
    weights, eqs. 9–12); group centering does not remove drift (§4). LLM RL under
    training–inference mismatch (weight noise, quantized samplers, staleness), 0.6B–30B, SGD;
    deliberately severe mismatch, 30B runs mostly single-seed (§5, B.3). Under staleness,
    centering plus importance correction beats centering alone (§5.3).
  - The sign of a replayed level, offline (§3, Fig. 2, fn. 4): training on a fixed sampler's
    data is stable only with non-negative rewards; with negative ones log-probabilities run
    to −∞ and the model collapses (Ren & Sutherland 2025, cited there). Online under mismatch
    the order reverses, because the sampler is a biased copy re-synced each step; "what
    matters is not the size of the mismatch, but whether the teacher is fixed or tracks the
    student" (§6). D9's replay 100 steps late sits between, and shows the offline sign.
- **Wu, Y., Tucker, G. & Nachum, O. (2019).** Behavior regularized offline reinforcement
  learning (BRAC). arXiv:1911.11361. **ABS+** (arXiv v1; abstract, §1–§3 read) ·
  `papers/wu-2019-behavior-regularized-offline-reinforcement-learning.txt`
  - Regularizes a learned policy toward the behavior policy by a divergence `D(π_θ, π_b)`
    (KL, MMD, Wasserstein), as a value penalty or a policy penalty (§3, eqs. 5–7; KL taken
    as `E_{π_θ}[log π_θ − log π_b]`, p. 5); the KL-control line (Jaques et al. 2019) and
    trust regions (Schulman et al. 2015) cited as kin. The closest precedent for D9's anchor,
    which a positive reward offset in uncorrected replay adds unasked as `−c ∇KL(q‖p)`, the
    other direction of the KL. TRPO constrains a KL; PPO (2017) clips its surrogate
    objective; the anchor enforces no bound.
- **Fedus, W., Gelada, C., Bengio, Y., Bellemare, M. G. & Larochelle, H. (2019).** Hyperbolic
  discounting and learning over multiple horizons. arXiv:1902.06865. **ABS+** (abstract,
  introduction, §9, Fig. 9) ·
  `papers/fedus-2019-hyperbolic-discounting-and-learning-over-multiple-horizons.txt`
  - Value heads for many discount factors at once, each an affine map of a shared
    representation; as an auxiliary task it often improves Rainbow on Atari. The precedent for
    a per-horizon critic (menu F2: news per horizon, not on the netted TD error).

## Games: guilt, Kantian morality, similarity (`notes/empathy.md`)

- **Battigalli, P. & Dufwenberg, M. (2007).** Guilt in games. *AER Papers & Proceedings*
  97(2): 170–176. doi:10.1257/aer.97.2.170. **FT** (Bocconi-hosted copy; math garbled in the
  text layer, glyph map in the header) · `papers/battigalli-2007-guilt-in-games.txt`
  - Simple guilt (eq. 1): `m_i − Σ_j θ_ij G_ij`, with `G_ij` the part of `j`'s letdown
    `max{0, E[m_j] − m_j}` due to `i`'s choice. Guilt from blame (eq. 3) weighs it by what `j`
    infers `i` intended; in two-player simultaneous games without chance their pure sequential
    equilibria coincide (Obs. 1).
  - Empathy with a partner who feels loss-averse news is simple guilt with `θ = w·n·(λ−1)`
    plus altruism (`notes/empathy.md`).
- **Khalmetski, K., Ockenfels, A. & Werner, P. (2015).** Surprising gifts: theory and
  laboratory evidence. *JET* 159(A): 163–208. doi:10.1016/j.jet.2015.05.008. **WP** (Cologne
  WP 61, May 2013; the published version reports more experiments) ·
  `papers/khalmetski-2013-surprising-gifts-theory-and-laboratory-evidence-cologne-wp61.txt`
  - Utility `m_i(1 − t_i) + S_i`, with `S_i` linear in the recipient's surprise: weight `α` on
    positive surprises, `β` (guilt) on negative, against the giver's belief about the
    recipient's expectation (eqs. 2–3; linearity "for convenience", fn. 5). Prop. 1: giving at
    or above the expected if `α ≥ β`, at or below if `α ≤ β`.
  - Empathy with a loss-averse news-feeling partner gives `α = wn`, `β = wnλ`, so `β ≥ α`.
- **Alger, I. & Weibull, J. W. (2013).** Homo moralis: preference evolution under incomplete
  information and assortative matching. *Econometrica* 81(6): 2269–2302.
  doi:10.3982/ECTA10637. **FT** (published text via a third-party copy, gwern.net) ·
  `papers/alger-2013-homo-moralis-preference-evolution-under-incomplete-information-and-assortative-matching.txt`
  - Homo moralis (Def. 4): `(1−κ)π(x,y) + κπ(x,x)`. Theorem 1: with assortativity `σ`
    (eq. 4), homo hamiltonensis (`κ = σ`) is evolutionarily stable against types that are not
    its behavioural clones, if its best replies are unique; under richness conditions types
    that behave differently are unstable.
  - §6.2: altruism `π(x,y) + απ(y,x)` has the same first-order conditions at interior
    symmetric equilibria for `α = κ` and different second-order ones. Prop. 2: in 2 × 2 games
    homo moralis is convex in own play iff `a₁₁ + a₂₂ > a₁₂ + a₂₁`. Prior art for "a twin is an
    altruist to first order".
  - Follow-up: Alger & Weibull (2016), Evolution and Kantian morality, *GEB* 98: 56–67
    (`n`-player groups; **ABS**), corrected in *GEB* 140 (2023): 585–587 (unread).
- **Bergstrom, T. C. (1995).** On the evolution of altruistic ethical rules for siblings.
  *AER* 85(1): 58–81. **WP** (July 1993) ·
  `papers/bergstrom-1993-on-the-evolution-of-altruistic-ethical-rules-for-siblings-wp.txt`
  - The semi-Kantian rule `½Π(x,x) + ½Π(x,x̄)` (homo moralis at `κ = ½`), from selection on
    actions against dominant mutants, against Hamilton's altruism at `r = ½`. Prop. 2: with
    strategic complementarity every symmetric equilibrium of the semi-Kantian rule is one of
    Hamilton's; with substitutability the reverse.
- **Oesterheld, C., Treutlein, J., Grosse, R., Conitzer, V. & Foerster, J. (2023).**
  Similarity-based cooperative equilibrium. *NeurIPS* 36. arXiv:2211.14468 (v1, 2022:
  "Similarity-based cooperation"). **FT** (arXiv v2) ·
  `papers/oesterheld-2023-similarity-based-cooperative-equilibrium.txt`
  - Policies map a perceived "diff" to play in a one-shot game; a folk theorem (Thm. 3).
    In a high-dimensional prisoner's dilemma, alternating best response from random
    initialization reached mutual defection in 26 of 26 runs; pretraining to cooperate against
    copies and defect against random (CCDR) gave partial cooperation in 26 of 28.
  - The twin dial with a copy signal learns CCDR by itself, through a gate on true identity.

## Anthropics and imperfect recall

- **Armstrong, S. (2011; rev. 2017).** Anthropic decision theory (for self-locating
  beliefs). arXiv:1110.6437. **FT** (v1, v3) ·
  `papers/armstrong-2011-anthropic-decision-theory-arxiv-v1.txt`,
  `papers/armstrong-2017-anthropic-decision-theory-arxiv-v3.txt`
  - Sleeping Beauty betting: total utilitarian gives SIA-like 2:1; average utilitarian
    gives SSA-like 1:1. The selfish case splits in v3 (psychological → SSA-like,
    physical → SIA-like).
  - Linked decisions. v1 §§2, 3.3.2: memory-only value gives SSA-like odds, the
    precedent for A2.
- **Armstrong, S. (2011).** Subjective anticipation as a decision process. LessWrong.
  **FT** · `web/armstrong-2011-subjective-anticipation-as-a-decision-process.md`
  - Anticipation is encoded in the utility function. Related posts saved in `web/`
    (ADT I, ADT IV, Solving selfishness for UDT 2014).
- **Yudkowsky, E. (2009).** The anthropic trilemma. LessWrong. **FT** ·
  `web/yudkowsky-2009-the-anthropic-trilemma.md`
  - The lottery trick: copy yourself a trillion times on winning, merge afterwards, and
    "subjectively" win. Horns: accept anthropic psychic powers (copy-counted anticipation),
    give up joint subjective probabilities, give up the personal future, or deny that
    copies add weight. The fifth: quantum measure is conserved by splits and merges, so
    Born-weighted branching avoids the trilemma.
  - A1's measure-weighted anticipation is the conserved-measure horn, applied to felt
    anticipation; A1's separate aggregation axiom is where the trillion copies' own welfare
    goes. The nearest LessWrong statement of the problem A1 answers.
- **Greaves, H. (2004).** Understanding Deutsch's probability in a deterministic
  multiverse. arXiv:quant-ph/0312136. **2ND** (literature agent)
  - Caring measure: the precedent for share-weighted anticipation in A1.
- **Bostrom, N. (2002).** *Anthropic Bias*, ch. 10. Routledge. **FT** (ch. 10) ·
  `web/bostrom-2002-anthropic-bias-ch10-observation-selection-theory.md`
  - SSSA: sample from observer-moments.
- **Elga, A. (2000).** Self-locating belief and the Sleeping Beauty problem. *Analysis*
  60(2): 143–147. doi:10.1093/analys/60.2.143. **FT** ·
  `papers/elga-2000-self-locating-belief-and-the-sleeping-beauty-problem.txt`
- **Piccione, M. & Rubinstein, A. (1997).** On the interpretation of decision problems with
  imperfect recall. *GEB* 20(1): 3–24. doi:10.1006/game.1997.0536. **FT** ·
  `papers/piccione-1997-interpretation-of-decision-problems-with-imperfect-recall.txt`
  - The planning-optimal driver strategy is not time-consistent (§6). Modified multiself
    consistency (Prop. 3). They hold no firm view on the resolution.
- **Aumann, R., Hart, S. & Perry, M. (1997).** The absent-minded driver. *GEB* 20(1):
  102–116. doi:10.1006/game.1997.0577. **FT** · `papers/aumann-1997-the-absent-minded-driver.txt`
  - Action-optimality is a symmetric equilibrium among selves. Planning-optimal implies
    action-optimal, not conversely. They dispute the inconsistency.
- **Oesterheld, C. & Conitzer, V. (2024).** Can de se choice be ex ante reasonable? **WP** ·
  `papers/oesterheld-2024-can-de-se-choice-be-ex-ante-reasonable.txt`
  - The ex-ante-optimal policy fits both CDT plus generalized thirding and EDT plus
    generalized double-halving.
- **Cooper, Oesterheld & Conitzer (2024).** Can CDT rationalise the ex ante optimal
  policy? **WP** · `papers/cooper-2024-can-cdt-rationalise-the-ex-ante-optimal-policy.txt`
- Informal LessWrong precedents, none involving felt anticipation or welfare (all in
  `web/`):
  - eugman 2011, Newcomb and procrastination;
  - Barta 2011, real-world Newcomb-like problems;
  - Apprentice 2012, the Noddy problem;
  - Schmied 2026, decision theory as commitment theory;
  - the Alignment Forum UDT wiki.
