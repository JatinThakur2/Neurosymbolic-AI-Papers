"""Stratified recall audit: draw records that the search query did NOT retrieve.

Population: Source B records that are neither in the screened union (search hits +
curated corpus) nor snowball candidates. They are stratified by which query block
they match (title + abstract): lm_only (language-model terms, no symbolic terms),
sym_only (symbolic terms, no language-model terms) and neither.
Draw 1 (seed 2026, one generator, file order): 200 lm_only, then 100 sym_only.
Draw 2 (seed 2027, added in revision): 100 neither.
The released audit decisions must cover exactly these draws; the script checks that.

Outputs: data/derived/audit_strata.json (stratum sizes and sampled ids)
"""
import csv
import hashlib
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
from config import DECISIONS, DERIVED, WORK, norm_title  # noqa: E402
from query import LM_RE, SYM_RE  # noqa: E402

SEED, SIZES = 2026, (("lm_only", 200), ("sym_only", 100))
SEED2, NEITHER_N = 2027, 100


def rid(title):
    return "r" + hashlib.sha1(norm_title(title).encode()).hexdigest()[:8]


def main():
    union = {json.loads(l)["rid"] for l in open(WORK / "search" / "records_union.jsonl", encoding="utf-8")}
    snow = {norm_title(json.loads(l)["title"])
            for l in open(WORK / "search" / "snowball_candidates.jsonl", encoding="utf-8")}
    strata, seen = {"neither": [], "lm_only": [], "sym_only": []}, set()
    for line in open(WORK / "search" / "source_b.jsonl", encoding="utf-8"):
        r = json.loads(line)
        k = rid(r["title"])
        if k in union or norm_title(r["title"]) in snow or k in seen:
            continue
        seen.add(k)
        text = f"{r['title']} {r['abstract']}"
        a, b = bool(LM_RE.search(text)), bool(SYM_RE.search(text))
        if a and b:
            continue
        strata["lm_only" if a else "sym_only" if b else "neither"].append(k)
    rng = random.Random(SEED)
    sample = {h: rng.sample(strata[h], n) for h, n in SIZES}
    sample["neither"] = random.Random(SEED2).sample(strata["neither"], NEITHER_N)
    released = {r["rid"] for r in csv.DictReader(open(DECISIONS / "screening" / "audit_screener_A.csv",
                                                       encoding="utf-8"))}
    drawn = set(sample["lm_only"]) | set(sample["sym_only"]) | set(sample["neither"])
    assert drawn == released, "released audit sample differs from the seeded draw"
    out = {"seed": SEED, "seed_neither": SEED2, "strata_sizes": {h: len(v) for h, v in strata.items()},
           "sample": {h: sorted(v) for h, v in sample.items()}}
    (DERIVED / "audit_strata.json").write_text(json.dumps(out, indent=1))
    print("[audit] strata", out["strata_sizes"], "- released sample matches the seeded draw")


if __name__ == "__main__":
    main()
