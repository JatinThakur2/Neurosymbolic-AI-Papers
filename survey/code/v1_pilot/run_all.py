"""Run the whole review pipeline end to end.

    python code/run_all.py --repo /path/to/Neurosymbolic-AI-Papers

Requires Python 3.9+ and poppler-utils (pdftotext). No third-party packages.
"""
import argparse
import csv
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(script, *args):
    cmd = [sys.executable, str(HERE / script), *args]
    print("$", " ".join(cmd[1:]))
    subprocess.run(cmd, check=True, cwd=HERE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, type=Path)
    a = ap.parse_args()
    repo = str(a.repo.resolve())
    run("s01_parse_corpus.py", "--repo", repo)
    run("s02_extract_text.py", "--repo", repo)
    run("s03_screen.py")
    with (HERE.parent / "data/derived/screening_log.csv").open(encoding="utf-8") as f:
        ids = ",".join(r["record_id"] for r in csv.DictReader(f) if r["stage"] == "included")
    run("s02_extract_text.py", "--repo", repo, "--fulltext-ids", ids)
    run("s04_coding.py")
    run("s05_fulltext_indicators.py")
    run("identification/replay_on_corpus.py")
    run("s06_make_bib.py")
    run("s07_build_latex.py")


if __name__ == "__main__":
    main()
