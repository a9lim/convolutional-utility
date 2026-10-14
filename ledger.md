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
