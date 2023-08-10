#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=48
#SBATCH --mem-per-cpu=2G
#SBATCH --time=12:00:00
#SBATCH --job-name=APO_Structures_test
#SBATCH --partition=short

module load GROMACS/2022.2-foss-2021a
module load Anaconda3/2022.10

conda activate RIN_test



python APO_Structures_test.py