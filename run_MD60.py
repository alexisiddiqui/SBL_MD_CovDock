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



# %%
settings = SBLSettings.GROMACS_Settings()
settings.suffix = "APO_md"
settings.search = "APO"
settings.config = os.path.join(settings.config, "APO_MD6test") 
print(settings.config)
settings.topology = os.path.join(settings.topology,settings.suffix.replace("_md","_npt"))
print(settings.topology)
# make sure to turn on MPI for HPC 
settings.gmx_mpi_on = False

# %%




print(__name__)
# specify ARGS: -P, -R, -N 
md = MD_Experiment(settings, 'APO_MD60_genvel', "1K55")
md.check_args()
md.create_directory_structure(overwrite=True)
md.run_experiment(search="APO")

save_path = md.save_experiment()

