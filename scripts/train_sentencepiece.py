from __future__ import print_function, division
import sys
import sentencepiece as spm

args = ' '.join(sys.argv[1:])

default_args='--input=wmt/corpus.tc.en --model_prefix=wmt.8k --model_type=bpe --vocab_size=8000'

if len(args)==0:
    args = default_args

spm.SentencePieceTrainer.Train(args)

