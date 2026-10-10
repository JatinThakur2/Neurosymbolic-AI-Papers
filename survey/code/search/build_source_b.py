"""Build the abstract-level search database (Source B) from machine-readable proceedings.

Sources (all fetched with git from GitHub; record the commit used):
  * Paper Copilot paper lists  https://github.com/papercopilot/paperlists
      ICLR 2020-2026, NeurIPS 2020-2025, ICML 2020-2026, AAAI 2021-2025, IJCAI 2020-2024,
      ACL 2021-2025, EMNLP 2021-2024, NAACL 2021/2022/2024/2025
      (ICLR 2025 and 2026 are Git-LFS files at HEAD; their last plain-blob versions are used,
       commits d4c51fa and 33f9884.)
  * ACL Anthology               https://github.com/acl-org/acl-anthology
      ACL 2020, EMNLP 2020 and EMNLP 2025 (main conference volumes).

Only accepted papers in archival research tracks are kept (see TRACK RULES below).

Usage: python build_source_b.py --paperlists DIR --anthology DIR --out records.jsonl
"""
import argparse
import glob
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

VENUE = {"iclr": "ICLR", "nips": "NeurIPS", "icml": "ICML", "aaai": "AAAI", "ijcai": "IJCAI",
         "acl": "ACL", "emnlp": "EMNLP", "naacl": "NAACL"}
REJECTED = {"reject", "withdraw", "desk reject", "neurips 2023 conference withdrawn submission"}


def keep(venue, rec):
    """TRACK RULES: accepted, archival, research-track papers only."""
    status = str(rec.get("status") or "").strip().lower()
    track = str(rec.get("track") or "").strip().lower()
    if status in REJECTED or "withdrawn" in status:
        return False
    if venue == "ICLR":
        return "conditional" not in status          # ICLR 2026 conditional decisions excluded
    if venue == "NeurIPS":
        return track in ("main", "datasets & benchmarks", "none", "")
    if venue == "AAAI":
        return track == "main"                       # technical track only
    if venue == "IJCAI":
        return track in ("main", "survey track", "ai for good", "human-centred ai",
                         "ai and arts", "ai, arts & creativity", "multi-year track on ai and social good",
                         "special track on ai for good")
    if venue in ("ACL", "EMNLP", "NAACL"):
        return status in ("long", "short", "main", "long main", "short main")   # main conference; Findings, Industry, Demos excluded
    return True                                      # ICML: all accepted


def clean(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


def from_paperlists(root):
    for f in sorted(glob.glob(str(Path(root) / "*" / "*.json"))):
        m = re.match(r".*/([a-z]+)/[a-z]+(\d{4})\.json$", f)
        if not m or m.group(1) not in VENUE or not ("2020" <= m.group(2) <= "2026"):
            continue
        venue, year = VENUE[m.group(1)], m.group(2)
        try:
            data = json.load(open(f, encoding="utf-8"))
        except json.JSONDecodeError:
            continue                                  # Git-LFS pointer
        for r in data:
            if not keep(venue, r):
                continue
            yield {
                "source": "paperlists", "source_id": str(r.get("id", "")), "venue": venue, "year": year,
                "track": clean(str(r.get("track") or "")), "status": clean(str(r.get("status") or "")),
                "title": clean(r.get("title")), "abstract": clean(r.get("abstract")),
                "authors": clean(r.get("author")).replace(";", "; "),
                "url": r.get("site") or r.get("openreview") or r.get("pdf") or "",
                "github": clean(r.get("github")), "bibtex": r.get("bibtex") or "",
            }


def text_of(el):
    return clean("".join(el.itertext())) if el is not None else ""


def from_anthology(root, files):
    for name in files:
        tree = ET.parse(Path(root) / "data" / "xml" / name)
        coll = tree.getroot().get("id")              # e.g. 2020.acl
        year, ev = coll.split(".")
        for vol in tree.getroot().findall("volume"):
            vid = vol.get("id")
            if vid not in ("main", "long", "short"):
                continue
            for p in vol.findall("paper"):
                yield {
                    "source": "acl-anthology", "source_id": f"{coll}-{vid}.{p.get('id')}",
                    "venue": ev.upper() if ev != "emnlp" else "EMNLP", "year": year,
                    "track": vid, "status": vid, "title": text_of(p.find("title")),
                    "abstract": text_of(p.find("abstract")),
                    "authors": "; ".join(f"{text_of(a.find('first'))} {text_of(a.find('last'))}".strip()
                                         for a in p.findall("author")),
                    "url": f"https://aclanthology.org/{text_of(p.find('url')) or f'{coll}-{vid}.{p.get("id")}'}/",
                    "github": "", "bibtex": "",
                }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paperlists", required=True)
    ap.add_argument("--anthology", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    seen, n = set(), 0
    with open(a.out, "w", encoding="utf-8") as out:
        for rec in list(from_paperlists(a.paperlists)) + list(
                from_anthology(a.anthology, ["2020.acl.xml", "2020.emnlp.xml", "2025.emnlp.xml"])):
            key = (rec["venue"], rec["year"], re.sub(r"[^a-z0-9]", "", rec["title"].lower()))
            if not rec["title"] or key in seen:
                continue
            seen.add(key)
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
    print(f"[source-b] {n} accepted records -> {a.out}")


if __name__ == "__main__":
    main()
