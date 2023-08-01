"""
Settings classes
"""

import platform
import os
from copy import deepcopy

class Settings:
    "Represents the global settings for MD and Docking runs"
    def __init__(self, name=None):
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

# inhrerit from Settings
class GROMACS_Settings(Settings):
    "Represents the settings for a given run of MD"
    def __init__(self, name=None):
        super().__init__(name)
        self.trial_name = self.trial_name + '_MD'
        self.structures_input = os.path.join(self.structures_input,"APO")
        self.structures_output = os.path.join(self.structures_output,"APO")

class DOCKING_Settings(Settings):
    "Represents the settings for a given run of Docking"
    def __init__(self, name=None):
        super().__init__(name)
        self.trial_name = self.trial_name + '_Dock'
        self.structures_input = os.path.join(self.structures_input,"Ligand_Substrate")
        self.structures_output = os.path.join(self.structures_output,"Ligand_Substrate")
