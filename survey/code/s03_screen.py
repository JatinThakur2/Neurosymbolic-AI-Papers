"""Stages 1-3: de-duplication, LM-term screening and eligibility.

Automated steps
  1. de-duplicate on normalised title (first occurrence kept)
  2. flag records whose title + abstract match config.LM_FILTER
Manual inputs (data/manual/)
  title_review_additions.csv  records added to the candidate pool by title review
  eligibility_decisions.csv   include / exclude (+ reason code) for every candidate

Outputs
  data/derived/screening_log.csv  one row per record with stage, decision, reason
  data/derived/prisma_counts.json counts for the PRISMA flow diagram
"""
import csv
import json
from collections import Counter

from config import DERIVED, LM_FILTER, MANUAL, TITLE_REVIEW_SCOPE, norm_title


def read(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    recs = read(DERIVED / "corpus_records.csv")
    abstracts = {r["record_id"]: r["abstract"] for r in read(DERIVED / "abstracts.csv")}
    additions = {norm_title(r["title"]): r for r in read(MANUAL / "title_review_additions.csv")}
    decisions = {norm_title(r["title"]): r for r in read(MANUAL / "eligibility_decisions.csv")}

    seen, log = {}, []
    for r in recs:
        key = norm_title(r["title"])
        row = {k: r[k] for k in ("record_id", "venue", "year", "title")}
        if key in seen:
            row.update(stage="identification", decision="excluded",
                       reason=f"duplicate of record {seen[key]}", lm_filter_hit="", evidence="")
            log.append(row)
            continue
        seen[key] = r["record_id"]
        hit = bool(LM_FILTER.search(r["title"] + ". " + abstracts.get(r["record_id"], "")))
        row["lm_filter_hit"] = "yes" if hit else "no"
        row["title_reviewed"] = "yes" if (not hit and (TITLE_REVIEW_SCOPE.search(r["title"])
                                                      or not abstracts.get(r["record_id"]))) else ""
        in_pool = hit or key in additions
        if not in_pool:
            row.update(stage="screening", decision="excluded",
                       reason="no language-model component evident in title or abstract", evidence="")
        else:
            if key not in decisions:
                raise SystemExit(f"[s03] candidate without a manual decision: {r['title']}")
            d = decisions[key]
            row["evidence"] = d["evidence"]
            if d["decision"] == "include":
                row.update(stage="included", decision="included", reason="")
            else:
                row.update(stage="eligibility", decision="excluded",
                           reason=f"{d['reason_code']}: {d['reason_text']}")
        row["added_by_title_review"] = "yes" if key in additions else ""
        log.append(row)

    unused = set(decisions) - {norm_title(r["title"]) for r in log if r["stage"] in ("included", "eligibility")}
    if unused:
        raise SystemExit(f"[s03] manual decisions that match no candidate: {sorted(unused)}")

    fields = ["record_id", "venue", "year", "title", "stage", "decision", "reason",
              "lm_filter_hit", "title_reviewed", "added_by_title_review", "evidence"]
    with (DERIVED / "screening_log.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for row in log:
            w.writerow({k: row.get(k, "") for k in fields})

    st = Counter(r["stage"] for r in log)
    reasons = Counter(r["reason"].split(":")[0] for r in log if r["stage"] == "eligibility")
    counts = {
        "identified": len(log),
        "with_local_pdf": sum(1 for r in recs if r["local_pdf"]),
        "duplicates": st["identification"],
        "screened": len(log) - st["identification"],
        "excluded_screening": st["screening"],
        "lm_filter_hits": sum(1 for r in log if r.get("lm_filter_hit") == "yes"),
        "abstracts_extracted": sum(1 for a in abstracts.values() if a),
        "title_reviewed": sum(1 for r in log if r.get("title_reviewed") == "yes"),
        "title_review_additions": sum(1 for r in log if r.get("added_by_title_review") == "yes"),
        "assessed": st["included"] + st["eligibility"],
        "excluded_eligibility": st["eligibility"],
        "exclusion_reasons": dict(sorted(reasons.items())),
        "included": st["included"],
        "included_from_published_abstract": sum(
            1 for r in log if r["stage"] == "included" and r["evidence"].startswith("published abstract")),
    }
    (DERIVED / "prisma_counts.json").write_text(json.dumps(counts, indent=2))
    print("[s03]", json.dumps(counts))


if __name__ == "__main__":
    main()
