from __future__ import print_function, division
import sys
import sentencepiece as spm

model_file = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]

sp = spm.SentencePieceProcessor()
sp.Load(model_file)

with open(output_file, 'w+') as out_f: 
    with open(input_file, 'r', encoding='latin-1') as in_f:
        for l in in_f:
            pieces = sp.EncodeAsPieces(l.strip())
            print(' '.join(pieces), file=out_f)


