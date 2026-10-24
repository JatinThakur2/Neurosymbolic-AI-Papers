"""Stage 3 (v2): study selection across all routes, agreement and recall.

Routes
  union     curated corpus (Source A) + query hits in the proceedings database (Source B)
  snowball  backward-snowballing candidates (references of included studies)
  audit     stratified random sample of Source B records the query did not retrieve
  search2   revision 2: records retrieved only by the augmented query, or added to Source B
  knownitem revision 2: references of an independent survey that no other route screened

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


def knownitem_summary(log):
    """Outcome of every reference in the known-item set (independent survey's reference list)."""
    refs = [dict(zip(("title", "venue", "year"), [x.strip() for x in l.split("|")]))
            for l in open(DECISIONS / "knownitem" / "cheng2025_refs.txt", encoding="utf-8") if l.strip()]
    by_title = {}
    for r in log:
        if r["title"]:
            by_title.setdefault(norm_title(r["title"]), []).append(r)
    srcb = set()
    for line in open(WORK / "search" / "source_b.jsonl", encoding="utf-8"):
        srcb.add(norm_title(json.loads(line)["title"]))
    rows = []
    for ref in refs:
        nt = norm_title(ref["title"])
        hits = by_title.get(nt, [])
        final = "include" if any(h["final"] == "include" for h in hits) else ("exclude" if hits else "")
        routes = sorted({h["route"] for h in hits})
        rows.append({**ref, "in_source_b": nt in srcb, "routes": routes, "final": final,
                     "found_by_search": final == "include" and any(r_ in ("union", "search2", "snowball")
                                                                   for r_ in routes)})
    elig = [r for r in rows if r["final"] == "include"]
    return {"references": len(rows), "in_source_b": sum(r["in_source_b"] for r in rows),
            "eligible": len(elig), "found_by_search": sum(r["found_by_search"] for r in elig),
            "missed": [r["title"] for r in elig if not r["found_by_search"]], "rows": rows}


def main():
    s = DECISIONS / "screening"
    union = {json.loads(l)["rid"]: json.loads(l) for l in open(WORK / "search" / "records_union.jsonl",
                                                                 encoding="utf-8")}
    snow = {}
    for line in open(WORK / "search" / "snowball_candidates.jsonl", encoding="utf-8"):
        r = json.loads(line)
        snow[__import__("hashlib").sha1(norm_title(r["title"]).encode()).hexdigest()[:8]] = r
    snow = {"r" + k: v for k, v in snow.items()}
    stage2 = {json.loads(l)["rid"]: json.loads(l) for l in open(WORK / "search" / "stage2_records.jsonl",
                                                                  encoding="utf-8")}
    known = {json.loads(l)["rid"]: json.loads(l) for l in open(WORK / "knownitem" / "records.jsonl",
                                                                 encoding="utf-8")}

    log, stats = [], {}
    for route, pre in (("union", "union"), ("snowball", "snowball"), ("search2", "search2"),
                       ("knownitem", "knownitem")):
        a, b, adj = read(s / f"{pre}_screener_A.csv"), read(s / f"{pre}_screener_B.csv"), \
            read(s / f"{pre}_adjudication.csv")
        final, sent = resolve(a, b, adj, route)
        x = [a[k]["decision"] for k in a]
        y = [b[k]["decision"] for k in a]
        po3, k3 = kappa(x, y)
        bx = [v == "include" for v in x]
        by = [v == "include" for v in y]
        po2, k2 = kappa(bx, by)
        if route == "search2" and set(a) != set(stage2):
            raise SystemExit("[s11] stage-2 screener files do not cover the stage-2 records exactly")
        if route == "knownitem" and set(a) != set(known):
            raise SystemExit("[s11] known-item screener files do not cover the unscreened references exactly")
        keep = [k for k in a if not (a[k]["decision"] == b[k]["decision"] == "unsure")]
        po3u, k3u = kappa([a[k]["decision"] for k in keep], [b[k]["decision"] for k in keep])
        stats[route] = {"n": len(a), "agree3": po3, "kappa3": k3, "agree_incl": po2, "kappa_incl": k2,
                        "both_unsure": len(a) - len(keep), "agree3_wo_both_unsure": po3u,
                        "kappa3_wo_both_unsure": k3u,
                        "adjudicated": sent, "included": sum(v == "include" for v in final.values()),
                        "unsure_any": sum(1 for k in a if "unsure" in (a[k]["decision"], b[k]["decision"])),
                        "adj_include": sum(1 for k in adj if adj[k]["decision"] == "include")}
        meta = {"union": union, "snowball": snow, "search2": stage2, "knownitem": known}[route]
        for k in a:
            if final[k] == "exclude":
                code = adj[k]["code"] if k in adj else a[k]["code"]
            else:
                code = ""
            m = meta.get(k, {})
            log.append({"rid": k, "route": route, "title": m.get("title", ""), "venue": m.get("venue", ""),
                        "year": m.get("year", ""), "in_corpus": m.get("in_corpus", "no"),
                        "in_search": m.get("in_search", "yes" if route in ("union", "search2") else "no"),
                        "screener_A": a[k]["decision"], "screener_B": b[k]["decision"],
                        "adjudication": adj[k]["decision"] if k in adj else "",
                        "evidence": adj[k].get("evidence", "") if k in adj else "abstract",
                        "final": final[k], "reason": code.split(" ")[0] if code else ""})

    # recall audit: two screeners (the second added in revision 2); every record that either
    # screener did not exclude was adjudicated
    aud = read(s / "audit_screener_A.csv")
    audb = read(s / "audit_screener_B.csv")
    aadj = read(s / "audit_adjudication.csv")
    if set(aud) != set(audb):
        raise SystemExit("[s11] audit screener files differ")
    strata_info = json.loads((DERIVED / "audit_strata.json").read_text())
    stratum = {rid: h for h, ids in strata_info["sample"].items() for rid in ids}
    audit_final = {}
    for k, r in aud.items():
        if (r["decision"] != "exclude" or audb[k]["decision"] != "exclude") and k not in aadj:
            raise SystemExit(f"[s11] audit record {k} not adjudicated")
        if r["decision"] == audb[k]["decision"] == "exclude" and k in aadj:
            raise SystemExit(f"[s11] superfluous audit adjudication {k}")
        audit_final[k] = aadj[k]["decision"] if k in aadj else "exclude"
        log.append({"rid": k, "route": f"audit:{stratum[k]}", "title": "", "venue": "", "year": "",
                    "in_corpus": "no", "in_search": "no", "screener_A": r["decision"],
                    "screener_B": audb[k]["decision"],
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
    xa = [aud[k]["decision"] for k in aud]
    xb = [audb[k]["decision"] for k in aud]
    stats["audit"] = dict(zip(("agree3", "kappa3"), kappa(xa, xb)), n=len(aud),
                          adjudicated=sum(1 for k in aud if k in aadj))
    # revision 2: audit extension (a further random draw from the revision-2 strata), two screeners,
    # every record that either screener did not exclude adjudicated
    r2 = strata_info["r2"]
    ea, eb = read(s / "audit_ext_screener_A.csv"), read(s / "audit_ext_screener_B.csv")
    eadj = read(s / "audit_ext_adjudication.csv")
    ext_stratum = {k: h for h, v in r2.items() for k in v.get("extension", [])}
    if set(ea) != set(ext_stratum) or set(eb) != set(ext_stratum):
        raise SystemExit("[s11] audit-extension screener files do not cover the extension sample exactly")
    ext_final = {}
    for k in ea:
        if (ea[k]["decision"] != "exclude" or eb[k]["decision"] != "exclude") and k not in eadj:
            raise SystemExit(f"[s11] audit-extension record {k} not adjudicated")
        if ea[k]["decision"] == eb[k]["decision"] == "exclude" and k in eadj:
            raise SystemExit(f"[s11] superfluous audit-extension adjudication {k}")
        ext_final[k] = eadj[k]["decision"] if k in eadj else "exclude"
        log.append({"rid": k, "route": f"audit_ext:{ext_stratum[k]}", "title": "", "venue": "", "year": "",
                    "in_corpus": "no", "in_search": "no", "screener_A": ea[k]["decision"],
                    "screener_B": eb[k]["decision"],
                    "adjudication": eadj[k]["decision"] if k in eadj else "",
                    "evidence": eadj[k].get("evidence", "") if k in eadj else "abstract",
                    "final": ext_final[k],
                    "reason": (eadj[k]["code"] if k in eadj else ea[k]["code"]).split(" ")[0]
                    if ext_final[k] == "exclude" else ""})
    stats["audit_ext"] = dict(zip(("agree3", "kappa3"), kappa([ea[k]["decision"] for k in ea],
                                                            [eb[k]["decision"] for k in ea])),
                              n=len(ea), adjudicated=len(eadj),
                              included=sum(v == "include" for v in ext_final.values()))
    # revision 2: recall of the full search (v2 query + augmented query + snowballing)
    s2_final = {r["rid"]: r["final"] for r in log if r["route"] == "search2"}
    aud_retrieved = {k for v in r2.values() for k in v["sample_retrieved_by_augmented_query"]}
    allfinal = {**audit_final, **ext_final}
    strata2 = {h: {"N": v["N"], "n": len(v["sample"]) + len(v.get("extension", [])),
                   "n_v2": len(v["sample"]), "n_ext": len(v.get("extension", [])),
                   "x": sum(1 for k in v["sample"] + v.get("extension", []) if allfinal[k] == "include")}
               for h, v in r2.items()}
    found2 = found_in_b + sum(v == "include" for v in s2_final.values()) \
        + sum(1 for k in aud_retrieved if audit_final[k] == "include")
    rec2 = recall_estimate(strata2, found2)
    # sensitivity: decisions made by the orchestrating assistant (marked in the decision files) reversed
    assist = {k for k, r in {**aadj, **eadj}.items() if "orchestrating" in r.get("evidence", "")}
    alt = {k: ({"include": "exclude", "exclude": "include"}[v] if k in assist else v) for k, v in allfinal.items()}
    strata2_alt = {h: dict(v, x=sum(1 for k in r2[h]["sample"] + r2[h].get("extension", []) if alt[k] == "include"))
                   for h, v in strata2.items()}
    rec2_alt = recall_estimate(strata2_alt, found2)
    rec2_sens = recall_estimate({h: v for h, v in strata2.items() if h != "neither"}, found2)

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
    reasons = Counter(r["reason"] for r in log if r["route"] in ("union", "snowball", "search2", "knownitem")
                      and r["final"] == "exclude")
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
        "search2_screened": stats["search2"]["n"], "search2_included": stats["search2"]["included"],
        "knownitem_screened": stats["knownitem"]["n"], "knownitem_included": stats["knownitem"]["included"],
        "knownitem": knownitem_summary(log),
        "included_total": stats["union"]["included"] + stats["snowball"]["included"]
        + sum(v == "include" for v in audit_final.values()) + stats["search2"]["included"]
        + stats["knownitem"]["included"] + stats["audit_ext"]["included"],
        "audit_ext_screened": stats["audit_ext"]["n"], "audit_ext_included": stats["audit_ext"]["included"],
        "audit_strata_r2": strata2, "recall_r2": rec2, "recall_r2_without_assistant_decisions": rec2_alt,
        "assistant_audit_decisions": sorted(assist), "recall_r2_without_neither": rec2_sens,
        "found_in_source_b_r2": found2, "audit_retrieved_by_augmented_query": len(aud_retrieved),
        "accounting": strata_info["accounting"],
        "stage2": json.loads((DERIVED / "stage2_summary.json").read_text()),
        "exclusion_reasons": dict(sorted(reasons.items())),
        "agreement": stats, "recall": rec, "recall_without_neither": rec_sens, "found_in_source_b": found_in_b,
        "v1_included": len(v1), "v1_matched": len(v1_rids), "v1_kept": v1_kept,
    }
    (DERIVED / "selection.json").write_text(json.dumps(out, indent=2))
    print(f"[s11] included {out['included_total']} (union {out['union_included']}, snowball "
          f"{out['snowball_included']}, audit {out['audit_included']}, stage 2 {out['search2_included']}); "
          f"recall v2 {rec['recall_median']:.2f} [{rec['recall_lo']:.2f}, {rec['recall_hi']:.2f}]; "
          f"recall r2 {rec2['recall_median']:.2f} [{rec2['recall_lo']:.2f}, {rec2['recall_hi']:.2f}]")


if __name__ == "__main__":
    main()
