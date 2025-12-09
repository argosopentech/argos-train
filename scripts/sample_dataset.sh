#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <data-directory>"
    echo "Example: $0 data-nllb-en_de"
    exit 1
fi

DATA_DIR="$1"
SRC="$DATA_DIR/source"
TGT="$DATA_DIR/target"

if [[ ! -f "$SRC" || ! -f "$TGT" ]]; then
    echo "Error: Expected files '$SRC' and '$TGT' not found."
    exit 1
fi

# Save random line numbers
shuf -i 1-"$(wc -l < "$SRC")" -n 10 > lines.txt

# Print source + target together
while read -r i; do
    src=$(sed -n "${i}p" "$SRC")
    tgt=$(sed -n "${i}p" "$TGT")
    echo "[$i] SRC: $src"
    echo "     TGT: $tgt"
    echo
done < lines.txt

rm lines.txt
