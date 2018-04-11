from __future__ import print_function, division
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pickle
from collections import defaultdict
from nltk.tokenize.moses import MosesTokenizer

import src.text as text

input_file = sys.argv[1]
dic_file = sys.argv[2]
oov_freqs_output_file = sys.argv[3]

# Load dictionary
with open(dic_file, 'rb') as f:
    dic = pickle.load(f)

# Initialize Moses tokenizer
tokenizer = MosesTokenizer()

# Count OOVs
counts = defaultdict(lambda:0)
with open(input_file, 'r') as f:
    for l in f:
        # Get first field
        comment = l.split('\t')[0]
        # Remove urls
        comment = ' '.join(filter(lambda w: not text.contains_url(w), comment.split()))
        # Normalize punctuation
        comment = text.normalize_punctuation(comment)
        # Tokenize with the moses tokenizer
        sentence = tokenizer.tokenize(comment)
        for w in sentence:
            # check whether the word is in the WMT dictionary
            if w.lower() not in dic:
                counts[w] += 1
# Sort by counts
sorted_counts = sorted(counts.items(), key=lambda x: x[1])

# Total number of OOVs
tot_oovs = sum(counts.values())

# Save to file
with open(oov_freqs_output_file, 'w+') as f:
    # Print frequency from most frequent to less frequent
    for w, count in reversed(sorted_counts):
        print('%s\t%.3f%%' % (w.encode('utf-8'), count / tot_oovs * 100), file=f)
