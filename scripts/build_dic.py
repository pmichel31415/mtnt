from __future__ import print_function, division
import sys
import pickle

wmt_training_file = sys.argv[1]
output_file = sys.argv[2]
lang = sys.argv[3]

dic = set()
dic_lower = set()

with open(wmt_training_file, 'r') as f:
    for l in f:
        if lang == 'ja':
            words = l.strip()
        else:
            words = l.strip().split()
        for word in words:
            dic.add(word)
            dic_lower.add(word.lower())

print('%d unique tokens, %d lowercased' % (len(dic), len(dic_lower)))

with open(output_file + '.bin', 'wb+') as f:
    pickle.dump(dic, f)

with open(output_file + '_lower.bin', 'wb+') as f:
    pickle.dump(dic_lower, f)
