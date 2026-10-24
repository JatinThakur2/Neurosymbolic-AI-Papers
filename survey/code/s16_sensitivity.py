"""Stage 6 (revision 2): sensitivity analyses requested by the second referee report.

  * M3  architecture shares by period on constant-venue panels (ICLR+ICML 2020-2026;
        ICLR+ICML+NeurIPS 2020-2025), methods only (A6 benchmarks set aside)
  * M4  growth: exact Poisson rate-ratio intervals; growth relative to all papers that match
        the language-model block; a vocabulary-drift check using only pre-2022 LM vocabulary
  * M7  main findings with and without program-aided studies (formalism F3)
  * M8  contribution type (method vs benchmark/evaluation); exact checks at inference (A2)
        separated from answer certification in benchmarks (A6)
  * association: leave-one-domain-out bias-corrected Cramer's V
  * "two communities": classical neurosymbolic semantics named in included abstracts
  * M1  key proportions on the human-confirmed subset (once the human sheets are filled)

Output: data/derived/sensitivity.json
"""
import csv
import json
import math
import re
from collections import Counter, defaultdict

import sys
from pathlib import Path

from config import DECISIONS, DERIVED, WORK
from s13_analysis import PERIODS, cramers, wilson

P2 = ("ICLR", "ICML")
P3 = ("ICLR", "ICML", "NeurIPS")
P5 = ("ICLR", "ICML", "NeurIPS", "ACL", "EMNLP")
# language-model vocabulary already in common use before 2022 (no "LLM", "prompting", "in-context", "CoT")
LM_STABLE = re.compile(r"\blanguage models?\b|\btransformers?\b|transformer-based|pre-?trained|\bBERT\b|\bT5\b|"
                       r"\bGPT-?\d?\b|\bCodex\b|seq2seq|sequence[- ]to[- ]sequence|neural sequence models?", re.I)
CLASSICAL = re.compile(r"probabilistic logic|ProbLog|DeepProbLog|Scallop|NeurASP|weighted model counting|"
                       r"knowledge compilation|semantic loss|abductive learning|inductive logic programming|\bILP\b|"
                       r"reasoning shortcuts?|Markov logic|probabilistic circuits?|tractable probabilistic", re.I)


def share_block(rows, key, codes):
    n = len(rows)
    c = Counter(key(r) for r in rows)
    return {"n": n, **{k: wilson(c[k], n) for k in codes}}


METHOD_IDS = None   # set in main(): studies whose coded contribution type is "method"


def is_method(r):
    """Method papers by the supplementary contribution-type coding; falls back to 'not A6'."""
    return r["rid"] in METHOD_IDS if METHOD_IDS is not None else r["architecture"] != "A6"


def period_of(y):
    return next(name for name, ys in PERIODS if y in ys)


def by_period(rows, venues=None, years=None):
    sel = [r for r in rows if (venues is None or r["venue"] in venues) and (years is None or r["year"] in years)]
    out = {}
    for name, ys in PERIODS:
        g = [r for r in sel if r["year"] in ys]
        if not g:
            continue
        meth = [r for r in g if is_method(r)]
        out[name] = {"all": share_block(g, lambda r: r["architecture"], ["A1", "A2", "A3"]),
                     "methods": share_block(meth, lambda r: r["architecture"], ["A1", "A2", "A3"]),
                     "methods_exact": wilson(sum(1 for r in meth if r["check_strength"] == "exact"), len(meth)),
                     "a2_exact_methods": wilson(sum(1 for r in meth if r["architecture"] == "A2"
                                                    and r["check_strength"] == "exact"), len(meth))}
    return out


def binom_cdf(k, n, p):
    if p <= 0:
        return 1.0
    if p >= 1:
        return 0.0 if k < n else 1.0
    lp, lq = math.log(p), math.log1p(-p)
    return min(1.0, sum(math.exp(math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) + i * lp
                                 + (n - i) * lq) for i in range(k + 1)))


def clopper_pearson(k, n, alpha=0.05):
    """Exact binomial interval by bisection on the binomial CDF."""
    def bisect(pred):          # pred is True below the root and False above it
        lo, hi = 0.0, 1.0
        for _ in range(80):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if pred(mid) else (lo, mid)
        return (lo + hi) / 2
    lower = 0.0 if k == 0 else bisect(lambda p: 1 - binom_cdf(k - 1, n, p) < alpha / 2)
    upper = 1.0 if k == n else bisect(lambda p: binom_cdf(k, n, p) > alpha / 2)
    return lower, upper


def rate_ratio(k1, e1, k2, e2):
    """Rate ratio (k2/e2)/(k1/e1) with an exact conditional (Clopper-Pearson) 95% interval."""
    n = k1 + k2
    lo, hi = clopper_pearson(k2, n)
    conv = lambda p: (p / (1 - p)) * (e1 / e2) if p < 1 else float("inf")
    return {"k1": k1, "e1": e1, "k2": k2, "e2": e2, "rr": (k2 / e2) / (k1 / e1) if k1 else float("inf"),
            "lo": conv(lo), "hi": conv(hi)}


def logit_trend(rows, iters=50):
    """Logistic regression of a binary outcome on year (centred at 2024) with venue fixed effects,
    fitted by Newton-Raphson; returns the odds ratio per year with a Wald 95% interval.
    rows: dicts with 'y' (0/1), 'year', 'venue'. Venues without variation in the outcome are dropped."""
    vs = sorted({r["venue"] for r in rows})
    keep = [v for v in vs if 0 < sum(r["y"] for r in rows if r["venue"] == v) < sum(1 for r in rows if r["venue"] == v)]
    data = [r for r in rows if r["venue"] in keep]
    if len(keep) < 1 or not data:
        return None
    X = [[1.0 if r["venue"] == v else 0.0 for v in keep] + [int(r["year"]) - 2024] for r in data]
    Y = [r["y"] for r in data]
    k = len(X[0])
    b = [0.0] * k
    for _ in range(iters):
        g = [0.0] * k
        H = [[0.0] * k for _ in range(k)]
        for x, y in zip(X, Y):
            z = sum(bi * xi for bi, xi in zip(b, x))
            p = 1 / (1 + math.exp(-max(-30, min(30, z))))
            w = p * (1 - p)
            for i in range(k):
                g[i] += (y - p) * x[i]
                for j in range(k):
                    H[i][j] += w * x[i] * x[j]
        step = solve(H, g)
        b = [bi + si for bi, si in zip(b, step)]
        if max(abs(si) for si in step) < 1e-9:
            break
    cov = invert(H)
    se = math.sqrt(cov[-1][-1])
    return {"or_per_year": math.exp(b[-1]), "lo": math.exp(b[-1] - 1.96 * se), "hi": math.exp(b[-1] + 1.96 * se),
            "n": len(data), "venues": keep}


def solve(A, bvec):
    n = len(A)
    M = [row[:] + [bvec[i]] for i, row in enumerate(A)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[piv] = M[piv], M[c]
        if abs(M[c][c]) < 1e-12:
            continue
        for r in range(n):
            if r != c:
                f = M[r][c] / M[c][c]
                M[r] = [a - f * bb for a, bb in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] if abs(M[i][i]) > 1e-12 else 0.0 for i in range(n)]


def invert(A):
    n = len(A)
    cols = [solve(A, [1.0 if i == j else 0.0 for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


MECH = ["A1", "A2", "A3", "A4", "A5", "A7"]
ORDERS = {"paper (A5,A1,A2,A4,A7,A3)": ["A5", "A1", "A2", "A4", "A7", "A3"],
          "verdict first (A2,A1,A5,A4,A7,A3)": ["A2", "A1", "A5", "A4", "A7", "A3"],
          "guidance before checking (A5,A1,A3,A2,A4,A7)": ["A5", "A1", "A3", "A2", "A4", "A7"],
          "reversed (A3,A7,A4,A2,A1,A5)": ["A3", "A7", "A4", "A2", "A1", "A5"]}


def kappa_(x, y):
    n = len(x)
    po = sum(a == b for a, b in zip(x, y)) / n
    cx, cy = Counter(x), Counter(y)
    pe = sum(cx[k] * cy[k] for k in set(x) | set(y)) / (n * n)
    return po, (po - pe) / (1 - pe) if pe < 1 else 1.0


def secondary_coding(inc):
    """Contribution type (method / benchmark / analysis) and every applicable mechanism, coded by two
    independent coders; contribution-type disagreements adjudicated. Mechanism sets are combined
    conservatively (a mechanism counts when both coders list it). Re-applying the decision tree in
    different orders to these sets shows how much the architecture shares depend on the order."""
    c = DECISIONS / "coding"
    fa, fb, fj = c / "secondary_coder_A.csv", c / "secondary_coder_B.csv", c / "secondary_adjudication.csv"
    if not fa.exists():
        return None
    A = {r["rid"]: r for r in csv.DictReader(open(fa, encoding="utf-8"))}
    B = {r["rid"]: r for r in csv.DictReader(open(fb, encoding="utf-8"))}
    J = {r["rid"]: r for r in csv.DictReader(open(fj, encoding="utf-8"))} if fj.exists() else {}
    ids = [r["rid"] for r in inc]
    if set(A) != set(ids) or set(B) != set(ids):
        raise SystemExit("[s16] secondary coding does not cover the included studies exactly")
    dis = {k for k in ids if A[k]["contribution_type"] != B[k]["contribution_type"]}
    if dis != set(J):
        raise SystemExit("[s16] secondary adjudication does not match the contribution-type disagreements")
    contrib = {k: (J[k] if k in J else A[k])["contribution_type"] for k in ids}
    sets = lambda r: {m.strip() for m in r["mechanisms"].split(";") if m.strip()}  # noqa: E731
    agreed = {k: sets(A[k]) & sets(B[k]) for k in ids}
    either = {k: sets(A[k]) | sets(B[k]) for k in ids}
    res = {"contribution": dict(Counter(contrib.values())),
           "contribution_agreement": kappa_([A[k]["contribution_type"] for k in ids],
                                            [B[k]["contribution_type"] for k in ids]),
           "contribution_adjudicated": len(J),
           "mechanism_kappa": {m: kappa_([m in sets(A[k]) for k in ids], [m in sets(B[k]) for k in ids])
                               for m in MECH},
           "mechanism_sets_identical": sum(sets(A[k]) == sets(B[k]) for k in ids)}
    arch = {r["rid"]: r["architecture"] for r in inc}
    res["A6_by_contribution"] = dict(Counter(contrib[k] for k in ids if arch[k] == "A6"))
    res["contribution_by_arch"] = {a: dict(Counter(contrib[k] for k in ids if arch[k] == a))
                                   for a in sorted(set(arch.values()))}
    meth = [r for r in inc if contrib[r["rid"]] == "method"]
    res["methods_n"] = len(meth)
    res["multi_mechanism_methods"] = sum(1 for r in meth if len(agreed[r["rid"]]) >= 2)
    res["multi_mechanism_methods_either"] = sum(1 for r in meth if len(either[r["rid"]]) >= 2)
    res["primary_in_agreed_set"] = sum(1 for r in meth if r["architecture"] in agreed[r["rid"]])
    res["primary_in_either_set"] = sum(1 for r in meth if r["architecture"] in either[r["rid"]])
    res["mechanism_prevalence_methods"] = {m: sum(1 for r in meth if m in agreed[r["rid"]]) for m in MECH}

    def recode(r, order, msets):
        m = msets[r["rid"]] or ({r["architecture"]} if r["architecture"] in MECH else set())
        return next((a for a in order if a in m), "none")

    res["orders"] = {}
    for name, order in ORDERS.items():
        o = {}
        for tag, msets in (("agreed", agreed), ("either", either)):
            codes = {r["rid"]: recode(r, order, msets) for r in meth}
            cnt = Counter(codes.values())
            early = [r for r in meth if r["year"] in ("2020", "2021", "2022")]
            late = [r for r in meth if r["year"] == "2026"]
            p2e = [r for r in early if r["venue"] in P2]
            p2l = [r for r in late if r["venue"] in P2]
            o[tag] = {"counts": dict(cnt), "same_as_primary": sum(codes[r["rid"]] == r["architecture"] for r in meth),
                      "A2_early": wilson(sum(codes[r["rid"]] == "A2" for r in early), len(early)),
                      "A2_2026": wilson(sum(codes[r["rid"]] == "A2" for r in late), len(late)),
                      "A3_early": wilson(sum(codes[r["rid"]] == "A3" for r in early), len(early)),
                      "A1_early": wilson(sum(codes[r["rid"]] == "A1" for r in early), len(early)),
                      "A1_2026": wilson(sum(codes[r["rid"]] == "A1" for r in late), len(late)),
                      "trend_A2": logit_trend([dict(r, y=int(codes[r["rid"]] == "A2")) for r in meth]),
                      "trend_A3": logit_trend([dict(r, y=int(codes[r["rid"]] == "A3")) for r in meth]),
                      "A3_2026": wilson(sum(codes[r["rid"]] == "A3" for r in late), len(late)),
                      "P2_A2_early": wilson(sum(codes[r["rid"]] == "A2" for r in p2e), len(p2e)),
                      "P2_A2_2026": wilson(sum(codes[r["rid"]] == "A2" for r in p2l), len(p2l)),
                      "P2_A3_early": wilson(sum(codes[r["rid"]] == "A3" for r in p2e), len(p2e)),
                      "P2_A3_2026": wilson(sum(codes[r["rid"]] == "A3" for r in p2l), len(p2l))}
        res["orders"][name] = o
    # methods-only period shares by the primary code, using the coded contribution type
    res["methods_by_period"] = by_period(meth)
    res["methods_by_period_P2"] = by_period(meth, P2)
    return res


def main():
    global METHOD_IDS
    inc = list(csv.DictReader(open(DERIVED / "included_studies.csv", encoding="utf-8")))
    c_ = DECISIONS / "coding"
    if (c_ / "secondary_coder_A.csv").exists():
        A_ = {r["rid"]: r for r in csv.DictReader(open(c_ / "secondary_coder_A.csv", encoding="utf-8"))}
        J_ = {r["rid"]: r for r in csv.DictReader(open(c_ / "secondary_adjudication.csv", encoding="utf-8"))}
        METHOD_IDS = {k for k in A_ if (J_[k] if k in J_ else A_[k])["contribution_type"] == "method"}
    abstracts = {json.loads(l)["rid"]: json.loads(l)["abstract"]
                 for l in open(WORK / "included_abstracts.jsonl", encoding="utf-8")}
    out = {}

    # ---- M3: constant-venue panels
    out["panels"] = {"all_venues": by_period(inc),
                     "P2_ICLR_ICML": by_period(inc, P2),
                     "P3_ICLR_ICML_NeurIPS": by_period(inc, P3, {str(y) for y in range(2020, 2026)})}
    archs = ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]
    with (DERIVED / "plot_arch_share_panels.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["label"] + archs + ["n"])
        for tag, ven in (("All venues", None), ("ICLR+ICML", P2)):
            for name, ys in PERIODS:
                g_ = [r for r in inc if r["year"] in ys and (ven is None or r["venue"] in ven)]
                c_ = Counter(r["architecture"] for r in g_)
                short = name.replace("2020--2022", "2020--22")
                w.writerow([f"{'All' if ven is None else 'ICLR+ICML'}: {short} ({len(g_)})"] + [round(100 * c_[a] / len(g_), 1) for a in archs]
                           + [len(g_)])
    out["venue_mix"] = {name: dict(Counter(r["venue"] for r in inc if r["year"] in ys)) for name, ys in PERIODS}
    out["nlp_share_A3"] = {"A3_in_nlp_venues": sum(1 for r in inc if r["architecture"] == "A3"
                                                     and r["venue"] in ("ACL", "EMNLP", "NAACL")),
                           "A3": sum(1 for r in inc if r["architecture"] == "A3")}

    # ---- M4: growth, denominators, vocabulary drift
    acc, lm_acc, lm_stable_acc = Counter(), Counter(), Counter()
    sys.path.insert(0, str(Path(__file__).resolve().parent / "search"))
    from query import LM_RE_V2  # noqa: E402  (frozen v2 language-model block)
    for line in open(WORK / "search" / "source_b.jsonl", encoding="utf-8"):
        r = json.loads(line)
        key = (r["venue"], r["year"])
        acc[key] += 1
        text = f"{r['title']} {r['abstract']}"
        if LM_RE_V2.search(text):
            lm_acc[key] += 1
        if LM_STABLE.search(text):
            lm_stable_acc[key] += 1
    years = [str(y) for y in range(2020, 2027)]
    growth = []
    for y in years:
        row = {"year": y}
        for tag, ven in (("p5", P5), ("p2", P2)):
            k = sum(1 for r in inc if r["venue"] in ven and r["year"] == y)
            a = sum(acc[(v, y)] for v in ven)
            lm = sum(lm_acc[(v, y)] for v in ven)
            ls = sum(lm_stable_acc[(v, y)] for v in ven)
            row[tag] = {"included": k, "accepted": a, "lm_papers": lm, "lm_stable_papers": ls,
                        "per1000": 1000 * k / a if a else None, "per1000_lm": 1000 * k / lm if lm else None,
                        "lm_share_of_accepted": lm / a if a else None}
        growth.append(row)
    with (DERIVED / "plot_growth_lm.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["year", "p5_per1000_lm", "p2_per1000_lm", "p5_lm_share"])
        for row in growth:
            p5, p2 = row["p5"], row["p2"]
            w.writerow([row["year"], round(p5["per1000_lm"], 1) if p5["per1000_lm"] and row["year"] != "2026" else "",
                        round(p2["per1000_lm"], 1) if p2["per1000_lm"] else "",
                        round(100 * p5["lm_share_of_accepted"], 1) if p5["lm_share_of_accepted"] and row["year"] != "2026" else ""])
    out["growth"] = growth
    g = {r["year"]: r for r in growth}
    out["rate_ratio_p5_2025_vs_2020"] = rate_ratio(g["2020"]["p5"]["included"], g["2020"]["p5"]["accepted"],
                                                   g["2025"]["p5"]["included"], g["2025"]["p5"]["accepted"])
    out["rate_ratio_p5_2025_vs_2020_lm"] = rate_ratio(g["2020"]["p5"]["included"], g["2020"]["p5"]["lm_papers"],
                                                      g["2025"]["p5"]["included"], g["2025"]["p5"]["lm_papers"])
    out["rate_ratio_p2_2026_vs_2020"] = rate_ratio(g["2020"]["p2"]["included"], g["2020"]["p2"]["accepted"],
                                                   g["2026"]["p2"]["included"], g["2026"]["p2"]["accepted"])
    out["rate_ratio_p5_2025_vs_2021_22"] = rate_ratio(
        g["2021"]["p5"]["included"] + g["2022"]["p5"]["included"],
        g["2021"]["p5"]["accepted"] + g["2022"]["p5"]["accepted"],
        g["2025"]["p5"]["included"], g["2025"]["p5"]["accepted"])
    out["rate_ratio_p5_2025_vs_2021_22_lm"] = rate_ratio(
        g["2021"]["p5"]["included"] + g["2022"]["p5"]["included"],
        g["2021"]["p5"]["lm_papers"] + g["2022"]["p5"]["lm_papers"],
        g["2025"]["p5"]["included"], g["2025"]["p5"]["lm_papers"])
    out["rate_ratio_p2_2026_vs_2021_22_lm"] = rate_ratio(
        g["2021"]["p2"]["included"] + g["2022"]["p2"]["included"],
        g["2021"]["p2"]["lm_papers"] + g["2022"]["p2"]["lm_papers"],
        g["2026"]["p2"]["included"], g["2026"]["p2"]["lm_papers"])
    # vocabulary drift: would the included Source-B studies of each year have matched old-style LM vocabulary?
    drift = {}
    for y in years:
        rows = [r for r in inc if r["year"] == y and r.get("in_search") == "yes"]
        k = sum(1 for r in rows if LM_STABLE.search(r["title"] + " " + abstracts.get(r["rid"], "")))
        drift[y] = {"n": len(rows), "stable_match": k, "share": wilson(k, len(rows))}
    out["vocab_drift"] = drift

    # M3: year trend with venue fixed effects (all studies; methods only)
    out["trend"] = {}
    for tag, rows_ in (("all", inc), ("methods", [r for r in inc if is_method(r)])):
        for a in ("A1", "A2", "A3"):
            out["trend"][f"{tag}_{a}"] = logit_trend([dict(r, y=int(r["architecture"] == a)) for r in rows_])
        out["trend"][f"{tag}_inference_exact"] = logit_trend(
            [dict(r, y=int(r["architecture"] == "A2" and r["check_strength"] == "exact")) for r in rows_])
    # M4: growth counting only included studies whose title/abstract use pre-2022 language-model vocabulary
    st = {y: sum(1 for r in inc if r["venue"] in P5 and r["year"] == y
                 and LM_STABLE.search(r["title"] + " " + abstracts.get(r["rid"], ""))) for y in years}
    out["rate_ratio_p5_2025_vs_2020_stable_vocab"] = rate_ratio(st["2020"], g["2020"]["p5"]["accepted"],
                                                                st["2025"], g["2025"]["p5"]["accepted"])

    # ---- M7: with and without program-aided studies (formalism F3)
    def key_findings(rows):
        n = len(rows)
        per = by_period(rows)
        f = [r for r in rows if r["faithfulness_reported"] in ("yes", "no", "unclear")]
        a2 = [r for r in rows if r["architecture"] == "A2"]
        pairs = [(r["domain"], r["architecture"]) for r in rows]
        _, v, vc = cramers(pairs)
        return {"n": n, "arch": dict(Counter(r["architecture"] for r in rows)),
                "A2_empirical": sum(1 for r in a2 if r["check_strength"] == "empirical"), "A2": len(a2),
                "faith_yes": sum(1 for r in f if r["faithfulness_reported"] == "yes"), "faith_n": len(f),
                "V": v, "Vc": vc,
                "early_A2": per.get("2020--2022", {}).get("all", {}).get("A2"),
                "y26_A2": per.get("2026", {}).get("all", {}).get("A2"),
                "early_A3": per.get("2020--2022", {}).get("all", {}).get("A3"),
                "y26_A3": per.get("2026", {}).get("all", {}).get("A3")}
    out["program_aided"] = {"all": key_findings(inc),
                            "without_F3": key_findings([r for r in inc if r["formalism"] != "F3"]),
                            "F3_n": sum(1 for r in inc if r["formalism"] == "F3"),
                            "F3_by_arch": dict(Counter(r["architecture"] for r in inc if r["formalism"] == "F3")),
                            "F3_by_check": dict(Counter(r["check_strength"] for r in inc if r["formalism"] == "F3"))}

    # ---- M8: contribution type; exact checks at inference vs benchmark certification
    meth = [r for r in inc if is_method(r)]
    bench = [r for r in inc if r["architecture"] == "A6"]
    out["contribution"] = {"method": len(meth), "benchmark_or_evaluation": len(bench),
                           "method_arch": dict(Counter(r["architecture"] for r in meth)),
                           "A2_exact": sum(1 for r in inc if r["architecture"] == "A2" and r["check_strength"] == "exact"),
                           "A6_exact": sum(1 for r in bench if r["check_strength"] == "exact"),
                           "A5_exact": sum(1 for r in inc if r["architecture"] == "A5" and r["check_strength"] == "exact")}
    per_exact = {}
    for name, ys in PERIODS:
        g_ = [r for r in inc if r["year"] in ys]
        m_ = [r for r in g_ if is_method(r)]
        b_ = [r for r in g_ if r["architecture"] == "A6"]
        per_exact[name] = {"inference_exact_share_of_methods": wilson(
            sum(1 for r in m_ if r["architecture"] == "A2" and r["check_strength"] == "exact"), len(m_)),
            "benchmark_exact": sum(1 for r in b_ if r["check_strength"] == "exact"), "benchmarks": len(b_)}
    out["exact_by_period"] = per_exact

    # ---- M8 (supplementary double coding): contribution type and all applicable mechanisms
    sec = secondary_coding(inc)
    if sec:
        out["secondary"] = sec

    # ---- M9: abstract-based codes against full-text codes (random sample of A1/A2 studies)
    ft = DECISIONS / "fulltext_check" / "fulltext_codes.csv"
    if ft.exists():
        F = list(csv.DictReader(open(ft, encoding="utf-8")))
        byid = {r["rid"]: r for r in inc}
        full = [r for r in F if "abstract only" not in r["source"].lower()]
        res = {"n": len(F), "full_text": len(full)}
        for f in ("check_strength", "faithfulness_reported"):
            pairs = [(byid[r["rid"]][f], r[f].strip()) for r in full if r["rid"] in byid]
            if f == "faithfulness_reported":
                pairs = [(a if a in ("yes", "no", "unclear") else "n/a", b if b in ("yes", "no", "unclear") else "n/a")
                         for a, b in pairs]
            po = sum(a == b for a, b in pairs) / len(pairs)
            cx, cy = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
            pe = sum(cx[k] * cy[k] for k in set(cx) | set(cy)) / len(pairs) ** 2
            res[f] = {"n": len(pairs), "agree": po, "kappa": (po - pe) / (1 - pe) if pe < 1 else 1.0,
                      "confusion": {f"{a}->{b}": c for (a, b), c in Counter(pairs).items()}}
        rel = [(byid[r["rid"]]["faithfulness_reported"], r["faithfulness_reported"].strip()) for r in full
               if r["rid"] in byid]
        res["faith_relevant_fulltext"] = sum(1 for _, b in rel if b in ("yes", "no", "unclear"))
        res["faith_yes_fulltext"] = sum(1 for _, b in rel if b == "yes")
        res["faith_yes_abstract_among_relevant"] = sum(1 for a, b in rel if b in ("yes", "no", "unclear") and a == "yes")
        res["exact_fulltext"] = sum(1 for r in full if r["check_strength"].strip() == "exact")
        res["exact_abstract"] = sum(1 for r in full if byid[r["rid"]]["check_strength"] == "exact")
        res["empirical_fulltext"] = sum(1 for r in full if r["check_strength"].strip() == "empirical")
        res["empirical_abstract"] = sum(1 for r in full if byid[r["rid"]]["check_strength"] == "empirical")
        arch_of = {r["rid"]: r["architecture"] for r in inc}
        for a in ("A1", "A2"):
            g = [(byid[r["rid"]]["check_strength"], r["check_strength"].strip()) for r in full if arch_of[r["rid"]] == a]
            res[f"check_{a}"] = {"n": len(g), "agree": sum(x == y for x, y in g),
                                 "fulltext": dict(Counter(y for _, y in g))}
        out["fulltext_check"] = res

    # ---- studies found only by the recall audit: do they resemble the found ones?
    logr = list(csv.DictReader(open(DERIVED / "screening_log.csv", encoding="utf-8")))
    aud_ids = {r["rid"] for r in logr if r["route"].startswith("audit") and r["final"] == "include"}
    af = [r for r in inc if r["rid"] in aud_ids]
    out["audit_found"] = {"n": len(af), "arch": dict(Counter(r["architecture"] for r in af)),
                          "F3": sum(1 for r in af if r["formalism"] == "F3"),
                          "A6_share_all": sum(1 for r in inc if r["architecture"] == "A6") / len(inc),
                          "F3_share_all": sum(1 for r in inc if r["formalism"] == "F3") / len(inc)}

    # ---- association: leave-one-domain-out
    pairs = [(r["domain"], r["architecture"]) for r in inc]
    lodo = {}
    for d in sorted({p[0] for p in pairs}):
        sub = [p for p in pairs if p[0] != d]
        lodo[d] = cramers(sub)[2]
    out["assoc_leave_one_domain_out"] = lodo
    meth_pairs = [(r["domain"], r["architecture"]) for r in meth]
    out["assoc_methods_only"] = cramers(meth_pairs)[2]

    # ---- "two communities"
    cl = [r for r in inc if CLASSICAL.search(r["title"] + " " + abstracts.get(r["rid"], ""))]
    out["classical_semantics"] = {"n": len(cl), "rids": [r["rid"] for r in cl],
                                  "terms": Counter(m.group(0).lower() for r in cl for m in
                                                   CLASSICAL.finditer(r["title"] + " " + abstracts.get(r["rid"], "")))}

    # ---- M1: human-confirmed subset (author's screening sample)
    hs = DECISIONS / "human_check" / "screening_sheet.csv"
    rows = list(csv.DictReader(open(hs, encoding="utf-8"))) if hs.exists() else []
    filled = [r for r in rows if r["decision"].strip()]
    if rows and len(filled) >= 0.9 * len(rows):
        inc_ids = {r["rid"] for r in inc}
        sampled_inc = [r for r in filled if r["rid"] in inc_ids]
        confirmed = {r["rid"] for r in sampled_inc if r["decision"].strip().lower() == "include"}
        rejected = [r for r in sampled_inc if r["decision"].strip().lower() != "include"]
        lo_hi = wilson(len(confirmed), len(sampled_inc))
        sub = [r for r in inc if r["rid"] in confirmed]
        samp = [r for r in inc if r["rid"] in {x["rid"] for x in sampled_inc}]
        out["human_confirmed"] = {"sampled_included": len(sampled_inc), "confirmed": len(confirmed),
                                  "precision": lo_hi, "rejected_codes": dict(Counter(r["code"].strip()[:2]
                                                                                    for r in rejected)),
                                  "findings_confirmed": key_findings(sub), "findings_sampled": key_findings(samp),
                                  "rejected_by_arch": dict(Counter(next(x["architecture"] for x in inc
                                                                       if x["rid"] == r["rid"]) for r in rejected)),
                                  "rejected_by_form": dict(Counter(next(x["formalism"] for x in inc
                                                                       if x["rid"] == r["rid"]) for r in rejected))}
    (DERIVED / "sensitivity.json").write_text(json.dumps(out, indent=1, default=list))
    p2 = out["panels"]["P2_ICLR_ICML"]
    print("[s16] P2 A2 early/2026:", p2["2020--2022"]["all"]["A2"][0], p2["2026"]["all"]["A2"][0],
          "| RR p5 2025/2020:", {k: round(v, 2) if isinstance(v, float) else v
                                  for k, v in out["rate_ratio_p5_2025_vs_2020"].items()},
          "| without F3 n:", out["program_aided"]["without_F3"]["n"],
          "| human:", "yes" if "human_confirmed" in out else "pending")


if __name__ == "__main__":
    main()
