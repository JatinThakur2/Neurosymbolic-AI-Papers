# Language Models Meet Symbolic Reasoning — Overleaf project and replication package

This is a PRISMA-ScR scoping review of how language models and explicit symbolic components are integrated in work at ten top-tier AI and NLP venues (AAAI, IJCAI, ICLR, ICML, NeurIPS, ACL, EMNLP, NAACL, TMLR, IEEE TPAMI; 2020–2026). It includes 659 studies. The package is version 2, revised after a referee report. `RESPONSE_TO_REVIEWERS.pdf` maps every referee point to a change.

## Use on Overleaf
1. Upload the zip: *New Project → Upload Project*.
2. Compiler: **pdfLaTeX**. Main file: `main.tex`. BibTeX runs automatically.
3. `supplement.tex` is a separate document listing all 659 included studies with their codes. To compile it, set it as the main document in Overleaf (Menu → Main document), or compile it locally.
4. One red **AUTHOR ACTION REQUIRED** box remains, in Section III-J. It disappears automatically once the human check below is done.

## Layout
```
main.tex, supplement.tex    paper and supplementary document
sections/                   00_abstract … 11_conclusion, A_appendix (PRISMA-ScR checklist, query, replication)
figures/                    TikZ / pgfplots sources (no image files)
tables/                     GENERATED: numbers.tex (\cnt{...} macros, \ifhumancheck), tables, query listings, supp_rows.tex
references_external.bib     background and method references (checked against Crossref)
references_studies.bib      GENERATED: 659 included + 12 related studies
data/decisions/             every reviewer decision; never written by the pipeline
  protocol_v2.md            the protocol
  screening/                two screeners + adjudication (union, snowball), recall-audit sample and decisions
  coding/                   two coders + adjudication
  webcheck/                 artifact-release web check (random sample + A7 census) and its design
  results/                  miniF2F results quoted from abstracts + comparability classification
  human_check/              blinded 30% sheets for the human verification (to be filled by the author)
  v1_pilot/                 decisions of the pilot version, kept for the pilot comparison
data/derived/               GENERATED: screening log, included studies, entities, analyses, plot data
docs/prompts/               the task prompts given to every LLM reviewer, verbatim, plus their viewers
code/                       the pipeline (below); code/v1_pilot/ holds the pilot scripts
```

## Regenerate everything (local machine)
```bash
bash code/search/fetch_sources.sh sources      # corpus + Paper Copilot + ACL Anthology at fixed commits
python code/run_all.py --sources sources       # Python 3.9+, poppler-utils; no third-party packages
```
The run checks that every record has exactly the decisions the procedure requires, and it regenerates every number, table and figure input. Re-upload `tables/`, `data/derived/` and `references_studies.bib` to Overleaf afterwards.

| Script | Stage |
|---|---|
| `s01_parse_corpus.py`, `s02_extract_text.py` | Source A records and local full text |
| `search/build_source_b.py`, `search/query.py`, `search/merge_sources.py` | Source B, the abstract-level query, the union |
| `s10_screen_union.py` | final screening decisions for the union |
| `search/snowball.py`, `search/audit_sample.py` | backward snowballing; stratified recall-audit sample (seeded) |
| `s11_selection.py` | screening log, agreement, recall estimate, pilot comparison |
| `s12_coding.py` | final codes, per-axis κ, entity agreement |
| `s13_analysis.py` | associations, period shares, growth panels, terminology control, artifacts, faithfulness, miniF2F |
| `s14_bib.py`, `s15_latex.py` | BibTeX; macros, tables, supplement rows, query listings |
| `human_check.py` | `--make` draws the 30% samples; `--score` scores them |

## What you still have to do before submission
1. **Human verification (required).** Every screening and coding decision was made by LLM agents. Fill the two sheets in `data/decisions/human_check/` yourself, applying `protocol_v2.md`, without looking at the LLM decisions:
   - `screening_sheet.csv` (751 records): put `include` or `exclude` in `decision` and an exclusion code E1–E5 in `code`;
   - `coding_sheet.csv` (198 studies): fill `architecture`, `check_strength`, `domain`, `formalism` and `faithfulness_reported`.
   Then run `python code/human_check.py --score` followed by `python code/s15_latex.py`, or the full `run_all.py`. Once at least 90% of each sheet is filled, the abstract, Section III-J and Section X switch automatically to report human–LLM agreement, and the red box disappears. If agreement is poor, revise the decisions you disagree with in `data/decisions/` and re-run.
2. **Push the replication package.** The Data Availability statement points to `https://github.com/JatinThakur2/Neurosymbolic-AI-Papers/tree/main/survey`. Merge the pull request that updates `survey/`.
3. **Model versions.** The LLM reviewers' model versions were not recorded for every batch. The paper says so. If you can recover them, add them to Section III-I.
4. **Venue.** The paper is journal length (about 14 pages plus references). Following the referee, TMLR, IEEE Access, *Artificial Intelligence Review* or the NeSy conference fit best. Check each venue's current policy on LLM-assisted reviewing before submitting.
5. **Bibliography.** The background and method references were checked against Crossref. The 671 study entries are generated from proceedings metadata; spot-check a sample against the venue pages.
