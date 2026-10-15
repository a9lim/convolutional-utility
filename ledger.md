# Ledger

Periodically compacted to git history.

## 2026-10-12 — premise check

- Two parallel literature agents (economics; philosophy/psychology) verified and saved
  sources. Codex (gpt-6-astra) did an adversarial pass on the math sketch: gaslamp job
  `cx-20261012-230641-77eb`, thread `conv-utility-premise`.
- Codex caught two errors in the first sketch: finite-section spectral radius ≠ mass,
  and the unqualified sign claim in the ramp theorem. It also pointed to Bergstrom 1999 §5
  and Ray, Vellodi & Wang 2024 as direct precursors.
- Blocked and not circumvented: Dorsey 2015 (KU 403), SSRN and Chicago journals
  (Cloudflare), JET/JPET/JME closed copies, Slote (lending-only).
- Codex's full reply, with the closed forms in `formalism/core.md` P4–P6, is kept at
  `~/.gaslamp/jobs/cx-20261012-230641-77eb/reply.md`.

## 2026-10-13 — decision theory and anthropics

- a9 chose the hedonic reading.
- First draft of `decision.md` identified CDT/FDT with the mortality/eternity split.
  Codex (job `cx-20261013-000724-0a6a`, same thread) showed that this overreaches. The
  defensible split is fixed-past choice versus advance commitment, parametrized by `J`.
- Codex also pointed to Kőszegi 2010 as prior art for the savoring-trap mechanism, and
  supplied the exact stopping conditions now in D3 (checked over 1500 draws).
- `checks.py` caught an A2 limit error before review (the odds go to 0, not to 1:1).
- Walkthrough with a9, point by point. Decisions: the post's value is reframing for
  LessWrong, not novelty to economics; beliefs-are-welfare (D5) is the leading spine; D6
  is stronger than first written; measure-weighted anticipation is the anthropics stance;
  Sleeping Beauty (old A2) is cut. a9's P2 reading (direct and recursive as two readings
  of one agent) replaced "recursion has no content".
- Re-reading turned up the P6 size caveat (`≈ 4μ₁/T`) and the D3 exceptions as
  preemption; both checked.
- Two literature agents (economics; LessWrong and philosophy) covered D5's prior art.
  The economics pass corrected a claim made to a9 in chat: dread outweighing savoring,
  as a kernel on outcomes, does not price information in the direct model, because
  anticipation stays linear in beliefs. `checks.py` confirms it, and shows the recursive
  model does price it.
- Blocked and not circumvented: AEA PDFs, Eil & Rao, Bénabou & Tirole 2016, Good 1967,
  Buchak 2010, philsci-archive, Philosophers' Imprint, the old LessWrong wiki.
- Felt news (core N1–N3) and affect policies (D7) built and checked. A third literature
  agent found prior art for both: Gollier & Muermann 2010 and van Dijk et al. 2003 for
  N3's optimism/bracing condition, Pagel 2018 for affect policies, Soares 2015 as the
  LessWrong precedent. Downgraded both from "not found" to "known in kind".
- Built the interactive playground (`formalism/playground/`), checked against
  `pathwise.py`. Published as a private artifact for a9.
- A fourth literature agent found Kimball & Willis 2006 §8 to be the prior art for news
  over experienced utility, including the threshold. Its control-character cleanup touched
  15 existing reference files; it restored them by re-extraction, and three spot-checks
  matched their PDFs byte for byte.
- a9 raised the 2×2 (echoes × news); added to core with measured signatures.
- Canonicalized recursive echoes with recursive news as the main model (a9's suggestion);
  the direct form is presented as its reduced form. A full comparison of discounting
  schemes was started and dropped at a9's call once the tail result was clear (P1d).
- News kernel simplified to `ν δ^j` (a9's suggestion), matching the anticipation and memory
  kernels; Kőszegi & Rabin's `γ` kept as an extension. Calibration: inverting present bias
  shows recursion alone would need an echo share near 1, and standard news-utility
  calibrations sit past the recursive-news threshold.
- A fifth literature agent supplied calibration anchors. Felt and choice-revealed values
  differ: felt loss aversion is near 1–2 (choice: about 2–3), which dissolves the
  recursive-news threshold tension. The echo-share bill is set by patience, and
  experience sampling suggests positive echo is small, so present bias has sources beyond
  felt echo.
- Notation (a9): every kernel is Latin strength times Greek reach, `a·α^j`, `m·μ^j`, `n·ν^j`;
  the first moment became `M₁`, the gain-loss function `φ_λ`, felt news `N_t`. Code renamed
  to match; checks output identical apart from labels.
- a9 proposed three natural horizons: a waking day, a full life, an LLM's context window
  (a9's wife is studying the peak-end effect in LLMs). Added to core calibration.
- Plan (a9): the model ships as a standalone post first; decision theory and the LLM
  peak-end study become follow-ups. a9 extended the horizons to a 2×2 (human/LLM ×
  short/long, soft/hard boundaries) and read compaction as a change of agent with memory
  and anticipation held across; recorded with the Parfit mapping (connectedness = direct
  kernel, continuity = resolvent).
- Pre-writing lookover for Post 1 (a9): canonical audit, Codex round 3, a prior-art pass,
  calibration.
  - Codex round 3 (gpt-6-astra) found no broken calculation in the echo math but several
    overclaims, all adopted. The forecast convention was never stated (`pathwise.py` used
    surprise-only forecasts, the N4 checks Bayesian ones). The reduced form holds only for
    foreseen lives, because a surprise misses the anticipation paths. "Bad news has no felt
    state, good news two" holds only just past the threshold, and the second state is
    unstable. P1(d) and the context-window bullet confused finite-life existence with
    uniform boundedness. Batching is not unconditional. Peak-end weights are resolvent
    rows. `pathwise.py`'s bisection could miss its bracket; replaced by exact roots, with
    output unchanged to 5e-15.
  - New, checked: the half-line threshold `κ = (n/H)(1−νμ)/(1−νq)` (Codex verified it
    independently); N3 in the canonical model, where a calibrated Bayesian is already
    braced and the loop amplifies loss aversion; D5's exact identity, with the straddle
    condition and rumination pricing information too.
  - Prior art: Andries & Haddad 2020 and Dillenberger 2010 have the recursive-kink
    mechanism behind clumping, in ex-ante form; dread-of-dread is a concave Kreps–Porteus
    aggregator in structure; Sáez-Martí & Weibull's eqs. 15–17 are the calibration
    inversion; Pagel's `γβ^τ` is the news kernel; Kimball & Willis's `θψ < 1` is a
    sufficient condition with `ψ` a processing factor; Lim et al. 2020 has
    recency-without-peak from linear fading. Corrected: Cosaert & Potoms grid-searched
    their parameters rather than estimating them; Pagel 2017's text and table differ.
  - Calibration: default sets for a waking day and a life. Echo is about 30% of
    experience, and the momentary felt row is nearly myopic (`β ≈ 0.06`).
  - The first literature agent died at its first step on an API filter error and was
    relaunched with a leaner brief.
  - Codex round 3b verified canonical N3 (adding `W″ < 0`: the interior optimum is global)
    and D5's identity, and caught the new root finder missing a root on an interval's end
    (fixed, with regression checks), "bounded gain-loss gives bistability" (only over a
    range of shocks), degenerate mixed revisions with a continuum of roots, a reveal time
    after realization in the D5 check, and "deep bracing" near the threshold (it is the
    felt reference that sinks, not the belief bias). The anticipation anchors give
    lag-specific weights, not masses, so the defaults are illustrative; the peak-end row
    identifies memory's primitives but not anticipation's.
  - The retried agent found Bernheim & Thomadsen's 2004 draft: partial prior art for D1
    (anticipation felt after the choice, dependence through self-inference). Bergstrom 1999
    has only the nearest-neighbour case, so P4 stands; Hori 1992 stayed paywalled.
- a9 agreed with rational forecasts as canonical and offered academic access for paywalled
  texts (list in `next-steps.md`, drop folder `references/inbox/`). a9 proposed folding the
  decision-theory post into the model post, and an extension: training an agent to choose
  its own expectations to maximize its felt utility, as an observer or in games.
- Plan (a9): one merged flagship post (model, a life, beliefs, choices, selves), with the
  formalism as a technical companion; the spine is "experience echoes". Outline
  restructured into acts. Next: the decision-theory audit, then the observer model.
- Decision-theory audit under the canonical model. A deviation from the plan past selves
  predicted is felt as news, so choice needs a credible-plan concept; Kőszegi & Rabin 2009
  (eq. 5, Prop. 5) already have own-deviation news and the plan as its own commitment
  device, so the choice side adopts their preferred credible plan, credited, for a
  means-based model with recursive news. Results: D2's deviation weights with news; the
  savoring trap fragile under felt news; D6 reversed (echoes make selves over-reliable,
  news can make them flaky). Codex round 4 corrected the D3 credibility test (it omitted
  replanning between credible continuations; with the full recursion the felt-calibration
  figure is 66%, not 78%), the "exact KR identification", "no news on the equilibrium
  path", A1's "unless affect is updateless", a decaying-kernel claim that fails for `ν`
  near 1, and a root-finder precision bug. A literature agent found the stop-gradient /
  CDT, full-flow / EDT mapping published (Oesterheld et al. 2023), and that a lagged
  self-predictor does not grade `J`.
- The canonical self is a learner that feels its own critic: anticipation is `a(V^α − e)`,
  linear news `(n/ν)` times a TD error. At felt calibrations, free beliefs go to N3's
  corners, so the observer needs a tether (question to a9).
- Built the observer (`experiments/learned_expectations/`): beliefs chosen for felt welfare
  under a KL cost of self-deception (a9's pick). Closed-form and differentiable, checked
  against an independent tree solver. Optimal paths at the life calibration stay calibrated
  far out, brace as the event nears and freeze at the end, for good, risky and bad events
  alike. The objective's kinks at zero revisions stalled L-BFGS (beliefs are sticky); Adam
  from several starts works. A network trained for two minutes captures a median 71% of the
  exact gain on held-out events.
- Overnight (a9 asleep, standing go-ahead): built the scheduling agent (the `J` dial as a
  gradient setting reproduces fixed-past and commitment play; graded `w` gives a staircase),
  the game agent (random 2×2 games; the twin dial reproduces causal against evidential play,
  graded `w` matching analytic thresholds), the hidden-game agent (a felt critic: rosy or
  braced by `aν` against `nλ(1−ν)`, play unchanged; a braced critic unexpectedly improves
  play through the shared state) and the credible-plan selection study (learning picks the
  earliest credible plan). Bugs found and fixed on the way: an off-by-one initialization that
  saturated a logit, Adam stalls on saturated sigmoids (fixed by preconditioning each self's
  gradient by reach and slope), and a coupled-game variant that trained against the wrong
  opponent policy.

## 2026-10-14 — the braced critic, anticipated news

- Anticipated news: the scheduling agent now solves the canonical model exactly (Bayesian
  forecasts over the worlds, sign iteration on the news terms), replacing a version whose
  forecasts left anticipated news out (git `c51a53e`). Fixed-past selection was unchanged seed
  for seed. The planner reached commitment 73% against 60%: those forecasts were rosier than
  rational, and randomizing away from a plan cost less with rational ones in 84% of directions.
- The braced critic, deflated and replaced. The "braced critic raises payoffs" result compared
  braced runs against a single honest seed that happened to stay on the complacent plateau;
  with seeds, honest critics escape 7/8 or 9/10 times. What holds: critics above realized
  payoffs (rosy, offsets, high expectiles) keep the agent complacent, through the shared
  state. Codex (thread `braced-critic`, jobs `cx-20261014-111752-a3aa`,
  `cx-20261014-122058-edaf`) showed that at `λ = 1` motivated training equals a fixed offset
  exactly, that an offset supplied outside the network gives honest gradients (so the network
  learning the bias is the intervention), and proposed the value/stay coupling, which the
  alignment measurement supports. Its centering test, verified for routing, stopped even the
  honest critic from escaping; left open.
- Not optimism but level: an honest critic of rewards shifted by +0.5 for the learners only
  (inputs and the policy's gradient unchanged) stays complacent 6/6, shifted by −0.5 escapes
  6/6, so the shared state carries the critic's absolute level, and "rosy" was a proxy for
  "high". Through the policy's baseline instead (Chung et al. 2021, verified), the level did
  nothing detectable at batch 2048.
- Lesson kept: learned-agent comparisons need seeds. The game agent's equilibrium-selection
  result is next in line for the same check.
- a9 asked which extensions I find exciting. My picks: optimism through the decision rule
  versus the shared state; fitting the model to momentary-happiness data; evolving felt
  parameters, in that order.

## 2026-10-14 (later) — D8, evolution, the data question

- a9 picked three extensions: evolving felt parameters, fitting momentary-happiness data,
  and a theorem. D8 states the shared-state mechanism (cross tangent kernel; linear-model
  forcing `(s·v)[μ/(1+‖v‖²) + f̃/‖v‖²]`; head alignment `αβ/σ` at the balanced rank-one
  factorization). Codex (thread `braced-critic`, job `cx-20261014-153455-dedc`) narrowed it:
  the forcing is the endpoint of critic-only fitting with heads frozen, (c) is a regression
  illustration and not a theorem about REINFORCE, the Adam caveat restated. Its prediction
  held: a critic whose level is kept outside the network ignores a reward shift.
- A literature agent found the effect known only in kind: Sun et al. 2022 (same sign, through
  learned Q-values), value-policy interference (Cobbe et al. 2021), plateaus from interference
  (Schaul et al. 2019).
- Evolution, first as population-based training (weights copied with parameters): when
  affect drives the policy, selection shrank it overall. Replaced by generational evolution
  (born untrained, weights not inherited), which separates the components: against
  anticipation, for news, indifferent to loss aversion.
- Data: a search agent found open trial-level datasets (the Great Brain Experiment smartphone
  data, CC0, 87.5 MB; Forbes & Bennett 2024 on OSF). Downloads await a9's go-ahead. Forbes &
  Bennett already report negative prediction errors moving affect and positive ones not.
- a9 cleared downloads. The Great Brain Experiment archive (Zenodo, MD5 checked) and Forbes &
  Bennett's CSVs (OSF, sizes checked) are in gitignored `data/`. First fits: Rutledge's model
  replicates (`γ = 0.72`); the recursive kernel wins on held-out participants. Caught before
  reporting: within gain-only and loss-only trials a gamble's EV equals the size of its RPE, so
  splitting RPE by sign within trial type was a choice of basis; that model is out, and `λ`
  waits for a mixed-trial analysis.

## 2026-10-15 — unfinished business

- a9 parked the Bates-world learner as its own future project (in `next-steps.md`). I had said
  it was noted there before it was; it is now.
- Happiness data: a bug, caught while writing the Forbes loader. Each GBE play's first rating
  comes before trial 1, but the fit had given it trial 1's outcome. Fixed (`gbe.design`); the
  kernel moved from `κ 0.45, γ 0.90` to `κ 0.41, γ 0.89`, `m` from 1.00 to 0.86, and the
  geometric's `γ` from 0.72 to 0.68. `λ` identified structurally from mixed gambles: 1.42.
  Forbes & Bennett reproduce the kernel in both experiments.
