# Instructions for the second human rater

Thank you for helping. You are an independent second rater for a scoping review of how language models are combined with explicit symbolic components: solvers, provers, planners, interpreters, logic programs, grammars and similar. Your answers are compared with the author's. That comparison tells us how reliably two people apply the same rules.

**Time:** about 4–6 hours. You can split it across several sessions.

## Before you start
1. Read `../../protocol_v2.md` in full, especially the eligibility rules (I1–I4, E1–E5, R1–R6) and the coding axes.
2. **Work independently.** Do not discuss records with the author, and do not look at any other files in the replication package. That includes the AI reviewers' decisions and the author's own sheets.
3. Decide from the title and abstract. Open the paper (the `url` column) only when the abstract cannot settle the question, and note in `note` when you did.

## Sheet 1: `screening_sheet_rater2.csv` (150 papers)
For each row, fill in:
- `decision`: `include` or `exclude`.
- `code`: for an exclusion, the most fundamental failing reason, one of E1–E5 (for E3 you may add the rule, e.g. `E3 R4`). Leave it empty for an inclusion.
- `note` (optional): anything that made the decision hard.

The sample deliberately contains about as many papers the pipeline included as papers it excluded, so expect many borderline cases.

## Sheet 2: `coding_sheet_rater2.csv` (60 included studies)
For each row, fill in, using the codebook in the protocol:
- `architecture`: A1–A7. Apply the decision tree in its order: A6, A5, A1, A2, A4, A7, A3.
- `check_strength`: `exact`, `empirical` or `none`.
- `domain`: D1–D8.
- `formalism`: F1–F7.
- `faithfulness_reported`: `yes`, `no` or `unclear` for A1/A2 studies in which the model writes formal statements; `n/a` for all others.

## When you are done
Return both files to the author unchanged apart from the columns you filled in. Keep the column order, and do not re-sort the rows.
