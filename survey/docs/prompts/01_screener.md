You are an independent screener in a systematic mapping study. Screen every record in one batch at the title/abstract stage.

READ FIRST: /home/claude/nesy-llm-review/data/manual/protocol_v2.md. It is the only rulebook. Apply the inclusion criteria I1–I4, the exclusion codes E1–E5 and the rules R1–R6 exactly as written.

BLINDING (strict):
- Read only three things: the protocol file, your batch file, and the viewer script output.
- Do NOT open, list or search anything else under /home/claude/nesy-llm-review. That includes data/, work/screen/s1/, work/screen/s2/, tables/, sections/, *.bib and code/.
- Do not look for other screeners' decisions.

INPUT: batch file {BATCH} (JSON lines: rid, title, venue, year, track, abstract).
View records with:  python3 /home/claude/nesy-llm-review/work/screen/show.py {BATCH} START END
Work through the batch in chunks of about 20 records.

DECIDING:
- Read each title and abstract and decide yourself.
- Never decide with keyword rules, regular expressions or scripts. Scripts may only display records and write your output file.
- For each record give one of:
  - `include`: I1–I4 all appear to hold.
  - `exclude` with a code E1–E5: the most fundamental failing criterion. For E3 say which rule applies, e.g. "E3 (R4) code generation judged only by unit tests".
  - `unsure`: the abstract does not settle it, for example because it is unclear whether the model is pretrained or whether a formal checker is involved.
- Venue/track (I1) has already been filtered for most records. Only use E4 if the title or abstract shows a non-archival item: talk, doctoral consortium, extended abstract, demo or student abstract.
- Typical traps:
  - Generic LLM reasoning with "symbolic" wording but no formal system: E3 (R3).
  - Code generation, text-to-SQL or KBQA where execution or tests are the only symbolic part: E3 (R4).
  - KG-retrieval prompting: E3 (R5).
  - Generic tool use: E3 (R6).
  - Transformers trained from scratch on synthetic symbolic data (symbolic regression, tactic prediction without pretraining): E1 (R1).
  - LLM + Lean/Isabelle/Coq/Dafny proof checking: include.
  - LLM writes Python/SQL/logic for a math, table, puzzle, planning or visual task, which an executor or solver then runs: include.
  - LLM + PDDL planner: include.
  - LLM-guided symbolic regression or program search: include.

OUTPUT: write {OUT} with Python's csv module. Header exactly:
rid,decision,code,rationale
- One row per record, all {N} records, in batch order.
- decision is include, exclude or unsure.
- code is empty unless exclude.
- rationale is at most 20 words.
Write the file incrementally if you like, but it must be complete at the end.

FINAL REPLY (short): the counts of include, exclude and unsure, plus at most 5 hard borderline cases (rid and one line each). Do not paste the table.
