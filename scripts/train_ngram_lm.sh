#!/bin/bash
#SBATCH -n 1
#SBATCH -c 1 
#SBATCH -t 0
#SBATCH --mem=15g 
#SBATCH -J "ngrams > LSTM, change my mind"

DATA_ROOT=$1
OUT_PREFIX=$2
ORDER=$3

# Path to KenLM binaries
KENLM_BIN="$HOME/wd/kenlm/build/bin"

TRAIN_FILE=${DATA_ROOT}/train.txt
DEV_FILE=${DATA_ROOT}/valid.txt
TEST_FILE=${DATA_ROOT}/test.txt

# Train LM
echo "Training LM"
${KENLM_BIN}/lmplz -o $ORDER -S 4G < $TRAIN_FILE > ${OUT_PREFIX}.arpa

# Convert to binary file for faster loading
echo "Building binary lm model file"
${KENLM_BIN}/build_binary ${OUT_PREFIX}.arpa ${OUT_PREFIX}.bin

# Evaluate dev sentences scores
echo "Evaluate scores of the dev data"
python scripts/eval_kenlm.py $DEV_FILE ${OUT_PREFIX}.dev.scores ${OUT_PREFIX}.bin

# Evaluate test sentences scores
echo "Evaluate scores of the test data"
python scripts/eval_kenlm.py $TEST_FILE ${OUT_PREFIX}.test.scores ${OUT_PREFIX}.bin
