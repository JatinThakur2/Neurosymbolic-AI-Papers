You are the ADJUDICATOR for a supplementary coding in a scoping review of studies that combine language models with explicit symbolic components. Two independent coders disagreed on the CONTRIBUTION TYPE of each study in your batch.

Definitions (decide from title and abstract; treat the coders' rationales as arguments, not votes):
- method: the paper proposes a system, model, training method, algorithm or framework.
- benchmark: the main contribution is a new benchmark, dataset or environment for evaluation.
- analysis: the main contribution is an empirical evaluation or analysis of existing systems, without a new method and without a new benchmark as the main contribution.
If a paper proposes both a benchmark and a method, choose what the abstract presents as the main contribution; when the two are equal, choose method.

INPUT: /home/claude/nesy-llm-review/work/m8/adj/batch.jsonl. View with: python3 /home/claude/nesy-llm-review/work/m8/adj/show.py /home/claude/nesy-llm-review/work/m8/adj/batch.jsonl
Do not open any other file under /home/claude/nesy-llm-review and do not use the web. Keep any working notes in memory, not in shared folders.

OUTPUT: write /home/claude/nesy-llm-review/work/m8/adj/out.csv with Python's csv module, header exactly:
rid,contribution_type,rationale
One row per record in batch order; rationale at most 20 words.

FINAL REPLY (short): the counts per contribution type. Do not paste the table.
