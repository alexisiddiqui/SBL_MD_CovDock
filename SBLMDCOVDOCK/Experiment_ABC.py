
import os
from abc import ABC, abstractmethod

### Abstract method for the MD and Docking experiment classes

class Experiment(ABC):
    """
    This class represents an experimental trial.
    WHat do we need in this class?
    This class will handle some of the folder checking as well as the settings used for the run.
    
    """    
    def __init__(self,settings, name=None):
        super.__init__()
        self.settings = settings
        self.name = name

        

    def check_trial_directory(self):
        """
        Checks if the trial directory exists. If not, it creates it.
        Otherwise it changes the trial name to a new one and checks again.
        """
        pass


    @abstractmethod
    def create_trial_directory(self):
        """
        Creates the trial directory.
        """
        pass
    @abstractmethod
    def create_directory_structure(self):
        """
        Creates the directory structure for the trial.
        """
        pass
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

    def save_experiment(self):
        """
        Writes the settings of the experiment (contents of class) to a pickle file.
        """
        pass

    def load_experiment(self):
        """
        Loads the settings of the experiment from a pickle file.
        """
        pass