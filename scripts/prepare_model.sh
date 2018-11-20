#!/bin/bash
#SBATCH -n 1
#SBATCH -c 1 
#SBATCH -t 0
#SBATCH --mem=15g 
#SBATCH -J FUN_JOB_NAME
##SBATCH -o logs/log_prepare_model.txt

# Command line arguments
CONFIG_FILE=${1:-"config/data.en.config"}

# Load config
source $CONFIG_FILE

# Path to KenLM binaries
KENLM_BIN="$HOME/wd/kenlm/build/bin"

# Filenames
# Corpora
CORPUS_FILE="${CORPUS_DIR}/${FILE_ROOT}.${LANG}.txt"
LOWERCASED_CORPUS_FILE="${CORPUS_DIR}/${FILE_ROOT}.low.${LANG}.txt"
TOKENIZED_CORPUS_FILE="${CORPUS_DIR}/${FILE_ROOT}.${LANG}.${VOCABULARY_SIZE}.${SUBWORD_MODEL}.txt"
CORPUS_LM_SCORES="${CORPUS_DIR}/${FILE_ROOT}.${LANG}.${VOCABULARY_SIZE}.${SUBWORD_MODEL}.scores"
# Token dictionary
DICT_FILE_PREFIX="models/${FILE_ROOT}.${LANG}.dic"
# Subwords
SUBWORD_MODEL_PREFIX="models/${FILE_ROOT}.${LANG}.${VOCABULARY_SIZE}.${SUBWORD_MODEL}"
SUBWORD_MODEL_FILE="${SUBWORD_MODEL_PREFIX}.model"
# Language model
LM_MODEL_PREFIX="models/${FILE_ROOT}.${LANG}.${VOCABULARY_SIZE}.${SUBWORD_MODEL}.lm.${LM_ORDER}"
LM_MODEL_ARPA_FILE="${LM_MODEL_PREFIX}.arpa"
LM_MODEL_BINARY_FILE="${LM_MODEL_PREFIX}.bin"

# Lowercase
tr '[:upper:]' '[:lower:]' < $CORPUS_FILE > $LOWERCASED_CORPUS_FILE

mkdir models/

# Build dictionaries
echo "Building dictionary"
python scripts/build_dic.py $CORPUS_FILE $DICT_FILE_PREFIX $LANG

# Train bpe
echo "Building BPE model"
python scripts/train_sentencepiece.py --input "$LOWERCASED_CORPUS_FILE" --model_prefix "$SUBWORD_MODEL_PREFIX" --model_type "$SUBWORD_MODEL" --vocab_size "$VOCABULARY_SIZE"

# Tokenize
echo "Tokenizing"
python scripts/tokenize_sentencepiece.py $SUBWORD_MODEL_FILE $LOWERCASED_CORPUS_FILE $TOKENIZED_CORPUS_FILE
sed -i '/^\s*$/d' $TOKENIZED_CORPUS_FILE

# Train LM
echo "Training LM"
${KENLM_BIN}/lmplz -o 5 -S 4G < $TOKENIZED_CORPUS_FILE > $LM_MODEL_ARPA_FILE

# Convert to binary file for faster loading
echo "Building binary lm model file"
${KENLM_BIN}/build_binary $LM_MODEL_ARPA_FILE $LM_MODEL_BINARY_FILE

# Evaluate training sentences scores
echo "Evaluate scores of the training data"
python scripts/eval_kenlm.py $TOKENIZED_CORPUS_FILE $CORPUS_LM_SCORES $LM_MODEL_BINARY_FILE
