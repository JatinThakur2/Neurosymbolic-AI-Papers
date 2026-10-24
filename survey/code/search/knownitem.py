"""Revision 2: fresh known-item check (referee report 2, minor issue 1).

The known-item set is the reference list of an independent recent survey (Cheng et al., 2025,
"Empowering LLMs with Logical Reasoning: A Comprehensive Survey", arXiv:2502.15652v4), restricted
to papers at the review's venues and years (data/decisions/knownitem/cheng2025_refs.txt; extracted
from the survey's bibliography and kept verbatim). The set was chosen after the search was frozen and
was not used to design the query.

For each reference this script finds the Source B record (same normalised title), and writes the
records that no stage of the review screened to work/knownitem/records.jsonl. Those records are
screened by two screeners with adjudication (route "knownitem" in s11). The summary of the check
is computed in s11.

Output: work/knownitem/records.jsonl
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
from config import DECISIONS, WORK, norm_title  # noqa: E402
from audit_sample import rid  # noqa: E402

REFS = DECISIONS / "knownitem" / "cheng2025_refs.txt"


def refs():
    for line in open(REFS, encoding="utf-8"):
        if line.strip():
            t, v, y = [x.strip() for x in line.split("|")]
            yield {"title": t, "venue": v, "year": y}


def screened_rids():
    s = set()
    for f in ("records_union.jsonl", "stage2_records.jsonl"):
        s |= {json.loads(l)["rid"] for l in open(WORK / "search" / f, encoding="utf-8")}
    s |= {rid(json.loads(l)["title"]) for l in open(WORK / "search" / "snowball_candidates.jsonl", encoding="utf-8")}
    strata = json.loads((HERE.parent.parent / "data" / "derived" / "audit_strata.json").read_text())
    s |= {k for v in strata["sample"].values() for k in v}
    return s


def main():
    want = {norm_title(r["title"]): r for r in refs()}
    found = {}
    for line in open(WORK / "search" / "source_b.jsonl", encoding="utf-8"):
        r = json.loads(line)
        nt = norm_title(r["title"])
        if nt in want and nt not in found:
            found[nt] = r
    done = screened_rids()
    out = []
    for nt, ref in want.items():
        r = found.get(nt)
        if r is None:
            continue
        k = rid(r["title"])
        if k not in done:
            out.append({"rid": k, "title": r["title"], "venue": r["venue"], "year": r["year"],
                        "track": r.get("track", ""), "abstract": r["abstract"], "url": r.get("url", "")})
    (WORK / "knownitem").mkdir(exist_ok=True)
    with (WORK / "knownitem" / "records.jsonl").open("w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[knownitem] {len(want)} references, {len(found)} in Source B, {len(out)} not screened by the review")


if __name__ == "__main__":
    main()
