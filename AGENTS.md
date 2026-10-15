# AGENTS.md

## What this is

A research project formalizing *convolutional utility*: experienced utility as base utility
convolved with a two-sided kernel — felt anticipation forward, felt memory backward,
optionally recursive (anticipated memories, remembered anticipations, and so on). The
project takes the hedonic reading: anticipation and memory are experiences, and welfare is
the life-sum of experienced utility. The questions are when the model is well-founded, and
what it implies for the shape of a life, discounting, decision theory (CDT/EDT/FDT),
utilitarian aggregation, and anthropics. Target: a LessWrong post.

## Map

- `README.md` — the working abstract and the landing page
- `outline.md` — **the authoritative writeup**
- `bibliography.md` — the annotated bibliography
- `ledger.md` — periodically compacted optional records (older entries stay in git history)
- `next-steps.md` — the working plan
- `formalism/` — proofs and formalization; `formalism/INDEX.md`
  is the manifest
- `experiments/` — data fits (`happiness/`) and learned agents (`learned_expectations/`),
  each with a README; `data/` holds the downloaded datasets (gitignored)
- `notes/` — ephemeral drafting sketches; distilled into the core docs, then deleted
- `references/` — the local project references; `references/INDEX.md`
  is the manifest

## How to work here

**Keep docs live.** No need for historical changes and notes; if something about the process
was meaningful, use `ledger.md` and git history. Try not to narrate changes in the core docs.

**Verify citations.** Every `bibliography.md` entry should be read by at least one agent and
verified at some point. Copies of verified texts should live in `references/`, txt or md
preferred.

**Review when unsure.** Codex is accessible via `gaslamp`, and it's always good to get a
different pair of eyes on an argument or a proposition.

**Authorship.** I'll write every published artifact myself, so prefer bullet points to prose
when scaffolding the final piece.
