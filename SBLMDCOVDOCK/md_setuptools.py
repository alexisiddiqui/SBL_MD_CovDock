# File for MD tools

from pdbtools import *
import matplotlib.pyplot as plt
import pandas as pd
import os
import subprocess



def parse_propka_output(pka_file, pH=7.4):
    # Initialize the dictionary to store the protonation states
    protonation_states = {}

    with open(pka_file, 'r') as file:
        for line in file:
            # Split the line into words
            words = line.split()

            # Look for the lines that start with a residue name
            if len(words) > 0 and words[0] in ['LYS', "LYN",'ARG', 'ASP', "ASH", 'GLU', "GLH", 'GLN', 'HIS',"HIP", "HID", "HIE", "KCX"]:
                residue_name = words[0]
                residue_number = int(words[1])
                pka_value = float(words[3].strip('*'))

                # Determine the protonation state based on the pKa value
                if pka_value < pH:
                    protonation_state = ['0']
                else:
                    protonation_state = ['1']

                # Add the protonation state to the dictionary
                protonation_states[(residue_name, residue_number)] = protonation_state
                # protonation_states = pd.DataFrame.from_dict(protonation_states, orient="index")

    return protonation_states

def rename_KCX(input_path):
    with open(input_path, "r") as f:
        lines = f.readlines()
    
    for idx,line in enumerate(lines):
        # print(line)
        split = line.split(' ')
        # remove empty strings
        split = list(filter(None, split))
        # print(line)
        try:
            if split[3] == "KCX":
                # print(line)
                lines[idx] = line.replace("HETATM", "ATOM  ")
                print("changed", idx, line[:30])
        except:
            pass
        # print(line)

    output_path = input_path.replace(".pdb", "_atom.pdb")

    with open(output_path, "w+") as f:
        f.writelines(lines)

    print("Wrote to", output_path)

def plot_xvg(filename):
    # Read the file and get lines
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Extract labels and units from the file
    x_label = [line.split('"')[1] for line in lines if '@    xaxis  label' in line][0]
    y_label = [line.split('"')[1] for line in lines if '@    yaxis  label' in line][0]
    title = filename.split("/")[-1].replace(".xvg", "") + " " + [line.split('"')[1] for line in lines if '@    title' in line][0]
    # Read the data, skipping comment lines starting with '#', '@', or '&'
    data = pd.read_csv(filename, comment='@', skiprows=24, delim_whitespace=True, names=['x', 'y'], header=None)

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(data['x'], data['y'])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.show()

# Call the function with the provided file

