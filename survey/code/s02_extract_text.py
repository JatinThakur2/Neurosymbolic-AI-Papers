"""Stage 2a: extract text from the local PDFs with poppler's pdftotext.

* first two pages of every record -> abstract (used for screening)
* full text of included studies    -> used by s05 (run after s03)

Output: work/first_pages/<record_id>.txt, work/fulltext/<record_id>.txt,
        data/derived/abstracts.csv
"""
import argparse
import csv
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from config import DERIVED, WORK

ABSTRACT_RE = re.compile(
    r"(?i)\babstract\b[\s\.:—-]*(.{200,2200}?)"
    r"(?=\b(1\.?\s+Introduction|Introduction|Keywords|Index Terms|I\. INTRODUCTION)\b)"
)


def pdftotext(pdf: Path, out: Path, first=None, last=None):
    cmd = ["pdftotext"]
    if first:
        cmd += ["-f", str(first), "-l", str(last), "-layout"]
    cmd += [str(pdf), str(out)]
    subprocess.run(cmd, capture_output=True, timeout=180)
    return out.exists()


def abstract_from(text: str) -> str:
    flat = re.sub(r"\s+", " ", text)
    m = ABSTRACT_RE.search(flat)
    return m.group(1).strip() if m else flat[:1800]


def load_records():
    with (DERIVED / "corpus_records.csv").open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--fulltext-ids", default="", help="comma-separated record ids (set by run_all)")
    args = ap.parse_args()
    recs = load_records()
    (WORK / "first_pages").mkdir(parents=True, exist_ok=True)
    (WORK / "fulltext").mkdir(parents=True, exist_ok=True)

    def first(r):
        if not r["local_pdf"]:
            return r["record_id"], ""
        out = WORK / "first_pages" / f"{r['record_id']}.txt"
        if not out.exists():
            pdftotext(args.repo / r["local_pdf"], out, 1, 2)
        return r["record_id"], abstract_from(out.read_text(errors="ignore")) if out.exists() else ""

    with ThreadPoolExecutor(8) as ex:
        abstracts = dict(ex.map(first, recs))
    with (DERIVED / "abstracts.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["record_id", "abstract"])
        for rid, a in abstracts.items():
            w.writerow([rid, a])
    print(f"[s02] abstracts: {sum(1 for a in abstracts.values() if a)} of {len(recs)} records")

    if args.fulltext_ids:
        ids = set(args.fulltext_ids.split(","))
        todo = [r for r in recs if r["record_id"] in ids and r["local_pdf"]]

        def full(r):
            out = WORK / "fulltext" / f"{r['record_id']}.txt"
            return out.exists() or pdftotext(args.repo / r["local_pdf"], out)

        with ThreadPoolExecutor(8) as ex:
            ok = sum(ex.map(full, todo))
        print(f"[s02] full text: {ok} of {len(ids)} included studies")


if __name__ == "__main__":
    main()
