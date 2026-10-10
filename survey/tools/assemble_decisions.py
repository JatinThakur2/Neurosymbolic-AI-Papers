"""One-off provenance step: copy the raw outputs of the independent AI screeners,
coders, adjudicators and web checkers (written batch by batch under work/) into
the versioned decision files under data/decisions/. Kept so that the path from raw
agent output to the released decision files is auditable.

Run once from the project root:  python tools/assemble_decisions.py
"""
import csv
import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
W = ROOT / "work"
D = ROOT / "data" / "decisions"
sys.path.insert(0, str(ROOT / "code"))
from config import norm_title  # noqa: E402


def concat(pattern, out, extra=None):
    rows, fields = [], None
    for f in sorted(glob.glob(str(W / pattern))):
        with open(f, encoding="utf-8") as fh:
            rd = csv.DictReader(fh)
            fields = fields or rd.fieldnames
            for r in rd:
                if extra:
                    r.update(extra(f, r))
                rows.append(r)
    if extra and rows:
        fields = list(rows[0].keys())
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    ids = [r["rid"] for r in rows]
    assert len(ids) == len(set(ids)), f"duplicate rid in {out}"
    print(f"{out.relative_to(ROOT)}: {len(rows)} rows")
    return rows


def main():
    s = D / "screening"
    concat("screen/s1/*.csv", s / "union_screener_A.csv")
    concat("screen/s2/*.csv", s / "union_screener_B.csv")
    concat("adjud/out/*.csv", s / "union_adjudication.csv")
    concat("screen/snow_s1/*.csv", s / "snowball_screener_A.csv")
    concat("screen/snow_s2/*.csv", s / "snowball_screener_B.csv")
    concat("adjud/snow_out/*.csv", s / "snowball_adjudication.csv")
    concat("screen/audit_s1/*.csv", s / "audit_screener_A.csv")
    concat("adjud/audit_out.csv", s / "audit_adjudication.csv")
    c = D / "coding"
    concat("code2/c1/*.csv", c / "coder_A.csv")
    concat("code2/c2/*.csv", c / "coder_B.csv")
    concat("code2/adj_out/*.csv", c / "adjudication.csv")

    # Web check of artifact release: first pass, overridden by the second pass where it ran.
    first = concat("webcheck/out_w*.csv", W / "webcheck" / "_first.csv")
    second = {r["rid"]: r for r in csv.DictReader(open(W / "webcheck" / "redo_out2.csv", encoding="utf-8"))}
    strata = {}
    for f in sorted(glob.glob(str(W / "webcheck" / "w*.jsonl"))):
        for line in open(f, encoding="utf-8"):
            r = json.loads(line)
            strata[r["rid"]] = (r["stratum"], r["title"])
    out = []
    for r in first:
        row = dict(r, pass_="first")
        if r["rid"] in second:
            row = dict(second[r["rid"]], pass_="second")
        row["stratum"], row["title"] = strata[r["rid"]]
        out.append(row)
    fields = ["rid", "title", "stratum", "released", "artifact_type", "url", "note", "pass_"]
    (D / "webcheck").mkdir(parents=True, exist_ok=True)
    with (D / "webcheck" / "artifact_release.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(out)
    (D / "webcheck" / "design.json").write_text((W / "webcheck" / "design.json").read_text())
    (W / "webcheck" / "_first.csv").unlink()
    print(f"data/decisions/webcheck/artifact_release.csv: {len(out)} rows")

    concat("results/out_m*.csv", D / "results" / "minif2f_extraction.csv")

    # Two adjudications were made by the orchestrating assistant rather than an adjudicator agent;
    # mark them so the provenance is visible in the released files.
    for path, rid in ((s / "audit_adjudication.csv", "ra0dd1fe6"), (c / "adjudication.csv", "r96e8617a")):
        rows = list(csv.DictReader(open(path, encoding="utf-8")))
        for r in rows:
            if r["rid"] == rid and "orchestrating" not in r["evidence"]:
                r["evidence"] += " (adjudicated by the orchestrating assistant)"
        with path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    (D / "screening" / "audit_sample.json").write_text((W / "screen" / "audit_design.json").read_text())


if __name__ == "__main__":
    main()
