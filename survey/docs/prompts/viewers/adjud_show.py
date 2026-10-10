"""Print adjudication records: python show.py BATCH START END (0-based, END exclusive)"""
import json, sys
recs = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
s, e = int(sys.argv[2]), int(sys.argv[3])
for i, r in enumerate(recs[s:e], s):
    A, B = r["screener_A"], r["screener_B"]
    print(f"[{i}] {r['rid']} | {r['venue']} {r['year']} {r['track']} | url: {r['url']}")
    print(f"TITLE: {r['title']}\nABSTRACT: {r['abstract'] or '(none)'}")
    print(f"LOCAL FULL TEXT: {r['fulltext_file'] or r['first_pages_file'] or '(none)'}")
    print(f"SCREENER A: {A['decision']} {A['code']} -- {A['rationale']}")
    print(f"SCREENER B: {B['decision']} {B['code']} -- {B['rationale']}\n")
