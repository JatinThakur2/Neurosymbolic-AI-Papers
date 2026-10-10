"""Run the complete v2 review pipeline end to end.

    bash code/search/fetch_sources.sh sources        # once: corpus + proceedings metadata
    python code/run_all.py --sources sources

Requires Python 3.9+ and poppler-utils (pdftotext). No third-party packages.
Decisions are read from data/decisions/ (never written); everything under
data/derived/, tables/ and work/ is regenerated.
"""
import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def run(script, *args):
    cmd = [sys.executable, str(HERE / script), *map(str, args)]
    print("$", " ".join(cmd[1:]), flush=True)
    subprocess.run(cmd, check=True, cwd=HERE / Path(script).parent)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", required=True, type=Path,
                    help="folder with corpus/, paperlists/ and acl-anthology/ (see fetch_sources.sh)")
    a = ap.parse_args()
    src = a.sources.resolve()
    corpus = src / "corpus"
    work = ROOT / "work" / "search"
    work.mkdir(parents=True, exist_ok=True)
    # Source A: curated corpus
    run("s01_parse_corpus.py", "--repo", corpus)
    run("s02_extract_text.py", "--repo", corpus)
    # Source B: proceedings metadata, abstract-level query, merge with Source A
    run("search/build_source_b.py", "--paperlists", src / "paperlists", "--anthology", src / "acl-anthology",
        "--out", work / "source_b.jsonl")
    run("search/query.py", "--records", work / "source_b.jsonl", "--out", work / "hits_b.jsonl")
    run("search/merge_sources.py")
    # screening of the union, then snowballing from included studies and the recall audit
    run("s10_screen_union.py")
    run("search/snowball.py", "--repo", corpus)
    run("search/audit_sample.py")
    run("s11_selection.py")
    # charting, analyses, bibliography, LaTeX
    run("s12_coding.py")
    run("s13_analysis.py")
    run("s14_bib.py")
    run("s15_latex.py")
    run("human_check.py", "--score")


if __name__ == "__main__":
    main()
