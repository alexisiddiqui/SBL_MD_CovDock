import os
from abc import ABC, abstractmethod

from SBLMDCOVDOCK.Experiment_ABC import Experiment
from SBLMDCOVDOCK.SBLSettings import GROMACS_Settings



class MD_Experiment(Experiment):
    def __init__(self,settings: GROMACS_Settings, name=None):
        super(MD_Experiment).__init__(settings, name)
        self.trajectories = {}
        self.replicate = 0
        self.traj_no = 0


    def prepare_config(self, file_names=None):
        """
        Prepares the configuration files for the trial based on file names. Otherwise grabs all files in the config folder.
        """
        config_files = os.listdir(os.path.join(self.settings.config))
        print("Config files: :", config_files)
        if file_names is not None:
            config_files = file_names

        print("Loading config files: ", config_files)

    
    def prepare_input_files(self, suffix=None, file_names=None):
        """
        Prepares the topology files for the trial.
        """
        
        topology_files = os.listdir(os.path.join(self.settings.topology))
        print("Topology files: :", topology_files)
        if suffix is None:
            suffix = self.settings.suffix

        if suffix is not None:
            topology_files = [file 
                              for file in topology_files 
                              if file.split(".")[-2].endswith(suffix)]
            
        if file_names is not None:
            topology_files = file_names
        
        print("Loading topology files: ", topology_files)

    def check_trajectory_files(self, data_dir=None, traj_extension=None):
        """
        Checks if the trajectory files exist. For a given trial goes into each replicate and checks for file with the correct extension.
        Adds the name to the trajectories dictionary. If a data dir is given, it will check it.
        """

        if data_dir is None:
            data_dir = self.settings.data_directory

        for rep in os.listdir(data_dir):
            self.trajectories[rep] = []
            for file in os.listdir(os.path.join(data_dir, rep)):
                if file.endswith(self.settings.traj_extension):
                    self.trajectories[rep].append(file)

        return self.trajectories
    ### TODO
    def pbc_conversion(self, traj_file):
        """
        Converts the trajectory file to correct for pbc.
        """
        trjconv_command1 = ["gmx", "trjconv", "-f", traj_file, "-s", self.settings.topology, "-pbc", "mol", "-o", traj_file.split(".")[0] + "_pbc.xtc"]
        trjconv_command2 = ["gmx", "trjconv", "-f", traj_file.split(".")[0] + "_pbc.xtc", "-s", self.settings.topology, "-pbc", "nojump", "-o", traj_file.split(".")[0] + "_pbc_nojump.xtc"]

        pass
    

    ### TODO
    def load_trajectory_files(self, data_dir=None):
        """
        This is for syncing the trajectory files to the current experiment.
        This is meant to be for when files need to be transferred from the scratch disk to the home disk.
        This will copy all files from the data_dir to the data dict.
        """


        ### One function for local copy

        ### One function for remote copy

    ### TODO
    def prepare_simulation(self):
        """
        This will prepare the simulation for the trial.
        """
        
        self.prepare_config()
        self.prepare_input_files()
        self.load_input_files()
        self.load_config_files()
  
    def prepare_analysis(self):
        """
        This will prepare the analysis for the trial.
        """
        self.pbc_conversion()



    def load_input_files(self):
        """
        Copies the topology files for the trial.
        Files must be local.
        """

        pass

    def load_config_files(self):
        """
        Copies the config files for the trial.
        Files must be local.
        """
        pass
        
    def set_replicate(self, replicate):
        """
        Sets the replicate for the trial.
        """
        self.replicate = int(replicate)


    def set_trajectory_number(self, trajectory_number):
        """
        Sets the trajectory number for the trial.
        """
        self.traj_no = int(trajectory_number)


    def find_latest_trajectory(self, suffix=None, replicate=None)):
        """
        Finds the latest trajectory for the trial.
        """
        if suffix is None:
            suffix = self.settings.suffix

        if replicate is None:
            replicate = self.replicate

        
        trajectory_files = self.trajectories[self.settings.rep_directory + str(replicate)]

        #remove entries which dont contain the suffix
        trajectory_files = [file for file in trajectory_files if file.contains(suffix)]

        #sort the files by the number at the end
        trajectory_files = sorted(trajectory_files, key=lambda x: int(x.split("_")[-1].split(".")[0]))

        # set traj_no
        self.traj_no = int(trajectory_files[-1].split("_")[-1].split(".")[0])


     