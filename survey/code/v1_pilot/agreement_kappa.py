"""Inter-rater agreement for a second, independent screener (Cohen's kappa).

Workflow
  1. python code/agreement_kappa.py --make-sheet
     writes data/manual/second_screener_sheet.csv: the candidate titles with
     blank 'decision' and 'reason_code' columns (first screener's verdicts hidden).
  2. A second reviewer fills the sheet independently.
  3. python code/agreement_kappa.py
     reports raw agreement and Cohen's kappa (include/exclude) and lists every
     disagreement for resolution by discussion.

No third-party packages are needed.
"""
import argparse
import csv
import random
from collections import Counter
from pathlib import Path

from config import DERIVED, MANUAL, norm_title

SHEET = MANUAL / "second_screener_sheet.csv"   # default: human second screener


def cohen_kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(a) | set(b)) / (n * n)
    return po, (po - pe) / (1 - pe) if pe < 1 else 1.0


def make_sheet():
    with (DERIVED / "screening_log.csv").open(encoding="utf-8") as f:
        cands = [r for r in csv.DictReader(f) if r["stage"] in ("included", "eligibility")]
    random.seed(0)
    random.shuffle(cands)  # hide the first screener's ordering
    with SHEET.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["title", "venue", "year", "decision", "reason_code"])
        for r in cands:
            w.writerow([r["title"], r["venue"], r["year"], "", ""])
    print(f"wrote {len(cands)} candidates to {SHEET}")


def score(sheet=SHEET):
    with (MANUAL / "eligibility_decisions.csv").open(encoding="utf-8") as f:
        first = {norm_title(r["title"]): r["decision"] for r in csv.DictReader(f)}
    with sheet.open(encoding="utf-8") as f:
        second = {norm_title(r["title"]): (r["decision"].strip().lower(), r["title"])
                  for r in csv.DictReader(f) if r["decision"].strip()}
    keys = [k for k in second if k in first]
    if not keys:
        raise SystemExit("second-screener sheet has no decisions yet")
    a = [first[k] for k in keys]
    b = [second[k][0] for k in keys]
    po, kappa = cohen_kappa(a, b)
    print(f"n = {len(keys)}  raw agreement = {po:.3f}  Cohen's kappa = {kappa:.3f}")
    for k in keys:
        if first[k] != second[k][0]:
            print(f"  DISAGREE  first={first[k]:8s} second={second[k][0]:8s} {second[k][1]}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--make-sheet", action="store_true")
    ap.add_argument("--sheet", default=str(SHEET), help="filled second-screener sheet to score")
    a = ap.parse_args()
    if a.make_sheet:
        make_sheet()
    else:
        score(Path(a.sheet))
