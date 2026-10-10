You are an independent CODER in a systematic mapping study of studies in which a language model and an explicit symbolic component interact. Every record in your batch has already been judged eligible. Your job is to code each one.

RULEBOOK: /home/claude/nesy-llm-review/data/manual/protocol_v2.md. Read it first, especially "Coding axes". It is the only rulebook.

BLINDING (strict):
- Read only three things: the protocol file, your batch file, and the viewer script's output.
- Do NOT open, list or search anything else under /home/claude/nesy-llm-review. That includes data/, work/ (except your batch and the viewer), tables/, sections/, *.bib and code/.
- Do not look for other coders' outputs. Do not use the web.

INPUT: batch file {BATCH} (JSON lines: rid, title, venue, year, abstract).
View records with: python3 /home/claude/nesy-llm-review/work/code2/show.py {BATCH} START END
Indexes are 0-based and END is exclusive. There are {N} records; view about 10 at a time.

CODE EACH RECORD FROM ITS TITLE AND ABSTRACT ONLY. Decide each code yourself by reading. Never assign codes with keyword rules or scripts; scripts may only display records and write your output file.

Fields:
1. **architecture.** One of A1–A7. Apply the protocol's decision tree IN ORDER and stop at the first yes (A6, A5, A1, A2, A4, A7, A3). Key boundaries:
   - If a proof assistant, solver or executor checks the model's outputs and the verdict selects, repairs, filters or rewards candidates, that is A2. This holds even when a learned value model or heuristic guides the search, and it covers tree search over tactics checked by Lean or Isabelle.
   - A3 is only for symbolic structure that steers generation and gives NO verdict on the output.
   - A1 is a single pass: the model writes a formal representation and the engine computes the answer, with no iterative checking.
2. **check_strength.** exact | empirical | none, as defined in the protocol.
   - exact: proof assistant, solver-checked certificate, model checker.
   - empirical: tests, execution results, fit to data, simulator success, answer matching.
   - none: the symbolic part never checks the final output.
   - An A1 pipeline whose engine computes the answer from the model's formalisation is "none": the engine computes but does not check the model's work. Use "exact" only for a check of the model's output.
3. **domain.** D1–D8.
4. **formalism.** F1–F7: the main symbolic representation the method manipulates.
5. **lm_named.** The language models named in the abstract, semicolon-separated, as written (e.g. "GPT-4; Llama-2-7B"). Empty if none are named.
6. **engine_named.** The symbolic engines or tools named (e.g. "Lean 4; Z3"). Empty if none.
7. **benchmarks_named.** The benchmarks or datasets named (e.g. "miniF2F; ProofNet"). Empty if none.
8. **faithfulness_reported.**
   - For A1/A2 studies whose model writes formal statements (formalisations, logic, specifications), answer yes, no or unclear, from the abstract only. "yes" means the abstract reports formalisation or translation accuracy or faithfulness separately from end-task accuracy.
   - Otherwise answer n/a.
9. **confidence.** high | medium | low, for the architecture code.
10. **rationale.** At most 25 words, explaining the architecture code.

OUTPUT: write {OUT} with Python's csv module. One row per record, all {N} records, in batch order. Header exactly:
rid,architecture,check_strength,domain,formalism,lm_named,engine_named,benchmarks_named,faithfulness_reported,confidence,rationale

FINAL REPLY (short): counts per architecture code, and at most 5 records where the code was hardest (rid and one line each). Do not paste the table.
