# Bibliography

Status: **FT** full text read · **WP** full text of a working/author version (published
text may differ) · **ABS** abstract or publisher record only · **2ND** primary unread,
described via the secondary named. Files are in `references/`. First verification pass
2026-10-12 (two literature agents plus Codex; spot-read by Claude where marked).

## Direct precursors of the premise

- **Bergstrom, T. (1999).** Systems of benevolent utility functions. *J. Public Economic
  Theory* 1(1): 71–100. doi:10.1111/1097-3923.00004. **WP** (CREST WP 87-4, 1987) ·
  `papers/bergstrom-1987-systems-benevolent-utility-interdependence.txt`
  - `U = u + AU`; nonnegative inverse ⟺ `I − A` dominant diagonal (M-matrix). On ℤ the
    Neumann series gives the unique *bounded* nonnegative inverse.
  - Prop. 5: nearest-neighbour two-sided `U_t = u_t + aU_{t−1} + bU_{t+1}` is well-behaved
    iff `a + b < 1`, and reduces to two-sided geometric weights on `u` (bounded root).
  - The conclusion sketches the *intrapersonal* reading: happiness depends on
    consumption, expected next-period happiness, and remembered past happiness. A finite
    life is called essential to the story. No results follow. Codex reports the same
    passage in the JPET version (§5, pp. 82–84).
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
  doi:10.1111/iere.12705. **ABS** (open-access full text saved, not yet read closely) ·
  `papers/cosaert-2024-anticipating-remembering-experiencing-selves.txt`
  - Carry-over parameters for anticipation and remembering, estimated on Spanish
    household data. Anticipation favours increasing profiles, memory decreasing ones.
    Direct, not recursive.
- **Knight, J. & Gunatilaka, R. (2014).** Memory and anticipation: new empirical support
  for an old theory of the utility function. Oxford Econ. DP 721. **FT** ·
  `papers/knight-2014-memory-and-anticipation-oxford-dp721.txt`
  - Tests the Bentham and Jevons utility of memory and anticipation with subjective
    well-being regressions on past and expected income.
- **Elster, J. & Loewenstein, G. (1992).** Utility from memory and anticipation. In
  Loewenstein & Elster (eds.), *Choice over Time*, Russell Sage, 213–234. **2ND**
  (Loewenstein & Prelec 1993; Shardlow et al. 2025)
  - Memory and anticipation each have a consumption effect and a contrast effect.
    Stronger backward contrast favours improvement.

## Recursion and altruism math

- **Sáez-Martí, M. & Weibull, J. (2005).** Discounting and altruism to future
  decision-makers. *J. Economic Theory* 122(2): 254–266. doi:10.1016/j.jet.2004.06.003.
  **WP** (IFN WP 575, 2002) · `papers/saez-marti-2002-discounting-and-future-selves-wp575.txt`
  - Altruism toward future selves' *total* utility ↔ discounting of consumption utility,
    `f = 1 + f* ∗ f`.
  - §4.4: quasi-hyperbolic `βδ^t` ↔ exponential altruism weights, which is core P3.
    Exponential discounting ↔ one-period altruism.
  - A nonnegative `f` need not give a nonnegative `f*`; the negative case is called
    "spite". The working paper states no convergence condition.
- **Galperti, S. & Strulovici, B. (2017).** A theory of intergenerational altruism.
  *Econometrica* 85(4): 1175–1218. doi:10.3982/ECTA13937. **WP** (Jan 2017 preprint) ·
  `papers/galperti-2017-a-theory-of-intergenerational-altruism-preprint.txt`
  - Axiomatizes pure altruism toward future generations' total utility. Present bias
    follows (Prop. 2).
  - Cor. 3: linear `G` gives `βδ^t` with `β = γ/(1+γ)`, `δ = (1+γ)α`, on
    `γ < (1−α)/α` — our `M < 1`.
  - §4.5: finite two-sided systems are solvable iff `αα̂ < 1` (two generations).
  - Credits Fels & Zeckhauser (2008, *J. Risk & Uncertainty* 37: 187–197; unread) for the
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
  - Hori (1992, *JET*) extends this to altruism over many generations (Codex, abstract
    level).
- **Ray, D. (1987).** Nonpaternalistic intergenerational altruism. *JET* 41(1): 112–132.
  **2ND** (Ray, Vellodi & Wang 2024; Galperti & Strulovici)
  - Poses representing utility-over-utility altruism in consumption form.
- **Heifetz, A., Minelli, E. & Polemarchakis, H. (2023).** Affective interdependence and
  welfare. arXiv:2305.10165. **WP** · `papers/heifetz-2023-affective-interdependence-and-welfare.txt`
  - A P-matrix suffices for Pareto-optimal affective equilibria. A resolvent with negative
    entries can still admit positive welfare weights, though equal weights may fail.
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
  feelings. *QJE* 116(1): 55–79. doi:10.1162/003355301556347. **ABS**
  - Anticipatory feelings in expected utility. They generate time inconsistency and
    preferences over information.
- **Brunnermeier, M. & Parker, J. (2005).** Optimal expectations. *AER* 95(4): 1092–1118.
  **2ND** (Codex)
  - Felicity includes memory, current flow and anticipated utility. Beliefs are chosen to
    trade anticipatory benefit against decision cost.
- **Kimball, M. & Willis, R. (2006).** Utility and happiness. U. Michigan WP. **WP**
  (keyword scan only) · `papers/kimball-2006-utility-and-happiness-*.txt`
  - News utility. With rational expectations, linear terms in lifetime-utility news leave
    preferences unchanged (the iterated-expectations point).
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
  doi:10.1086/678373. **ABS** (2ND: Brown 2019)
  - An ecumenical shape-of-a-life hypothesis with a relational view. Relations between
    events can enter momentary well-being. Rejects instrumental and pro-attitude
    explanations because they explain the hypothesis away.
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

## Psychology

- **Caruso, E., Gilbert, D. & Wilson, T. (2008).** A wrinkle in time: asymmetric
  valuation of past and future events. *Psychological Science* 19(8): 796–801.
  doi:10.1111/j.1467-9280.2008.02159.x. **ABS**
  - Future events are valued more than equivalent past ones, between subjects only. See
    Caruso et al. 2025 for the replication problem.
- **Van Boven, L. & Ashworth, L. (2007).** Looking forward, looking back: anticipation is
  more evocative than retrospection. *JEP: General* 136(2): 289–300.
  doi:10.1037/0096-3445.136.2.289. **ABS**
  - Five experiments. Anticipation is more emotionally intense, mediated by mental
    simulation. The expected-versus-remembered gap is slight.
- **Tversky, A. & Griffin, D. (1991).** Endowment and contrast in judgments of
  well-being. In Strack, Argyle & Schwarz (eds.), *Subjective Well-Being*, 101–118. **2ND**
  (Griffin & Gonzalez 2013, `papers/griffin-gonzalez-2013-endowment-contrast-model.*`)
  - Satisfaction = salience-weighted endowment from memory + current endowment +
    relatedness × contrast. Satisfaction and choice come apart.
- **Diener, E., Wirtz, D. & Oishi, S. (2001).** End effects of rated life quality: the
  James Dean effect. *Psychological Science* 12(2): 124–128. doi:10.1111/1467-9280.00321.
  **ABS**
  - Adding mildly pleasant years makes a wonderful life rated worse. Years added in the
    middle matter less than years added at the end.
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
  115(503): 271–304. **ABS** (RePEc; paywalled)
  - Anticipatory emotions plus imperfect memory make seemingly dominated strategies
    rational. Gives a resolution of Newcomb needing only a small weight on anticipation,
    and near-certain cooperation in the Prisoner's Dilemma. Nearest prior art for D1;
    a library copy is the top read.
- **Bodner, R. & Prelec, D. (2003).** Self-signaling and diagnostic utility in everyday
  decision making. In Brocas & Carrillo (eds.), *The Psychology of Economic Decisions*,
  vol. 1. **FT** · `papers/bodner-2003-self-signaling-and-diagnostic-utility.txt`
  - EDT-flavoured diagnostic utility. Discusses Newcomb experiments and naive versus
    sophisticated selves.
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
