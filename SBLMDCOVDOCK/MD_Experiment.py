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
from SBLMDCOVDOCK.SBLSettings import GROMACS_Settings

class MD_Experiment(Experiment):
    def __init__(self,settings: GROMACS_Settings, name=None, pdbcode=None, rep=None):
        super().__init__(settings, name)
        self.trajectories = {}
        self.rep_no : int = None
        self.traj_no : int = 0
        self.set_replicate(rep)
        self.args = self.check_args()
        self.set_mdrun_gmx()
        self.set_environs()
        self.config_files = []
        self.topology_files = []
        if pdbcode is not None:
            self.settings.pdbcode = pdbcode
        self.generate_path_structure(name)

    def set_mdrun_gmx(self, mpi_on: bool = None):
        if mpi_on is None:
            mpi_on = self.settings.gmx_mpi_on

        if mpi_on:
            self.gmx = ("gmx_mpi","gmx")
        else:
            self.gmx = ("gmx","gmx_mpi")

    def set_environs(self):
        """
        Sets the environment variables for the trial.
        """
        os.environ[self.settings.environ] = self.settings.environ_path

    def check_args(self):
        """
        Checks the arguments for the trial.
        """
        if __name__ == '__main__':
            parser = argparse.ArgumentParser()

            parser.add_argument("-R", "--replicate", 
                                dest="replicate",
                                help="Replicate number", type=int,
                                default=0)
            
            ### TODO setup traj continuation
            # parser.add_argument("-T", "--trajectory", 
            #                     dest="traj_no", 
            #                     help="Trajectory number", type=int)
                                
            
            parser.add_argument("-P", "--pdbcode", 
                                dest="pdbcode", 
                                help="PDB code", type=str)
            
            parser.add_argument("-N", "--name",
                                dest="name",
                                help="Name of the trial", type=str)
            
            parser.add_argument("-S", "--suffix",
                                dest="suffix",
                                help="string for the trajectory files", type=str)
            
            parser.add_argument("-s", "--search",
                                dest="search",
                                help="search string for the top files", type=str)


            args = parser.parse_args()

            print("Arguments: ", args)

            if args.replicate is not None:
                self.set_replicate(args.replicate)

            if args.traj_no is not None:
                self.traj_no = args.traj_no

            if args.pdbcode is not None:
                self.settings.pdbcode = args.pdbcode

            if args.name is not None:
                self.name = args.name
            
            if args.suffix is not None:
                self.settings.suffix = args.suffix

            if args.search is not None:
                self.settings.search = args.search

            return args
    
    def create_directories(self):
        # we are using the ABC method here
        super().create_directories()
        # then we can create the MD specific directories
        rep_dirs = [self.settings.rep_directory + 
                          str(i) for i in range(1,self.settings.replicates+1)]

        data_dir = self.generate_path_structure(self.name)

        for directory in rep_dirs:
            print("Creating directory: ", directory, end=" ")
            path = os.path.join(data_dir, directory)
            os.makedirs(path, exist_ok=True)

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

    def prepare_input_files(self, search=None, file_names=None):
        """
        Prepares the topology files for the trial.
        """
        ### TODO refactor this to use self.dirs
        topology_files = os.listdir(os.path.join(self.settings.topology))
        topology_files = [file 
                        for file in topology_files 
                        if self.settings.pdbcode in file.split(".")[-2]]  
     
        print(f"Topology files for {self.settings.pdbcode}: ", topology_files)
        if search is None:
            search = self.settings.search

        if search is not None:
            topology_files = [file 
                              for file in topology_files 
                              if search in file.split(".")[-2]]
            
        if file_names is not None:
            topology_files = [file for file in topology_files if file in file_names]
        
        self.topology_files = topology_files
        print("Loading topology files: ", self.topology_files)

### This is mostly to check remote directories: return to this later.
    def check_all_trajectory_files(self, data_dir=None, traj_extension=None):
        """
        Checks if the trajectory files exist. For a given trial goes into each replicate and checks for file with the correct extension.
        Adds the name to the trajectories dictionary. If a data dir is given, it will check it.
        """
        if data_dir is None:
            data_dir = self.dirs[self.settings.data_directory]

        if traj_extension is None:
            traj_extension = self.settings.search_traj

        for rep in os.listdir(data_dir):
            self.trajectories[rep] = []
            for file in os.listdir(os.path.join(data_dir, rep)):
                if traj_extension in file and "#" not in file:
                    self.trajectories[rep].append(file)
        print("Trajectory files: ", self.trajectories)
        return self.trajectories
    
    def pbc_conversion(self, tpr_path):
        """
        Converts the trajectory file to correct for pbc.
        Returns the corrected trajectory file name.
        """
        traj_file = tpr_path.replace(".tpr", ".xtc")
        traj_file1 = traj_file.split(".")[-2] + self.settings.pbc_extensions[0] + ".xtc"
        traj_file2 = traj_file.split(".")[-2] + self.settings.pbc_extensions[1] + ".xtc"
        
        trjconv_command1 = ["gmx", "trjconv",
                             "-f", traj_file, 
                             "-s", tpr_path, 
                             *self.settings.pbc_commands[0], 
                             "-o", traj_file1]
        
        trjconv_command2 = ["gmx", "trjconv", 
                             "-f", traj_file1, 
                             "-s", tpr_path, 
                             *self.settings.pbc_commands[1], 
                             "-o", traj_file2]
        
        print("Running trjconv command 1: ", trjconv_command1)
        subprocess.run(trjconv_command1, input=b"1\n0\n", check=True)

        print("Running trjconv command 2: ", trjconv_command2)
        subprocess.run(trjconv_command2, input=b"1\n0\n", check=True)

        return traj_file2

### TODO later: This is for loading remote trajectories into local folder
    def load_trajectory_files(self, data_dir=None):
        """
        This is for syncing the trajectory files to the current experiment.
        This is meant to be for when files need to be transferred from the scratch disk to the home disk.
        This will copy all files from the data_dir to the data dict.
        """


        ### One function for local copy

        ### One function for remote copy

    def prepare_simulation(self, search=None):
        """
        This will prepare the simulation for the trial.
        """
        self.prepare_config()
        self.prepare_input_files(search)
        self.load_input_files()

    def run_MD_step(self):
        """
        This will run a step of MD for the trial.
        Retruns the tpr file name.
        """

        topo_files = [f for f in self.topology_files if f.endswith(".top")]
        gro_files = [f for f in self.topology_files if f.endswith(".gro")]
        tpr_name = "_".join([self.settings.suffix, 
                             self.settings.pdbcode, 
                            str(self.traj_no)]) + ".tpr"
        
        tpr_path = os.path.join(self.dirs[self.settings.data_directory], 
                                self.settings.rep_directory + str(self.rep_no), 
                                tpr_name)
        
        md_mdp = os.path.join(self.settings.config, self.config_files)
        
        topo_name = topo_files[0]
        topo_path = os.path.join(self.dirs[self.settings.data_directory], 
                                self.settings.rep_directory + str(self.rep_no), 
                                topo_name)
        
        gro_name = gro_files[0]
        input_path = os.path.join(self.dirs[self.settings.data_directory], 
                                self.settings.rep_directory + str(self.rep_no), 
                                gro_name) 

        grompp_command = ["gmx", "grompp", "-f", md_mdp, "-c", input_path, "-p", topo_path, "-o", tpr_path, "-r", input_path, "-v"]
        subprocess.run(grompp_command, check=True)
        ### TODO add try except for gmx vs gmx_mpi
        mdrun_command = [self.gmx[0], "mdrun", "-v", "-deffnm", tpr_path.replace(".tpr","")]
        subprocess.run(mdrun_command, check=True)

        self.set_trajectory_number()
        return tpr_path


    def run_experiment(self, search=None, rep=None):
        """
        This will run the experiment for the trial.
        suffix is the suffix for the initial topology files. 
        Should revert back to the suffix set in the settings.
        """

        self.set_replicate(rep)
        self.prepare_simulation(search)
        tpr_path = self.run_MD_step()
        traj_file = self.prepare_analysis(tpr_path=tpr_path)
        self.run_analysis(traj_file=traj_file)

### TODO sort out the trajfile naming
    def prepare_analysis(self, tpr_path):
        """
        This will prepare the analysis for the trial.
        """
        return self.pbc_conversion(tpr_path)
### TODO create analysis commands - add data to the dataframe
    def run_analysis(self, traj_file=None, tpr_path=None):
        ### This will take args from settings for what analyses to run
        # for now we just convert to pdb
        #if traj file is not given try to rebuild name
        if tpr_path is None:
            tpr_name = "_".join([self.settings.suffix, 
                                            self.settings.pdbcode, 
                                            str(self.traj_no)]) + ".tpr"
            tpr_path = os.path.join(self.dirs[self.settings.data_directory], 
                                    self.settings.rep_directory + str(self.rep_no), 
                                    tpr_name)

        if traj_file is None:
            traj_file = tpr_path.replace(".tpr", ".xtc")
            traj_file = traj_file.split(".")[-2] + self.settings.pbc_extensions[1] + ".xtc"
            pdb_name = str(self.rep_no) + "_" + tpr_name.replace(".tpr", ".pdb")
            pdb_name = pdb_name.split(os.sep)[-1]
        else:
            pdb_name = str(self.rep_no) + "_" + traj_file.replace(".xtc", ".pdb")
            pdb_name = pdb_name.split(os.sep)[-1]


        pdb_path = os.path.join(self.dirs[self.settings.viz], pdb_name)
        

        pdbout_command = ["gmx", "trjconv", 
                            "-f", traj_file,
                            "-s", tpr_path,
                            "-o", pdb_path]
        
        subprocess.run(pdbout_command, input=b"1\n", check=True)
        print("Saved pdb file to: ", pdb_path)



    def load_input_files(self, rep=None):
        """
        Copies the topology files for the trial.
        Files must be local.
        """
        if rep is None:
            rep = self.rep_no

        if rep is None:
            raise ValueError("Replicate number not set.")

        for file in self.topology_files:
            file_path = os.path.join(self.settings.topology, file)
            ### TODO refactor this to use self.dirs
            destination = os.path.join(self.dirs[self.settings.data_directory],
                                       self.settings.rep_directory + str(rep),
                                       file)
            shutil.copyfile(file_path, destination)
  
    def set_replicate(self, rep=None):
        """
        Sets the replicate for the trial.
        """
        if rep is not None:
            self.rep_no = int(rep)
        
        # check self.trajectories[rep] exists
        if self.trajectories.get(self.settings.rep_directory + str(self.rep_no)) is None:
            self.trajectories[self.settings.rep_directory + str(self.rep_no)] = []

        print("Replicate number: ", self.rep_no)

    def set_trajectory_number(self, trajectory_number=None):
        """
        Sets the trajectory number for the trial.
        """
        if trajectory_number is None:
            self.traj_no = self.find_latest_trajectory()
        else:
            self.traj_no = int(trajectory_number)
        print("Trajectory number: ", self.traj_no)

    def find_latest_trajectory(self, suffix=None, rep=None):
        """
        Finds the latest trajectory for the current trial. Uses the trajectory settings.
        Does not check converted trajectories.
        """
        if suffix is None:
            suffix = self.settings.suffix

        if rep is None:
            rep = self.rep_no

        if rep is None:
            raise ValueError("Replicate number not set.")

        self.check_all_trajectory_files()

        trajectory_files = self.trajectories[self.settings.rep_directory + str(rep)]
        #remove entries which dont contain the suffix
        trajectory_files = [file for file in trajectory_files if suffix in file]

        #sort the files by the number at the end
        trajectory_files = sorted(trajectory_files, 
                                  key=lambda x: int(x.split("_")[-1].split(".")[0]))

        # return traj_no
        return int(trajectory_files[-1].split("_")[-1].split(".")[0])

    def save_experiment(self, save_name=None):
        super().save_experiment(save_name=save_name)

        unix_time = int(time.time())
        if save_name is None:
            save_name = [self.settings.parent,
                        self.settings.pdbcode, 
                        self.name,
                        str(self.rep_no),
                        str(unix_time)]
            save_name = "_".join(save_name)+".pkl"
            
            log_dir = self.dirs[self.settings.logs_directory]
            
            save_path = os.path.join(log_dir, save_name)

            with open(save_path, 'wb') as f:
                pickle.dump(self, f)
        print("Saved experiment to: ", save_path)
        return save_path


        
