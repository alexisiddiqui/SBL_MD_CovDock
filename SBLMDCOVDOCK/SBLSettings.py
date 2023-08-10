"""
Settings classes
"""

import platform
import os
from copy import deepcopy
import pandas as pd

# AMPC - https://journals.asm.org/doi/10.1128/AAC.02073-20
ampc = "6T3D"
# KPC-2 - BLDB: http://dx.doi.org/10.1021/ACS.JMEDCHEM.7B00158
kpc2 = "5UL8"
# OXA-10 - BLDB: https://www.pnas.org/doi/full/10.1073/pnas.241442898
oxa10 = "1K55"

structures = pd.DataFrame({"PDBID": [ampc, kpc2, oxa10], 
                           "Name": ["AmpC", "KPC2", "OXA10"]})



class Settings:
    "Represents the global settings for MD and Docking runs"
    def __init__(self, name=None, pdbcode: str = None):
        if pdbcode is not None:
            if pdbcode not in structures["PDBID"]:
                raise ValueError("PDBID not in database")
            self.pdbcode = pdbcode

        if name is not None:
            self.trial_name = name
        else:
            self.trial_name = 'base'
        self.temporary_directory = 'temporary'
        self.logs_directory = 'logs'
        self.data_directory = 'data'
        self.structures_input = "start_structures"
        self.structures_output = "prod_structures"
        self.config = 'config'
        self.topology = 'topology'
        self.viz = 'visualisation'
        self.pH = 7.4
        self.parent = None
        self.replicates = 5
        self.rep_directory = 'R_'
        self.ARGS = {}


# inhrerit from Settings
class GROMACS_Settings(Settings):
    "Represents the settings for a given run of MD"
    def __init__(self, name=None, pdbcode: str = None):
        super().__init__(name, pdbcode)
        if name is None:
            self.trial_name = self.trial_name + '_MD'
        self.structures_input = os.path.join(self.structures_input,"APO")
        self.structures_output = os.path.join(self.structures_output,"APO")
        self.parent = "MD"
        self.trial_dirs = [self.config, self.topology, self.viz]
        self.suffix = "MD"
        self.traj_extension = "xtc"

class DOCKING_Settings(Settings):
    "Represents the settings for a given run of Docking"
    def __init__(self, name=None, pdbcode: str = None):
        super().__init__(name, pdbcode)
        if name is None:
            self.trial_name = self.trial_name + '_Dock'
        self.structures_input = os.path.join(self.structures_input,"Ligand_Substrate")
        self.structures_output = os.path.join(self.structures_output,"Ligand_Substrate")
        self.parent = "Dock"


# fprint_calculator.py

fprint_params = {'bits': 4096, 'radius_multiplier': 1.5, 'rdkit_invariants': True}

confgen_params = {'max_energy_diff': 20.0, 'first': 1}


def calculate_fprint(row_dict, confgen_params, fprint_params):
    smiles = row_dict['SMILES']
    name = row_dict['Ligands']
    fprint = fprints_from_smiles(smiles, name, confgen_params=confgen_params, fprint_params=fprint_params)
    return fprint
