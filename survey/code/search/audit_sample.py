"""Stratified recall audit: draw records that the search query did NOT retrieve.

Population: Source B records that are neither in the screened union (search hits +
curated corpus) nor snowball candidates. They are stratified by which query block
they match (title + abstract): lm_only (language-model terms, no symbolic terms),
sym_only (symbolic terms, no language-model terms) and neither.
Draw 1 (seed 2026, one generator, file order): 200 lm_only, then 100 sym_only.
Draw 2 (seed 2027, added in revision): 100 neither.
The released audit decisions must cover exactly these draws; the script checks that.

Revision 2: the strata and the draw are reproduced on the v2 population (v2 query; records
added by the revision-2 track rule skipped). The script then re-states each stratum for the
augmented query: records the augmented query retrieves leave the stratum (they were screened as
search hits), and the r2-added records the query does not retrieve join their stratum.
It also writes an accounting of every Source B record.

Outputs: data/derived/audit_strata.json (stratum sizes, sampled ids, revision-2 strata, accounting)
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
from query import LM_RE_V2 as LM_RE, SYM_RE_V2 as SYM_RE, matches  # noqa: E402

SEED, SIZES = 2026, (("lm_only", 200), ("sym_only", 100))
SEED2, NEITHER_N = 2027, 100
# Revision 2 (referee report 2, M5/M6): the audit is extended with a further simple random draw from
# the revision-2 strata (records not retrieved by the full search), to narrow the recall interval.
SEED3, EXTENSION = 2028, (("neither", 300), ("lm_only", 200))


def rid(title):
    return "r" + hashlib.sha1(norm_title(title).encode()).hexdigest()[:8]


def main():
    union = {json.loads(l)["rid"] for l in open(WORK / "search" / "records_union.jsonl", encoding="utf-8")}
    snow = {norm_title(json.loads(l)["title"])
            for l in open(WORK / "search" / "snowball_candidates.jsonl", encoding="utf-8")}
    strata, seen = {"neither": [], "lm_only": [], "sym_only": []}, set()
    acct = {"records": 0, "r2_added": 0, "duplicate_title": 0, "id_collision": 0, "in_union": 0,
            "snowball_candidate": 0, "v2_hit_not_in_union": 0, "audit_population": 0}
    titles_seen = set()
    retrieved_aug, added_nonhit = set(), {"neither": 0, "lm_only": 0, "sym_only": 0}
    added_ids = {"neither": [], "lm_only": [], "sym_only": []}
    for line in open(WORK / "search" / "source_b.jsonl", encoding="utf-8"):
        r = json.loads(line)
        acct["records"] += 1
        k, nt = rid(r["title"]), norm_title(r["title"])
        text = f"{r['title']} {r['abstract']}"
        a, b = bool(LM_RE.search(text)), bool(SYM_RE.search(text))
        h = "lm_only" if a and not b else "sym_only" if b and not a else "neither" if not (a or b) else None
        if r.get("r2_added"):
            acct["r2_added"] += 1
            if k not in union and nt not in snow and h and not matches(r["title"], r["abstract"]):
                added_nonhit[h] += 1
                added_ids[h].append(k)
            continue
        if nt in titles_seen:
            acct["duplicate_title"] += 1
            continue
        titles_seen.add(nt)
        if k in union:
            acct["in_union"] += 1
            continue
        if nt in snow:
            acct["snowball_candidate"] += 1
            continue
        if k in seen:
            acct["id_collision"] += 1
            continue
        seen.add(k)
        if h is None:
            acct["v2_hit_not_in_union"] += 1
            continue
        acct["audit_population"] += 1
        strata[h].append(k)
        if matches(r["title"], r["abstract"]):
            retrieved_aug.add(k)
    rng = random.Random(SEED)
    sample = {h: rng.sample(strata[h], n) for h, n in SIZES}
    sample["neither"] = random.Random(SEED2).sample(strata["neither"], NEITHER_N)
    released = {r["rid"] for r in csv.DictReader(open(DECISIONS / "screening" / "audit_screener_A.csv",
                                                       encoding="utf-8"))}
    drawn = set(sample["lm_only"]) | set(sample["sym_only"]) | set(sample["neither"])
    assert drawn == released, "released audit sample differs from the seeded draw"
    r2 = {h: {"N": len([k for k in v if k not in retrieved_aug]) + added_nonhit[h],
              "sample": sorted(k for k in sample[h] if k not in retrieved_aug),
              "sample_retrieved_by_augmented_query": sorted(k for k in sample[h] if k in retrieved_aug),
              "retrieved_by_augmented_query": len([k for k in v if k in retrieved_aug]),
              "r2_added_not_retrieved": added_nonhit[h]} for h, v in strata.items()}
    # revision-2 extension: simple random draw from each revision-2 stratum, excluding records
    # already in the audit sample (population order is the Source B file order, so the draw is
    # reproducible from the source files and the seed)
    rng3 = random.Random(SEED3)
    for h, n in EXTENSION:
        pop = [k for k in strata[h] if k not in retrieved_aug and k not in set(sample[h])] + added_ids[h]
        ext = rng3.sample(pop, n)
        r2[h]["extension"] = sorted(ext)
    out = {"seed": SEED, "seed_neither": SEED2, "seed_extension": SEED3,
           "strata_sizes": {h: len(v) for h, v in strata.items()},
           "sample": {h: sorted(v) for h, v in sample.items()}, "r2": r2, "accounting": acct}
    (DERIVED / "audit_strata.json").write_text(json.dumps(out, indent=1))
    print("[audit] strata", out["strata_sizes"], "- released sample matches the seeded draw;",
          "r2 strata", {h: v["N"] for h, v in r2.items()}, "| accounting", acct)


if __name__ == "__main__":
    main()
