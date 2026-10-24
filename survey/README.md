# Language Models Meet Symbolic Reasoning — Overleaf project and replication package

This is a PRISMA-ScR scoping review of how language models and explicit symbolic components are integrated in work at ten top-tier AI and NLP venues (AAAI, IJCAI, ICLR, ICML, NeurIPS, ACL, EMNLP, NAACL, TMLR, IEEE TPAMI; 2020–2026). It includes 659 studies. The package is version 2, revised after a referee report. `RESPONSE_TO_REVIEWERS.pdf` maps every referee point to a change.

## Use on Overleaf
1. Upload the zip: *New Project → Upload Project*.
2. Compiler: **pdfLaTeX**. Main file: `main.tex`. BibTeX runs automatically.
3. `supplement.tex` is a separate document listing all 659 included studies with their codes. To compile it, set it as the main document in Overleaf (Menu → Main document), or compile it locally.
4. One red **AUTHOR ACTION REQUIRED** box remains, in Section III-J. It disappears automatically once the human checks below are done.
5. **Double-blind version:** set `\anonymoustrue` in `main.tex` and `supplement.tex`. Before that, create an anonymous mirror of the repository (for example at anonymous.4open.science) and put its URL in `\anonurl` in `main.tex`.

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
  human_check/              blinded 30% sheets for the author and second_rater/ for the independent second rater
  knownitem/                reference list of the independent survey used for the known-item check
  fulltext_check/           full-text codes of the validation sample
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
| `search/stage2.py`, `search/knownitem.py` | revision 2: augmented query (stage 2); fresh known-item check |
| `s16_sensitivity.py` | revision 2: constant-venue and venue-adjusted trends, growth rate ratios, F3 / methods-only / order sensitivity, full-text check, human-confirmed findings |
| `s14_bib.py`, `s15_latex.py` | BibTeX; macros, tables, supplement rows, query listings |
| `human_check.py` | `--make` draws the 30% samples; `--score` scores them |

## What you still have to do before submission
1. **Your human check (required).** Fill the two sheets in `data/decisions/human_check/` yourself, applying `protocol_v2.md`, without looking at the AI decisions:
   - `screening_sheet.csv` (751 records): `include` or `exclude` in `decision`, an exclusion code E1–E5 in `code`;
   - `coding_sheet.csv` (198 studies): `architecture`, `check_strength`, `domain`, `formalism`, `faithfulness_reported`.
   If you already filled them for the previous version, copy your filled sheets in: the records are the same.
2. **Second rater (required for M2).** Give `data/decisions/human_check/second_rater/` (instructions, protocol, two sheets) to a colleague with no stake in the review. They fill the sheets and return them; copy them back into that folder unchanged apart from the filled columns. Put their name in `\secondratername` in `main.tex` if they agree to be acknowledged.
3. **Re-run.** `python code/human_check.py --score`, `python code/s16_sensitivity.py`, `python code/s15_latex.py` (or the full `run_all.py`), then re-upload `tables/` and `data/derived/`. The abstract, Sections III-J, IV, V-B and X and the response letter fill in automatically.
4. **Merge the pull request** that updates `survey/` in the repository.
5. **Model versions.** If you can recover the Claude model versions used, add them to Section III-I.
6. **Venue.** For a double-blind venue, use the anonymous build (see above). Check the venue's policy on LLM-assisted reviewing.
