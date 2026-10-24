You are a FULL-TEXT CODER in a scoping review of studies that combine language models with explicit symbolic components. Every study in your batch is included and uses a translate-and-solve (A1) or checker-in-the-loop (A2) design. Your task is to code two attributes from the FULL TEXT of each paper, not from the abstract.

RULEBOOK: /home/claude/nesy-llm-review/data/decisions/protocol_v2.md. Read the sections "Check strength" and "Further extracted fields" (faithfulness_reported).
Do not open any other file under /home/claude/nesy-llm-review except the rulebook, your batch file and the viewer.

INPUT: {BATCH} (20 records). View with: python3 /home/claude/nesy-llm-review/work/fulltext_check/show.py {BATCH}

For every record, obtain the full text with WebFetch: arXiv (search the title; use https://arxiv.org/abs/<id> or the HTML version https://arxiv.org/html/<id>), OpenReview (https://openreview.net/pdf?id=<id>), the ACL Anthology (URL + ".pdf") or the proceedings page. Ask WebFetch pointed questions, for example: "Does a symbolic component (prover, solver, interpreter, test suite, simulator) check the model's FINAL output, and is that check a sound formal verdict or an execution/test/data-based check? Does the paper report the accuracy or faithfulness of the model-written formal statements (formalisation accuracy, translation accuracy, semantic equivalence) separately from end-task accuracy? Quote the relevant sentences."

Code:
- check_strength: exact (sound formal verdict on the final output: proof assistant, solver-checked certificate, model checker, type-checked formal statement) | empirical (tests, execution results, fit to data, simulator success, answer matching) | none (no symbolic check of the final output).
- faithfulness_reported: yes | no | n/a. n/a when the model does not write formal statements (logic, formal specifications, theorem statements, logical forms, planning domains); executable programs whose output is just run are n/a. yes when the paper reports formalisation accuracy or faithfulness separately from end-task accuracy anywhere in the paper (main text or appendix).
- source: the URL you read, or "abstract only" if no full text could be obtained (then code from the abstract and say so).
- quote: at most 30 words from the paper supporting your codes.

OUTPUT: write {OUT} with Python's csv module, one row per record in batch order, header exactly:
rid,check_strength,faithfulness_reported,source,quote
Other agents share the session scratchpad: keep notes in memory or in files whose names include '{TAG}'.

FINAL REPLY (short): rows written, how many full texts obtained, counts per check_strength and faithfulness_reported. Do not paste the table.
