"""Stage 5 (v2): analyses reported in the paper.

  * association of architecture with domain: Cramer's V, bias-corrected V
    (Bergsma 2013), permutation null, and a sensitivity analysis
  * architecture and check strength by period, with Wilson intervals
  * growth normalised by accepted papers at venue-years covered by Source B, and a
    terminology check (how many included studies call themselves neurosymbolic)
  * artifact release from the web check (random sample, A7 census)
  * formalisation-faithfulness reporting; miniF2F results reported in abstracts
  * benchmark fragmentation

Outputs: data/derived/analysis.json and plot data (data/derived/plot_*.csv)
"""
import csv
import json
import math
import random
import re
from collections import Counter, defaultdict

from config import DECISIONS, DERIVED, SEED, WORK

PERIODS = [("2020--2022", {"2020", "2021", "2022"}), ("2023", {"2023"}), ("2024", {"2024"}),
           ("2025", {"2025"}), ("2026", {"2026"})]
PANEL5 = {"ICLR", "ICML", "NeurIPS", "ACL", "EMNLP"}
NESY = re.compile(r"neuro-?symbolic|neural[- ]symbolic", re.I)


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0.0, c - h), min(1.0, c + h))


def chi2(pairs):
    n = len(pairs)
    rc, cc, cell = Counter(r for r, _ in pairs), Counter(c for _, c in pairs), Counter(pairs)
    return sum((cell[(r, c)] - rc[r] * cc[c] / n) ** 2 / (rc[r] * cc[c] / n) for r in rc for c in cc)


def cramers(pairs):
    n = len(pairs)
    r, k = len({a for a, _ in pairs}), len({b for _, b in pairs})
    x2 = chi2(pairs)
    v = math.sqrt(x2 / n / (min(r, k) - 1))
    phi2c = max(0.0, x2 / n - (k - 1) * (r - 1) / (n - 1))           # Bergsma (2013)
    rc, kc = r - (r - 1) ** 2 / (n - 1), k - (k - 1) ** 2 / (n - 1)
    vc = math.sqrt(phi2c / min(kc - 1, rc - 1))
    return x2, v, vc


def permutation(pairs, n_perm=10000, seed=SEED):
    rows = [a for a, _ in pairs]
    cols = [b for _, b in pairs]
    x2, v, vc = cramers(pairs)
    rng = random.Random(seed)
    ge, null_v = 0, []
    for _ in range(n_perm):
        rng.shuffle(cols)
        p = list(zip(rows, cols))
        x = chi2(p)
        null_v.append(cramers(p)[1])
        ge += x >= x2 - 1e-9
    return {"n": len(pairs), "chi2": x2, "V": v, "V_corrected": vc, "V_null_mean": sum(null_v) / n_perm,
            "p_perm": (ge + 1) / (n_perm + 1), "n_perm": n_perm}


def main():
    inc = list(csv.DictReader(open(DERIVED / "included_studies.csv", encoding="utf-8")))
    abstracts = {json.loads(l)["rid"]: json.loads(l) for l in open(WORK / "included_abstracts.jsonl",
                                                                       encoding="utf-8")}
    out = {}

    # ---- association
    pairs = [(r["domain"], r["architecture"]) for r in inc]
    out["assoc_all"] = permutation(pairs)
    sub = [(d, a) for d, a in pairs if d not in ("D1", "D6")]
    out["assoc_wo_D1_D6"] = permutation(sub)
    out["assoc_formalism_domain"] = permutation([(r["domain"], r["formalism"]) for r in inc], n_perm=2000)

    # ---- architecture / check strength by period
    per = defaultdict(Counter)
    chk = defaultdict(Counter)
    for r in inc:
        for name, ys in PERIODS:
            if r["year"] in ys:
                per[name][r["architecture"]] += 1
                chk[name][r["check_strength"]] += 1
    archs = sorted({r["architecture"] for r in inc})
    with (DERIVED / "plot_arch_period.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["period"] + archs + ["total"])
        for name, _ in PERIODS:
            w.writerow([name] + [per[name][a] for a in archs] + [sum(per[name].values())])
    out["period"] = {}
    for name, _ in PERIODS:
        n = sum(per[name].values())
        out["period"][name] = {
            "n": n, "A1": wilson(per[name]["A1"], n), "A2": wilson(per[name]["A2"], n), "A1A2": wilson(per[name]["A1"] + per[name]["A2"], n),
            "A3": wilson(per[name]["A3"], n), "exact": wilson(chk[name]["exact"], n),
            "checked": wilson(chk[name]["exact"] + chk[name]["empirical"], n)}

    # ---- growth normalised by accepted papers (Source B venue-years)
    accepted = Counter()
    for line in open(WORK / "search" / "source_b.jsonl", encoding="utf-8"):
        r = json.loads(line)
        accepted[(r["venue"], r["year"])] += 1
    years = [str(y) for y in range(2020, 2027)]
    rows = []
    for y in years:
        p5_acc = sum(accepted[(v, y)] for v in PANEL5)
        p5_inc = sum(1 for r in inc if r["venue"] in PANEL5 and r["year"] == y)
        p2_acc = sum(accepted[(v, y)] for v in ("ICLR", "ICML"))
        p2_inc = sum(1 for r in inc if r["venue"] in ("ICLR", "ICML") and r["year"] == y)
        nesy_t = sum(1 for r in inc if r["year"] == y and NESY.search(r["title"]))
        nesy_ta = sum(1 for r in inc if r["year"] == y and NESY.search(r["title"] + " "
                                                                       + abstracts[r["rid"]]["abstract"]))
        all_y = sum(1 for r in inc if r["year"] == y)
        rows.append({"year": y, "included": all_y, "panel5_included": p5_inc, "panel5_accepted": p5_acc,
                     "panel5_per1000": round(1000 * p5_inc / p5_acc, 2) if p5_acc and y != "2026" else "",
                     "panel2_included": p2_inc, "panel2_accepted": p2_acc,
                     "panel2_per1000": round(1000 * p2_inc / p2_acc, 2) if p2_acc else "",
                     "nesy_title": nesy_t, "nesy_title_or_abstract": nesy_ta,
                     "nesy_title_share": round(100 * nesy_t / all_y) if all_y else 0})
    with (DERIVED / "plot_growth.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    out["growth"] = rows
    out["nesy_title_total"] = sum(1 for r in inc if NESY.search(r["title"]))
    out["nesy_any_total"] = sum(1 for r in inc if NESY.search(r["title"] + " " + abstracts[r["rid"]]["abstract"]))

    # ---- artifacts (web check)
    wc = list(csv.DictReader(open(DECISIONS / "webcheck" / "artifact_release.csv", encoding="utf-8")))
    arch = {r["rid"]: r["architecture"] for r in inc}
    def rate(rows_):
        c = Counter(r["released"] for r in rows_)
        n = len(rows_)
        return {"n": n, "yes": c["yes"], "no": c["no"], "unclear": c["unclear"],
                "rate": wilson(c["yes"], n), "rate_if_unclear_yes": wilson(c["yes"] + c["unclear"], n),
                "rate_known": wilson(c["yes"], c["yes"] + c["no"])}
    rnd = [r for r in wc if r["stratum"] == "random"]
    a7 = [r for r in wc if arch.get(r["rid"]) == "A7"]
    out["artifacts"] = {"random": rate(rnd), "A7_all": rate(a7),
                        "by_arch_random": {a: rate([r for r in rnd if arch[r["rid"]] == a]) for a in archs},
                        "referee_named": {r["title"][:40]: r["released"] for r in wc
                                          if any(t in r["title"].lower() for t in
                                                 ("learned concept library", "hysynth", "zebralogic"))}}

    # ---- formalisation faithfulness (A1/A2 studies whose model writes formal statements)
    f = [r for r in inc if r["faithfulness_reported"] in ("yes", "no", "unclear")]
    out["faithfulness"] = {"n": len(f), **dict(Counter(r["faithfulness_reported"] for r in f)),
                           "by_domain": {d: dict(Counter(r["faithfulness_reported"] for r in f if r["domain"] == d))
                                         for d in sorted({r["domain"] for r in f})}}

    # ---- miniF2F results reported in abstracts
    ext = {r["rid"]: r for r in csv.DictReader(open(DECISIONS / "results" / "minif2f_extraction.csv",
                                                     encoding="utf-8"))}
    comp = list(csv.DictReader(open(DECISIONS / "results" / "minif2f_comparability.csv", encoding="utf-8")))
    pts = []
    for c in comp:
        if c["comparable"] != "yes":
            continue
        e, r = ext[c["rid"]], next(x for x in inc if x["rid"] == c["rid"])
        name = re.split(r"[:\-–]", r["title"])[0].strip()
        name = name if len(name) <= 22 else name[:20] + "."
        lang = e["proof_language"] if e["proof_language"] in ("Lean", "Isabelle") else "unspecified"
        pts.append({"rid": c["rid"], "year": r["year"], "score": float(e["score_pct"]), "lang": lang,
                    "attempts": e["attempts"] or "n/s", "split": e["split"], "name": name,
                    "arch": r["architecture"]})
    pts.sort(key=lambda p: (p["year"], p["score"]))
    with (DERIVED / "plot_minif2f.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(pts[0]))
        w.writeheader()
        w.writerows(pts)
    d1 = [r for r in inc if r["domain"] == "D1"]
    out["minif2f"] = {"d1_or_mention": sum(1 for _ in ext), "reported": sum(1 for r in ext.values()
                                                                            if r["minif2f_reported"] == "yes"),
                      "comparable": len(pts), "max": max(p["score"] for p in pts),
                      "max_name": max(pts, key=lambda p: p["score"])["name"],
                      "by_year_max": {y: max(p["score"] for p in pts if p["year"] == y)
                                      for y in sorted({p["year"] for p in pts})},
                      "d1": len(d1)}

    # ---- benchmarks
    ents = list(csv.DictReader(open(DERIVED / "entities_long.csv", encoding="utf-8")))
    b = [e for e in ents if e["group"] == "benchmark"]
    bc = Counter(e["entity"] for e in b)
    studies_b = {e["rid"] for e in b}
    out["benchmarks"] = {"studies_naming": len(studies_b), "distinct": len(bc),
                         "singletons": sum(1 for v in bc.values() if v == 1),
                         "top": bc.most_common(12),
                         "named_by_5plus": sum(1 for v in bc.values() if v >= 5)}
    for g in ("lm", "engine"):
        e = [x for x in ents if x["group"] == g]
        out[g] = {"studies_naming": len({x["rid"] for x in e}),
                  "counts": Counter(x["entity"] for x in e).most_common()}
    prop = {"GPT-4 family", "GPT-3/3.5, ChatGPT, Codex", "Claude", "Gemini/PaLM/Bard"}
    fam = defaultdict(set)
    for x in ents:
        if x["group"] == "lm":
            fam[x["rid"]].add(x["entity"])
    out["lm_open_any"] = sum(1 for v in fam.values() if v - prop)
    out["lm_prop_any"] = sum(1 for v in fam.values() if v & prop)
    out["lm_prop_only"] = sum(1 for v in fam.values() if v <= prop)
    out["lm_open_only"] = sum(1 for v in fam.values() if not v & prop)
    (DERIVED / "analysis.json").write_text(json.dumps(out, indent=1))
    a = out["assoc_all"]
    print(f"[s13] V={a['V']:.2f} Vc={a['V_corrected']:.2f} null={a['V_null_mean']:.2f} p={a['p_perm']:.4f}; "
          f"artifacts random {out['artifacts']['random']['rate'][0]:.2f}; miniF2F comparable {len(pts)}")


if __name__ == "__main__":
    main()
