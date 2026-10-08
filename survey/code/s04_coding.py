"""Stage 4 (data extraction): join the manual coding sheet to the included studies.

Inputs : data/derived/screening_log.csv, data/manual/coding.csv,
         data/manual/taxonomy_codebook.csv, data/manual/code_availability.csv
Outputs: data/derived/included_studies.csv  (one row per included study)
         data/derived/coding_summary.json    (counts per axis and cross-tab)
"""
import csv
import json
from collections import Counter

from config import DERIVED, MANUAL, norm_title


def read(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    log = read(DERIVED / "screening_log.csv")
    recs = {r["record_id"]: r for r in read(DERIVED / "corpus_records.csv")}
    coding = {norm_title(r["title"]): r for r in read(MANUAL / "coding.csv")}
    avail = {norm_title(r["title"]): r for r in read(MANUAL / "code_availability.csv")}
    book = read(MANUAL / "taxonomy_codebook.csv")
    labels = {(b["axis"], b["code"]): b["label"] for b in book}

    included = [r for r in log if r["stage"] == "included"]
    missing = [r["title"] for r in included if norm_title(r["title"]) not in coding]
    if missing:
        raise SystemExit(f"[s04] included studies without coding: {missing}")
    if len(coding) != len(included):
        raise SystemExit(f"[s04] coding sheet has {len(coding)} rows for {len(included)} included studies")

    rows = []
    for r in included:
        c = coding[norm_title(r["title"])]
        a = avail.get(norm_title(r["title"]), {})
        rows.append({
            "record_id": r["record_id"], "venue": r["venue"], "year": r["year"], "title": r["title"],
            "authors": recs[r["record_id"]]["authors"],
            "domain": c["domain"], "architecture": c["architecture"], "formalism": c["formalism"],
            "fulltext_available": a.get("fulltext_available", ""),
            "artifact_released": a.get("artifact_released", ""),
            "evidence": r["evidence"],
        })
    with (DERIVED / "included_studies.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    summary = {
        "n": len(rows),
        "domain": dict(Counter(r["domain"] for r in rows)),
        "architecture": dict(Counter(r["architecture"] for r in rows)),
        "formalism": dict(Counter(r["formalism"] for r in rows)),
        "venue": dict(Counter(r["venue"] for r in rows)),
        "year": dict(sorted(Counter(r["year"] for r in rows).items())),
        "cross_domain_architecture": {f"{d}|{a}": n for (d, a), n in
                                      Counter((r["domain"], r["architecture"]) for r in rows).items()},
        "artifact_released": dict(Counter(r["artifact_released"] for r in rows)),
        "labels": {f"{k[0]}|{k[1]}": v for k, v in labels.items()},
    }
    (DERIVED / "coding_summary.json").write_text(json.dumps(summary, indent=2))
    print(f"[s04] coded {len(rows)} studies; architectures {summary['architecture']}")


if __name__ == "__main__":
    main()
