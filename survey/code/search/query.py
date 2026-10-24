"""Frozen abstract-level search query (Source B) and its application.

A record is retrieved when its title + abstract match LM_BLOCK AND SYMBOLIC_BLOCK
(case-insensitive Python regular expressions).

Usage: python query.py --records source_b.jsonl --out hits.jsonl
"""
import argparse
import json
import re

LM_BLOCK = (
    r"large language model|\bLLMs?\b|\blanguage models?\b|\bLMs?\b|\bGPT-?\d|ChatGPT|\bCodex\b|"
    r"vision[- ]language model|\bVLMs?\b|\bMLLMs?\b|multimodal large|foundation models?|\bPaLM\b|LLaMA|"
    r"pre-?trained (language|transformer|sequence)|\bT5\b|\bBERT\b|chain[- ]of[- ]thought|in-context learning|"
    r"prompting|neural sequence models?|sequence[- ]to[- ]sequence|seq2seq|transformer-based|\btransformers?\b|"
    r"code models?"
)
SYMBOLIC_BLOCK = (
    r"neuro-?symbolic|neural[- ]symbolic|\bsymbolic\b|theorem prov|\bprovers?\b|proof assistant|\bLean ?4?\b|"
    r"\bIsabelle\b|\bCoq\b|formali[sz]|formal (proof|verification|logic|language|specification|mathematics|reasoning)|"
    r"\bSMT\b|\bZ3\b|\bSAT solver|\bsolvers?\b|satisfiability|constraint satisfaction|answer[- ]set program|\bASP\b|"
    r"\bProlog\b|logic program|first[- ]order logic|\bFOL\b|description logic|logical (query|queries|rules?|constraints?)|"
    r"logic rules?|rule induction|inductive logic|abductive|logic(al)? (grid )?puzzles?|\bPDDL\b|classical planner|"
    r"temporal logic|\bLTL\b|program synthesis|program induction|programs? of thought|program[- ]aided|"
    r"\bPython programs?\b|executable (program|code)|interpreter|\bverifier\b|probabilistic logic|knowledge compilation|"
    r"domain[- ]specific language|\bDSL\b|logical form|semantic pars|declarative|computer algebra|SymPy|"
    r"equation discovery"
)
# Revision 2 (second referee report, M5): terms added to both blocks. The v2 blocks above are kept
# unchanged; the review's search is the union of the v2 query and this augmented query.
LM_BLOCK_ADD = r"\bQwen|\bMistral\b|\bGemini\b|\bDeepSeek|\bClaude\b|\bGPT\b|reasoning models?|language agents?"
SYMBOLIC_BLOCK_ADD = (
    r"model[- ]check(ing|ers?)|\bNuSMV\b|\bDafny\b|\bVerus\b|\bDatalog\b|\bplanners?\b|"
    r"planning (domains?|languages?|problems?|tasks?)|automated planning|\bMILP\b|mixed[- ]integer|"
    r"(integer|linear) programm?ing|optimi[sz]ation (modell?ing|models?|problems?|formulations?)|\bPyomo\b|\bGurobi\b|"
    r"\bproofs?\b|\bSQL\b|execution traces?|\bTLA\+|\bAlloy\b"
)
LM_RE_V2 = re.compile(LM_BLOCK, re.I)
SYM_RE_V2 = re.compile(SYMBOLIC_BLOCK, re.I)
LM_RE = re.compile(LM_BLOCK + "|" + LM_BLOCK_ADD, re.I)
SYM_RE = re.compile(SYMBOLIC_BLOCK + "|" + SYMBOLIC_BLOCK_ADD, re.I)


def matches_v2(title, abstract):
    text = f"{title} {abstract}"
    return bool(LM_RE_V2.search(text)) and bool(SYM_RE_V2.search(text))


def matches(title, abstract):
    """Augmented query (revision 2); every v2 hit is also a hit here."""
    text = f"{title} {abstract}"
    return bool(LM_RE.search(text)) and bool(SYM_RE.search(text))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--v2", action="store_true", help="apply the frozen v2 query only")
    a = ap.parse_args()
    match = matches_v2 if a.v2 else matches
    n = k = 0
    with open(a.out, "w", encoding="utf-8") as out:
        for line in open(a.records, encoding="utf-8"):
            r = json.loads(line)
            if a.v2 and r.get("r2_added"):
                continue        # added to Source B in revision 2; screened in stage 2 (stage2.py)
            n += 1
            if match(r["title"], r["abstract"]):
                k += 1
                out.write(line)
    print(f"[query] {k} of {n} records retrieved -> {a.out}")


if __name__ == "__main__":
    main()
