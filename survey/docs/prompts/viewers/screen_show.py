"""Print records of a batch file in a readable form: python show.py BATCH START END"""
import json, sys
recs = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
s, e = int(sys.argv[2]), int(sys.argv[3])
for i, r in enumerate(recs[s:e], s):
    print(f"[{i}] {r['rid']} | {r['venue']} {r['year']} {r['track']}\nTITLE: {r['title']}\nABSTRACT: {r['abstract'] or '(none)'}\n")
