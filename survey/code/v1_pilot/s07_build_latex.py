"""Stage 7: generate every number, table and plot-data file the paper uses.

The paper never types a count by hand: it uses \\cnt{...} macros from
tables/numbers.tex, and the tables/plots below are regenerated from data/derived.

Outputs (tables/):  numbers.tex, tab_exclusions.tex, tab_venues.tex,
                    tab_domain_arch.tex, tab_formalism.tex, tab_indicators.tex,
                    tab_included.tex
        (data/derived/): share_by_year.csv, included_by_year_venue.csv,
                         arch_by_period.csv
"""
import csv
import json
from collections import Counter
from pathlib import Path

import re
import sys

import config
from config import CLASSICAL_THEMES, DERIVED, TABLES

REASON_TEXT = {
    "E1": "No language model involved",
    "E2": "Language model only as background, baseline or frozen encoder",
    "E3": "No explicit symbolic component",
    "E4": "Not a full research paper (talk or doctoral-consortium abstract)",
    "E5": "Secondary study (survey or overview)",
}
SHORT_ARCH = {"A1": "Translate-and-solve", "A2": "Verifier-in-the-loop", "A3": "Symbolic guidance",
              "A4": "LM-induced artifacts", "A5": "Symbolic-to-neural", "A6": "Symbolic-oracle evaluation",
              "A7": "LM as interface"}
VENUE_ORDER = ["AAAI", "ICLR", "ICML", "IJCAI", "NeurIPS", "TMLR", "TPAMI"]
YEARS = [str(y) for y in range(2020, 2027)]
PERIODS = [("2020--2023", {"2020", "2021", "2022", "2023"}), ("2024", {"2024"}),
           ("2025", {"2025"}), ("2026$^\\ast$", {"2026"})]


def read(name):
    with (DERIVED / name).open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def tex_escape(s):
    return (s.replace("&", r"\&").replace("%", r"\%").replace("_", r"\_").replace("#", r"\#"))


def chi2_stat(pairs):
    """Pearson chi-square statistic of a contingency table given (row, col) pairs."""
    n = len(pairs)
    rc, cc, cell = Counter(r for r, _ in pairs), Counter(c for _, c in pairs), Counter(pairs)
    return sum((cell[(r, c)] - rc[r] * cc[c] / n) ** 2 / (rc[r] * cc[c] / n) for r in rc for c in cc)


def association(pairs, n_perm=10000, seed=2026):
    """Chi-square, Cramer's V and a permutation p-value (labels of one axis shuffled)."""
    import math
    import random
    rows = [r for r, _ in pairs]
    cols = [c for _, c in pairs]
    obs = chi2_stat(pairs)
    k = min(len(set(rows)), len(set(cols))) - 1
    v = math.sqrt(obs / (len(pairs) * k))
    rng = random.Random(seed)
    ge = 0
    for _ in range(n_perm):
        rng.shuffle(cols)
        if chi2_stat(list(zip(rows, cols))) >= obs - 1e-9:
            ge += 1
    return obs, v, (ge + 1) / (n_perm + 1)


def main():
    TABLES.mkdir(exist_ok=True)
    pc = json.loads((DERIVED / "prisma_counts.json").read_text())
    cs = json.loads((DERIVED / "coding_summary.json").read_text())
    ind = json.loads((DERIVED / "indicator_summary.json").read_text())
    log = read("screening_log.csv")
    inc = read("included_studies.csv")
    keys = {r["record_id"]: r["bibkey"] for r in read("bibkeys.csv")}
    labels = {k.split("|")[1]: v for k, v in cs["labels"].items()}

    # ---------------- numbers.tex ----------------
    screened = [r for r in log if r["stage"] != "identification"]
    scr_year = Counter(r["year"] for r in screened)
    inc_year = Counter(r["year"] for r in inc)
    share = {y: round(100 * inc_year[y] / scr_year[y]) for y in YEARS}
    art = Counter(r["artifact_released"] for r in inc)
    n_ft = sum(1 for r in inc if r["fulltext_available"] == "yes")
    macros = {
        "identified": pc["identified"], "withpdf": pc["with_local_pdf"],
        "duplicates": pc["duplicates"], "screened": pc["screened"],
        "exclscreen": pc["excluded_screening"], "filterhits": pc["lm_filter_hits"],
        "titleadds": pc["title_review_additions"], "abstracts": pc["abstracts_extracted"],
        "titlereviewed": pc["title_reviewed"], "notflagged": pc["screened"] - pc["lm_filter_hits"], "assessed": pc["assessed"],
        "exclelig": pc["excluded_eligibility"], "included": pc["included"],
        "includedpct": round(100 * pc["included"] / pc["identified"]),
        "pubabstract": pc["included_from_published_abstract"],
        "fulltext": n_ft, "artifact": art["yes"],
        "artifactpct": round(100 * art["yes"] / n_ft),
        "threshold": ind["threshold"], "spotn": ind["spotcheck_n"], "spotok": ind["spotcheck_confirmed"],
        "nolmfamily": len(ind["studies_without_attributed_lm_family"]),
        "early": sum(inc_year[y] for y in ("2020", "2021", "2022", "2023")),
        "late": sum(inc_year[y] for y in ("2024", "2025", "2026")),
    }
    with (DERIVED.parent / "manual" / "indicator_spotcheck_round1.csv").open(encoding="utf-8") as f:
        r1 = list(csv.DictReader(f))
    macros.update(spotonen=len(r1), spotoneok=sum(1 for r in r1 if r["used_in_study"] == "yes"))
    rp = json.loads((DERIVED / "identification_replay.json").read_text())
    macros.update(replayflagged=rp["flagged"], replaycore=rp["core"], replayadjacent=rp["adjacent"],
                  replaymissed=rp["records"] - rp["flagged"],
                  replaypct=f"{100 * rp['flagged'] / rp['records']:.1f}")
    for k in ("studies_with_lm_family", "studies_with_benchmark", "studies_with_engine", "proprietary_any", "open_any", "both", "open_only", "proprietary_only"):
        macros[k.replace("_", "")] = ind[k]
    for g, d in ind["attributed"].items():
        for name, n in d.items():
            macros["ind" + "".join(ch for ch in name.split(" ")[0] if ch.isalnum())] = n
    for code, n in pc["exclusion_reasons"].items():
        macros[code] = n
    for ax in ("domain", "architecture", "formalism", "venue"):
        for code, n in cs[ax].items():
            macros[code] = n
    for y in YEARS:
        macros[f"y{y}"] = inc_year[y]
        macros[f"s{y}"] = scr_year[y]
        macros[f"share{y}"] = share[y]
    for (d_a, n) in cs["cross_domain_architecture"].items():
        macros[d_a.replace("|", "")] = n
    # ---------------- classical themes vs included ----------------
    abstr = {r["record_id"]: r["abstract"] for r in read("abstracts.csv")}
    inc_ids = {r["record_id"] for r in inc}
    theme_rows = [r"\begin{tabular}{@{}lrrr@{}}", r"\toprule",
                  r"Theme & Screened & Included & Share (\%) \\", r"\midrule"]
    for name, rx in CLASSICAL_THEMES.items():
        hits = [r for r in screened if re.search(rx, r["title"] + " " + abstr.get(r["record_id"], ""), re.I)]
        k = sum(1 for r in hits if r["record_id"] in inc_ids)
        theme_rows.append(rf"{name.capitalize()} & {len(hits)} & {k} & {round(100 * k / len(hits)) if hits else 0} \\")
        slug = "".join(ch for ch in name if ch.isalpha())
        macros[f"theme{slug}"] = len(hits)
        macros[f"themeinc{slug}"] = k
    theme_rows += [r"\bottomrule", r"\end{tabular}"]
    (TABLES / "tab_themes.tex").write_text("\n".join(theme_rows) + "\n")

    # ---------------- second-screener agreement ----------------
    from agreement_kappa import cohen_kappa
    from config import MANUAL, norm_title
    with (MANUAL / "first_screener_pre_resolution.csv").open(encoding="utf-8") as f:
        first = {norm_title(r["title"]): r["decision"] for r in csv.DictReader(f)}
    with (MANUAL / "second_screener_ai.csv").open(encoding="utf-8") as f:
        second = {norm_title(r["title"]): r["decision"] for r in csv.DictReader(f)}
    with (MANUAL / "second_screener_resolution.csv").open(encoding="utf-8") as f:
        resolution = list(csv.DictReader(f))
    ks = sorted(set(first) & set(second))
    po, kap = cohen_kappa([first[k] for k in ks], [second[k] for k in ks])
    macros.update(kappa=f"{kap:.2f}", rawagree=f"{100 * po:.1f}", kappan=len(ks),
                  ndisagree=sum(first[k] != second[k] for k in ks),
                  secondincluded=sum(second[k] == "include" for k in ks),
                  firstincluded=sum(first[k] == "include" for k in ks),
                  resolvedsecond=sum(r["resolved_toward"] == "second" for r in resolution),
                  resolvedfirst=sum(r["resolved_toward"] == "first" for r in resolution),
                  resolvedcode=sum(r["resolved_toward"].startswith("neither") for r in resolution))
    chi, cv, pval = association([(r["domain"], r["architecture"]) for r in inc])
    macros.update(chisq=f"{chi:.1f}", cramerv=f"{cv:.2f}", permp=f"{pval:.4f}", nperm="10{,}000")
    lines = ["% Auto-generated by code/s07_build_latex.py -- do not edit by hand.",
             r"\makeatletter"]
    for k, v in macros.items():
        lines.append(rf"\expandafter\def\csname cnt@{k}\endcsname{{{v}}}")
    lines += [r"\newcommand{\cnt}[1]{\@ifundefined{cnt@#1}{\textbf{??#1??}}{\csname cnt@#1\endcsname}}",
              r"\makeatother"]
    (TABLES / "numbers.tex").write_text("\n".join(lines) + "\n")

    # ---------------- exclusion reasons ----------------
    rows = [r"\begin{tabular}{@{}lp{0.68\columnwidth}r@{}}", r"\toprule", r"Code & Reason & $n$ \\", r"\midrule"]
    for code in sorted(pc["exclusion_reasons"], key=lambda c: -pc["exclusion_reasons"][c]):
        rows.append(rf"{code} & {REASON_TEXT[code]} & {pc['exclusion_reasons'][code]} \\")
    rows += [r"\midrule", rf"& Total excluded at eligibility & {pc['excluded_eligibility']} \\",
             r"\bottomrule", r"\end{tabular}"]
    (TABLES / "tab_exclusions.tex").write_text("\n".join(rows) + "\n")

    # ---------------- venues: corpus vs included ----------------
    corpus_v = Counter(r["venue"] for r in screened)
    rows = [r"\begin{tabular}{@{}lrrr@{}}", r"\toprule",
            r"Venue & Screened & Included & Share (\%) \\", r"\midrule"]
    for v in VENUE_ORDER:
        rows.append(rf"{v} & {corpus_v[v]} & {cs['venue'].get(v, 0)} & "
                    rf"{round(100 * cs['venue'].get(v, 0) / corpus_v[v]) if corpus_v[v] else 0} \\")
    rows += [r"\midrule", rf"Total & {len(screened)} & {len(inc)} & {round(100 * len(inc) / len(screened))} \\",
             r"\bottomrule", r"\end{tabular}"]
    (TABLES / "tab_venues.tex").write_text("\n".join(rows) + "\n")

    # ---------------- domain x architecture heat table ----------------
    doms = sorted(cs["domain"], key=lambda d: -cs["domain"][d])
    archs = sorted(cs["architecture"])
    cross = cs["cross_domain_architecture"]
    peak = max(cross.values())
    rows = [r"\setlength{\tabcolsep}{3.2pt}", r"\begin{tabular}{@{}l" + "c" * len(archs) + "r@{}}", r"\toprule",
            "Domain & " + " & ".join(archs) + r" & $\Sigma$ \\", r"\midrule"]
    for d in doms:
        cells = []
        for a in archs:
            n = cross.get(f"{d}|{a}", 0)
            shade = int(10 + 60 * n / peak) if n else 0
            cells.append(rf"\cellcolor{{nsblue!{shade}}}{n}" if n else r"\textcolor{black!35}{0}")
        rows.append(rf"{d}: {tex_escape(labels[d])} & " + " & ".join(cells) + rf" & {cs['domain'][d]} \\")
    rows += [r"\midrule", r"$\Sigma$ & " + " & ".join(str(cs["architecture"][a]) for a in archs)
             + rf" & {len(inc)} \\", r"\bottomrule", r"\end{tabular}"]
    (TABLES / "tab_domain_arch.tex").write_text("\n".join(rows) + "\n")

    # ---------------- formalisms ----------------
    rows = [r"\begin{tabular}{@{}llr@{}}", r"\toprule", r"Code & Symbolic formalism & $n$ \\", r"\midrule"]
    for f_ in sorted(cs["formalism"], key=lambda c: -cs["formalism"][c]):
        rows.append(rf"{f_} & {tex_escape(labels[f_])} & {cs['formalism'][f_]} \\")
    rows += [r"\bottomrule", r"\end{tabular}"]
    (TABLES / "tab_formalism.tex").write_text("\n".join(rows) + "\n")

    # ---------------- full-text indicators ----------------
    att = ind["attributed"]
    def block(title, d, top):
        out = [rf"\multicolumn{{2}}{{@{{}}l}}{{\textit{{{title}}}}} \\"]
        for k, v in list(d.items())[:top]:
            out.append(rf"\quad {tex_escape(k)} & {v} \\")
        return out
    rows = [r"\begin{tabular}{@{}lr@{}}", r"\toprule", r"Entity & Studies \\", r"\midrule"]
    rows += block("Language-model families", att["lm"], 10) + [r"\midrule"]
    rows += block("Symbolic engines", att["engine"], 9) + [r"\midrule"]
    rows += block("Benchmarks", att["benchmark"], 9)
    rows += [r"\bottomrule", r"\end{tabular}"]
    (TABLES / "tab_indicators.tex").write_text("\n".join(rows) + "\n")

    # ---------------- appendix: all included studies ----------------
    vshort = {"AAAI": "AAAI", "ICLR": "ICLR", "ICML": "ICML", "IJCAI": "IJCAI",
              "NeurIPS": "NeurIPS", "TMLR": "TMLR", "TPAMI": "TPAMI"}
    rows = []
    order = sorted(inc, key=lambda r: (r["domain"], r["architecture"], r["year"], r["title"]))
    for i, r in enumerate(order, 1):
        t = tex_escape(r["title"])
        a = {"yes": r"\checkmark", "no": "--", "not assessed": "n/a"}[r["artifact_released"]]
        rows.append(rf"{i} & {t}~\cite{{{keys[r['record_id']]}}} & {vshort[r['venue']]}'{r['year'][2:]} & "
                    rf"{r['domain']} & {r['architecture']} & {r['formalism']} & {a} \\")
    (TABLES / "tab_included_rows.tex").write_text("\n".join(rows) + "\n")

    # ---------------- plot data ----------------
    with (DERIVED / "share_by_year.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "screened", "included", "share"])
        for y in YEARS:
            w.writerow([y, scr_year[y], inc_year[y], share[y]])
    vy = Counter((r["year"], r["venue"]) for r in inc)
    with (DERIVED / "included_by_year_venue.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year"] + VENUE_ORDER)
        for y in YEARS:
            w.writerow([y] + [vy[(y, v)] for v in VENUE_ORDER])
    ap = Counter()
    for r in inc:
        for name, ys in PERIODS:
            if r["year"] in ys:
                ap[(name, r["architecture"])] += 1
    pkey = {"2020--2023": "early", "2024": "y2024", "2025": "y2025", "2026$^\\ast$": "y2026"}
    lines2 = [r"\makeatletter"]
    for pname, _ in PERIODS:
        for a in archs:
            lines2.append(rf"\expandafter\def\csname cnt@{pkey[pname]}{a}\endcsname{{{ap[(pname, a)]}}}")
        lines2.append(rf"\expandafter\def\csname cnt@{pkey[pname]}AoneAtwo\endcsname{{{ap[(pname, 'A1')] + ap[(pname, 'A2')]}}}")
        lines2.append(rf"\expandafter\def\csname cnt@{pkey[pname]}total\endcsname{{{sum(ap[(pname, a)] for a in archs)}}}")
    lines2.append(r"\makeatother")
    with (TABLES / "numbers.tex").open("a") as f:
        f.write("\n".join(lines2) + "\n")
    art_a = Counter((r["architecture"], r["artifact_released"]) for r in inc)
    rows = [r"\begin{tabular}{@{}lrrr@{}}", r"\toprule",
            r"Architecture & Released & Assessed & Rate (\%) \\", r"\midrule"]
    for a in archs:
        yes, n = art_a[(a, "yes")], art_a[(a, "yes")] + art_a[(a, "no")]
        rows.append(rf"{a} {SHORT_ARCH[a]} & {yes} & {n} & {round(100 * yes / n) if n else 0} \\")
    with (TABLES / "numbers.tex").open("a") as f:
        f.write(r"\makeatletter" + "\n")
        for a in archs:
            yes, n = art_a[(a, "yes")], art_a[(a, "yes")] + art_a[(a, "no")]
            f.write(rf"\expandafter\def\csname cnt@art{a}\endcsname{{{round(100 * yes / n) if n else 0}}}" + "\n")
            f.write(rf"\expandafter\def\csname cnt@artn{a}\endcsname{{{n}}}" + "\n")
            f.write(rf"\expandafter\def\csname cnt@arty{a}\endcsname{{{yes}}}" + "\n")
        f.write(r"\makeatother" + "\n")
    tot_y = sum(art_a[(a, "yes")] for a in archs); tot_n = tot_y + sum(art_a[(a, "no")] for a in archs)
    rows += [r"\midrule", rf"All & {tot_y} & {tot_n} & {round(100 * tot_y / tot_n)} \\", r"\bottomrule", r"\end{tabular}"]
    (TABLES / "tab_artifacts.tex").write_text("\n".join(rows) + "\n")
    with (DERIVED / "arch_by_period.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["period"] + archs + ["total"])
        for name, _ in PERIODS:
            tot = sum(ap[(name, a)] for a in archs)
            w.writerow([name] + [ap[(name, a)] for a in archs] + [tot])
    # ---------------- patterns for the appendix (verbatim from the code) ----------------
    sys.path.insert(0, str(Path(__file__).resolve().parent / "identification"))
    import reference_dblp_classifier as rdc
    pats = {
        "pat_lm_filter.txt": config.LM_FILTER.pattern,
        "pat_title_review.txt": config.TITLE_REVIEW_SCOPE.pattern,
        "pat_core.txt": rdc.CORE.pattern,
        "pat_adjacent.txt": rdc.ADJACENT.pattern,
    }
    for fname, pat in pats.items():
        (TABLES / fname).write_text(pat + "\n")
    dict_lines = []
    for title, d in (("Language-model families", config.LM_FAMILIES),
                     ("Symbolic engines", config.SYMBOLIC_ENGINES), ("Benchmarks", config.BENCHMARKS)):
        dict_lines.append(f"# {title}")
        dict_lines += [f"{k:40s} {v}" for k, v in d.items()]
        dict_lines.append("")
    (TABLES / "pat_dictionaries.txt").write_text("\n".join(dict_lines))
    print(f"[s07] wrote {len(macros)} macros and 8 table files")


if __name__ == "__main__":
    main()
