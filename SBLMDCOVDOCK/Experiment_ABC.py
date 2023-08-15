
import os
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
        super.__init__()
        self.settings = settings
        if name is not None:
            self.name = name
        else:
            self.name = self.settings.trial_name

        self.dataframe  = pd.DataFrame()
        self.dirs = {
            self.settings.temporary_directory: None,
            self.settings.data_directory: None,
            self.settings.logs_directory: None,
            self.settings.viz : None,
            self.settings.ana: None,
        }


    @abstractmethod
    def check_args(self):
        """
        Checks the arguments for the trial.
        """
        pass

    def create_directory_structure(self, overwrite=False):
        """
        Creates the directory structure for the trial.
        Checks if the trial directory exists. If not, creates it.
        Otherwise, adds a number to the end of the trial name and tries again.
        """
        if not overwrite:
            trial_name = self.name
            dirs_to_join = [self.settings.data_directory, 
                            self.settings.parent,
                            self.settings.pdbcode, 
                            trial_name]
            trial_dir = os.path.join(*dirs_to_join)

            trial_exists = os.path.exists(trial_dir)
            trial_number = 1

            while trial_exists:
                trial_name = self.name + str(trial_number)
                dirs_to_join = [self.settings.data_directory, 
                                self.settings.parent,
                                self.settings.pdbcode, 
                                trial_name]
                trial_dir = os.path.join(*dirs_to_join)
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
        for dir in self.settings.dirs_to_create:
            trial_name = self.name
            dirs_to_join = [dir, 
                            self.settings.parent,
                            self.settings.pdbcode, 
                            trial_name]
            trial_dir = os.path.join(*dirs_to_join)

            self.dirs[dir] = trial_dir
            
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

    @abstractmethod
    def load_experiment(self, latest=False, load_path=None):
        """
        Loads the settings of the experiment from a pickle file.
        """
        if load_path is not None:
            try:
                with open(load_path, 'rb') as f:
                    print("Loadeing experiment from: ", load_path)
                    return pickle.load(f)
            except:
                search_dir = load_path

        elif load_path is None:
            dirs_to_search = [self.settings.logs_directory,
                            self.settings.parent,
                            self.settings.pdbcode,
                            self.name]
            search_dir = os.path.join(*dirs_to_search)
        
        try:
            search_dir = os.path.join(search_dir)
            pkl_files = glob.glob(search_dir, "*.pkl")
            print("Found files: ", pkl_files)
        except:
            pkl_files = glob.glob(search_dir, "*.pkl")
            print("Found files: ", pkl_files)

        if not pkl_files:
            print("No experiment files found.")
            raise FileNotFoundError
        
        if latest is True:
            file = max(pkl_files, key=os.path.getctime)
        
        else:
            file = min(pkl_files, key=os.path.getctime)
        
        load_path = file    
        print("Loading experiment from: ", load_path)
        with open(load_path, 'rb') as f:
            return pickle.load(f)
