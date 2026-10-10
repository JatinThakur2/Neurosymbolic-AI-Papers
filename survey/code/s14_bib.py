"""Stage 6 (v2): BibTeX for the included studies and for corpus records cited as related work.

Metadata come from the proceedings sources (Paper Copilot lists, ACL Anthology, AAAI
OJS records) or, for venue-years covered only by the curated corpus, from the corpus.
DOIs and page ranges are copied from the proceedings BibTeX when it provides them.

Outputs: references_studies.bib, data/derived/bibkeys.csv (rid, bibkey, role)
"""
import csv
import json
import re
import unicodedata

from config import DERIVED, PROJECT, WORK, norm_title

VENUE = {
    "AAAI": ("inproceedings", "Proc. AAAI Conference on Artificial Intelligence"),
    "ICLR": ("inproceedings", "Proc. International Conference on Learning Representations (ICLR)"),
    "ICML": ("inproceedings", "Proc. International Conference on Machine Learning (ICML)"),
    "IJCAI": ("inproceedings", "Proc. International Joint Conference on Artificial Intelligence (IJCAI)"),
    "NeurIPS": ("inproceedings", "Advances in Neural Information Processing Systems (NeurIPS)"),
    "ACL": ("inproceedings", "Proc. Annual Meeting of the Association for Computational Linguistics (ACL)"),
    "EMNLP": ("inproceedings", "Proc. Conference on Empirical Methods in Natural Language Processing (EMNLP)"),
    "NAACL": ("inproceedings", "Proc. Conference of the North American Chapter of the Association for "
                               "Computational Linguistics (NAACL)"),
    "TMLR": ("article", "Transactions on Machine Learning Research"),
    "TPAMI": ("article", "IEEE Transactions on Pattern Analysis and Machine Intelligence"),
}
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
PARTICLES = {"de", "van", "von", "der", "den", "le", "la", "da", "di", "du", "del", "dos", "d'", "ter", "ten"}
STOP = {"a", "an", "the", "on", "of", "for", "and", "via", "with", "to", "in", "is", "are", "towards", "from", "can",
        "do", "how", "what", "when", "why", "we", "by", "at", "beyond", "into", "not", "all", "llm", "llms"}
UNI = {"\u2019": "'", "\u2018": "'", "\u201c": "``", "\u201d": "''", "\u2013": "--", "\u2014": "---",
       "\u2212": "-", "\u00d7": r"$\times$", "\u2192": r"$\rightarrow$", "\u2264": r"$\leq$", "\u2265": r"$\geq$",
       "\u03b1": r"$\alpha$", "\u03b2": r"$\beta$", "\u03bb": r"$\lambda$", "\u03c0": r"$\pi$", "\u00b2": r"$^2$",
       "\u2026": r"\ldots{}", "\u00a0": " ", "\u2009": " ", "\u221e": r"$\infty$"}
LATIN1_OK = set("áàâäãåçéèêëíìîïñóòôöõøúùûüýÿÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕØÚÙÛÜÝßæÆœŒłŁšŠžŽčČćĆřŘğĞşŞıőŐűŰ")


ACCENT = {"'": "\u0301", "`": "\u0300", "^": "\u0302", '"': "\u0308", "~": "\u0303", "c": "\u0327",
          "v": "\u030c", "u": "\u0306", "=": "\u0304", ".": "\u0307", "H": "\u030b"}


def latex_accents(s):
    """{\\'e}, \\'{e}, \\'e -> e-acute (only for names taken from BibTeX)."""
    def sub(m):
        return unicodedata.normalize("NFC", m.group(2) + ACCENT[m.group(1)])
    s = re.sub(r"\{\\([\'`^\"~cvu=.H])\s*\{?([A-Za-z])\}?\}", sub, s)
    s = re.sub(r"\\([\'`^\"~cvu=.H])\s*\{?([A-Za-z])\}?", sub, s)
    return s.replace("{\\i}", "i").replace("\\i ", "i")


def clean_text(s):
    s = latex_accents(s or "")
    s = re.sub(r"\\texttt\{([^}]*)\}|\\textsc\{([^}]*)\}|\\textbf\{([^}]*)\}|\\emph\{([^}]*)\}",
               lambda m: next(g for g in m.groups() if g is not None), s)
    s = s.replace("{", "").replace("}", "").replace("\\", "").replace("$", "")
    out = []
    for ch in s:
        if ch in UNI:
            out.append(UNI[ch])
        elif ord(ch) < 128 or ch in LATIN1_OK:
            out.append({"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_"}.get(ch, ch))
        else:
            out.append(unicodedata.normalize("NFKD", ch).encode("ascii", "ignore").decode())
    return re.sub(r"\s+", " ", "".join(out)).strip()


SPECIAL = {"ł": r"{\l}", "Ł": r"{\L}", "ø": r"{\o}", "Ø": r"{\O}", "ß": r"{\ss}", "æ": r"{\ae}",
           "Æ": r"{\AE}", "œ": r"{\oe}", "Œ": r"{\OE}", "ı": r"{\i}"}
COMBINING = {"\u0301": "'", "\u0300": "`", "\u0302": "^", "\u0308": '"', "\u0303": "~", "\u0327": "c",
             "\u030c": "v", "\u0306": "u", "\u0304": "=", "\u0307": ".", "\u030b": "H", "\u030a": "r",
             "\u0328": "k"}


def to_bibtex_ascii(s):
    """Write non-ASCII letters as BibTeX special characters, e.g. e-acute -> {\\'e}.

    BibTeX styles abbreviate first names byte by byte, which breaks multi-byte UTF-8 letters."""
    out = []
    for ch in s:
        if ord(ch) < 128:
            out.append(ch)
        elif ch in SPECIAL:
            out.append(SPECIAL[ch])
        else:
            d = unicodedata.normalize("NFD", ch)
            if len(d) == 2 and d[0].isascii() and d[1] in COMBINING:
                acc, base = COMBINING[d[1]], d[0]
                sep = " " if acc.isalpha() else ""
                out.append("{\\" + acc + sep + base + "}")
            else:
                out.append(unicodedata.normalize("NFKD", ch).encode("ascii", "ignore").decode())
    return "".join(out)


def bib_field(bib, name):
    m = re.search(name + r"\s*=\s*[{\"](.+?)[}\"]\s*,?\s*\n", bib or "", re.I | re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def author_list(rec):
    raw = rec.get("authors", "").strip()
    if raw:
        names = [n.strip() for n in re.split(r";", raw) if n.strip()]
    else:
        names = [n.strip() for n in re.split(r"\s+and\s+", bib_field(rec.get("bibtex", ""), "author")) if n.strip()]
    out = []
    for n in names:
        n = clean_text(n)
        if "," in n:
            out.append(n)
            continue
        t = n.split()
        if len(t) < 2:
            out.append(n)
            continue
        i = len(t) - 1
        while i > 1 and t[i - 1].lower() in PARTICLES:
            i -= 1
        out.append(f"{' '.join(t[i:])}, {' '.join(t[:i])}")
    return out


def make_key(authors, year, title, used):
    sur = authors[0].split(",")[0] if authors else "anon"
    sur = re.sub(r"[^a-z]", "", unicodedata.normalize("NFKD", sur).encode("ascii", "ignore").decode().lower())
    word = next((w for w in re.findall(r"[A-Za-z][A-Za-z0-9]*", title) if w.lower() not in STOP), "x").lower()
    key = f"{sur or 'anon'}{year}{word}"
    base, n = key, 1
    while key in used:
        n += 1
        key = f"{base}{chr(96 + n)}"
    used.add(key)
    return key


def entry(rec, key, authors):
    kind, venue = VENUE[rec["venue"]]
    fields = [f"  author = {{{to_bibtex_ascii(' and '.join(authors)) or 'Anonymous'}}}",
              f"  title = {{{{{to_bibtex_ascii(clean_text(rec['title']))}}}}}",
              f"  {'journal' if kind == 'article' else 'booktitle'} = {{{venue}}}",
              f"  year = {{{rec['year']}}}"]
    bib = rec.get("bibtex", "")
    doi = bib_field(bib, "doi") or rec.get("doi", "")
    pages = bib_field(bib, "pages")
    if pages and re.fullmatch(r"[\d\s\-–]+", pages):
        fields.append(f"  pages = {{{pages.replace('–', '--')}}}")
    if doi:
        fields.append(f"  doi = {{{doi}}}")
    elif rec["venue"] == "TMLR" and rec.get("url"):
        fields.append(f"  url = {{{rec['url']}}}")
    return f"@{kind}{{{key},\n" + ",\n".join(fields) + "\n}\n"


def main():
    inc = {json.loads(l)["rid"]: json.loads(l) for l in open(WORK / "included_abstracts.jsonl", encoding="utf-8")}
    union = [json.loads(l) for l in open(WORK / "search" / "records_union.jsonl", encoding="utf-8")]
    corpus = {r["record_id"]: r for r in csv.DictReader(open(DERIVED / "corpus_records.csv", encoding="utf-8"))}
    related = {norm_title(t) for t in RELATED_TITLES}
    # related work: the earliest publication of each title (corpus records include reprints that
    # the union drops as duplicates); union records preferred at equal venue-year (fuller metadata)
    cands = [dict(r, _pref=0) for r in union] + [
        {"rid": f"corpus{c['record_id']}", "title": c["title"], "venue": c["venue"], "year": c["year"],
         "authors": c["authors"], "doi": c.get("doi", ""), "bibtex": "", "url": c.get("url", ""), "_pref": 1}
        for c in corpus.values()]
    rel = {}
    for r in sorted(cands, key=lambda r: (r["year"], r["_pref"])):
        k = norm_title(r["title"])
        if k in related and k not in rel and r["rid"] not in inc:
            rel[k] = r
    if related - set(rel):
        raise SystemExit(f"[s14] related titles not found: {related - set(rel)}")
    used, out, keys = set(), [], []
    todo = [(r, "included") for r in inc.values()] + [(r, "related") for r in rel.values()]
    for rec, role in sorted(todo, key=lambda x: (x[0]["year"], x[0]["title"])):
        authors = author_list(rec)
        key = make_key(authors, rec["year"], rec["title"], used)
        out.append(entry(rec, key, authors))
        keys.append({"rid": rec["rid"], "bibkey": key, "role": role, "title": rec["title"],
                     "venue": rec["venue"], "year": rec["year"]})
    header = ("% Generated by code/s14_bib.py from the proceedings metadata (Paper Copilot lists,\n"
              "% ACL Anthology, AAAI OJS) and, for corpus-only venue-years, the curated corpus.\n\n")
    (PROJECT / "references_studies.bib").write_text(header + "\n".join(out), encoding="utf-8")
    with (DERIVED / "bibkeys.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["rid", "bibkey", "role", "title", "venue", "year"])
        w.writeheader()
        w.writerows(keys)
    print(f"[s14] {len(keys)} BibTeX entries ({sum(k['role'] == 'included' for k in keys)} included studies)")


if __name__ == "__main__":
    main()
