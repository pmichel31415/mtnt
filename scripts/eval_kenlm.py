# -*- coding: utf-8 -*-
from __future__ import print_function, division

import sys

import kenlm

from math import exp, log, log10, log2

input_file = sys.argv[1]
output_file = sys.argv[2]
model_file = sys.argv[3]

model = kenlm.Model(model_file)

full_score = 0
num_tokens = 0
with open(output_file, 'w+') as out_f:
    with open(input_file, 'r') as in_f:
        for l in in_f:
            score = model.score(l.strip(), bos = True, eos = True)
            print('%.5f\t%.5f' % (score, score/len(l.split())), file=out_f)
            full_score += score
            num_tokens += len(l.split())

print('ppl: %.3f' % exp(-full_score / num_tokens * log(10)))
print('bpc: %.3f' % (-full_score / num_tokens * log2(10)))

