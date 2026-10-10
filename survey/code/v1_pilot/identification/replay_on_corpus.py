"""Replay the reference title classifier over the repository's own 391 titles.

This measures how closely the re-implemented classifier agrees with the
repository's identification stage. It is NOT a recall estimate against the
venues (that would need the full dblp title lists).

Output: data/derived/identification_replay.json
"""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
from config import DERIVED  # noqa: E402
from reference_dblp_classifier import classify  # noqa: E402


def main():
    with (DERIVED / "corpus_records.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with (DERIVED / "included_studies.csv").open(encoding="utf-8") as f:
        inc = {r["record_id"] for r in csv.DictReader(f)}
    tiers = Counter(classify(r["title"]) or "none" for r in rows)
    out = {
        "records": len(rows),
        "flagged": len(rows) - tiers["none"],
        "core": tiers["core"],
        "adjacent": tiers["adjacent"],
        "included": len(inc),
        "included_flagged": sum(1 for r in rows if r["record_id"] in inc and classify(r["title"])),
        "unflagged": [r["title"] for r in rows if not classify(r["title"])],
    }
    (DERIVED / "identification_replay.json").write_text(json.dumps(out, indent=2))
    print(f"[replay] classifier flags {out['flagged']} of {out['records']} repository titles "
          f"({out['core']} core, {out['adjacent']} adjacent)")


if __name__ == "__main__":
    main()
