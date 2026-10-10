"""Stage 6: BibTeX for the included studies and for corpus records cited as related work.

Metadata come from the repository README (title, authors, venue, year, DOI/URL).
The README lists ICML authors by surname only, so ICML_FULL_NAMES restores the full
names, transcribed from each PDF's first page.

IMPORTANT: page numbers, volumes and editors are not in the source data. Check every
entry against dblp before camera-ready.

Outputs: references_studies.bib (project root), data/derived/bibkeys.csv
"""
import csv
import re
import unicodedata

from config import DERIVED, JOURNALS, PROJECT, VENUE_NAMES, norm_title

# Corpus records cited as related work (matched by normalised title).
RELATED_TITLES = [
    "Scallop: From Probabilistic Deductive Databases to Scalable Differentiable Reasoning",
    "NeurASP: Embracing Neural Networks into Answer Set Programming",
    "Not All Neuro-Symbolic Concepts Are Created Equal: Analysis and Mitigation of Reasoning Shortcuts",
    "Analysis for Abductive Learning and Neural-Symbolic Reasoning Shortcuts",
    "Graph Neural Networks Meet Neural-Symbolic Computing: A Survey and Perspective",
    "Neuro-Symbolic Artificial Intelligence: A Task-Directed Survey in the Black-Box Models Era",
    "Towards Data-And Knowledge-Driven AI: A Survey on Neuro-Symbolic Computing",
    "Empowering LLMs with Logical Reasoning: A Comprehensive Survey",
    "Neuro-Symbolic Artificial Intelligence: Towards Improving the Reasoning Abilities of Large Language Models",
    "From Statistical Relational to Neuro-Symbolic Artificial Intelligence",
    "On the Hardness of Probabilistic Neurosymbolic Learning",
    "A-NeSI: A Scalable Approximate Method for Probabilistic Neurosymbolic Inference",
]

ICML_FULL_NAMES = {
    "Neuro-Symbolic Language Modeling with Automaton-augmented Retrieval":
        "Uri Alon; Frank F. Xu; Junxian He; Sudipta Sengupta; Dan Roth; Graham Neubig",
    "End-to-End Neuro-Symbolic Reinforcement Learning with Textual Explanations":
        "Lirui Luo; Guoxi Zhang; Hongming Xu; Yaodong Yang; Cong Fang; Qing Li",
    "StackSight: Unveiling WebAssembly through Large Language Models and Neurosymbolic Chain-of-Thought Decompilation":
        "Weike Fang; Zhejian Zhou; Junzhou He; Weihang Wang",
    "Subgoal-based Demonstration Learning for Formal Theorem Proving":
        "Xueliang Zhao; Wenda Li; Lingpeng Kong",
    "Dataflow-Guided Neuro-Symbolic Language Models for Type Inference":
        "Gen Li; Yao Wan; Hongyu Zhang; Zhou Zhao; Wenbin Jiang; Xuanhua Shi; Hai Jin; Zheng Wang",
    "MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving":
        "Ruida Wang; Rui Pan; Yuxin Li; Jipeng Zhang; Yizhen Jia; Shizhe Diao; Renjie Pi; Junjie Hu; Tong Zhang",
    "ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis":
        "Haoxiong Liu; Jiacheng Sun; Zhenguo Li; Andrew C. Yao",
    "Self-Improving Language Models for Evolutionary Program Synthesis: A Case Study on ARC-AGI":
        "Julien Pourcel; Cédric Colas; Pierre-Yves Oudeyer",
    "STP: Self-play LLM Theorem Provers with Iterative Conjecturing and Proving":
        "Kefan Dong; Tengyu Ma",
    "ZebraLogic: On the Scaling Limits of LLMs for Logical Reasoning":
        "Bill Yuchen Lin; Ronan Le Bras; Kyle Richardson; Ashish Sabharwal; Radha Poovendran; Peter Clark; Yejin Choi",
    "Automated Formal Proofs of Combinatorial Identities via Wilf-Zeilberger Guidance and LLMs":
        "Beibei Xiong; Hangyu Lv; Junqi Liu; Yisen Wang; Shaoshi Chen; Jianlin Wang; Zhengfeng Yang; Lihong Zhi",
    "A Minimal Agent for Automated Theorem Proving":
        "Borja Requena; Austin Letson; Krystian Nowakowski; Izan Beltran-Ferreiro; Leopoldo Sarra",
    "Decompose, Structure, and Repair: A Neuro-Symbolic Framework for Autoformalization via Operator Trees":
        "Xiaoyang Liu; Zineng Dong; Yifan Bai; Yantao Li; Yuntian Liu; Tao Luo",
    "Deliberate Evolution: Agentic Reasoning for Sample-Efficient Symbolic Regression with LLMs":
        "Xinyu Pang; Zhanke Zhou; Xuan Li; Fangrui Lv; Shanshan Wei; Sen Cui; Bo Han; Changshui Zhang",
    "Distilling Neuro-Symbolic Programs into 3D Multi-modal LLMs":
        "Wentao Mo; Yang Liu",
    "Faults in Our Formal Benchmarking: Dataset Defects and Evaluation Failures in Lean Theorem Proving":
        "Pawan Sasanka Ammanamanchi; Siddharth Bhat; Stella Biderman",
    "From LLM-Generated Conjectures to Lean Formalizations: Automated Polynomial Inequality Proving via Sum-of-Squares Certificates":
        "Ruobing Zuo; Hanrui Zhao; Gaolei He; Zhengfeng Yang; Jianlin Wang",
    "Influence-Guided Symbolic Regression: Scientific Discovery via LLM-Driven Equation Search with Granular Feedback":
        "Evgeny S. Saveliev; Samuel Holt; Nabeel Seedat; David L. Bentley; Jim Weatherall; Mihaela van der Schaar",
    "Lifting Traces to Logic: Programmatic Skill Induction with Neuro-Symbolic Learning for Long-Horizon Agentic Tasks":
        "Jie-Jing Shao; Haiyan Yin; Yueming Lyu; Xingrui Yu; Lan-Zhe Guo; Ivor W. Tsang; James T. Kwok; Yu-Feng Li",
    "Analysis for Abductive Learning and Neural-Symbolic Reasoning Shortcuts":
        "Xiao-Wen Yang; Wen-Da Wei; Jie-Jing Shao; Yu-Feng Li; Zhi-Hua Zhou",
    "On the Hardness of Probabilistic Neurosymbolic Learning":
        "Jaron Maene; Vincent Derkinderen; Luc De Raedt",
}

# 2026 records whose proceedings were not yet published: cite the arXiv preprint.
ARXIV_2026 = {
    "Automated Formal Proofs of Combinatorial Identities via Wilf-Zeilberger Guidance and LLMs": "2605.04472",
    "A Minimal Agent for Automated Theorem Proving": "2602.24273",
    "Decompose, Structure, and Repair: A Neuro-Symbolic Framework for Autoformalization via Operator Trees": "2604.19000",
    "Deliberate Evolution: Agentic Reasoning for Sample-Efficient Symbolic Regression with LLMs": "2606.04360",
    "Distilling Neuro-Symbolic Programs into 3D Multi-modal LLMs": "2606.01215",
    "Faults in Our Formal Benchmarking: Dataset Defects and Evaluation Failures in Lean Theorem Proving": "2606.29493",
    "From LLM-Generated Conjectures to Lean Formalizations: Automated Polynomial Inequality Proving via Sum-of-Squares Certificates": "2605.15445",
    "Influence-Guided Symbolic Regression: Scientific Discovery via LLM-Driven Equation Search with Granular Feedback": "2605.29184",
    "Lifting Traces to Logic: Programmatic Skill Induction with Neuro-Symbolic Learning for Long-Horizon Agentic Tasks": "2605.01293",
}

# Capitalised multi-word surnames that BibTeX would otherwise split as first names.
SURNAME_FIX = {"Luc De Raedt": "De Raedt, Luc", "Ronan Le Bras": "Le Bras, Ronan"}

STOP = {"a", "an", "the", "on", "of", "for", "and", "via", "with", "to", "in", "is", "are", "towards", "from"}
LATEX_ESC = {"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_", "$": r"\$"}


def ascii_slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z]", "", s.lower())


def esc(s):
    return "".join(LATEX_ESC.get(c, c) for c in s)


def authors_bib(venue, title, raw):
    full = {norm_title(k): v for k, v in ICML_FULL_NAMES.items()}.get(norm_title(title))
    names = full or raw
    sep = ";" if ";" in names else ","
    return " and ".join(esc(SURNAME_FIX.get(n.strip(), n.strip())) for n in names.split(sep) if n.strip())


def make_key(authors, year, title, used):
    first = authors.split(" and ")[0].strip()
    if "," in first:
        surname = first.split(",")[0].replace(" ", "")
    else:
        surname = first.split()[-1] if " " in first else first
    word = next((w for w in re.findall(r"[A-Za-z][A-Za-z0-9]*", title) if w.lower() not in STOP), "x")
    key = f"{ascii_slug(surname)}{year}{ascii_slug(word)}"
    base, n = key, 1
    while key in used:
        n += 1
        key = f"{base}{chr(96 + n)}"
    used.add(key)
    return key


def entry(r, key, authors):
    v, y, t = r["venue"], r["year"], r["title"]
    fields = [f"  author = {{{authors}}}", f"  title = {{{{{esc(t)}}}}}", f"  year = {{{y}}}"]
    arx = {norm_title(k): a for k, a in ARXIV_2026.items()}.get(norm_title(t))
    if v in JOURNALS:
        kind = "article"
        fields.append(f"  journal = {{{VENUE_NAMES[v]}}}")
    else:
        kind = "inproceedings"
        fields.append(f"  booktitle = {{{VENUE_NAMES[v]}}}")
    if r.get("doi"):
        fields.append(f"  doi = {{{r['doi']}}}")
    if arx:
        fields.append(f"  note = {{To appear; arXiv:{arx}}}")
    elif r.get("url") and "openreview" in r["url"]:
        fields.append(f"  url = {{{r['url']}}}")
    return f"@{kind}{{{key},\n" + ",\n".join(fields) + "\n}\n"


def main():
    with (DERIVED / "corpus_records.csv").open(encoding="utf-8") as f:
        recs = list(csv.DictReader(f))
    with (DERIVED / "included_studies.csv").open(encoding="utf-8") as f:
        inc_ids = {r["record_id"] for r in csv.DictReader(f)}
    related = {norm_title(t) for t in RELATED_TITLES}
    used, out, keys = set(), [], []
    seen_titles = set()
    # earliest year first, so a related-work title resolves to its original publication
    for r in sorted(recs, key=lambda x: (x["year"], int(x["record_id"]))):
        nt = norm_title(r["title"])
        role = "included" if r["record_id"] in inc_ids else ("related" if nt in related else None)
        if role is None or nt in seen_titles:
            continue
        seen_titles.add(nt)
        authors = authors_bib(r["venue"], r["title"], r["authors"])
        key = make_key(authors, r["year"], r["title"], used)
        out.append(entry(r, key, authors))
        keys.append({"record_id": r["record_id"], "title": r["title"], "role": role, "bibkey": key})
    missing = related - {norm_title(k["title"]) for k in keys}
    if missing:
        raise SystemExit(f"[s06] related-work titles not found in corpus: {missing}")
    header = ("% Auto-generated by code/s06_make_bib.py from the repository README.\n"
              "% Verify pages/volumes against dblp before camera-ready.\n\n")
    (PROJECT / "references_studies.bib").write_text(header + "\n".join(out), encoding="utf-8")
    with (DERIVED / "bibkeys.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["record_id", "title", "role", "bibkey"])
        w.writeheader()
        w.writerows(keys)
    print(f"[s06] {len(keys)} BibTeX entries ({sum(k['role'] == 'included' for k in keys)} included studies)")


if __name__ == "__main__":
    main()
