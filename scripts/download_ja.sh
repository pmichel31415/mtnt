#!/bin/bash
#SBATCH -n 4
#SBATCH -t 0
#SBATCH --mem 10g
#SBATCH -J EN_JA_DOWNLOAD
#SBATCH -o logs/log_ja_download.txt

# Command line arguments
CONFIG_FILE=${1:-"config/data.ja.config"}

# Load config
source $CONFIG_FILE

# File name
CORPUS_FILE="${CORPUS_DIR}/${FILE_ROOT}.${LANG}.txt"

# Create corpus dir
mkdir -p $CORPUS_DIR

# Download JESC
wget -nv -O ${CORPUS_DIR}/jesc.tar.gz https://goo.gl/idaoxo
# Download KFTT
wget -nv -O ${CORPUS_DIR}/kftt.tar.gz http://www.phontron.com/kftt/download/kftt-data-1.0.tar.gz
# Download TED
wget -nv -O ${CORPUS_DIR}/ted.en-ja.tgz https://wit3.fbk.eu/archive/2017-01-trnted//texts/en/ja/en-ja.tgz

# Visualize file structures
tar -tf ${CORPUS_DIR}/ted.en-ja.tgz
tar -tf ${CORPUS_DIR}/jesc.tar.gz
tar -tf ${CORPUS_DIR}/kftt.tar.gz

# Extract japanese training files
tar -zxvf ${CORPUS_DIR}/ted.en-ja.tgz -C ${CORPUS_DIR} en-ja/train.ja
tar -zxvf ${CORPUS_DIR}/jesc.tar.gz -C ${CORPUS_DIR} detokenized/train.ja
tar -zxvf ${CORPUS_DIR}/kftt.tar.gz -C ${CORPUS_DIR} kftt-data-1.0/data/orig/kyoto-train.ja

# concatenate
cat ${CORPUS_DIR}/en-ja/train.ja ja/detokenized/train.ja ja/kftt-data-1.0/data/orig/kyoto-train.ja > $CORPUS_FILE
# Remove empty lines
sed -i '/^\s*$/d' $CORPUS_FILE

# Delete residual files and folders
rm -r ${CORPUS_DIR}/en-ja
rm -r ${CORPUS_DIR}/detokenized
rm -r ${CORPUS_DIR}/kftt-data-1.0
rm ${CORPUS_DIR}/*.{tar.gz,tgz}

