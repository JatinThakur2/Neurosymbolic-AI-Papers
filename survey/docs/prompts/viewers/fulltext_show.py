import json, sys
for i, r in enumerate(json.loads(l) for l in open(sys.argv[1], encoding="utf-8")):
    print(f"[{i}] {r['rid']} | {r['venue']} {r['year']} | url: {r['url']}\nTITLE: {r['title']}\nABSTRACT: {r['abstract']}\n")
