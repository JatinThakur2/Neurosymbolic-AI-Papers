"""Revision-2 provenance step: copy the raw outputs of the stage-2 screeners and adjudicators,
and of the second audit screener, into the versioned decision files.

Run once from the project root:  python tools/assemble_r2.py
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble_decisions import D, concat  # noqa: E402


def concat_or_empty(pattern, out, header):
    """Like concat, but writes a header-only file when there is nothing to concatenate."""
    import glob as _g
    from assemble_decisions import W
    if _g.glob(str(W / pattern)):
        concat(pattern, out)
    else:
        with out.open("w", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerow(header)


def main():
    s = D / "screening"
    concat("screen/aug_s1/*.csv", s / "search2_screener_A.csv")
    concat("screen/aug_s2/*.csv", s / "search2_screener_B.csv")
    concat("adjud/r2/out/*.csv", s / "search2_adjudication.csv")
    concat("screen/audit_s2/*.csv", s / "audit_screener_B.csv")
    # audit extension (revision 2): two screeners; adjudication of every record not excluded by both
    concat("screen/audext_s1/*.csv", s / "audit_ext_screener_A.csv")
    concat("screen/audext_s2/*.csv", s / "audit_ext_screener_B.csv")
    concat_or_empty("adjud/audext/out/*.csv", s / "audit_ext_adjudication.csv",
                    ["rid", "decision", "code", "evidence", "rationale"])
    # fresh known-item check: references of an independent survey that no other route screened
    concat(["knownitem/out/screener_A.csv", "knownitem/out/screener_A_2.csv"], s / "knownitem_screener_A.csv")
    concat(["knownitem/out/screener_B.csv", "knownitem/out/screener_B_2.csv"], s / "knownitem_screener_B.csv")
    concat("knownitem/out/adjudication.csv", s / "knownitem_adjudication.csv")
    # coding: stage-1 coders' files plus the stage-2 files (studies included by the augmented query)
    c = D / "coding"
    for who, old, new in (("coder_A", "c1", "r2_c1"), ("coder_B", "c2", "r2_c2")):
        concat([f"code2/{old}/*.csv", f"code2/{new}/*.csv"], c / f"{who}.csv")
    concat(["code2/adj_out/*.csv", "code2/r2_adj_out/*.csv"], c / "adjudication.csv")
    # miniF2F extraction including the studies added in revision 2
    concat("results/out_m*.csv", D / "results" / "minif2f_extraction.csv")
    # full-text validation sample (revision 2, M9)
    concat("fulltext_check/out/*.csv", D / "fulltext_check" / "fulltext_codes.csv")
    import shutil
    shutil.copy(Path(__file__).resolve().parent.parent / "work" / "fulltext_check" / "design.json",
                D / "fulltext_check" / "design.json")
    # supplementary coding (revision 2, M8): contribution type and all applicable mechanisms
    concat("m8/c1/*.csv", c / "secondary_coder_A.csv")
    concat("m8/c2/*.csv", c / "secondary_coder_B.csv")
    concat("m8/adj/out.csv", c / "secondary_adjudication.csv")
    # keep the provenance marker of the assistant-made coding adjudication (see assemble_decisions.py)
    path = c / "adjudication.csv"
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    for r in rows:
        if r["rid"] == "r96e8617a" and "orchestrating" not in r["evidence"]:
            r["evidence"] += " (adjudicated by the orchestrating assistant)"
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
