"""Stage 5: full-text indicators for the included studies.

For every included study with a local PDF, count how often each language-model
family, symbolic engine and benchmark is named outside the reference block.
An entity is attributed to a study when it reaches INDICATOR_MIN_MENTIONS.
Precision of this rule was spot-checked by hand (data/manual/indicator_spotcheck.csv).

Outputs: data/derived/indicators_long.csv  (study x entity counts)
         data/derived/indicator_summary.json
"""
import csv
import json
import random
import re
from collections import Counter

from config import (BENCHMARKS, DERIVED, INDICATOR_MIN_MENTIONS, LM_FAMILIES,
                    MANUAL, SYMBOLIC_ENGINES, WORK)

GROUPS = {"lm": LM_FAMILIES, "engine": SYMBOLIC_ENGINES, "benchmark": BENCHMARKS}


def strip_references(text: str) -> str:
    """Drop the span from the last 'References' heading to the appendix (if any)."""
    heads = list(re.finditer(r"\n\s*(References|REFERENCES|Bibliography)\s*\n", text))
    if not heads:
        return text
    a = heads[-1].start()
    tail = text[a + 12:]
    b = re.search(r"\n\s*(Appendix|APPENDIX|Appendices|Supplementary|SUPPLEMENTARY|"
                  r"A\.?\s+[A-Z][A-Za-z]+[^\n]{0,60}\n)", tail)
    return text[:a] + (tail[b.start():] if b else "")


def main():
    with (DERIVED / "included_studies.csv").open(encoding="utf-8") as f:
        studies = list(csv.DictReader(f))
    long_rows, attributed = [], {g: Counter() for g in GROUPS}
    n_text = 0
    for s in studies:
        p = WORK / "fulltext" / f"{s['record_id']}.txt"
        if not p.exists():
            continue
        n_text += 1
        text = strip_references(p.read_text(errors="ignore"))
        for g, pats in GROUPS.items():
            for name, rx in pats.items():
                n = len(re.findall(rx, text))
                if n:
                    long_rows.append({"record_id": s["record_id"], "title": s["title"],
                                      "group": g, "entity": name, "mentions": n,
                                      "attributed": "yes" if n >= INDICATOR_MIN_MENTIONS else "no"})
                if n >= INDICATOR_MIN_MENTIONS:
                    attributed[g][name] += 1
    with (DERIVED / "indicators_long.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["record_id", "title", "group", "entity", "mentions", "attributed"])
        w.writeheader()
        w.writerows(long_rows)

    with (MANUAL / "indicator_spotcheck.csv").open(encoding="utf-8") as f:
        spot = list(csv.DictReader(f))
    no_lm = [s["title"] for s in studies
             if (WORK / "fulltext" / f"{s['record_id']}.txt").exists()
             and not any(r["record_id"] == s["record_id"] and r["group"] == "lm" and r["attributed"] == "yes"
                         for r in long_rows)]
    proprietary = {"GPT-4 family (incl. GPT-4o, o1/o3)", "GPT-3.5 / ChatGPT", "GPT-3 / Codex / GPT-2",
                   "Claude", "Gemini / PaLM", "Chinchilla / Gopher"}
    per_study = {}
    for r in long_rows:
        if r["group"] == "lm" and r["attributed"] == "yes":
            per_study.setdefault(r["record_id"], set()).add(r["entity"])
    prop = {k for k, v in per_study.items() if v & proprietary}
    open_ = {k for k, v in per_study.items() if v - proprietary}
    summary = {
        "studies_with_fulltext": n_text,
        "studies_with_lm_family": len(per_study),
        "studies_with_benchmark": len({r["record_id"] for r in long_rows
                                       if r["group"] == "benchmark" and r["attributed"] == "yes"}),
        "studies_with_engine": len({r["record_id"] for r in long_rows
                                    if r["group"] == "engine" and r["attributed"] == "yes"}),
        "proprietary_any": len(prop),
        "open_any": len(open_),
        "both": len(prop & open_),
        "open_only": len(open_ - prop),
        "proprietary_only": len(prop - open_),
        "threshold": INDICATOR_MIN_MENTIONS,
        "attributed": {g: dict(c.most_common()) for g, c in attributed.items()},
        "studies_without_attributed_lm_family": no_lm,
        "spotcheck_n": len(spot),
        "spotcheck_confirmed": sum(1 for r in spot if r["used_in_study"] == "yes"),
    }
    (DERIVED / "indicator_summary.json").write_text(json.dumps(summary, indent=2))
    print(f"[s05] {n_text} full texts; spot-check precision "
          f"{summary['spotcheck_confirmed']}/{summary['spotcheck_n']}")


def draw_spotcheck_sample(k=20, seed=11):
    """Draw a manual spot-check sample of attributed (study, entity) pairs.

    The archived sample in data/manual/indicator_spotcheck.csv was drawn with this
    procedure (seed 11) during the review; re-drawing may give a different sample
    because the pair order depends on file iteration order."""
    with (DERIVED / "indicators_long.csv").open(encoding="utf-8") as f:
        pairs = [(r["title"], r["entity"]) for r in csv.DictReader(f) if r["attributed"] == "yes"]
    random.seed(seed)
    return random.sample(pairs, k)


if __name__ == "__main__":
    main()
