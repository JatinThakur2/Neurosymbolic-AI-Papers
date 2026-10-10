"""Stage 4 (v2): data charting of the included studies.

Two independent LLM coders coded every included study from its title and abstract
(protocol v2); an adjudicator decided every record on which they disagreed in any
coded field. This script joins the codes to the study metadata, computes per-axis
agreement and normalises the models, engines and benchmarks the coders extracted.

Outputs
  data/derived/included_studies.csv   one row per included study (metadata + final codes)
  data/derived/entities_long.csv      study x normalised entity (model / engine / benchmark)
  data/derived/coding.json            per-axis agreement, distributions, entity statistics
  work/included_abstracts.jsonl       abstracts of the included studies (not shipped)
"""
import csv
import hashlib
import json
import re
from collections import Counter

from config import (DECISIONS, DERIVED, ENGINE_FAMILY_V2, LM_FAMILY_V2, WORK, norm_benchmark,
                    norm_title)
from s11_selection import kappa

AXES = ["architecture", "check_strength", "domain", "formalism", "faithfulness_reported"]
ENTITY = {"lm": ("lm_named", LM_FAMILY_V2), "engine": ("engine_named", ENGINE_FAMILY_V2)}


def rid_of(title):
    return "r" + hashlib.sha1(norm_title(title).encode()).hexdigest()[:8]


def read(path):
    with path.open(encoding="utf-8") as f:
        return {r["rid"]: r for r in csv.DictReader(f)}


def families(text, table):
    out = set()
    for item in (t.strip() for t in text.split(";")):
        if not item:
            continue
        for fam, rx in table.items():
            if re.search(rx, item, re.I):
                out.add(fam)
                break
    return out


def main():
    c = DECISIONS / "coding"
    A, B, J = read(c / "coder_A.csv"), read(c / "coder_B.csv"), read(c / "adjudication.csv")
    log = list(csv.DictReader(open(DERIVED / "screening_log.csv", encoding="utf-8")))
    included = {r["rid"]: r for r in log if r["final"] == "include"}
    if set(A) != set(included) or set(B) != set(included):
        raise SystemExit("[s12] coder files do not cover the included studies exactly")
    disputed = {k for k in A if any(A[k][f] != B[k][f] for f in AXES)}
    if disputed != set(J):
        raise SystemExit(f"[s12] adjudication mismatch: {len(disputed ^ set(J))} records")

    # metadata: union records carry it; snowball/audit records come from Source B
    meta = {}
    for line in open(WORK / "search" / "records_union.jsonl", encoding="utf-8"):
        r = json.loads(line)
        if r["rid"] in included:
            meta[r["rid"]] = r
    need = set(included) - set(meta)
    for line in open(WORK / "search" / "source_b.jsonl", encoding="utf-8"):
        r = json.loads(line)
        k = rid_of(r["title"])
        if k in need and k not in meta:
            meta[k] = r
    if set(included) - set(meta):
        raise SystemExit("[s12] metadata missing for some included studies")

    rows, ents = [], []
    with (WORK / "included_abstracts.jsonl").open("w", encoding="utf-8") as fa:
        for k, s in sorted(included.items(), key=lambda kv: (meta[kv[0]]["year"], meta[kv[0]]["venue"],
                                                              meta[kv[0]]["title"])):
            m = meta[k]
            fin = J[k] if k in J else A[k]
            route = s["route"].split(":")[0]
            rows.append({"rid": k, "title": m["title"], "venue": m["venue"], "year": m["year"],
                         "authors": m.get("authors", ""), "url": m.get("url", ""), "route": route,
                         "in_corpus": m.get("in_corpus", "no"),
                         **{f: fin[f] for f in AXES},
                         "adjudicated": "yes" if k in J else "no"})
            fa.write(json.dumps({"rid": k, "title": m["title"], "abstract": m.get("abstract", ""),
                                 "bibtex": m.get("bibtex", ""), "authors": m.get("authors", ""),
                                 "venue": m["venue"], "year": m["year"], "url": m.get("url", "")},
                                ensure_ascii=False) + "\n")
            for group, (field, table) in ENTITY.items():
                for fam in sorted(families(A[k][field], table) | families(B[k][field], table)):
                    ents.append({"rid": k, "group": group, "entity": fam})
            bench = {norm_benchmark(x): x.strip() for x in (A[k]["benchmarks_named"] + ";"
                                                            + B[k]["benchmarks_named"]).split(";") if x.strip()}
            for key, name in sorted(bench.items()):
                if key:
                    ents.append({"rid": k, "group": "benchmark", "entity": key, "label": name})

    with (DERIVED / "included_studies.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with (DERIVED / "entities_long.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["rid", "group", "entity", "label"])
        w.writeheader()
        w.writerows(ents)

    ks = sorted(A)
    agree = {}
    for f in AXES:
        po, kp = kappa([A[k][f] for k in ks], [B[k][f] for k in ks])
        agree[f] = {"agree": po, "kappa": kp}
    # entity agreement: mean Jaccard of the two coders' family sets (studies where either named one)
    jac = {}
    for group, (field, table) in ENTITY.items():
        vals = []
        for k in ks:
            fa_, fb_ = families(A[k][field], table), families(B[k][field], table)
            if fa_ or fb_:
                vals.append(len(fa_ & fb_) / len(fa_ | fb_))
        jac[group] = sum(vals) / len(vals)
    bvals = []
    for k in ks:
        sa = {norm_benchmark(x) for x in A[k]["benchmarks_named"].split(";") if x.strip()}
        sb = {norm_benchmark(x) for x in B[k]["benchmarks_named"].split(";") if x.strip()}
        if sa or sb:
            bvals.append(len(sa & sb) / len(sa | sb))
    jac["benchmark"] = sum(bvals) / len(bvals)

    out = {"n": len(rows), "agreement": agree, "adjudicated": len(J), "entity_jaccard": jac,
           "dist": {f: dict(Counter(r[f] for r in rows)) for f in AXES + ["venue", "year", "route"]}}
    (DERIVED / "coding.json").write_text(json.dumps(out, indent=1))
    print(f"[s12] {len(rows)} studies coded; kappa " +
          ", ".join(f"{f[:6]}={agree[f]['kappa']:.2f}" for f in AXES) +
          f"; entity Jaccard " + ", ".join(f"{g}={v:.2f}" for g, v in jac.items()))


if __name__ == "__main__":
    main()
