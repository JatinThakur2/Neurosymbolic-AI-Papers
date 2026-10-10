You are the CODING ADJUDICATOR in a systematic mapping study. Two independent coders coded each record in your batch and disagreed on at least one field. Decide the final value of every field.

RULEBOOK: /home/claude/nesy-llm-review/data/manual/protocol_v2.md. Read it first, especially "Coding axes", and apply it exactly. The architecture decision tree is applied IN ORDER (A6, A5, A1, A2, A4, A7, A3), stopping at the first yes. Key boundaries:
- A2 when a proof assistant, solver or executor checks model outputs and the verdict selects, repairs, filters or rewards candidates. This includes proof search over tactics checked by Lean or Isabelle, even when a value model guides the search.
- A3 only when the symbolic structure steers generation and gives NO verdict on the output.
- A1 is single-pass: the model writes a formal representation and the engine computes the answer.
- check_strength: exact = sound formal verdict on the model's final output; empirical = tests, execution, data fit, simulator, answer matching; none = no check of the final output. A1 pipelines are "none" unless the model's output is also checked.
- faithfulness_reported: yes/no/unclear only for A1/A2 studies whose model writes formal statements (formalisations, logic, specifications, logical forms); n/a otherwise.

INPUT: {BATCH}. View with: python3 /home/claude/nesy-llm-review/work/code2/show_adj.py {BATCH} START END (0-based, END exclusive; {N} records).
Each record shows the title, abstract, both coders' codes and rationales. Treat the rationales as arguments, not votes. Decide from the abstract and the protocol. If the abstract cannot settle the architecture, you may use WebFetch on the paper (arXiv, OpenReview, ACL Anthology, proceedings), at most about 6 fetches for the whole batch.

Do NOT open other files under /home/claude/nesy-llm-review except the protocol, your batch and the viewer.

OUTPUT: write {OUT} with Python's csv module, one row per record in batch order, header exactly:
rid,architecture,check_strength,domain,formalism,faithfulness_reported,evidence,rationale
Give the FINAL value for every field (copy the agreed value where the coders agreed). evidence: "abstract" or "web: <url>". rationale: at most 25 words on the disputed fields.

FINAL REPLY (short): how many records you changed from coder A's architecture, how many web fetches, and any record still genuinely doubtful (rid + one line). Do not paste the table.
