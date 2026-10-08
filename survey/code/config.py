"""Shared configuration for the review pipeline.

Every pattern used to screen or code records lives here, so that the paper's
appendix and the code cannot drift apart.
"""
from pathlib import Path
import re

PROJECT = Path(__file__).resolve().parent.parent
DATA = PROJECT / "data"
MANUAL = DATA / "manual"      # human decisions (versioned, never overwritten)
DERIVED = DATA / "derived"    # everything the scripts regenerate
TABLES = PROJECT / "tables"   # LaTeX fragments \input by the paper
WORK = PROJECT / "work"       # extracted PDF text (large, not shipped)

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
