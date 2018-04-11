#!/bin/bash
#SBATCH -n 4
#SBATCH -t 0
#SBATCH --mem 10g
#SBATCH -J WMT15_EN_FR_DOWNLOAD
#SBATCH -o logs/log_fr_download.txt

# Command line arguments
CONFIG_FILE=${1:-"config/data.fr.config"}
MOSES_TOKENIZER=${1:-"~/wd/mosesdecoder/scripts/tokenizer/tokenizer.perl"}

# Load config
source $CONFIG_FILE

# File name
CORPUS_FILE="${CORPUS_DIR}/${FILE_ROOT}.${LANG}.txt"

# Create corpus dir
mkdir -p $CORPUS_DIR

# Download data
wget -nv -O ${CORPUS_DIR}/europarl.tgz http://www.statmt.org/europarl/v7/fr-en.tgz
wget -nv -O ${CORPUS_DIR}/commoncrawl.tgz http://www.statmt.org/wmt13/training-parallel-commoncrawl.tgz
wget -nv -O ${CORPUS_DIR}/un.tgz http://www.statmt.org/wmt13/training-parallel-un.tgz
wget -nv -O ${CORPUS_DIR}/nc.tgz http://www.statmt.org/wmt15/training-parallel-nc-v10.tgz
wget -nv -O ${CORPUS_DIR}/giga.tar http://www.statmt.org/wmt10/training-giga-fren.tar


# Extract French training files
tar -zxvf ${CORPUS_DIR}/europarl.tgz -C ${CORPUS_DIR} europarl-v7.fr-en.fr
tar -zxvf ${CORPUS_DIR}/commoncrawl.tgz -C ${CORPUS_DIR} commoncrawl.fr-en.fr
tar -zxvf ${CORPUS_DIR}/un.tgz -C ${CORPUS_DIR} un/undoc.2000.fr-en.fr
tar -zxvf ${CORPUS_DIR}/nc.tgz -C ${CORPUS_DIR} news-commentary-v10.fr-en.fr
tar -xvf ${CORPUS_DIR}/giga.tar -C ${CORPUS_DIR} giga-fren.release2.fixed.fr.gz
gzip -d giga-fren.release2.fixed.fr.gz

# Concatenate
cat ${CORPUS_DIR}/giga-fren.release2.fixed.fr ${CORPUS_DIR}/commoncrawl.fr-en.fr ${CORPUS_DIR}/news-commentary-v10.fr-en.fr ${CORPUS_DIR}/un/undoc.2000.fr-en.fr ${CORPUS_DIR}/europarl-v7.fr-en.fr > $CORPUS_FILE

# Tokenize
$MOSES_TOKENIZER -l fr -threads 4 < ${CORPUS_FILE}.temp > $CORPUS_FILE
mv ${CORPUS_FILE}.temp $CORPUS_FILE

# Delete residual files and folders
rm -r ${CORPUS_DIR}/un
rm ${CORPUS_DIR}/*.{tar,gz,tgz}
