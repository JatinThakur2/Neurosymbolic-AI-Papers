"""REFERENCE RE-IMPLEMENTATION -- NOT THE ORIGINAL COLLECTION SCRIPT.

The Neurosymbolic-AI-Papers repository documents (README, "Methodology") how its
391 records were identified: venue title listings from dblp, filtered by a two-tier
keyword classifier (a CORE pattern for explicit neuro-symbolic terms and an
ADJACENT pattern for closely related sub-fields), followed by manual removal of
false positives. The original scripts are not part of the repository.

This file re-implements that documented procedure so that readers can repeat the
identification stage. It was written from the README description and has NOT
been run against dblp by the authors of this review (network access to dblp was
unavailable in the environment used to prepare it). Replace it with the original
scripts if they are available, and report any difference in the paper.

Usage
    python reference_dblp_classifier.py --venue conf/icml --year 2023 > hits.csv

It queries the dblp search API (https://dblp.org/faq/How+to+use+the+dblp+search+API.html),
pages through all titles of one venue-year, and prints the titles that match
CORE or ADJACENT together with the tier.
"""
import argparse
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request

CORE = re.compile(r"neuro-?symbolic|neural[- ]symbolic|neurosymbolic", re.I)

# One group of alternatives per adjacent sub-field listed in the repository README.
ADJACENT = re.compile(
    r"program (synthesis|induction|abstraction)|programmatic|programs? from|differentiable program|"
    r"symbolic (regression|policy|policies|expression|equivalence)|equation (search|discovery)|"
    r"inductive logic programming|\bILP\b|logic program(s|ming)?\b|"
    r"rules?\b.*(induction|learning|mining|discover)|(induction|learning|mining) (of )?(logical )?rules?|"
    r"constraints? (induction|mining|learning|from data)|"
    r"abduct|"
    r"differentiable (logic|reasoning)|logic gate network|logical reasoning|first-order logic|"
    r"probabilistic logic|deep probabilistic logic|"
    r"complex (logical )?query|logical quer|multi-hop logical|"
    r"temporal logic|"
    r"theorem prov|formal (proof|theorem|mathemat)|autoformal|\bLean\b|"
    r"answer[- ]set program",
    re.I,
)

API = "https://dblp.org/search/publ/api"


def dblp_titles(venue_key: str, year: int, page: int = 1000):
    """Yield (title, authors, doi/ee) for one venue-year via the dblp search API."""
    stream = venue_key.split("/")[-1]
    first = 0
    while True:
        q = f"stream:streams/{venue_key}: year:{year}:"
        url = f"{API}?{urllib.parse.urlencode({'q': q, 'h': page, 'f': first, 'format': 'json'})}"
        with urllib.request.urlopen(url, timeout=60) as resp:
            hits = json.load(resp)["result"]["hits"]
        items = hits.get("hit", [])
        for h in items:
            info = h["info"]
            authors = info.get("authors", {}).get("author", [])
            if isinstance(authors, dict):
                authors = [authors]
            yield (re.sub(r"\.$", "", info.get("title", "")),
                   "; ".join(a.get("text", "") for a in authors),
                   info.get("ee", ""))
        first += len(items)
        if not items or first >= int(hits.get("@total", 0)):
            break
        time.sleep(1.0)  # be polite to dblp


def classify(title: str) -> str:
    if CORE.search(title):
        return "core"
    if ADJACENT.search(title):
        return "adjacent"
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--venue", required=True, help="dblp stream key, e.g. conf/icml, conf/nips, journals/tmlr")
    ap.add_argument("--year", required=True, type=int)
    a = ap.parse_args()
    w = csv.writer(sys.stdout)
    w.writerow(["tier", "title", "authors", "link"])
    for title, authors, ee in dblp_titles(a.venue, a.year):
        tier = classify(title)
        if tier:
            w.writerow([tier, title, authors, ee])
    # Every hit must then be checked by hand against its abstract (README: manual
    # removal of false positives such as generic temporal point processes).


if __name__ == "__main__":
    main()
