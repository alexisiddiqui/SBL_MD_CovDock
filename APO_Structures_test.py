# %%
### APO Structure creation ###

from SBLMDCOVDOCK import SBLSettings

settings = SBLSettings.GROMACS_Settings()

import pandas as pd
import os

# %%
# collect APO structures 

# AMPC - https://journals.asm.org/doi/10.1128/AAC.02073-20
ampc = "6T3D"
# KPC-2 - BLDB: http://dx.doi.org/10.1021/ACS.JMEDCHEM.7B00158
kpc2 = "5UL8"
# OXA-10 - BLDB: https://www.pnas.org/doi/full/10.1073/pnas.241442898
oxa10 = "1K55"

structures = pd.DataFrame({"PDBID": [ampc, kpc2, oxa10], 
                           "Name": ["AmpC", "KPC2", "OXA10"]})

# %%
# Download structures

from pdbtools import *

for pdbcode in structures.PDBID:
    output_path = os.path.join(settings.structures_input, pdbcode + ".pdb")
    !pdb_fetch {pdbcode} > {output_path}


# %%
# Clean structures from APO - remove water and hetatoms

for pdbcode in structures.PDBID:
    input_path = os.path.join(settings.structures_input, pdbcode + ".pdb")
    cleaned_path = os.path.join(settings.structures_input, "APO_" + pdbcode + ".pdb")
    !pdb_selchain -A {input_path} | pdb_delhetatm | pdb_tidy > {cleaned_path}

# %%
# Assign protonation states to the APO structures



# %%
# Prep simulations - set box size, solvate and ions




