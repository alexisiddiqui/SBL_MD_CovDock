#!/bin/bash

# Generic options:

#SBATCH --account=bdhbs10 # Run job under project <project>
#SBATCH --time=24:0:0         # Run for a max of 24 hour

# Node resources:
# (choose between 1-4 gpus per node)

#SBATCH --partition=gpu    # Choose either "gpu" or "infer" node type
#SBATCH --nodes=1          # Resources from a single node
#SBATCH --gres=gpu:1       # One GPU per node (plus 25% of node CPU and RAM per GPU)

# Run commands:

nvidia-smi  # Display available gpu resources

source ~/.bashrc

module load hecbiosim
module load gromacs/2023.1

conda activate RIN_test

nvidia-smi

