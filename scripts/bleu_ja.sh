#!/bin/bash

HYP=$1
REF=$2

cat $REF | kytea -model ~/kytea/share/kytea/model.bin -out tok > 'tmp.ref.ja'

cat $HYP | kytea -model ~/kytea/share/kytea/model.bin -out tok | sacrebleu --tokenize intl 'tmp.ref.ja'

rm 'tmp.ref.ja'
