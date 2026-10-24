"""Stage 7 (v2): every number, table and plot-data file used by the paper.

The paper never types a count: it uses \\cnt{...} macros from tables/numbers.tex.
Outputs (tables/): numbers.tex, tab_*.tex, supp_rows.tex, query_*.txt
        (data/derived/): plot_arch_share.csv (plus the plot_*.csv written by s13)
"""
import csv
import json
from collections import Counter

from config import DERIVED, TABLES, WORK
from s13_analysis import wilson
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


def fmt_rr(x):
    """Rate ratios: one decimal below 10, integers above, thousands separators for very wide bounds."""
    return f"{x:.1f}" if x < 10 else fmt_int(round(x))


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

    # ---- revision 2: search stage 2, double-screened audit, recall of the full search, accounting
    if "recall_r2" in sel:
        r2 = sel["recall_r2"]
        m.update(recalltwo=f"{r2['recall_median']:.2f}", recalltwolo=f"{r2['recall_lo']:.2f}",
                 recalltwohi=f"{r2['recall_hi']:.2f}", recalltwoplugin=f"{r2['recall_point']:.2f}",
                 missedtwo=fmt_int(r2["missed_median"]), missedtwolo=fmt_int(r2["missed_lo"]),
                 missedtwohi=fmt_int(r2["missed_hi"]), foundtwo=fmt_int(sel["found_in_source_b_r2"]))
        rs2 = sel["recall_r2_without_neither"]
        m.update(recalltwosens=f"{rs2['recall_median']:.2f}", recalltwosenslo=f"{rs2['recall_lo']:.2f}",
                 recalltwosenshi=f"{rs2['recall_hi']:.2f}")
        for h, v in sel["audit_strata_r2"].items():
            tag = {"lm_only": "lm", "sym_only": "sym", "neither": "nei"}[h]
            m[f"audtwo{tag}N"], m[f"audtwo{tag}n"], m[f"audtwo{tag}x"] = fmt_int(v["N"]), v["n"], v["x"]
        m["auditretrieved"] = sel["audit_retrieved_by_augmented_query"]
        st2 = sel["stage2"]
        m.update(augmentedhits=fmt_int(st2["augmented_hits"]), newhits=st2["new_hits"],
                 searchtwo=st2["screened_in_stage2"], searchtwoincl=sel["search2_included"])
        a2 = sel["agreement"]["search2"]
        m.update(kappasearchtwo=f"{a2['kappa3']:.2f}", agreesearchtwo=pct(a2["agree3"], 1),
                 adjsearchtwo=a2["adjudicated"], adjinclsearchtwo=a2["adj_include"])
        au = sel["agreement"]["audit"]
        m.update(kappaaudit=f"{au['kappa3']:.2f}", agreeaudit=pct(au["agree3"], 1), adjaudit=au["adjudicated"])
        for route, tag in (("union", "union"), ("snowball", "snow"), ("search2", "searchtwo")):
            a_ = sel["agreement"][route]
            m[f"kappanu{tag}"] = f"{a_['kappa3_wo_both_unsure']:.2f}"
            m[f"bothunsure{tag}"] = a_["both_unsure"]
        acct = sel["accounting"]
        m.update(srcbrecords=fmt_int(acct["records"]), srcbaddedtwo=acct["r2_added"],
                 srcbdup=acct["duplicate_title"], srcbcollision=acct["id_collision"],
                 srcbinunion=fmt_int(acct["in_union"]), srcbsnow=acct["snowball_candidate"],
                 srcbauditpop=fmt_int(acct["audit_population"]))
        single = sum(sel["agreement"][r]["adj_include"] for r in ("union", "snowball", "search2"))
        dbl = sum(sel["agreement"][r]["included"] for r in ("union", "snowball", "search2"))
        m.update(singleadjincl=single, singleadjinclpct=pct(single / dbl))

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

    # ---- revision 2: Source B composition, audit extension, known-item check
    added = Counter()
    for line in open(WORK / "search" / "source_b.jsonl", encoding="utf-8"):
        rr = json.loads(line)
        if rr.get("r2_added"):
            added[rr["source"]] += 1
    acct = sel["accounting"]
    m.update(sourceb=fmt_int(acct["records"]), sourcebvtwo=fmt_int(acct["records"] - acct["r2_added"]),
             sourcebtitles=fmt_int(sel["source_b_records"]), srcbaddaaai=added["paperlists"],
             srcbaddanth=added["acl-anthology"])
    if "audit_ext" in sel["agreement"]:
        ae = sel["agreement"]["audit_ext"]
        m.update(auditextn=ae["n"], auditextincl=ae["included"], kappaauditext=f"{ae['kappa3']:.2f}",
                 agreeauditext=pct(ae["agree3"], 1), adjauditext=ae["adjudicated"])
        for h, v in sel["audit_strata_r2"].items():
            tag = {"lm_only": "lm", "sym_only": "sym", "neither": "nei"}[h]
            m[f"audext{tag}n"] = v.get("n_ext", 0)
            m[f"audvtwo{tag}n"] = v.get("n_v2", v["n"])
    au_all = sel["audit_included"] + sel.get("audit_ext_included", 0)
    m["auditinclall"] = au_all
    m["otherincl"] = sel["snowball_included"] + au_all + sel.get("knownitem_included", 0)
    m["searchtwoexcl"] = sel["search2_screened"] - sel["search2_included"]
    m["auditall"] = sel["audit_screened"] + sel.get("audit_ext_screened", 0)
    m["exclall"] = fmt_int(sum(sel["exclusion_reasons"].values()))
    ki = sel.get("knownitem")
    if ki:
        p_, lo, hi = wilson(ki["found_by_search"], ki["eligible"])
        m.update(kiref=ki["references"], kisrcb=ki["in_source_b"], kielig=ki["eligible"], kifound=ki["found_by_search"],
                 kifoundpct=pct(p_), kifoundlo=pct(lo), kifoundhi=pct(hi), kinotsrcb=ki["references"] - ki["in_source_b"],
                 kiscreened=sel["knownitem_screened"], kiincl=sel["knownitem_included"],
                 kimissed=ki["eligible"] - ki["found_by_search"])

    # ---- revision 2: sensitivity analyses (s16)
    sp = DERIVED / "sensitivity.json"
    if sp.exists():
        se = json.loads(sp.read_text())
        ptag2 = {"2020--2022": "early", "2023": "ythree", "2024": "yfour", "2025": "yfive", "2026": "ysix"}
        for pname, ptag in (("P2_ICLR_ICML", "ptw"), ("P3_ICLR_ICML_NeurIPS", "pth"), ("all_venues", "pall")):
            for per, v in se["panels"][pname].items():
                t = ptag + ptag2[per]
                m[f"{t}n"], m[f"{t}mn"] = v["all"]["n"], v["methods"]["n"]
                for a in ("A1", "A2", "A3"):
                    an = a.replace("1", "one").replace("2", "two").replace("3", "three")
                    for grp, gt in (("all", ""), ("methods", "m")):
                        p_, lo, hi = v[grp][a]
                        m[f"{t}{gt}{an}"], m[f"{t}{gt}{an}lo"], m[f"{t}{gt}{an}hi"] = pct(p_), pct(lo), pct(hi)
                p_, lo, hi = v["a2_exact_methods"]
                m[f"{t}infexact"], m[f"{t}infexactlo"], m[f"{t}infexacthi"] = pct(p_), pct(lo), pct(hi)
        for key, tag in (("rate_ratio_p5_2025_vs_2020", "rr"), ("rate_ratio_p5_2025_vs_2020_lm", "rrlm"),
                         ("rate_ratio_p2_2026_vs_2020", "rrtw"), ("rate_ratio_p5_2025_vs_2021_22", "rrtt"),
                         ("rate_ratio_p5_2025_vs_2021_22_lm", "rrttlm"), ("rate_ratio_p2_2026_vs_2021_22_lm", "rrtwlm")):
            r_ = se[key]
            m[f"{tag}"], m[f"{tag}lo"], m[f"{tag}hi"] = fmt_rr(r_['rr']), fmt_rr(r_['lo']), fmt_rr(r_['hi'])
            m[f"{tag}kone"], m[f"{tag}ktwo"] = r_["k1"], r_["k2"]
        for row in se["growth"]:
            y = row["year"]
            if row["p5"]["per1000_lm"] is not None and y != "2026":
                m[f"pfivelm{y}"] = f"{row['p5']['per1000_lm']:.1f}"
                m[f"lmshare{y}"] = pct(row["p5"]["lm_share_of_accepted"])
            if row["p2"]["per1000_lm"] is not None:
                m[f"ptwolm{y}"] = f"{row['p2']['per1000_lm']:.1f}"
        dr = se["vocab_drift"]
        shares = {y: v["share"][0] for y, v in dr.items() if v["n"]}
        m["driftmin"], m["driftminyear"] = pct(min(shares.values())), min(shares, key=shares.get)
        m["drifttwentyfive"], m["drifttwentysix"] = pct(shares["2025"]), pct(shares["2026"])
        pa = se["program_aided"]
        wo = pa["without_F3"]
        m.update(Fthreen=pa["F3_n"], woFthreen=wo["n"], woFthreeVc=f"{wo['Vc']:.2f}",
                 woFthreefaithyes=wo["faith_yes"], woFthreefaithn=wo["faith_n"],
                 woFthreeAtwoemp=wo["A2_empirical"], woFthreeAtwo=wo["A2"])
        incl_ = list(csv.DictReader(open(DERIVED / "included_studies.csv", encoding="utf-8")))
        m.update(woFthreeAtwoexact=sum(1 for r in incl_ if r["formalism"] != "F3" and r["architecture"] == "A2"
                                       and r["check_strength"] == "exact"),
                 FthreeAtwoemp=sum(1 for r in incl_ if r["formalism"] == "F3" and r["architecture"] == "A2"
                                   and r["check_strength"] == "empirical"))
        for k_, t in (("early_A2", "earlyAtwo"), ("y26_A2", "ysixAtwo"), ("early_A3", "earlyAthree"), ("y26_A3", "ysixAthree")):
            p_, lo, hi = wo[k_]
            m[f"woFthree{t}"], m[f"woFthree{t}lo"], m[f"woFthree{t}hi"] = pct(p_), pct(lo), pct(hi)
        for a, c in pa["F3_by_arch"].items():
            m[f"Fthree{a}"] = c
        for c_, v in pa["F3_by_check"].items():
            m[f"Fthree{c_}"] = v
        co = se["contribution"]
        m.update(contribmethod=co["method"], contribbench=co["benchmark_or_evaluation"], Atwoexactinf=co["A2_exact"],
                 Asixexact=co["A6_exact"], Afiveexact=co["A5_exact"])
        lodo = se["assoc_leave_one_domain_out"]
        m.update(lodomin=f"{min(lodo.values()):.2f}", lodomax=f"{max(lodo.values()):.2f}",
                 Vcmethods=f"{se['assoc_methods_only']:.2f}")
        m["classicaln"] = se["classical_semantics"]["n"]
        m["athreenlp"], m["athreeall"] = se["nlp_share_A3"]["A3_in_nlp_venues"], se["nlp_share_A3"]["A3"]
        sc = se.get("secondary")
        if sc:
            ct = sc["contribution"]
            m.update(contribmethodtwo=ct.get("method", 0), contribbenchtwo=ct.get("benchmark", 0),
                     contribanalysis=ct.get("analysis", 0),
                     kappacontrib=f"{sc['contribution_agreement'][1]:.2f}", adjcontrib=sc["contribution_adjudicated"],
                     mechkappamin=f"{min(v[1] for v in sc['mechanism_kappa'].values()):.2f}",
                     mechkappamax=f"{max(v[1] for v in sc['mechanism_kappa'].values()):.2f}",
                     mechmulti=sc["multi_mechanism_methods"], mechmultieither=sc["multi_mechanism_methods_either"],
                     mechmultipct=pct(sc["multi_mechanism_methods"] / sc["methods_n"]),
                     methodsn=sc["methods_n"], primaryinagreed=sc["primary_in_agreed_set"],
                     primaryinagreedpct=pct(sc["primary_in_agreed_set"] / sc["methods_n"]),
                     asixbench=sc["A6_by_contribution"].get("benchmark", 0),
                     asixanalysis=sc["A6_by_contribution"].get("analysis", 0),
                     asixmethod=sc["A6_by_contribution"].get("method", 0))
            for i, (name, o) in enumerate(sc["orders"].items(), 1):
                t = "ord" + "abcd"[i - 1]
                g = o["agreed"]
                for key, mk in (("P2_A2_early", "Atwoe"), ("P2_A2_2026", "Atwol"), ("P2_A3_early", "Athreee"),
                                ("P2_A3_2026", "Athreel"), ("A2_early", "allAtwoe"), ("A2_2026", "allAtwol")):
                    m[t + mk] = pct(g[key][0])
                m[t + "same"] = g["same_as_primary"]
                m[t + "A2"] = g["counts"].get("A2", 0)
                m[t + "A3"] = g["counts"].get("A3", 0)
            mp = sc["methods_by_period_P2"]
            for per, tag in (("2020--2022", "early"), ("2026", "ysix")):
                v = mp[per]["all"]
                for a in ("A1", "A2", "A3"):
                    an = a.replace("1", "one").replace("2", "two").replace("3", "three")
                    p_, lo, hi = v[a]
                    m[f"cmp{tag}{an}"], m[f"cmp{tag}{an}lo"], m[f"cmp{tag}{an}hi"] = pct(p_), pct(lo), pct(hi)
                m[f"cmp{tag}n"] = v["n"]
        af = se["audit_found"]
        m.update(afn=af["n"], afAsix=af["arch"].get("A6", 0), afFthree=af["F3"],
                 allAsixpct=pct(af["A6_share_all"]), allFthreepct=pct(af["F3_share_all"]))
        eb = se["exact_by_period"]
        m.update(benchexactearly=eb["2020--2022"]["benchmark_exact"], benchexactsix=eb["2026"]["benchmark_exact"])
        f2 = lambda x: f"{x:.2f}"  # noqa: E731
        for key, tag in (("all_A1", "trAone"), ("all_A2", "trAtwo"), ("all_A3", "trAthree"),
                         ("all_inference_exact", "trexact"), ("methods_A1", "trmAone"), ("methods_A2", "trmAtwo"),
                         ("methods_A3", "trmAthree"), ("methods_inference_exact", "trmexact")):
            t_ = se["trend"][key]
            m[tag], m[tag + "lo"], m[tag + "hi"] = f2(t_["or_per_year"]), f2(t_["lo"]), f2(t_["hi"])
        r_ = se["rate_ratio_p5_2025_vs_2020_stable_vocab"]
        m.update(rrst=fmt_rr(r_['rr']), rrstlo=fmt_rr(r_['lo']), rrsthi=fmt_rr(r_['hi']))
        if sc:
            o2 = [o["agreed"]["trend_A2"] for o in sc["orders"].values()]
            o3 = [o["agreed"]["trend_A3"] for o in sc["orders"].values()]
            m.update(ordtwomin=f2(min(t_["or_per_year"] for t_ in o2)), ordtwomax=f2(max(t_["or_per_year"] for t_ in o2)),
                     ordtwolomin=f2(min(t_["lo"] for t_ in o2)),
                     ordthreemin=f2(min(t_["or_per_year"] for t_ in o3)), ordthreemax=f2(max(t_["or_per_year"] for t_ in o3)),
                     ordthreehimax=f2(max(t_["hi"] for t_ in o3)))
            ys = [o["agreed"]["A2_2026"][0] for o in sc["orders"].values()]
            m.update(ordtwosixmin=pct(min(ys)), ordtwosixmax=pct(max(ys)))
            ys = [o["agreed"]["A3_2026"][0] for o in sc["orders"].values()]
            m.update(ordthreesixmin=pct(min(ys)), ordthreesixmax=pct(max(ys)))
            ys = [o["agreed"]["A3_early"][0] for o in sc["orders"].values()]
            m.update(ordthreeearlymin=pct(min(ys)), ordthreeearlymax=pct(max(ys)))
        fc = se.get("fulltext_check")
        if fc:
            p_, lo, hi = wilson(fc["faith_yes_fulltext"], fc["faith_relevant_fulltext"])
            m.update(ftn=fc["n"], ftfull=fc["full_text"], ftcheckkappa=f"{fc['check_strength']['kappa']:.2f}",
                     ftfaithkappa=f"{fc['faithfulness_reported']['kappa']:.2f}",
                     ftAtwon=fc["check_A2"]["n"], ftAtwoagree=fc["check_A2"]["agree"],
                     ftAonen=fc["check_A1"]["n"], ftAonenone=fc["check_A1"]["fulltext"].get("none", 0),
                     ftAoneexec=fc["check_A1"]["n"] - fc["check_A1"]["fulltext"].get("none", 0),
                     ftfaithrel=fc["faith_relevant_fulltext"], ftfaithyes=fc["faith_yes_fulltext"],
                     ftfaithyespct=pct(p_), ftfaithyeslo=pct(lo), ftfaithyeshi=pct(hi),
                     ftfaithabs=fc["faith_yes_abstract_among_relevant"])
        hcf = se.get("human_confirmed")
        if hcf:
            p_, lo, hi = hcf["precision"]
            m["precisioninv"] = max(2, round(1 / (1 - p_))) if p_ < 1 else "--"
            m.update(precision=pct(p_), precisionlo=pct(lo), precisionhi=pct(hi),
                     precisionn=hcf["sampled_included"], precisionk=hcf["confirmed"])
            fc = hcf["findings_confirmed"]
            m.update(hcn=fc["n"], hcAtwo=fc["arch"].get("A2", 0), hcVc=f"{fc['Vc']:.2f}",
                     hcfaithyes=fc["faith_yes"], hcfaithn=fc["faith_n"])
            for k_, t in (("early_A2", "earlyAtwo"), ("y26_A2", "ysixAtwo")):
                if fc[k_]:
                    m[f"hc{t}"] = pct(fc[k_][0])

    ra = sel.get("recall_r2_without_assistant_decisions")
    if ra:
        m.update(recallassist=f"{ra['recall_median']:.2f}", recallassistlo=f"{ra['recall_lo']:.2f}",
                 recallassisthi=f"{ra['recall_hi']:.2f}")
    # ---- human check
    hs, hc = hum.get("screening"), hum.get("coding")
    m["humandone"] = "1" if hum.get("complete") else "0"
    if hs and "precision_adjudicated" in hs:
        for tag, t in (("adjudicated", "adj"), ("agreed", "agr")):
            v = hs[f"precision_{tag}"]
            p_, lo, hi = wilson(v["confirmed"], v["n"]) if v["n"] else (0, 0, 0)
            m.update({f"prec{t}n": v["n"], f"prec{t}k": v["confirmed"], f"prec{t}": pct(p_),
                      f"prec{t}lo": pct(lo), f"prec{t}hi": pct(hi)})
        rc = hs.get("rejected_codes", {})
        m.update(rejEthree=rc.get("E3", 0), rejtotal=sum(rc.values()))
    s2, c2 = hum.get("second_screening"), hum.get("second_coding")
    m["seconddone"] = "1" if s2 and c2 else "0"
    if s2:
        m.update(secscrn=s2["n"], secscrkappa=f"{s2['kappa']:.2f}", secscragree=pct(s2["agree"], 1))
    if c2:
        m["seccodn"] = c2["n"]
        for f, tag in (("architecture", "arch"), ("check_strength", "check"), ("domain", "dom"),
                       ("formalism", "form"), ("faithfulness_reported", "faith")):
            if f in c2:
                m[f"seccod{tag}"] = f"{c2[f]['kappa']:.2f}"
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
              r"\newif\ifhumancheck " + (r"\humanchecktrue" if hum.get("complete") else r"\humancheckfalse"),
              r"\newif\ifsecondrater " + (r"\secondratertrue" if m.get("seconddone") == "1" else r"\secondraterfalse")]
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
    rows += [r"\midrule", rf"& Total excluded & {m['excltotal']} \\", r"\bottomrule", r"\end{tabular}"]
    write("tab_exclusions.tex", rows)

    rows = [r"\begin{tabular}{@{}lrrrr@{}}", r"\toprule", r"Decision & $n$ & Agr.\ (\%) & $\kappa$ & $\kappa^{*}$ \\", r"\midrule",
            r"\multicolumn{5}{@{}l}{\textit{Screening (include / exclude / unsure)}} \\"]
    for route, lab in (("union", "Stage 1 (union)"), ("search2", "Stage 2"), ("snowball", "Snowball candidates")):
        a = ag[route]
        rows.append(rf"\quad {lab} & {fmt_int(a['n'])} & {pct(a['agree3'], 1)} & {a['kappa3']:.2f} & {a['kappa3_wo_both_unsure']:.2f} \\")
    for route, lab in (("audit", "Recall audit"), ("audit_ext", "Audit extension")):
        if route in ag:
            a = ag[route]
            rows.append(rf"\quad {lab} & {a['n']} & {pct(a['agree3'], 1)} & {a['kappa3']:.2f} & -- \\")
    rows.append(r"\multicolumn{5}{@{}l}{\textit{Coding of included studies}} \\")
    for f, lab in (("architecture", "Architecture"), ("check_strength", "Check strength"), ("domain", "Domain"),
                   ("formalism", "Formalism"), ("faithfulness_reported", "Faithfulness reported")):
        rows.append(rf"\quad {lab} & {n} & {pct(cod['agreement'][f]['agree'], 1)} & {cod['agreement'][f]['kappa']:.2f} & -- \\")
    rows += [r"\bottomrule", r"\multicolumn{5}{@{}l}{\scriptsize $\kappa^{*}$: records that both screeners marked unsure removed.} \\",
             r"\end{tabular}"]
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
    rows += block(f"Benchmarks named by $\\geq$5 studies ({m['benchstudies']} studies name one)",
                  [x for x in top_b if x[1] >= 5], 50)
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
    (TABLES / "query_lm_add.txt").write_text(q.LM_BLOCK_ADD + "\n")
    (TABLES / "query_sym_add.txt").write_text(q.SYMBOLIC_BLOCK_ADD + "\n")
    print(f"[s15] wrote {len(m)} macros and tables")


if __name__ == "__main__":
    main()
