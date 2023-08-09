
import os
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
        if name is not None
            self.name = name
        else:
            self.name = settings.trial_name

    def create_directory_structure(self):
        dirs_to_join = [self.settings.data_directory, 
                        self.settings.parent,
                        self.settings.pdbcode, 
                        self.settings.trial_name]
        self.data_directory = os.path.join(*dirs_to_join)

        if self.check_trial_directory():
            self.create_trial_directory()
        else:
            raise ValueError("Trial directory already exists")


    def check_trial_directory(self):
        """
        Checks if the trial directory exists. If not, returns True.
        """
        if os.path.exists(self.data_directory):
            return False
        else:
            return True
        

    def create_trial_directory(self):
        """
        Creates the trial directory. And replicate directories
        """

        dirs_to_create = self.settings.trial_dirs.append([self.settings.rep_directory +
                                                        str(i) for i in range(self.settings.replicates)])

        for directory in dirs_to_create:
            os.makedirs(os.path.join(self.data_directory, directory))
        
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

    def 