#!/bin/bash
#SBATCH -t 0
#SBATCH --mem=6g
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -J ROBOT_OVERTAKING_INTERNET_DONT_DISTURB
#SBATCH -o logs/log_scraper.txt

python src/run_scraper.py config/my_config.yaml
