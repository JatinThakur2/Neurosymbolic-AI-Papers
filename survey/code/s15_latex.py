"""Stage 7 (v2): every number, table and plot-data file used by the paper.

The paper never types a count: it uses \\cnt{...} macros from tables/numbers.tex.
Outputs (tables/): numbers.tex, tab_*.tex, supp_rows.tex, query_*.txt
        (data/derived/): plot_arch_share.csv (plus the plot_*.csv written by s13)
"""
import csv
import json
from collections import Counter

from config import DERIVED, TABLES, WORK
from s14_bib import clean_text

ARCH = {"A1": "Translate-and-solve", "A2": "Checker-in-the-loop", "A3": "Symbolic guidance",
        "A4": "LM-induced artifacts", "A5": "Symbolic-to-neural transfer", "A6": "Symbolic-oracle evaluation",
        "A7": "LM as interface"}
DOM = {"D1": "Theorem proving \\& autoformalisation", "D2": "Logical \\& deductive reasoning",
       "D3": "Program synthesis \\& structured data", "D4": "Symbolic regression \\& discovery",
       "D5": "Embodied planning \\& agents", "D6": "Vision-language \\& multimodal",
       "D7": "Mathematical problem solving", "D8": "Language, knowledge \\& data"}
FORM = {"F1": "Logic (FOL, ASP, Prolog, SAT/SMT, constraints)", "F2": "Proof assistants \\& verification languages",
        "F3": "General-purpose programs", "F4": "Symbolic mathematics \\& computer algebra",
        "F5": "Rules, knowledge graphs \\& scene graphs", "F6": "Planning languages \\& temporal logic",
        "F7": "DSLs, grammars, automata \\& static analysis"}
REASON = {"E1": "No language model (rule R1)", "E2": "Language model only as baseline, background or frozen encoder",
          "E3": "No interacting explicit symbolic component (R2--R6)", "E4": "Not an archival research paper in scope",
          "E5": "Survey, overview or position paper"}
VENUES = ["AAAI", "IJCAI", "ICLR", "ICML", "NeurIPS", "ACL", "EMNLP", "NAACL", "TMLR", "TPAMI"]


def fmt_int(n):
    return f"{n:,}"


def pct(x, nd=0):
    return f"{100 * x:.{nd}f}"


def main():
    TABLES.mkdir(exist_ok=True)
    sel = json.loads((DERIVED / "selection.json").read_text())
    cod = json.loads((DERIVED / "coding.json").read_text())
    ana = json.loads((DERIVED / "analysis.json").read_text())
    hum = json.loads((DERIVED / "human_check.json").read_text()) if (DERIVED / "human_check.json").exists() else {}
    inc = list(csv.DictReader(open(DERIVED / "included_studies.csv", encoding="utf-8")))
    keys = {r["rid"]: r["bibkey"] for r in csv.DictReader(open(DERIVED / "bibkeys.csv", encoding="utf-8"))}
    m = {}

    # ---- selection
    for k, name in [("corpus_records", "corpusrecords"), ("corpus_duplicates", "corpusdup"),
                    ("source_b_records", "sourceb"), ("query_hits", "queryhits"), ("overlap", "overlap"),
                    ("union", "union"), ("union_included", "unionincl"), ("union_excluded", "unionexcl"),
                    ("union_included_in_corpus", "unioninclcorpus"),
                    ("union_included_search_only", "unioninclsearchonly"),
                    ("union_included_corpus_only", "unioninclcorpusonly"),
                    ("snowball_candidates", "snowcand"), ("snowball_included", "snowincl"),
                    ("audit_screened", "auditscreened"), ("audit_included", "auditincl"),
                    ("included_total", "included"), ("v1_included", "vone"), ("v1_kept", "vonekept"),
                    ("found_in_source_b", "foundinb")]:
        m[name] = fmt_int(sel[k])
    m["snowseeds"] = json.loads((DERIVED / "snowball_summary.json").read_text())["seed_studies_with_local_pdf"]
    m["corpusscreened"] = fmt_int(sel["corpus_records"] - sel["corpus_duplicates"])
    m["vonedropped"] = sel["v1_included"] - sel["v1_kept"]
    for h, s in sel["audit_strata"].items():
        tag = {"lm_only": "lm", "sym_only": "sym", "neither": "nei"}[h]
        m[f"audit{tag}N"], m[f"audit{tag}n"], m[f"audit{tag}x"] = fmt_int(s["N"]), s["n"], s["x"]
    m["excltotal"] = fmt_int(sum(sel["exclusion_reasons"].values()))
    for c, n in sel["exclusion_reasons"].items():
        m[f"excl{c}"] = fmt_int(n)
    ag = sel["agreement"]
    for route, tag in (("union", "union"), ("snowball", "snow")):
        a = ag[route]
        m[f"kappa{tag}"] = f"{a['kappa3']:.2f}"
        m[f"agree{tag}"] = pct(a["agree3"], 1)
        m[f"kappa{tag}incl"] = f"{a['kappa_incl']:.2f}"
        m[f"agree{tag}incl"] = pct(a["agree_incl"], 1)
        m[f"adj{tag}"] = a["adjudicated"]
        m[f"unsure{tag}"] = a["unsure_any"]
        m[f"adjincl{tag}"] = a["adj_include"]
    r = sel["recall"]
    m.update(recallpoint=f"{r['recall_point']:.2f}", recallmedian=f"{r['recall_median']:.2f}",
             recalllo=f"{r['recall_lo']:.2f}", recallhi=f"{r['recall_hi']:.2f}",
             missedpoint=fmt_int(r["missed_point"]), missedlo=fmt_int(r["missed_lo"]),
             missedhi=fmt_int(r["missed_hi"]))
    rs = sel["recall_without_neither"]
    m.update(recallsenslo=f"{rs['recall_lo']:.2f}", recallsenshi=f"{rs['recall_hi']:.2f}",
             recallsensmedian=f"{rs['recall_median']:.2f}")

    # ---- coding
    for f, tag in (("architecture", "arch"), ("check_strength", "check"), ("domain", "dom"),
                   ("formalism", "form"), ("faithfulness_reported", "faith")):
        m[f"kappa{tag}"] = f"{cod['agreement'][f]['kappa']:.2f}"
        m[f"agree{tag}"] = pct(cod["agreement"][f]["agree"], 1)
    m["adjcoding"] = cod["adjudicated"]
    for g, v in cod["entity_jaccard"].items():
        m[f"jac{g}"] = f"{v:.2f}"
    n = len(inc)
    for f in ("architecture", "domain", "formalism", "check_strength", "venue", "year"):
        for k, v in Counter(r[f] for r in inc).items():
            m[k if f != "year" else f"y{k}"] = v
            if f in ("architecture", "domain", "check_strength"):
                m[f"{k}pct"] = pct(v / n)
    for (d, a), v in Counter((r["domain"], r["architecture"]) for r in inc).items():
        m[f"{d}{a}"] = v
    for (a, c), v in Counter((r["architecture"], r["check_strength"]) for r in inc).items():
        m[f"{a}{c}"] = v
    for (d, c), v in Counter((r["domain"], r["check_strength"]) for r in inc).items():
        m[f"{d}{c}"] = v
    for (d, f), v in Counter((r["domain"], r["formalism"]) for r in inc).items():
        m[f"{d}{f}"] = v

    # ---- analysis
    for k, tag in (("assoc_all", "all"), ("assoc_wo_D1_D6", "sens"), ("assoc_formalism_domain", "form")):
        a = ana[k]
        m[f"V{tag}"], m[f"Vc{tag}"], m[f"Vnull{tag}"] = f"{a['V']:.2f}", f"{a['V_corrected']:.2f}", f"{a['V_null_mean']:.2f}"
        m[f"chisq{tag}"] = f"{a['chi2']:.0f}"
        m[f"p{tag}"] = f"{a['p_perm']:.4f}"
        m[f"nperm{tag}"] = fmt_int(a["n_perm"])
        m[f"n{tag}"] = a["n"]
    ptag = {"2020--2022": "early", "2023": "ythree", "2024": "yfour", "2025": "yfive", "2026": "ysix"}
    for p, v in ana["period"].items():
        t = ptag[p]
        m[f"{t}n"] = v["n"]
        for key in ("A1", "A2", "A1A2", "A3", "exact", "checked"):
            k2 = key.replace("1", "one").replace("2", "two").replace("3", "three")
            m[f"{t}{k2}"], m[f"{t}{k2}lo"], m[f"{t}{k2}hi"] = (pct(v[key][0]), pct(v[key][1]), pct(v[key][2]))
    for row in ana["growth"]:
        y = row["year"]
        m[f"pfive{y}"] = row["panel5_per1000"]
        m[f"ptwo{y}"] = row["panel2_per1000"]
        m[f"nesyt{y}"] = row["nesy_title"]
        m[f"incy{y}"] = row["included"]
    m["growthratio"] = round(ana["growth"][5]["panel5_per1000"] / ana["growth"][0]["panel5_per1000"])
    m["pretwentyfour"] = ana["period"]["2020--2022"]["n"] + ana["period"]["2023"]["n"]
    m["accfive2020"] = fmt_int(ana["growth"][0]["panel5_accepted"])
    m["accfive2025"] = fmt_int(ana["growth"][5]["panel5_accepted"])
    m["nesytitle"], m["nesyany"] = ana["nesy_title_total"], ana["nesy_any_total"]
    m["nesytitlepct"], m["nesyanypct"] = pct(ana["nesy_title_total"] / n), pct(ana["nesy_any_total"] / n)
    ar = ana["artifacts"]
    for tag, d in (("rand", ar["random"]), ("aseven", ar["A7_all"])):
        m[f"art{tag}n"], m[f"art{tag}yes"], m[f"art{tag}no"], m[f"art{tag}unc"] = d["n"], d["yes"], d["no"], d["unclear"]
        m[f"art{tag}rate"], m[f"art{tag}lo"], m[f"art{tag}hi"] = (pct(d["rate"][0]), pct(d["rate"][1]), pct(d["rate"][2]))
        m[f"art{tag}known"] = pct(d["rate_known"][0])
        m[f"art{tag}upper"] = pct(d["rate_if_unclear_yes"][0])
    fa = ana["faithfulness"]
    m.update(faithn=fa["n"], faithyes=fa.get("yes", 0), faithno=fa.get("no", 0), faithunc=fa.get("unclear", 0),
             faithyespct=pct(fa.get("yes", 0) / fa["n"]))
    for d, c in fa["by_domain"].items():
        m[f"faith{d}"] = sum(c.values())
        m[f"faith{d}yes"] = c.get("yes", 0)
    mf = ana["minif2f"]
    m.update(mfmention=mf["d1_or_mention"], mfreported=mf["reported"], mfcomparable=mf["comparable"],
             mfmax=f"{mf['max']:.1f}", mfmaxname=mf["max_name"])
    for y, v in mf["by_year_max"].items():
        m[f"mfmax{y}"] = f"{v:.1f}"
    b = ana["benchmarks"]
    m.update(benchstudies=b["studies_naming"], benchdistinct=b["distinct"], benchsingle=b["singletons"],
             benchsinglepct=pct(b["singletons"] / b["distinct"]), benchfiveplus=b["named_by_5plus"])
    for name, c in b["top"][:6]:
        m[f"bench{name}"] = c
    m.update(lmopen=ana["lm_open_any"], lmprop=ana["lm_prop_any"], lmproponly=ana["lm_prop_only"],
             lmopenonly=ana["lm_open_only"])
    m["lmstudies"], m["enginestudies"] = ana["lm"]["studies_naming"], ana["engine"]["studies_naming"]
    m["lmstudiespct"] = pct(ana["lm"]["studies_naming"] / n)
    for name, c in ana["lm"]["counts"]:
        m["lm" + "".join(ch for ch in name.split("/")[0].split(" ")[0] if ch.isalnum())] = c
    for name, c in ana["engine"]["counts"]:
        m["eng" + "".join(ch for ch in name.split(" ")[0] if ch.isalnum())] = c

    # ---- human check
    hs, hc = hum.get("screening"), hum.get("coding")
    m["humandone"] = "1" if hum.get("complete") else "0"
    if hs:
        m.update(humscrn=hs["done"], humscrkappa=f"{hs['kappa']:.2f}", humscragree=pct(hs["agree"], 1),
                 humscrhi=hs["human_incl_llm_excl"], humscrhe=hs["human_excl_llm_incl"])
    if hc:
        m["humcodn"] = hc["done"]
        for f, tag in (("architecture", "arch"), ("check_strength", "check"), ("domain", "dom"),
                       ("formalism", "form"), ("faithfulness_reported", "faith")):
            if f in hc:
                m[f"humcod{tag}"] = f"{hc[f]['kappa']:.2f}"

    lines = ["% Generated by code/s15_latex.py -- do not edit.", r"\makeatletter"]
    for k, v in m.items():
        lines.append(rf"\expandafter\def\csname cnt@{k}\endcsname{{{v}}}")
    lines += [r"\newcommand{\cnt}[1]{\@ifundefined{cnt@#1}{\textbf{??#1??}}{\csname cnt@#1\endcsname}}",
              r"\makeatother",
              r"\newif\ifhumancheck " + (r"\humanchecktrue" if hum.get("complete") else r"\humancheckfalse")]
    (TABLES / "numbers.tex").write_text("\n".join(lines) + "\n")

    # ---- tables
    def write(name, rows):
        (TABLES / name).write_text("\n".join(rows) + "\n")

    # sources and coverage
    acc = Counter()
    yrs = {}
    for line in open(WORK / "search" / "source_b.jsonl", encoding="utf-8"):
        rr = json.loads(line)
        acc[rr["venue"]] += 1
        yrs.setdefault(rr["venue"], set()).add(rr["year"])
    def span(ys):
        ys = sorted(ys)
        runs, start, prev = [], ys[0], ys[0]
        for y in ys[1:]:
            if int(y) != int(prev) + 1:
                runs.append(start if start == prev else f"{start}--{prev[2:]}")
                start = y
            prev = y
        runs.append(start if start == prev else f"{start}--{prev[2:]}")
        return ", ".join(runs)
    corpus_years = {"AAAI": "2020, 2026", "IJCAI": "2025", "TMLR": "2022--26", "TPAMI": "2023--26"}
    inc_v = Counter(r["venue"] for r in inc)
    rows = [r"\begin{tabular}{@{}lllrr@{}}", r"\toprule",
            r"Venue & Source B years & Source A only & Source B records & Included \\", r"\midrule"]
    for v in VENUES:
        rows.append(rf"{v} & {span(yrs[v]) if v in yrs else '--'} & {corpus_years.get(v, '--')} & "
                    rf"{fmt_int(acc[v]) if acc[v] else '--'} & {inc_v[v]} \\")
    rows += [r"\midrule", rf"Total & & & {fmt_int(sum(acc.values()))} & {n} \\", r"\bottomrule", r"\end{tabular}"]
    write("tab_sources.tex", rows)

    rows = [r"\begin{tabular}{@{}lp{0.68\columnwidth}r@{}}", r"\toprule", r"Code & Reason & $n$ \\", r"\midrule"]
    for c in sorted(sel["exclusion_reasons"], key=lambda c: -sel["exclusion_reasons"][c]):
        rows.append(rf"{c} & {REASON[c]} & {fmt_int(sel['exclusion_reasons'][c])} \\")
    rows += [r"\midrule", rf"& Total excluded (union and snowball) & {m['excltotal']} \\", r"\bottomrule", r"\end{tabular}"]
    write("tab_exclusions.tex", rows)

    rows = [r"\begin{tabular}{@{}lrrr@{}}", r"\toprule", r"Decision & $n$ & Agreement (\%) & $\kappa$ \\", r"\midrule",
            r"\multicolumn{4}{@{}l}{\textit{Screening (include / exclude / unsure)}} \\",
            rf"\quad Union records & {fmt_int(ag['union']['n'])} & {m['agreeunion']} & {m['kappaunion']} \\",
            rf"\quad Snowball candidates & {ag['snowball']['n']} & {m['agreesnow']} & {m['kappasnow']} \\",
            r"\multicolumn{4}{@{}l}{\textit{Coding of included studies}} \\"]
    for f, lab in (("architecture", "Architecture"), ("check_strength", "Check strength"), ("domain", "Domain"),
                   ("formalism", "Formalism"), ("faithfulness_reported", "Faithfulness reported")):
        rows.append(rf"\quad {lab} & {n} & {pct(cod['agreement'][f]['agree'], 1)} & {cod['agreement'][f]['kappa']:.2f} \\")
    rows += [r"\bottomrule", r"\end{tabular}"]
    write("tab_agreement.tex", rows)

    doms = sorted(DOM, key=lambda d: -m.get(d, 0))
    cross = Counter((r["domain"], r["architecture"]) for r in inc)
    peak = max(cross.values())
    rows = [r"\setlength{\tabcolsep}{2.6pt}", r"\begin{tabular}{@{}l" + "c" * 7 + "r|rrr@{}}", r"\toprule",
            r"Domain & " + " & ".join(ARCH) + r" & $\Sigma$ & ex. & emp. & none \\", r"\midrule"]
    for d in doms:
        cells = []
        for a in ARCH:
            v = cross.get((d, a), 0)
            cells.append(rf"\cellcolor{{nsblue!{int(8 + 62 * v / peak)}}}{v}" if v else r"\textcolor{black!30}{0}")
        rows.append(rf"{d} {DOM[d]} & " + " & ".join(cells) + rf" & {m[d]} & {m.get(d + 'exact', 0)} & "
                    rf"{m.get(d + 'empirical', 0)} & {m.get(d + 'none', 0)} \\")
    rows += [r"\midrule", r"$\Sigma$ & " + " & ".join(str(m.get(a, 0)) for a in ARCH) +
             rf" & {n} & {m['exact']} & {m['empirical']} & {m['none']} \\", r"\bottomrule", r"\end{tabular}"]
    write("tab_domain_arch.tex", rows)

    rows = [r"\begin{tabular}{@{}llr@{}}", r"\toprule", r"Code & Symbolic formalism & $n$ \\", r"\midrule"]
    for f in sorted(FORM, key=lambda f: -m.get(f, 0)):
        rows.append(rf"{f} & {FORM[f]} & {m.get(f, 0)} \\")
    rows += [r"\bottomrule", r"\end{tabular}"]
    write("tab_formalism.tex", rows)

    def block(title, items, k=8):
        out = [rf"\multicolumn{{2}}{{@{{}}l}}{{\textit{{{title}}}}} \\"]
        for name, c in items[:k]:
            out.append(rf"\quad {name} & {c} \\")
        return out
    bench_label = {}
    for e in csv.DictReader(open(DERIVED / "entities_long.csv", encoding="utf-8")):
        if e["group"] == "benchmark":
            bench_label.setdefault(e["entity"], Counter())[e["label"]] += 1
    top_b = [(bench_label[k].most_common(1)[0][0].replace("&", r"\&"), c) for k, c in b["top"]]
    rows = [r"\begin{tabular}{@{}lr@{}}", r"\toprule", r"Named in abstract & Studies \\", r"\midrule"]
    rows += block(f"Language-model families ({m['lmstudies']} studies name one)", ana["lm"]["counts"], 9) + [r"\midrule"]
    rows += block(f"Symbolic engines ({m['enginestudies']} studies name one)",
                  [(k.replace("&", r"\&"), v) for k, v in ana["engine"]["counts"]], 9) + [r"\midrule"]
    rows += block(f"Benchmarks ({m['benchstudies']} studies name one)", top_b, 9)
    rows += [r"\bottomrule", r"\end{tabular}"]
    write("tab_entities.tex", rows)

    rows = [r"\begin{tabular}{@{}lrrrr@{}}", r"\toprule",
            r"Stratum & $n$ & Released & Not found & Unclear \\", r"\midrule"]
    for a in ARCH:
        d = ar["by_arch_random"].get(a)
        if d and d["n"]:
            rows.append(rf"\quad {a} {ARCH[a]} & {d['n']} & {d['yes']} & {d['no']} & {d['unclear']} \\")
    rr_ = ar["random"]
    rows += [r"\midrule", rf"Random sample & {rr_['n']} & {rr_['yes']} & {rr_['no']} & {rr_['unclear']} \\",
             rf"A7 census & {ar['A7_all']['n']} & {ar['A7_all']['yes']} & {ar['A7_all']['no']} & {ar['A7_all']['unclear']} \\",
             r"\bottomrule", r"\end{tabular}"]
    write("tab_artifacts.tex", rows)

    # ---- plot data: architecture shares per period
    rows_ = list(csv.DictReader(open(DERIVED / "plot_arch_period.csv", encoding="utf-8")))
    with (DERIVED / "plot_arch_share.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["period"] + list(ARCH) + ["n"])
        for r_ in rows_:
            t = int(r_["total"])
            w.writerow([r_["period"]] + [round(100 * int(r_[a]) / t, 1) for a in ARCH] + [t])

    # ---- supplement rows (all included studies)
    order = sorted(inc, key=lambda r: (r["domain"], r["architecture"], r["year"], r["title"]))
    rows = []
    for i, r_ in enumerate(order, 1):
        rows.append(rf"{i} & {clean_text(r_['title'])}~\cite{{{keys[r_['rid']]}}} & {r_['venue']}'{r_['year'][2:]} & {r_['domain']} & "
                    rf"{r_['architecture']} & { {'exact': 'exa', 'empirical': 'emp'}.get(r_['check_strength'], r_['check_strength'])} & {r_['formalism']} \\")
    write("supp_rows.tex", rows)

    # ---- query blocks for the appendix
    import importlib.util
    spec = importlib.util.spec_from_file_location("query", str(WORK.parent / "code" / "search" / "query.py"))
    q = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(q)
    (TABLES / "query_lm.txt").write_text(q.LM_BLOCK + "\n")
    (TABLES / "query_sym.txt").write_text(q.SYMBOLIC_BLOCK + "\n")
    print(f"[s15] wrote {len(m)} macros and tables")


if __name__ == "__main__":
    main()
