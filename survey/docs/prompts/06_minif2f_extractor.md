You extract REPORTED RESULTS from paper abstracts for a systematic review. Use ONLY the abstract text given. Do not use the web. Do not read other files.

INPUT: {BATCH} (JSON lines: rid, title, venue, year, architecture, abstract). There are {N} records. View them with: python3 -c "import json,sys;[print(i,r['rid'],r['year'],r['title'],'\n',r['abstract'],'\n') for i,r in enumerate(map(json.loads,open('{BATCH}')))]"

For each record, find whether the abstract reports a numeric result on the miniF2F benchmark (test split, or valid if only that is given).

OUTPUT: write {OUT} with Python's csv module, header exactly:
rid,minif2f_reported,split,score_pct,attempts,proof_language,model,quote
- minif2f_reported: yes | no
- split: test | valid | unspecified | (empty if no)
- score_pct: the method's headline miniF2F number in percent as stated (e.g. 52.0). If several numbers are given, take the paper's own best method's main number. Empty if none.
- attempts: the sampling budget as stated (e.g. "pass@32", "pass@1", "64x6400"), or empty if not stated.
- proof_language: Lean | Isabelle | Metamath | other | unspecified
- model: the prover model named for that number (short), or empty.
- quote: the exact phrase from the abstract that contains the number (at most 25 words), or empty.
Copy numbers exactly; never infer a number that is not written. One row per record, all {N}, in input order.

FINAL REPLY: how many abstracts report a miniF2F number. Do not paste the table.
