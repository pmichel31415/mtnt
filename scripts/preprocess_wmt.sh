#!/bin/bash
#SBATCH -n 1
#SBATCH -c 1 
#SBATCH -t 0
#SBATCH --mem=5g 
#SBATCH -J FUN_JOB_NAME
#SBATCH -o logs/log_preprocessing_wmt.txt

# Command line arguments
SUBWORD_MODEL=${1:-'bpe'}
VOCABULARY_SIZE=${2:-'1000'}
LM_ORDER=${3:-'5'}

# Path to KenLM binaries
KENLM_BIN="$HOME/wd/kenlm/build/bin"

# Filenames
# Corpora
CORPUS_FILE='wmt/corpus.tc.en'
LOWERCASED_CORPUS_FILE='wmt/corpus.low.en'
TOKENIZED_CORPUS_FILE="wmt/corpus.${VOCABULARY_SIZE}.${SUBWORD_MODEL}.en"
CORPUS_LM_SCORES="wmt/corpus.${VOCABULARY_SIZE}.${SUBWORD_MODEL}.scores"
# Token dictionary
DICT_FILE_PREFIX='models/wmt.en.dic'
# Subwords
SUBWORD_MODEL_PREFIX="models/wmt.${VOCABULARY_SIZE}.${SUBWORD_MODEL}"
SUBWORD_MODEL_FILE="${SUBWORD_MODEL_PREFIX}.model"
# Language model
LM_MODEL_ARPA_PREFIX="models/wmt.${VOCABULARY_SIZE}.${SUBWORD_MODEL}.lm.${LM_ORDER}"
LM_MODEL_ARPA_FILE="${LM_MODEL_PREFIX}.arpa"
LM_MODEL_BINARY_FILE="${LM_MODEL_PREFIX}.bin"

# Get data
wget http://data.statmt.org/wmt17/translation-task/preprocessed/de-en/corpus.tc.en.gz
# Decompress
gzip -d corpus.tc.en.gz
mkdir -p wmt
mv corpus.tc.en wmt
# Clean up
rm corpus.tc.en.gz

tr '[:upper:]' '[:lower:]' < $CORPUS_FILE > $LOWERCASED_CORPUS_FILE

# Build dictionaries
python scripts/build_dic.py $CORPUS_FILE $DICT_FILE_PREFIX

# Train bpe
python scripts/train_sentencepiece.py --input "$LOWERCASED_CORPUS_FILE" --model_prefix "$SUBWORD_MODEL_PREFIX" --model_type "$SUBWORD_MODEL" --vocab_size "$VOCABULARY_SIZE"

# Tokenize
python scripts/tokenize_sentencepiece.py $SUBWORD_MODEL_FILE $LOWERCASED_CORPUS_FILE $TOKENIZED_CORPUS_FILE

# Train LM
${KENLM_BIN}/lmplz -o 5 -S 4G < $TOKENIZED_CORPUS_FILE > $LM_MODEL_ARPA_FILE

# Convert to binary file for faster loading
${KENLM_BIN}/build_binary $LM_MODEL_ARPA_FILE $LM_MODEL_BINARY_FILE

# Evaluate training sentences scores
python scripts/eval_kenlm.py $TOKENIZED_CORPUS_FILE $CORPUS_LM_SCORES $LM_MODEL_BINARY_FILE
