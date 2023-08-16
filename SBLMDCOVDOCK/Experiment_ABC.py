
import os
from copy import deepcopy
import glob
import pandas as pd
import time
import pickle
from abc import ABC, abstractmethod
from SBLMDCOVDOCK.SBLSettings import Settings

### Abstract method for the MD and Docking experiment classes

class Experiment(ABC):
    """
    This class represents an experimental trial.
    WHat do we need in this class?
    This class will handle some of the folder checking as well as the settings used for the run.
    
    """    
    def __init__(self,settings: Settings, name=None):
        super().__init__()
        self.settings = settings
        if name is not None:
            self.name = name
        else:
            self.name = self.settings.trial_name

        self.dataframe  = pd.DataFrame()
        self.dirs = {dir : None for dir in self.settings.dirs_to_create}


    @abstractmethod
    def check_args(self):
        """
        Checks the arguments for the trial.
        """
        pass

    def generate_path_structure(self, trial_name=None):
        """
        Generates the path structure for the trial.
        Sets self.dirs.
        Returns the data directory.
        """
        if trial_name is None:
            trial_name = self.name

        for dir in self.dirs.keys():
            dirs_to_join = [dir, 
                            self.settings.parent,
                            self.settings.pdbcode, 
                            trial_name]
            trial_dir = os.path.join(*dirs_to_join)
            print(f"Trial directory {dir}: ", trial_dir)
            self.dirs[dir] = trial_dir

        return self.dirs[self.settings.data_directory] 

    def create_directory_structure(self, overwrite=False):
        """
        Creates the directory structure for the trial.
        Checks if the trial directory exists. If not, creates it.
        Otherwise, adds a number to the end of the trial name and tries again.
        """
        if not overwrite:
            trial_name = self.name
            trial_dir = self.generate_path_structure(trial_name)
            trial_exists = os.path.exists(trial_dir)
            trial_number = 1

            while trial_exists:
                trial_name = self.name + str(trial_number)
                trial_dir = self.generate_path_structure(trial_name)
                trial_exists = os.path.exists(trial_dir)
                trial_number += 1

            self.name = trial_name

        self.create_directories()
        print("Created directories for trial: ", self.name)

    @abstractmethod
    def create_directories(self):
        """
        Creates the trial directories
        """
        data_dir = self.generate_path_structure()
        for dir in self.settings.dirs_to_create:
            #split path back into list
            dirs_to_join = data_dir.split(os.sep)
            dirs_to_join[0] = dir
            trial_dir = os.path.join(*dirs_to_join)
            
            os.makedirs(trial_dir, exist_ok=True)

        
    @abstractmethod
    def prepare_config(self):
        """
        Prepares the configuration file for the trial.
        """
        pass

    @abstractmethod
    def load_input_files(self):
        """
        Loads the input files for the trial.
        """
        pass

    @abstractmethod
    def prepare_input_files(self):
        """
        Prepares the input files for the trial.
        """
        pass

    @abstractmethod
    def save_experiment(self, save_name=None):
        """
        Writes the settings of the experiment (contents of class) to a pickle file. Logs???
        """
        unix_time = int(time.time())
        if save_name is not None:
            save_name = save_name+"_"+str(unix_time)+".pkl"
            save_path = os.path.join(self.settings.logs_directory, save_name)

            with open(save_path, 'wb') as f:
                pickle.dump(self, f)
                print("Saving experiment to: ", save_path)
                return save_path

    def load_experiment(self, latest=False, idx=None, load_path=None):
        """
        Loads the settings of the experiment from a pickle file.
        """
        if load_path is not None:
            print("Attempting to load experiment from: ", load_path)
            with open(load_path, 'rb') as f:
                print("Loading experiment from: ", load_path)
                return pickle.load(f)
            # print("Loaded object type:", type(loaded_obj))

            # return deepcopy(loaded_obj)


        # If no explicit path is provided
        search_dir = self.dirs[self.settings.logs_directory]
        print("Searching for experiment files in: ", search_dir)

        pkl_files = glob.glob(os.path.join(search_dir, "*.pkl"))
        print("Found files: ", pkl_files)

        if not pkl_files:
            print("No experiment files found.")
            raise FileNotFoundError
        pkl_files = sorted(pkl_files, key=os.path.getctime)
        if latest is True:
            print("Loading latest experiment.")
            file = pkl_files[-1]
        elif idx is not None:
            print(f"Loading {idx} experiment.")
            file = pkl_files[idx]
        else:
            print("Loading first experiment.")
            file = pkl_files[0]

        
        load_path = file    
        print("Loading experiment from: ", load_path)
        with open(load_path, 'rb') as f:
            return pickle.load(f)

        # return deepcopy(loaded_obj)
