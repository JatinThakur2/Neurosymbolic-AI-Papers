"""Stage 1 (identification): turn the repository README into one row per record.

Input : README.md of the Neurosymbolic-AI-Papers repository
Output: data/derived/corpus_records.csv
"""
import argparse
import csv
import re
import urllib.parse
from pathlib import Path

from config import DERIVED


def parse_readme(readme: Path):
    venue = year = None
    rows = []
    for line in readme.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^### (\w+)", line)
        if m:
            venue = m.group(1)
            continue
        m = re.match(r"^#### (\w+) (\d{4})", line)
        if m:
            venue, year = m.group(1), m.group(2)
            continue
        if not (line.startswith("|") and venue and year):
            continue
        if line.startswith("|---") or line.startswith("| Paper"):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if len(cells) < 2:
            continue
        link_m = re.match(r"\[(.*?)\]\((.*?)\)", cells[0])
        title = link_m.group(1) if link_m else cells[0]
        link = link_m.group(2) if link_m else ""
        extra = cells[2] if len(cells) > 2 else ""
        doi = ""
        d = re.search(r"\[(10\.\d{4,}/[^\]]+)\]", extra)
        if d:
            doi = d.group(1)
        rows.append({
            "record_id": len(rows),
            "venue": venue,
            "year": year,
            "title": title,
            "authors": cells[1],
            "local_pdf": urllib.parse.unquote(link) if link.endswith(".pdf") else "",
            "url": link if link.startswith("http") else "",
            "doi": doi,
            "readme_summary": extra if not doi else "",
        })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, type=Path)
    args = ap.parse_args()
    rows = parse_readme(args.repo / "README.md")
    DERIVED.mkdir(parents=True, exist_ok=True)
    out = DERIVED / "corpus_records.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    n_pdf = sum(1 for r in rows if r["local_pdf"])
    print(f"[s01] {len(rows)} records parsed ({n_pdf} with a local PDF) -> {out}")


if __name__ == "__main__":
    main()
