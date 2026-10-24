You are an independent CODER in a scoping review of studies that integrate language models with explicit symbolic components. Every study in your batch is already included and already has a primary architecture code. Your task is a supplementary coding that records (1) what kind of contribution the paper makes and (2) every integration mechanism the paper's own system uses, not only the primary one.

RULEBOOK: /home/claude/nesy-llm-review/data/decisions/protocol_v2.md. Read the section "Coding axes", subsection "Architecture", for the definitions of A1-A7. Use those definitions.

BLINDING: Do NOT open, list or search any other file under /home/claude/nesy-llm-review: not data/, not other folders under work/, not tables/, sections/, *.bib or code/. You may open only the rulebook, your batch file and the viewer. Do not use the web.

INPUT: {BATCH} ({N} records). View with:  python3 /home/claude/nesy-llm-review/work/m8/show.py {BATCH} START END   (0-based, END exclusive; view about 15 records at a time.)

For every record, decide from the title and abstract:

1. contribution_type (exactly one):
   - method: the paper proposes a system, model, training method, algorithm or framework.
   - benchmark: the main contribution is a new benchmark, dataset or environment for evaluation.
   - analysis: the main contribution is an empirical evaluation or analysis of existing systems, without a new method and without a new benchmark as the main contribution.
   If a paper proposes both a benchmark and a method, choose what the abstract presents as the main contribution; when the two are equal, choose method.

2. mechanisms: ALL of the integration mechanisms below that the paper's own system or evaluation pipeline uses, as a semicolon-separated list in the order A1;A2;A3;A4;A5;A7 (leave empty if none applies). Judge each one independently, ignoring the decision-tree order:
   - A1: the model writes a formal representation and a symbolic engine computes the answer from it.
   - A2: a symbolic checker or executor returns verdicts or feedback on model outputs that select, repair, filter or reward candidates (at inference or in online training, including RL from checker feedback and proof search checked by a proof assistant).
   - A3: symbolic structure steers search, decoding, retrieval, decomposition or the training loss without giving a verdict on the output.
   - A4: the model writes rules, programs, predicates or modules that are stored and reused beyond a single query.
   - A5: a symbolic component creates training data, targets or a training signal offline, and the deployed model runs without it.
   - A7: a language or vision-language model grounds perception or verbalises output for a symbolic core that makes the decision.
   For benchmark and analysis papers, a symbolic system that only generates the test problems or grades the answers is NOT a mechanism; list a mechanism only if the paper's evaluated pipeline itself uses it (for example, a benchmark whose baselines all translate to a solver: A1).
   Do not list a mechanism that appears only in baselines or related work.

3. rationale: at most 20 words.

OUTPUT: write {OUT} with Python's csv module, one row per record in batch order, header exactly:
rid,contribution_type,mechanisms,rationale
Every record must have exactly one row. Check the row count against {N} before you finish.

FINAL REPLY (short): number of rows written, counts per contribution_type, and how many records list two or more mechanisms. Do not paste the table.
