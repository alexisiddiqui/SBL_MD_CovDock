# %%
### APO Production MD testing ###

# %%

from SBLMDCOVDOCK import SBLSettings
from SBLMDCOVDOCK.md_setuptools import plot_xvg
from SBLMDCOVDOCK.MD_Experiment import MD_Experiment
import pickle
from copy import deepcopy

import pandas as pd
import os

# import gmxapi as gmx
import subprocess
import matplotlib.pyplot as plt

# AMPC - https://journals.asm.org/doi/10.1128/AAC.02073-20
ampc = "6T3D"
# KPC-2 - BLDB: http://dx.doi.org/10.1021/ACS.JMEDCHEM.7B00158
kpc2 = "5UL8"
# OXA-10 - BLDB: https://www.pnas.org/doi/full/10.1073/pnas.241442898
oxa10 = "1K55"

structures = pd.DataFrame({"PDBID": [ampc, kpc2, oxa10], 
                           "Name": ["AmpC", "KPC2", "OXA10"]})


script_template = """#!/bin/bash

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


"""


for pdb in structures.PDBID:
    for res in range(1,5+1):

        line = f"python run_MD60_mpi.py -P {pdb} --replicate {res} -N APO_MD60_genvel --search APO" + "\n"

        with open(f"test.sh", 'w') as f:
            f.write(script_template)
            f.write(line)

        !sbatch test.sh
        
        break

