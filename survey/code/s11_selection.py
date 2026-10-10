"""Stage 3 (v2): study selection across all routes, agreement and recall.

Routes
  union     curated corpus (Source A) + query hits in the proceedings database (Source B)
  snowball  backward-snowballing candidates (references of included studies)
  audit     stratified random sample of Source B records the query did not retrieve

Outputs
  data/derived/screening_log.csv   one row per screened record: route, both screeners,
                                    adjudication, final decision and reason code
  data/derived/selection.json       PRISMA-ScR flow counts, agreement, recall estimate
"""
import csv
import json
import math
import random
from collections import Counter

from config import DECISIONS, DERIVED, SEED, WORK, norm_title
from s10_screen_union import read, resolve


def kappa(x, y):
    n = len(x)
    po = sum(a == b for a, b in zip(x, y)) / n
    cx, cy = Counter(x), Counter(y)
    pe = sum(cx[k] * cy[k] for k in set(x) | set(y)) / (n * n)
    return po, (po - pe) / (1 - pe)


def recall_estimate(strata, found, draws=100_000):
    """Monte Carlo over Jeffreys Beta posteriors of the eligible proportion per stratum."""
    rng = random.Random(SEED)
    missed, recall = [], []
    for _ in range(draws):
        m = sum(s["N"] * rng.betavariate(s["x"] + 0.5, s["n"] - s["x"] + 0.5) for s in strata.values())
        missed.append(m)
        recall.append(found / (found + m))
    missed.sort()
    recall.sort()
    q = lambda v, p: v[int(p * (len(v) - 1))]  # noqa: E731
    point = sum(s["N"] * s["x"] / s["n"] for s in strata.values())
    return {"missed_point": round(point), "missed_median": round(q(missed, .5)),
            "missed_lo": round(q(missed, .025)), "missed_hi": round(q(missed, .975)),
            "recall_point": found / (found + point), "recall_median": q(recall, .5),
            "recall_lo": q(recall, .025), "recall_hi": q(recall, .975)}


def main():
    s = DECISIONS / "screening"
    union = {json.loads(l)["rid"]: json.loads(l) for l in open(WORK / "search" / "records_union.jsonl",
                                                                 encoding="utf-8")}
    snow = {}
    for line in open(WORK / "search" / "snowball_candidates.jsonl", encoding="utf-8"):
        r = json.loads(line)
        snow[__import__("hashlib").sha1(norm_title(r["title"]).encode()).hexdigest()[:8]] = r
    snow = {"r" + k: v for k, v in snow.items()}

    log, stats = [], {}
    for route, pre in (("union", "union"), ("snowball", "snowball")):
        a, b, adj = read(s / f"{pre}_screener_A.csv"), read(s / f"{pre}_screener_B.csv"), \
            read(s / f"{pre}_adjudication.csv")
        final, sent = resolve(a, b, adj, route)
        x = [a[k]["decision"] for k in a]
        y = [b[k]["decision"] for k in a]
        po3, k3 = kappa(x, y)
        bx = [v == "include" for v in x]
        by = [v == "include" for v in y]
        po2, k2 = kappa(bx, by)
        stats[route] = {"n": len(a), "agree3": po3, "kappa3": k3, "agree_incl": po2, "kappa_incl": k2,
                        "adjudicated": sent, "included": sum(v == "include" for v in final.values()),
                        "unsure_any": sum(1 for k in a if "unsure" in (a[k]["decision"], b[k]["decision"])),
                        "adj_include": sum(1 for k in adj if adj[k]["decision"] == "include")}
        meta = union if route == "union" else snow
        for k in a:
            if final[k] == "exclude":
                code = adj[k]["code"] if k in adj else a[k]["code"]
            else:
                code = ""
            m = meta.get(k, {})
            log.append({"rid": k, "route": route, "title": m.get("title", ""), "venue": m.get("venue", ""),
                        "year": m.get("year", ""), "in_corpus": m.get("in_corpus", "no"),
                        "in_search": m.get("in_search", "yes" if route == "union" else "no"),
                        "screener_A": a[k]["decision"], "screener_B": b[k]["decision"],
                        "adjudication": adj[k]["decision"] if k in adj else "",
                        "evidence": adj[k].get("evidence", "") if k in adj else "abstract",
                        "final": final[k], "reason": code.split(" ")[0] if code else ""})

    # recall audit (one screener; every non-exclude was adjudicated)
    aud = read(s / "audit_screener_A.csv")
    aadj = read(s / "audit_adjudication.csv")
    strata_info = json.loads((DERIVED / "audit_strata.json").read_text())
    stratum = {rid: h for h, ids in strata_info["sample"].items() for rid in ids}
    audit_final = {}
    for k, r in aud.items():
        if r["decision"] != "exclude" and k not in aadj:
            raise SystemExit(f"[s11] audit record {k} not adjudicated")
        audit_final[k] = aadj[k]["decision"] if k in aadj else "exclude"
        log.append({"rid": k, "route": f"audit:{stratum[k]}", "title": "", "venue": "", "year": "",
                    "in_corpus": "no", "in_search": "no", "screener_A": r["decision"], "screener_B": "",
                    "adjudication": aadj[k]["decision"] if k in aadj else "",
                    "evidence": aadj[k].get("evidence", "") if k in aadj else "abstract",
                    "final": audit_final[k],
                    "reason": (aadj[k]["code"] if k in aadj else r["code"]).split(" ")[0]
                    if audit_final[k] == "exclude" else ""})

    sizes = strata_info["strata_sizes"]
    strata = {h: {"N": sizes[h], "n": len(strata_info["sample"][h]),
                  "x": sum(1 for k in strata_info["sample"][h] if audit_final[k] == "include")}
              for h in strata_info["sample"]}
    union_final = {r["rid"]: r["final"] for r in log if r["route"] == "union"}
    found_in_b = sum(1 for k, v in union_final.items() if v == "include" and union[k]["in_search_sources"] == "yes") \
        + stats["snowball"]["included"]
    rec = recall_estimate(strata, found_in_b)
    rec_sens = recall_estimate({h: v for h, v in strata.items() if h != "neither"}, found_in_b)

    # v1 pilot inclusions under the v2 protocol
    with (DECISIONS / "v1_pilot" / "eligibility_decisions.csv").open(encoding="utf-8") as f:
        v1 = {norm_title(r["title"]) for r in csv.DictReader(f) if r["decision"] == "include"}
    v1_rids = {k for k, r in union.items() if norm_title(r["title"]) in v1}
    v1_kept = sum(1 for k in v1_rids if union_final[k] == "include")

    fields = list(log[0].keys())
    with (DERIVED / "screening_log.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(log)
    summ = json.loads((DERIVED / "search_summary.json").read_text())
    reasons = Counter(r["reason"] for r in log if r["route"] in ("union", "snowball") and r["final"] == "exclude")
    out = {
        "corpus_records": summ["corpus_records"], "corpus_duplicates": summ["corpus_duplicates"],
        "source_b_records": summ["search_records_total"], "query_hits": summ["search_hits"],
        "overlap": summ["overlap"], "union": len(union_final),
        "union_included": stats["union"]["included"], "union_excluded": len(union_final) - stats["union"]["included"],
        "union_included_in_corpus": sum(1 for k, v in union_final.items() if v == "include" and union[k]["in_corpus"] == "yes"),
        "union_included_search_only": sum(1 for k, v in union_final.items()
                                          if v == "include" and union[k]["in_corpus"] == "no"),
        "union_included_corpus_only": sum(1 for k, v in union_final.items()
                                          if v == "include" and union[k]["in_search"] == "no"),
        "snowball_candidates": stats["snowball"]["n"], "snowball_included": stats["snowball"]["included"],
        "audit_screened": len(aud), "audit_included": sum(v == "include" for v in audit_final.values()),
        "audit_strata": strata,
        "included_total": stats["union"]["included"] + stats["snowball"]["included"]
        + sum(v == "include" for v in audit_final.values()),
        "exclusion_reasons": dict(sorted(reasons.items())),
        "agreement": stats, "recall": rec, "recall_without_neither": rec_sens, "found_in_source_b": found_in_b,
        "v1_included": len(v1), "v1_matched": len(v1_rids), "v1_kept": v1_kept,
    }
    (DERIVED / "selection.json").write_text(json.dumps(out, indent=2))
    print(f"[s11] included {out['included_total']} (union {out['union_included']}, snowball "
          f"{out['snowball_included']}, audit {out['audit_included']}); recall "
          f"{rec['recall_point']:.2f} [{rec['recall_lo']:.2f}, {rec['recall_hi']:.2f}]")


if __name__ == "__main__":
    main()
