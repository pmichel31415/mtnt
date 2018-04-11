from __future__ import print_function, division
import sys
import numpy as np

from src.util import loadtxt, savetxt

# Command line args
in_file = sys.argv[1]
out_file = sys.argv[2]
low_percentile = float(sys.argv[3])
high_percentile = float(sys.argv[4])

# Load records
records = loadtxt(in_file)

# Retrieve scores (2nd column in tsv)
scores = np.zeros(len(records))
for idx, line in enumerate(records):
    scores[idx] = float(line.split('\t')[1])

# Compute score thresholds
floor_score = np.percentile(scores, low_percentile)
ceil_score = np.percentile(scores, high_percentile)

# Filter out outlier scores
filtered_records = []
for line, score in zip(records, scores):
    if score >= floor_score and score <= ceil_score:
        filtered_records.append(line)

# Save to file
savetxt(out_file, filtered_records)
