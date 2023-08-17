import os
from copy import deepcopy
import glob
import shutil
import subprocess
from abc import ABC, abstractmethod
import pandas as pd
import argparse
import time
import pickle
from SBLMDCOVDOCK.Experiment_ABC import Experiment
from SBLMDCOVDOCK.SBLSettings import DOCKING_Settings

class DOCKING_Experiment(Experiment):
    def __init__(self,settings: DOCKING_Settings, name=None, pdbcode=None):
        super().__init__(settings, name)
        self.ligands = {}
        self.args = self.check_args()
        self.config_files = []
        self.topology_files = []
        if pdbcode is not None:
            self.settings.pdbcode = pdbcode
        self.generate_path_structure(name)



    def check_args(self):
        pass

    def create_directories(self):
        # we are using the ABC method here
        super().create_directories()
        ### Create docking specific directories


    def prepare_config(self, file_names=None):
        """
        Prepares the configuration files for the trial based on file names. 
        Otherwise grabs all files in the config folder.
        """
        config_files = os.listdir(os.path.join(self.settings.config))
        print("Config files: :", config_files)
        if file_names is not None:
            config_files = file_names

        self.config_files = config_files[0]
        print("Loading config files: ", config_files)

    def prepare_input_files(self):
        pass

    def load_input_files(self):
        pass

    def save_experiment(self, save_name=None):
        super().save_experiment(save_name)
    
        unix_time = int(time.time())
        if save_name is None:
            save_name = [self.settings.parent,
                        self.settings.pdbcode, 
                        self.name,
                        str(unix_time)]
            save_name = "_".join(save_name)+".pkl"
            
            log_dir = self.dirs[self.settings.logs_directory]
            
            save_path = os.path.join(log_dir, save_name)

            with open(save_path, 'wb') as f:
                pickle.dump(self, f)
        print("Saved experiment to: ", save_path)
        return save_path