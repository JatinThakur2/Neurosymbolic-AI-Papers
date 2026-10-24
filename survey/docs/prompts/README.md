# Prompts given to the LLM reviewers

These are the task prompts used in the review, released verbatim. Every agent also received
`data/decisions/protocol_v2.md` as its rulebook. When the review was run, that folder was named
`data/manual/`, which is why the prompts refer to `data/manual/protocol_v2.md`. Placeholders such as
`{BATCH}`, `{N}`, `START` and `END` were filled in per batch.

| File | Stage | Output files |
|---|---|---|
| `01_screener.md` | Title/abstract screening by two independent screeners (union, snowball candidates, recall audit) | `data/decisions/screening/union_screener_{A,B}.csv`, `snowball_screener_{A,B}.csv`, `audit_screener_A.csv` |
| `02_screening_adjudicator.md` | Adjudication of every conflict or `unsure` | `data/decisions/screening/*_adjudication.csv` |
| `03_coder.md` | Data charting by two independent coders | `data/decisions/coding/coder_{A,B}.csv` |
| `04_coding_adjudicator.md` | Adjudication of every study with any coding disagreement | `data/decisions/coding/adjudication.csv` |
| `05_artifact_webcheck.md` | Web check of author-released code, models or data | `data/decisions/webcheck/artifact_release.csv` |
| `06_minif2f_extractor.md` | Extraction of miniF2F results stated in abstracts, with quotes | `data/decisions/results/minif2f_extraction.csv` |

`viewers/` holds the small scripts the agents used to display their batch (one record at a time:
title, venue, year, abstract and link). Blinding rules are stated at the top of each prompt: a reviewer
saw only the protocol, its prompt, its batch and the viewer, never another reviewer's output
(adjudicators excepted, who saw both decisions and rationales by design).

The agents were instances of Anthropic Claude models; model versions were not recorded for every batch
(see the paper, Sections III-I and X).

## Revision 2 (second referee report)

| File | Stage | Output files |
|---|---|---|
| `07_screener_revision2.md` | Screening of stage-2 records, the recall audit (second screener) and its extension, and the known-item records (the protocol path is `data/decisions/`) | `screening/search2_screener_{A,B}.csv`, `audit_screener_B.csv`, `audit_ext_screener_{A,B}.csv`, `knownitem_screener_{A,B}.csv` |
| `02_screening_adjudicator.md` | Adjudication in revision 2 used the same prompt, with the protocol path updated | `screening/search2_adjudication.csv`, `audit_ext_adjudication.csv`, `knownitem_adjudication.csv` |
| `03_coder.md`, `04_coding_adjudicator.md` | Coding of the studies included in revision 2 | appended to `coding/coder_{A,B}.csv`, `coding/adjudication.csv` |
| `08_supplementary_coder.md` | Contribution type and all applicable mechanisms (two coders) | `coding/secondary_coder_{A,B}.csv` |
| `09_contribution_adjudicator.md` | Adjudication of contribution-type disagreements | `coding/secondary_adjudication.csv` |
| `10_fulltext_coder.md` | Full-text check of check strength and faithfulness reporting | `fulltext_check/fulltext_codes.csv` |

Placeholders (`{BATCH}`, `{N}`, `{OUT}`, `{TAG}`) were filled per batch. Agents shared a scratchpad directory; from the second batch onwards prompts told them to use private file names, and every output was checked against its batch (row count, record order).
