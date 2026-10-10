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
LM_RE = re.compile(LM_BLOCK, re.I)
SYM_RE = re.compile(SYMBOLIC_BLOCK, re.I)


def matches(title, abstract):
    text = f"{title} {abstract}"
    return bool(LM_RE.search(text)) and bool(SYM_RE.search(text))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    n = k = 0
    with open(a.out, "w", encoding="utf-8") as out:
        for line in open(a.records, encoding="utf-8"):
            r = json.loads(line)
            n += 1
            if matches(r["title"], r["abstract"]):
                k += 1
                out.write(line)
    print(f"[query] {k} of {n} records retrieved -> {a.out}")


if __name__ == "__main__":
    main()
