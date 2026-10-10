"""Merge Source A (curated corpus) and Source B (database-search hits) into one record set.

* Records are matched on normalised title.
* A corpus record that also appears anywhere in Source B (hit or not) takes the
  proceedings abstract, BibTeX and GitHub fields from Source B.
* Output: data/derived/records_union.csv (no abstracts; redistributable) and
  work/search/records_union.jsonl (with abstracts; regenerated from the sources).
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from config import DERIVED, WORK, norm_title  # noqa: E402


def rid(title):
    return "r" + hashlib.sha1(norm_title(title).encode()).hexdigest()[:8]


def main():
    allb = {}
    for line in open(WORK / "search" / "source_b.jsonl", encoding="utf-8"):
        r = json.loads(line)
        allb.setdefault(norm_title(r["title"]), r)
    hits = {}
    for line in open(WORK / "search" / "hits_b.jsonl", encoding="utf-8"):
        r = json.loads(line)
        hits.setdefault(norm_title(r["title"]), r)
    with (DERIVED / "corpus_records.csv").open(encoding="utf-8") as f:
        corpus = list(csv.DictReader(f))
    with (DERIVED / "abstracts.csv").open(encoding="utf-8") as f:
        pdf_abs = {r["record_id"]: r["abstract"] for r in csv.DictReader(f)}

    union, dup_corpus = {}, 0
    for c in corpus:
        k = norm_title(c["title"])
        if k in union:
            dup_corpus += 1
            continue
        b = allb.get(k)
        if b and (b["venue"], b["year"]) != (c["venue"], c["year"]):
            b = None        # same title, different venue-year (reprint / extended abstract): keep corpus metadata
        union[k] = {
            "rid": rid(c["title"]), "title": c["title"], "venue": c["venue"], "year": c["year"],
            "authors": (b or {}).get("authors") or c["authors"],
            "abstract": (b or {}).get("abstract") or pdf_abs.get(c["record_id"], ""),
            "abstract_source": "proceedings" if b and b.get("abstract") else ("pdf" if pdf_abs.get(c["record_id"]) else "none"),
            "in_corpus": "yes", "corpus_record_id": c["record_id"], "local_pdf": c["local_pdf"],
            "in_search": "yes" if k in hits else "no",
            "in_search_sources": "yes" if b else "no",
            "url": (b or {}).get("url") or c["url"], "github": (b or {}).get("github", ""),
            "track": (b or {}).get("track", ""), "bibtex": (b or {}).get("bibtex", ""),
        }
    for k, b in hits.items():
        if k in union:
            continue
        union[k] = {
            "rid": rid(b["title"]), "title": b["title"], "venue": b["venue"], "year": b["year"],
            "authors": b["authors"], "abstract": b["abstract"], "abstract_source": "proceedings",
            "in_corpus": "no", "corpus_record_id": "", "local_pdf": "", "in_search": "yes",
            "in_search_sources": "yes", "url": b["url"], "github": b.get("github", ""),
            "track": b.get("track", ""), "bibtex": b.get("bibtex", ""),
        }
    rows = sorted(union.values(), key=lambda r: (r["venue"], r["year"], r["title"]))
    ids = [r["rid"] for r in rows]
    assert len(ids) == len(set(ids)), "record-id collision"
    with (WORK / "search" / "records_union.jsonl").open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    fields = ["rid", "title", "venue", "year", "authors", "abstract_source", "in_corpus",
              "corpus_record_id", "in_search", "in_search_sources", "url", "github", "track"]
    with (DERIVED / "records_union.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    both = sum(1 for r in rows if r["in_corpus"] == "yes" and r["in_search"] == "yes")
    summary = {
        "corpus_records": len(corpus), "corpus_duplicates": dup_corpus,
        "search_records_total": len(allb), "search_hits": len(hits),
        "overlap": both, "union": len(rows),
        "corpus_in_search_sources": sum(1 for r in rows if r["in_corpus"] == "yes" and r["in_search_sources"] == "yes"),
        "no_abstract": sum(1 for r in rows if r["abstract_source"] == "none"),
    }
    (DERIVED / "search_summary.json").write_text(json.dumps(summary, indent=2))
    print("[merge]", summary)


if __name__ == "__main__":
    main()
