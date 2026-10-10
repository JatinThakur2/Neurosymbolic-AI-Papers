#!/usr/bin/env bash
# Fetch the two machine-readable proceedings sources used to build Source B, at the
# exact commits used in the review. Usage: bash code/search/fetch_sources.sh <dest-dir>
set -euo pipefail
DEST=${1:-sources}
mkdir -p "$DEST"

# Paper Copilot paper lists (accepted papers with abstracts).
PAPERLISTS_COMMIT=9fcfd1234879a8e5630b5116dde411ec143dd763
git clone --filter=blob:none --no-checkout https://github.com/papercopilot/paperlists "$DEST/paperlists"
git -C "$DEST/paperlists" sparse-checkout set --no-cone /aaai /acl /emnlp /iclr /icml /ijcai /naacl /nips
git -C "$DEST/paperlists" checkout "$PAPERLISTS_COMMIT"
# At that commit ICLR 2025/2026 are Git-LFS pointers; use their last plain-blob versions.
git -C "$DEST/paperlists" show d4c51fa:iclr/iclr2025.json > "$DEST/paperlists/iclr/iclr2025.json"
git -C "$DEST/paperlists" show 33f9884:iclr/iclr2026.json > "$DEST/paperlists/iclr/iclr2026.json"

# ACL Anthology metadata (ACL 2020, EMNLP 2020 and EMNLP 2025 main volumes).
ANTHOLOGY_COMMIT=73f3b3aa2f20b6dd71b75a8190c596258243bf5c
git clone --filter=blob:none --no-checkout https://github.com/acl-org/acl-anthology "$DEST/acl-anthology"
git -C "$DEST/acl-anthology" sparse-checkout set --no-cone /data/xml/2020.acl.xml /data/xml/2020.emnlp.xml /data/xml/2025.emnlp.xml
git -C "$DEST/acl-anthology" checkout "$ANTHOLOGY_COMMIT"

# Curated corpus (Source A).
CORPUS_COMMIT=9a42645fabe56053214584de5e970ff638762aef
git clone https://github.com/JatinThakur2/Neurosymbolic-AI-Papers "$DEST/corpus"
git -C "$DEST/corpus" checkout "$CORPUS_COMMIT"
echo "sources ready in $DEST"
