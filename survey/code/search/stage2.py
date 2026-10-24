"""Revision 2, search stage 2: records retrieved by the augmented query only.

Stage 1 is the frozen v2 search (v2 query, curated corpus, backward snowballing, recall audit).
Stage 2 applies the augmented query (query.py, revision 2) to all Source B records, including
those admitted by the revised track rule, and keeps the hits that stage 1 did not screen:
not in the v2 union, not a snowball candidate and not in the audit sample (audit records the
augmented query retrieves keep their audit decisions).

Inputs : work/search/source_b.jsonl, records_union.jsonl, snowball_candidates.jsonl,
         data/derived/audit_strata.json
Outputs: work/search/stage2_records.jsonl, data/derived/stage2_summary.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
from config import DERIVED, WORK, norm_title  # noqa: E402
from audit_sample import rid  # noqa: E402
from query import matches, matches_v2  # noqa: E402


def main():
    union = {json.loads(l)["rid"] for l in open(WORK / "search" / "records_union.jsonl", encoding="utf-8")}
    snow = {norm_title(json.loads(l)["title"])
            for l in open(WORK / "search" / "snowball_candidates.jsonl", encoding="utf-8")}
    strata = json.loads((DERIVED / "audit_strata.json").read_text())
    audit = {k for v in strata["sample"].values() for k in v}
    out, seen = [], set()
    n_aug = n_v2 = in_union = in_snow = in_audit = dup = 0
    for line in open(WORK / "search" / "source_b.jsonl", encoding="utf-8"):
        r = json.loads(line)
        if not matches(r["title"], r["abstract"]):
            continue
        n_aug += 1
        if matches_v2(r["title"], r["abstract"]):
            n_v2 += 1
            if not r.get("r2_added"):
                continue              # screened in stage 1 (v2 union); records added to Source B in
                                      # revision 2 were not, so they are screened here
        k, nt = rid(r["title"]), norm_title(r["title"])
        if k in union:
            in_union += 1
        elif nt in snow:
            in_snow += 1
        elif k in audit:
            in_audit += 1
        elif nt in seen:
            dup += 1
        else:
            seen.add(nt)
            out.append({"rid": k, "title": r["title"], "venue": r["venue"], "year": r["year"],
                        "track": r.get("track", ""), "abstract": r["abstract"], "url": r.get("url", ""),
                        "authors": r.get("authors", ""), "bibtex": r.get("bibtex", ""),
                        "github": r.get("github", ""), "r2_added": r.get("r2_added", False)})
    with (WORK / "search" / "stage2_records.jsonl").open("w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    summ = {"augmented_hits": n_aug, "v2_hits_within": n_v2, "new_hits": n_aug - n_v2,
            "r2_added_screened": sum(1 for r in out if r["r2_added"]),
            "new_in_v2_union": in_union, "new_snowball_candidates": in_snow, "new_in_audit_sample": in_audit,
            "duplicate_titles": dup, "screened_in_stage2": len(out)}
    (DERIVED / "stage2_summary.json").write_text(json.dumps(summ, indent=2))
    print("[stage2]", summ)


if __name__ == "__main__":
    main()
