"""Stage 2 (v2): final title/abstract decision for every record of the screened union.

Rule: when both independent screeners say include, or both say exclude, that is the
final decision; every other combination (any 'unsure', or a conflict) goes to the
adjudicator, whose decision is final.

Inputs : work/search/records_union.jsonl
         data/decisions/screening/union_screener_{A,B}.csv, union_adjudication.csv
Outputs: work/final_screen.json  (rid -> include/exclude; read by search/snowball.py)
"""
import csv
import json

from config import DECISIONS, WORK


def read(path):
    with path.open(encoding="utf-8") as f:
        return {r["rid"]: r for r in csv.DictReader(f)}


def resolve(a, b, adj, label):
    final, sent = {}, 0
    for rid in a:
        x, y = a[rid]["decision"], b[rid]["decision"]
        if x == y and x in ("include", "exclude"):
            final[rid] = x
        else:
            sent += 1
            if rid not in adj:
                raise SystemExit(f"[{label}] record {rid} needs adjudication but has none")
            final[rid] = adj[rid]["decision"]
    extra = set(adj) - {r for r in a if not (a[r]["decision"] == b[r]["decision"] != "unsure")}
    if extra:
        raise SystemExit(f"[{label}] adjudications for records that did not need one: {sorted(extra)[:5]}")
    return final, sent


def main():
    s = DECISIONS / "screening"
    union = [json.loads(l)["rid"] for l in open(WORK / "search" / "records_union.jsonl", encoding="utf-8")]
    a, b, adj = read(s / "union_screener_A.csv"), read(s / "union_screener_B.csv"), read(s / "union_adjudication.csv")
    if set(a) != set(union) or set(b) != set(union):
        raise SystemExit("[s10] screener files do not cover the union exactly")
    final, sent = resolve(a, b, adj, "s10")
    (WORK / "final_screen.json").write_text(json.dumps(final))
    print(f"[s10] union {len(final)}: {sum(v == 'include' for v in final.values())} included; "
          f"{sent} adjudicated")


if __name__ == "__main__":
    main()
