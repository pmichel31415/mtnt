#!/bin/bash
#SBATCH -n 10
#SBATCH -t 0
#SBATCH --mem 10g
#SBATCH -J WMT15_EN_FR_PREPROC
#SBATCH -o logs/log_en_fr_preprocessing.txt

# Command line arguments
CONFIG_FILE=${1:-"config/data.fr.config"}
MOSES_SCRIPTS=${2:-"${HOME}/wd/mosesdecoder/scripts"}
PERL="perl"

# Load config
source $CONFIG_FILE

# File names
RAW_FILE="${CORPUS_DIR}/raw"
CLEAN_FILE="${CORPUS_DIR}/clean"

# Concatenate the training set..
cat ${CORPUS_DIR}/news-commentary-v10.fr-en.fr ${CORPUS_DIR}/europarl-v7.fr-en.fr > ${RAW_FILE}.fr
cat ${CORPUS_DIR}/news-commentary-v10.fr-en.en ${CORPUS_DIR}/europarl-v7.fr-en.en > ${RAW_FILE}.en

# Clean
$PERL scripts/clean-corpus-n.perl $RAW_FILE fr en $CLEAN_FILE 1 70

# Get the dev/test data
wget -nv -O ${CORPUS_DIR}/dev.tgz http://www.statmt.org/wmt15/dev-v2.tgz
wget -nv -O ${CORPUS_DIR}/test.tgz http://www.statmt.org/wmt15/test.tgz

# Extract dev/test files
tar -xvzf ${CORPUS_DIR}/dev.tgz -C ${CORPUS_DIR} dev/newsdiscussdev2015-fren-ref.en.sgm dev/newsdiscussdev2015-fren-src.fr.sgm
tar -xvzf ${CORPUS_DIR}/test.tgz -C ${CORPUS_DIR} test/newsdiscusstest2015-fren-ref.en.sgm test/newsdiscusstest2015-fren-src.fr.sgm

# Remove XML tags
sed '/<seg/!d' ${CORPUS_DIR}/dev/newsdiscussdev2015-fren-ref.en.sgm | sed -e 's/\s*<[^>]*>\s*//g' > ${CORPUS_DIR}/dev.en
sed '/<seg/!d' ${CORPUS_DIR}/dev/newsdiscussdev2015-fren-src.fr.sgm | sed -e 's/\s*<[^>]*>\s*//g' > ${CORPUS_DIR}/dev.fr
sed '/<seg/!d' ${CORPUS_DIR}/test/newsdiscusstest2015-fren-ref.en.sgm | sed -e 's/\s*<[^>]*>\s*//g' > ${CORPUS_DIR}/test.en
sed '/<seg/!d' ${CORPUS_DIR}/test/newsdiscusstest2015-fren-src.fr.sgm | sed -e 's/\s*<[^>]*>\s*//g' > ${CORPUS_DIR}/test.fr
sed '/<seg/!d' ${CORPUS_DIR}/dev/newstest2014-fren-ref.fr.sgm | sed -e 's/\s*<[^>]*>\s*//g' > ${CORPUS_DIR}/newstest2014.fr
sed '/<seg/!d' ${CORPUS_DIR}/dev/newstest2014-fren-src.en.sgm | sed -e 's/\s*<[^>]*>\s*//g' > ${CORPUS_DIR}/newstest2014.en

