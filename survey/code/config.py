"""Shared configuration for the review pipeline.

Every pattern used to screen or code records lives here, so that the paper's
appendix and the code cannot drift apart.
"""
from pathlib import Path
import re

PROJECT = Path(__file__).resolve().parent.parent
DATA = PROJECT / "data"
DECISIONS = DATA / "decisions"  # screening/coding/web-check decisions (versioned; scripts never write here)
MANUAL = DECISIONS / "v1_pilot"  # decisions of the superseded v1 pilot (code/v1_pilot)
DERIVED = DATA / "derived"    # everything the scripts regenerate
TABLES = PROJECT / "tables"   # LaTeX fragments \input by the paper
WORK = PROJECT / "work"       # large intermediate files (PDF text, source database); not shipped
SEED = 20261010               # seed for all v2 random draws not fixed elsewhere

VENUE_NAMES = {
    "AAAI": "Proc. AAAI Conference on Artificial Intelligence",
    "ICLR": "Proc. International Conference on Learning Representations (ICLR)",
    "ICML": "Proc. International Conference on Machine Learning (ICML)",
    "IJCAI": "Proc. International Joint Conference on Artificial Intelligence (IJCAI)",
    "NeurIPS": "Advances in Neural Information Processing Systems (NeurIPS)",
    "TMLR": "Transactions on Machine Learning Research",
    "TPAMI": "IEEE Transactions on Pattern Analysis and Machine Intelligence",
}
JOURNALS = {"TMLR", "TPAMI"}

# ---------------------------------------------------------------------------
# Stage 2 (screening): language-model term filter, applied to title + abstract.
# Recall-oriented on purpose: every hit goes to manual eligibility review.
# ---------------------------------------------------------------------------
LM_FILTER = re.compile(
    r"large language model|\bLLMs?\b|language models?\b|\bGPT|\bBERT\b|\bT5\b|"
    r"foundation model|vision-language|\bVLMs?\b|\bMLLMs?\b|chain-of-thought|"
    r"in-context|pre-?trained (language|transformer)|reasoning models?|\bLRMs?\b|"
    r"code model|Codex|LLaMA|Qwen",
    re.I,
)

# Records NOT flagged by LM_FILTER whose titles were nevertheless read by hand
# (titles with related terms, or records without an extracted abstract).
TITLE_REVIEW_SCOPE = re.compile(
    r"transformer|theorem|formal|lean|agent|code|prompt|pretrain|pre-train|generat|"
    r"neural network|diffusion|embodied|robot|reasoning|survey|benchmark",
    re.I,
)

# ---------------------------------------------------------------------------
# Stage 5 (full-text indicators). An entity counts for a study when it is
# named at least INDICATOR_MIN_MENTIONS times outside the reference block.
# ---------------------------------------------------------------------------
INDICATOR_MIN_MENTIONS = 3

LM_FAMILIES = {
    "GPT-4 family (incl. GPT-4o, o1/o3)": r"(?i)\bGPT-?4(o|\.1|v)?\b|\bo1-(mini|preview)\b|\bo3(-mini)?\b",
    "GPT-3.5 / ChatGPT": r"(?i)GPT-?3\.5|ChatGPT|text-davinci",
    "GPT-3 / Codex / GPT-2": r"\bGPT-?[23](?![\.\d])|Codex\b",
    "Llama family": r"(?i)\bllama[- ]?\d?|code ?llama",
    "Qwen family": r"(?i)\bqwen",
    "DeepSeek family": r"(?i)deepseek",
    "Mistral / Mixtral": r"(?i)mistral|mixtral",
    "Claude": r"\bClaude\b",
    "Gemini / PaLM": r"Gemini|PaLM\b|PaLM ?2",
    "Gemma": r"\bGemma",
    "Chinchilla / Gopher": r"Chinchilla|Gopher",
    "T5 / CodeT5": r"\b(Flan-?)?T5\b|CodeT5",
    "BERT / RoBERTa": r"\bBERT\b|RoBERTa|DeBERTa",
    "InternLM": r"InternLM",
    "LLaVA / BLIP / CLIP": r"LLaVA|BLIP-?2|InstructBLIP|\bCLIP\b",
}
SYMBOLIC_ENGINES = {
    "Lean": r"\bLean ?4?\b",
    "Isabelle": r"Isabelle",
    "Coq": r"\bCoq\b",
    "Z3 / SMT solver": r"\bZ3\b|\bSMT\b|cvc5",
    "Prover9 / FOL prover": r"Prover9|\bVampire\b",
    "ASP (clingo)": r"clingo|[Aa]nswer [Ss]et [Pp]rogram|\bASP\b",
    "Prolog": r"Prolog",
    "PDDL planner": r"PDDL|Fast Downward",
    "SymPy / CAS": r"SymPy|computer algebra",
    "Probabilistic logic (ProbLog, Scallop, MLN)": r"ProbLog|Scallop|Markov logic",
}
BENCHMARKS = {
    "miniF2F": r"miniF2F",
    "ProofNet": r"ProofNet",
    "FOLIO": r"FOLIO",
    "ProofWriter": r"ProofWriter",
    "PrOntoQA": r"(?i)prontoqa",
    "ARC (ARC-AGI or AI2-ARC)": r"\bARC\b",
    "GSM8K": r"GSM8K",
    "MATH": r"\bMATH\b",
    "CLEVR": r"CLEVR",
    "GQA": r"\bGQA\b",
    "ALFWorld": r"ALFWorld",
    "VirtualHome": r"VirtualHome",
    "SRBench / Feynman": r"SRBench|Feynman",
    "Spider / BIRD": r"\bSpider\b|\bBIRD\b",
}


def norm_title(t: str) -> str:
    """Normalised title used as the stable key for every record."""
    t = t.lower().replace("(extended abstract)", "").replace("(abstract reprint)", "")
    return re.sub(r"[^a-z0-9]", "", t)


# Classical neurosymbolic themes, used to measure their overlap with the included set (RQ4).
CLASSICAL_THEMES = {
    "abductive learning": r"abduct",
    "probabilistic logic": r"probabilistic (logic|neurosymbolic|neuro-symbolic)|deepproblog|problog|semantic loss|knowledge compilation",
    "differentiable or fuzzy logic": r"differentiable logic|logic gate|t-norm|fuzzy logic",
    "reasoning shortcuts": r"reasoning shortcut",
    "symbolic regression": r"symbolic regression",
    "inductive logic programming": r"inductive logic programming|\bILP\b",
}


# ---------------------------------------------------------------------------
# v2: normalisation of entities named in abstracts (coded by two LLM coders).
# A study "names" a family when either coder listed a matching string.
# ---------------------------------------------------------------------------
LM_FAMILY_V2 = {
    "GPT-4 family": r"gpt-?4|gpt-?4o|\bo[134](-mini|-preview)?\b|openai[- ]o[134]|gpt-?5",
    "GPT-3/3.5, ChatGPT, Codex": r"gpt-?3|chatgpt|codex|text-davinci|instructgpt|\bgpt\b$",
    "GPT-2 and earlier": r"gpt-?2|gpt-?1\b",
    "Llama family": r"llama|vicuna|alpaca",
    "DeepSeek family": r"deepseek",
    "Qwen family": r"qwen",
    "Mistral/Mixtral": r"mistral|mixtral",
    "Claude": r"claude",
    "Gemini/PaLM/Bard": r"gemini|palm|bard|minerva|flan-u-palm",
    "Gemma": r"gemma",
    "T5 family": r"\bt5\b|flan-t5|codet5|byt5",
    "BERT family": r"bert|roberta|deberta|electra",
    "Specialised provers": r"prover|kimina|goedel|internlm.*(step|math)|lean-?star|theoremllama",
    "Vision-language (LLaVA, CLIP, BLIP, ...)": r"llava|clip|blip|gpt-?4v|vision|vlm|qwen-?vl|internvl",
}
ENGINE_FAMILY_V2 = {
    "Lean": r"\blean|mathlib|leandojo",
    "Isabelle": r"isabelle|sledgehammer|\bpisa\b",
    "Coq/Rocq": r"\bcoq\b|\brocq\b",
    "Dafny/Verus/Why3/F*": r"dafny|verus|why3|\bf\*|frama|boogie",
    "Python interpreter/executor": r"python|code interpreter|interpreter|executor|pandas|sandbox",
    "SAT/SMT (Z3, cvc5)": r"\bz3\b|\bsmt\b|\bsat\b|cvc|maxsat|satisfiab",
    "Logic programming (Prolog, ASP, Datalog)": r"prolog|answer set|\basp\b|clingo|datalog|scallop|problog",
    "Planners (PDDL)": r"pddl|planner|fast downward",
    "Model checkers / temporal logic": r"nusmv|model check|\bltl\b|temporal logic|spin\b|prism",
    "Optimisation solvers (LP/MILP/CP)": r"\blp\b|milp|linear program|gurobi|cplex|pyomo|or-tools|minizinc|constraint program|optimi[sz]ation solver",
    "Computer algebra (SymPy, Mathematica)": r"sympy|mathematica|computer algebra|wolfram|\bcas\b",
    "Theorem provers (FOL)": r"prover9|vampire|\be prover|first-order prover|theorem prover",
}

def norm_benchmark(name: str) -> str:
    """Canonical benchmark key: case/punctuation-insensitive; split suffixes dropped."""
    k = name.lower()
    k = re.sub(r"\(.*?\)", "", k)
    k = re.sub(r"[-_ ]?(test|valid|validation|dev|train)(\s*set)?$", "", k.strip())
    return re.sub(r"[^a-z0-9+]", "", k)
