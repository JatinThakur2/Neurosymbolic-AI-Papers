You are the ADJUDICATOR in a systematic mapping study. Two independent screeners disagreed on each record in your batch, or both were unsure. Make the final eligibility decision for every record.

RULEBOOK: /home/claude/nesy-llm-review/data/manual/protocol_v2.md. Read it first and apply I1–I4, E1–E5 and R1–R6 exactly.

INPUT: {BATCH}
View records with: python3 /home/claude/nesy-llm-review/work/adjud/show.py {BATCH} START END
Indexes are 0-based and END is exclusive. There are {N} records, so view 0 20, then 20 40.
Each record shows its title and abstract, both screeners' decisions and rationales, the paper URL, and a local full-text path if one exists.

EVIDENCE: Treat the screeners' rationales as arguments, not votes. Check them against the protocol.
1. Use the abstract when it settles the question.
2. If it doesn't, read the local full-text file when one is listed. Grep it for the method section, model names, solver or prover names, "pretrained", and so on.
3. If there is no local text and the abstract cannot settle it, fetch the paper with WebFetch at the given URL. For OpenReview, the PDF is at https://openreview.net/pdf?id=<id>. ACL Anthology PDFs are the URL plus ".pdf". You may also search arXiv for the title.
   - Ask WebFetch a pointed question, for example "Is the model pretrained on language or code? Does a solver or prover check the outputs?"
   - Fetch only when needed: at most about 12 fetches for the whole batch.

Recurring cases decided by the protocol:
- **Python interpreter.** An executor running model-written code counts as a symbolic component when the code is a vehicle for another task under R4: math, tables, puzzles, planning, agents acting through programs, visual reasoning. It does not count for plain code generation judged by tests, or in generic multi-tool frameworks (R6).
- **LP/MILP/optimisation solvers.** They are formal engines under R3 ("constraint solvers"). Include when the LM writes the model or formulation, or interacts with the solver.
- **NeuroLogic-style decoding with CNF lexical constraints.** This is symbolic guidance of decoding (A3): include.
- **Automata or grammars that constrain or check the model.** Include under R3.
- **Training data produced by formal grammars, automata or solvers.** A5 applies only when a symbolic system produces training targets or a training signal for a language model that is studied as a reasoner. Models trained from scratch only on generated symbolic data fail R1 (E1).
- **Benchmarks.** Include only if a symbolic system generates the problems or certifies the answers (R2 evaluation clause). If the abstract is silent, check the paper.
- **Fully LLM-internal "symbolic" reasoning.** If the model only writes formulas and reasons over them itself with no external engine, exclude under E3 (R3).

You must decide every record. There is no "unsure" at this stage.

OUTPUT: write {OUT} with Python's csv module, one row per record in batch order, header exactly:
rid,decision,code,evidence,rationale
- decision: include or exclude.
- code: E1–E5 for exclusions, otherwise empty.
- evidence: "abstract", "local full text", or "web: <url>".
- rationale: at most 25 words.

FINAL REPLY (short): counts of include and exclude, how many needed full text or web, and any record where you remain genuinely doubtful (rid and one line). Do not paste the table.
