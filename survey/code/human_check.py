"""Human verification of the LLM reviewers (author task).

  python code/human_check.py --make     # write the blinded sheets (once)
  python code/human_check.py --score    # score whatever has been filled in

Samples (simple random, seed in config.SEED):
  screening: 30% of the records screened by two LLM screeners (union + snowball)
  coding:    30% of the included studies
The sheets show only title, venue, year, abstract and link; the LLM decisions are hidden.
Fill `decision` (include/exclude) and `code` (E1-E5) on the screening sheet, and the
five coded fields on the coding sheet, applying data/decisions/protocol_v2.md.

--score writes data/derived/human_check.json. The paper reports human-vs-LLM agreement
automatically once at least 90% of each sheet is filled; until then it states that the
human check is pending.
"""
import argparse
import csv
import json
import random

from config import DECISIONS, DERIVED, SEED, WORK
from s11_selection import kappa

HC = DECISIONS / "human_check"
AXES = ["architecture", "check_strength", "domain", "formalism", "faithfulness_reported"]
FRACTION = 0.30


def make():
    HC.mkdir(parents=True, exist_ok=True)
    if (HC / "screening_sheet.csv").exists():
        raise SystemExit("sheets already exist; delete them first to redraw")
    log = [r for r in csv.DictReader(open(DERIVED / "screening_log.csv", encoding="utf-8"))
           if r["route"] in ("union", "snowball")]
    abstracts = {}
    for line in open(WORK / "search" / "records_union.jsonl", encoding="utf-8"):
        r = json.loads(line)
        abstracts[r["rid"]] = (r.get("abstract", ""), r.get("url", ""))
    for line in open(WORK / "search" / "snowball_candidates.jsonl", encoding="utf-8"):
        r = json.loads(line)
        abstracts.setdefault(__import__("s12_coding").rid_of(r["title"]), (r.get("abstract", ""), r.get("url", "")))
    rng = random.Random(SEED)
    scr = rng.sample(log, round(FRACTION * len(log)))
    with (HC / "screening_sheet.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rid", "title", "venue", "year", "url", "abstract", "decision", "code", "note"])
        for r in scr:
            ab, url = abstracts.get(r["rid"], ("", ""))
            w.writerow([r["rid"], r["title"], r["venue"], r["year"], url, ab, "", "", ""])
    inc = list(csv.DictReader(open(DERIVED / "included_studies.csv", encoding="utf-8")))
    ab = {json.loads(l)["rid"]: json.loads(l)["abstract"] for l in open(WORK / "included_abstracts.jsonl",
                                                                         encoding="utf-8")}
    cod = rng.sample(inc, round(FRACTION * len(inc)))
    with (HC / "coding_sheet.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rid", "title", "venue", "year", "url", "abstract"] + AXES + ["note"])
        for r in cod:
            w.writerow([r["rid"], r["title"], r["venue"], r["year"], r["url"], ab[r["rid"]]] + [""] * 6)
    print(f"[human] wrote {len(scr)} screening and {len(cod)} coding rows to {HC}")


def score():
    out = {"screening": None, "coding": None}
    sheet = HC / "screening_sheet.csv"
    if sheet.exists():
        rows = list(csv.DictReader(open(sheet, encoding="utf-8")))
        done = [r for r in rows if r["decision"].strip().lower() in ("include", "exclude")]
        final = {r["rid"]: r["final"] for r in csv.DictReader(open(DERIVED / "screening_log.csv", encoding="utf-8"))}
        if done:
            h = [r["decision"].strip().lower() for r in done]
            m = [final[r["rid"]] for r in done]
            po, k = kappa(h, m)
            out["screening"] = {"sample": len(rows), "done": len(done), "agree": po, "kappa": k,
                                "human_incl_llm_excl": sum(1 for a, b in zip(h, m) if a == "include" != b),
                                "human_excl_llm_incl": sum(1 for a, b in zip(h, m) if a == "exclude" != b)}
    sheet = HC / "coding_sheet.csv"
    if sheet.exists():
        rows = list(csv.DictReader(open(sheet, encoding="utf-8")))
        done = [r for r in rows if all(r[f].strip() for f in AXES[:4])]
        fin = {r["rid"]: r for r in csv.DictReader(open(DERIVED / "included_studies.csv", encoding="utf-8"))}
        if done:
            out["coding"] = {"sample": len(rows), "done": len(done)}
            for f in AXES:
                pairs = [(r[f].strip(), fin[r["rid"]][f]) for r in done if r[f].strip()]
                if pairs:
                    po, k = kappa([a for a, _ in pairs], [b for _, b in pairs])
                    out["coding"][f] = {"n": len(pairs), "agree": po, "kappa": k}
    complete = bool(out["screening"] and out["screening"]["done"] >= 0.9 * out["screening"]["sample"]
                    and out["coding"] and out["coding"]["done"] >= 0.9 * out["coding"]["sample"])
    out["complete"] = complete
    (DERIVED / "human_check.json").write_text(json.dumps(out, indent=1))
    s = out["screening"]
    print(f"[human] screening done {s['done'] if s else 0}; coding done "
          f"{out['coding']['done'] if out['coding'] else 0}; complete={complete}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--make", action="store_true")
    ap.add_argument("--score", action="store_true")
    a = ap.parse_args()
    if a.make:
        make()
    if a.score or not a.make:
        score()
