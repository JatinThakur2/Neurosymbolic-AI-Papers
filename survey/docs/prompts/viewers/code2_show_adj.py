"""Print coding-adjudication records: python show_adj.py BATCH START END (0-based, END exclusive)"""
import json, sys
recs = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
s, e = int(sys.argv[2]), int(sys.argv[3])
for i, r in enumerate(recs[s:e], s):
    print(f"[{i}] {r['rid']} | {r['venue']} {r['year']}\nTITLE: {r['title']}\nABSTRACT: {r['abstract'] or '(none)'}")
    print(f"DISPUTED FIELDS: {', '.join(r['disputed'])}")
    for who in ("coder_A", "coder_B"):
        c = r[who]
        print(f"{who}: arch={c['architecture']} check={c['check_strength']} domain={c['domain']} form={c['formalism']} faith={c['faithfulness_reported']} ({c['confidence']}) -- {c['rationale']}")
    print()
