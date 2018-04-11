#!/bin/bash
#SBATCH -n 1
#SBATCH -c 1 
#SBATCH -t 0
#SBATCH --mem=15g 
#SBATCH -J DOWNLOAD_WMT
#SBATCH -o logs/log_wmt_download.txt

# Command line arguments
CONFIG_FILE=${1:-"config/dat.en.config"}

# Load config
source $CONFIG_FILE

# File name
CORPUS_FILE="${CORPUS_DIR}/${FILE_ROOT}.${LANG}.txt"

# Create corpus dir
mkdir -p $CORPUS_DIR

# Get data
if [ -e $CORPUS_FILE ]
then
    echo "File $CORPUS_FILE already exists, not downloading"
else
    echo "Downloading data"
    wget $WMT_URL
    # Decompress
    gzip -d corpus.tc.${LANG}.gz
    mkdir -p wmt
    mv corpus.tc.$LANG $CORPUS_FILE
    # Clean up
    rm corpus.tc.${LANG}.gz
fi

