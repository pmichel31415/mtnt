#!/bin/bash
#SBATCH -n 4
#SBATCH -t 0
#SBATCH --mem 10g
#SBATCH -J EN_JA_DOWNLOAD
#SBATCH -o logs/log_ja_download.txt

# Command line arguments
CONFIG_FILE=${1:-"config/data.ja.config"}
MOSES_SCRIPTS=${2:-"${HOME}/wd/mosesdecoder/scripts"}
KYTEA_BIN=${2:-"${HOME}/wd/mosesdecoder/scripts"}
PERL="LANG=C perl"

# Load config
source $CONFIG_FILE

# File name
CORPUS_FILE="${CORPUS_DIR}/${FILE_ROOT}.ja"
TRAIN_FILE="${CORPUS_DIR}/train"
DEV_FILE="${CORPUS_DIR}/dev"
TEST_FILE="${CORPUS_DIR}/test"
TEMP_FILE="${CORPUS_DIR}/temp"

# Create corpus dir
mkdir -p $CORPUS_DIR

# ================== Download data ============================================

# Download JESC
wget -nv -O ${CORPUS_DIR}/jesc.tar.gz https://goo.gl/idaoxo
# Download KFTT
wget -nv -O ${CORPUS_DIR}/kftt.tar.gz http://www.phontron.com/kftt/download/kftt-data-1.0.tar.gz
# Download TED
wget -nv -O ${CORPUS_DIR}/ted.en-ja.tgz https://wit3.fbk.eu/archive/2017-01-trnted//texts/en/ja/en-ja.tgz

# ================== Extract data =============================================

# Visualize file structures
tar -tf ${CORPUS_DIR}/ted.en-ja.tgz
tar -tf ${CORPUS_DIR}/jesc.tar.gz
tar -tf ${CORPUS_DIR}/kftt.tar.gz

# Extract to files
for lang in 'en' 'ja';
do
    # Extract training files
    tar -zxvf ${CORPUS_DIR}/ted.en-ja.tgz -C ${CORPUS_DIR} en-ja/train.tags.en-ja.$lang
    tar -zxvf ${CORPUS_DIR}/jesc.tar.gz -C ${CORPUS_DIR} detokenized/train.$lang
    tar -zxvf ${CORPUS_DIR}/kftt.tar.gz -C ${CORPUS_DIR} kftt-data-1.0/data/orig/kyoto-train.$lang

    # Extract dev files
    tar -zxvf ${CORPUS_DIR}/ted.en-ja.tgz -C ${CORPUS_DIR} en-ja/IWSLT17.TED.tst2014.en-ja.${lang}.xml
    tar -zxvf ${CORPUS_DIR}/jesc.tar.gz -C ${CORPUS_DIR} detokenized/val.$lang
    tar -zxvf ${CORPUS_DIR}/kftt.tar.gz -C ${CORPUS_DIR} kftt-data-1.0/data/orig/kyoto-dev.$lang
    
    # Extract test files
    tar -zxvf ${CORPUS_DIR}/ted.en-ja.tgz -C ${CORPUS_DIR} en-ja/IWSLT17.TED.tst2015.en-ja.${lang}.xml
    tar -zxvf ${CORPUS_DIR}/jesc.tar.gz -C ${CORPUS_DIR} detokenized/test.$lang
    tar -zxvf ${CORPUS_DIR}/kftt.tar.gz -C ${CORPUS_DIR} kftt-data-1.0/data/orig/kyoto-test.$lang
done

# Special case: TED talks monolingual data
tar -zxvf ${CORPUS_DIR}/ted.en-ja.tgz -C ${CORPUS_DIR} en-ja/train.ja
mv ${CORPUS_DIR}/en-ja/train.ja ${CORPUS_DIR}/en-ja/mono.ja

# ================= Prepare monolingual data ==================================

# Corpus file without preprocessing for monolingual experiments
cat ${CORPUS_DIR}/en-ja/mono.ja ${CORPUS_DIR}/detokenized/train.ja ${CORPUS_DIR}/kftt-data-1.0/data/orig/kyoto-train.ja > ${CORPUS_FILE}

# Remove empty lines
sed -i '/^\s*$/d' $CORPUS_FILE

# ================== Prepare bilingual data ===================================

# Create files
for lang in 'en' 'ja';
do
    # Remove XML tags
    sed '/^\s*</d' ${CORPUS_DIR}/en-ja/train.tags.en-ja.${lang} | sed -e 's/^\s*//g' | sed -e 's/\s*$//g' > ${CORPUS_DIR}/en-ja/train.$lang 
    sed '/<seg/!d' ${CORPUS_DIR}/en-ja/IWSLT17.TED.tst2014.en-ja.${lang}.xml | sed -e 's/\s*<[^>]*>\s*//g' > ${CORPUS_DIR}/en-ja/dev.$lang 
    sed '/<seg/!d' ${CORPUS_DIR}/en-ja/IWSLT17.TED.tst2015.en-ja.${lang}.xml | sed -e 's/\s*<[^>]*>\s*//g' > ${CORPUS_DIR}/en-ja/test.$lang 

    # De-segment (remove ascii spaces)
    if [ $lang = 'ja' ]; then
        sed -i 's/ //' ${CORPUS_DIR}/en-ja/train.$lang
        sed -i 's/ //' ${CORPUS_DIR}/detokenized/train.$lang
        sed -i 's/ //' ${CORPUS_DIR}/en-ja/dev.$lang
        sed -i 's/ //' ${CORPUS_DIR}/detokenized/val.$lang
        sed -i 's/ //' ${CORPUS_DIR}/en-ja/test.$lang
        sed -i 's/ //' ${CORPUS_DIR}/detokenized/test.$lang
    fi
    # Concatenate to training file
    cat ${CORPUS_DIR}/en-ja/train.$lang ${CORPUS_DIR}/detokenized/train.$lang ${CORPUS_DIR}/kftt-data-1.0/data/orig/kyoto-train.$lang > ${TRAIN_FILE}.$lang

    # Concatenate to dev file
    cat ${CORPUS_DIR}/en-ja/dev.$lang ${CORPUS_DIR}/detokenized/val.$lang ${CORPUS_DIR}/kftt-data-1.0/data/orig/kyoto-dev.$lang > ${DEV_FILE}.$lang

    # Concatenate to test file
    cat ${CORPUS_DIR}/en-ja/test.$lang ${CORPUS_DIR}/detokenized/test.$lang ${CORPUS_DIR}/kftt-data-1.0/data/orig/kyoto-test.$lang > ${TEST_FILE}.$lang
done

# Clean training file
#$PERL scripts/clean-corpus-n.perl $TEMP_FILE ja en $TRAIN_FILE 1 70
rm ${TEMP_FILE}.*

# Concatenate training files (for shared vocab)
cat ${TRAIN_FILE}.en ${TRAIN_FILE}.ja > ${TRAIN_FILE}.both

# ================== Cleanup ==================================================

# Delete residual files and folders
rm ${CORPUS_DIR}/*.{tar.gz,tgz}

