# File for MD tools

from pdbtools import *

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
