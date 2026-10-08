# Replication package — *Language Models Meet Symbolic Reasoning: A PRISMA-Guided Systematic Mapping of Neurosymbolic Integration at Top-Tier AI Venues (2020–2026)*

This folder reproduces every count, table and figure-data file in the survey. It draws on the 391 records of this repository (AAAI, ICLR, ICML, IJCAI, NeurIPS, TMLR, TPAMI; 2020–2026).

**Result in one line:** 391 records were identified. After removing 4 duplicates, 387 were screened and 97 assessed for eligibility; **73 studies** were included. Two independent, blinded screeners reached Cohen's κ = 0.77 (91.8% raw agreement).

## Reproduce
```bash
cd survey
python code/run_all.py --repo ..        # Python 3.9+, poppler-utils (pdftotext); no pip packages
```
Extracted PDF text goes to `survey/work/`, which is git-ignored. Every other output is overwritten in place, so `git diff` after a run shows whether anything changed.

## Contents
| Path | What it is |
|---|---|
| `data/manual/` | **Human/assistant decisions. The scripts read these and never write them.** `eligibility_decisions.csv` (all 97 candidates, with reason codes and evidence), `first_screener_pre_resolution.csv`, `second_screener_ai.csv`, `second_screener_resolution.csv`, `consistency_recheck.csv`, `title_review_additions.csv`, `coding.csv`, `taxonomy_codebook.csv`, `code_availability.csv`, `indicator_spotcheck*.csv` |
| `data/derived/` | Generated: `screening_log.csv` (one row per record with stage, decision and reason), `included_studies.csv`, `indicators_long.csv`, PRISMA counts and plot data |
| `code/` | Pipeline `s01`–`s07` and `run_all.py`; `agreement_kappa.py` for a further (human) screener; `identification/` holds a re-implementation of this repository's title classifier and its replay over the corpus |
| `tables/`, `figures/` | Generated LaTeX fragments and TikZ/pgfplots figure sources used by the paper |
| `references_*.bib` | Bibliography of the included and related studies |

## Change a decision
Edit the relevant CSV in `data/manual/` and re-run `run_all.py`. The scripts stop with an error if a candidate lacks a decision or an included study lacks a code.

## Add a human second screener
```bash
python code/agreement_kappa.py --make-sheet          # writes a blinded, shuffled sheet
# a colleague fills data/manual/second_screener_sheet.csv
python code/agreement_kappa.py                        # prints kappa and every disagreement
```

## AI-assistance disclosure
Several parts of this work were done with AI models (Claude, Anthropic):

- **First pass:** first-pass screening, eligibility decisions, coding, artifact-availability judgements and indicator spot-check verdicts.
- **Second screener:** an independent, blinded instance of a different Claude model.
- **Code:** the pipeline.

Every decision is released here so that it can be audited or overturned.
