"""Backward snowballing (Wohlin 2014) from the reference lists of included studies.

For every included study with a local PDF, the reference list is extracted with
pdftotext and matched against all records of Source B (the in-scope proceedings,
not only the search hits). A Source B record is a snowball candidate when its
normalised title (>= 25 characters) occurs in the normalised reference text of at
least one included study and the record is NOT already in the screened union.

Inputs : work/search/source_b.jsonl, work/search/records_union.jsonl,
         work/final_screen.json (rid -> include/exclude), corpus PDFs
Outputs: work/search/snowball_candidates.jsonl, data/derived/snowball_summary.json
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from config import DERIVED, WORK, norm_title  # noqa: E402

MIN_LEN = 25


def reference_text(pdf: Path, cache: Path) -> str:
    if not cache.exists():
        subprocess.run(["pdftotext", str(pdf), str(cache)], capture_output=True, timeout=300)
    if not cache.exists():
        return ""
    t = cache.read_text(errors="ignore")
    heads = list(re.finditer(r"\n\s*(References|REFERENCES|Bibliography|BIBLIOGRAPHY)\s*\n", t))
    return t[heads[0].start():] if heads else t[len(t) // 2:]   # fall back to the second half


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, type=Path)
    a = ap.parse_args()
    union = [json.loads(l) for l in open(WORK / "search" / "records_union.jsonl", encoding="utf-8")]
    final = json.load(open(WORK / "final_screen.json"))
    in_union = {norm_title(r["title"]) for r in union}
    seeds = [r for r in union if final.get(r["rid"]) == "include" and r.get("local_pdf")]
    cache_dir = WORK / "fulltext_all"
    cache_dir.mkdir(parents=True, exist_ok=True)
    docs = {}
    for r in seeds:
        txt = reference_text(a.repo / r["local_pdf"], cache_dir / f"{r['rid']}.txt")
        docs[r["rid"]] = norm_title(txt)
    blob = "\n".join(f"{rid}\t{t}" for rid, t in docs.items())
    cands, seen = {}, set()
    for line in open(WORK / "search" / "source_b.jsonl", encoding="utf-8"):
        rec = json.loads(line)
        k = norm_title(rec["title"])
        if len(k) < MIN_LEN or k in seen:
            continue
        seen.add(k)
        if k not in blob:
            continue
        cited_by = [rid for rid, t in docs.items() if k in t]
        if k in in_union:
            continue
        rec["cited_by"] = cited_by
        cands[k] = rec
    out = WORK / "search" / "snowball_candidates.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for rec in cands.values():
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    summary = {"seed_studies_with_local_pdf": len(seeds), "candidates_not_in_union": len(cands)}
    (DERIVED / "snowball_summary.json").write_text(json.dumps(summary, indent=2))
    print("[snowball]", summary)


if __name__ == "__main__":
    main()
