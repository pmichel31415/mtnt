#!/bin/bash
#SBATCH -t 0
#SBATCH --mem=20g
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -J ROBOT_OVERTAKING_INTERNET_DONT_DISTURB

CONFIG_FILE=${1:-'config/my_config.yaml'}

python src/run_scraper.py $CONFIG_FILE
