#!/bin/bash
# English
sort -u -k1 output/test-en-1000.txt > output/uniq-en-1000.txt
python scripts/remove-tabs.py output/uniq-en-1000.txt output/uniq-en-1000.txt 9
python scripts/remove-outliers.py output/uniq-en-1000.txt output/uniq-en-1000-no-outliers.txt 5 70
cat output/uniq-en-1000-no-outliers.txt | shuf | head -n15000 | cat output/headers.txt - > output/en-1k.15000.txt
# French
sort -u -k1 output/test-fr-1000.txt > output/uniq-fr-1000.txt
python scripts/remove-tabs.py output/uniq-fr-1000.txt output/uniq-fr-1000.txt 9
python scripts/remove-outliers.py output/uniq-fr-1000.txt output/uniq-fr-1000-no-outliers.txt 5 50
cat output/uniq-fr-1000-no-outliers.txt | shuf | head -n15000 | cat output/headers.txt - > output/fr-1k.15000.txt
# Japanese
sort -u -k1 output/test-ja-4000.txt > output/uniq-ja-4000.txt
python scripts/remove-tabs.py output/uniq-ja-4000.txt output/uniq-ja-4000.txt 9
python scripts/remove-outliers.py output/uniq-ja-4000.txt output/uniq-ja-4000-no-outliers.txt 10 70
cat output/uniq-ja-4000-no-outliers.txt | shuf | head -n15000 | cat output/headers.txt - > output/ja-4k.15000.txt

# Zip everything
zip data.15k.zip output/fr-1k.15000.txt output/en-1k.15000.txt output/ja-4k.15000.txt
