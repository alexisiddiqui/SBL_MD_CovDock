# %%
### APO Production MD testing ###

# %%

from SBLMDCOVDOCK import SBLSettings
from SBLMDCOVDOCK.md_setuptools import plot_xvg

settings = SBLSettings.GROMACS_Settings()

import pandas as pd
import os

# import gmxapi as gmx
import subprocess
import matplotlib.pyplot as plt
#collect APO structures 

# AMPC - https://journals.asm.org/doi/10.1128/AAC.02073-20
ampc = "6T3D"
# KPC-2 - BLDB: http://dx.doi.org/10.1021/ACS.JMEDCHEM.7B00158
kpc2 = "5UL8"
# OXA-10 - BLDB: https://www.pnas.org/doi/full/10.1073/pnas.241442898
oxa10 = "1K55"

structures = pd.DataFrame({"PDBID": [ampc, kpc2, oxa10], 
                           "Name": ["AmpC", "KPC2", "OXA10"]})


settings.structures_output = os.path.join(settings.structures_output, 'amber14')
print(settings.structures_output)

amber14sb_ff_path = os.path.join(os.getcwd())

# Set the GMXLIB environment variable
os.environ["GMXLIB"] = amber14sb_ff_path

# %%


# %% [markdown]
# 

# %%
#Perform free production md of the apo protein

for pdbcode in structures.PDBID:
    # pdbcode = structures.PDBID[1]
    print(pdbcode)
    # break
    md_mdp = os.path.join(settings.config, 'md.mdp')
    topo_path = os.path.join(settings.structures_output, "APO_" + pdbcode+ ".top")

    input_path = os.path.join(settings.structures_output, "APO_" + pdbcode + "_npt.gro")
    tpr_path = os.path.join(settings.structures_output, "APO_" + pdbcode + "_md.tpr")

    grompp_command = ["gmx", "grompp", "-f", md_mdp, "-c", input_path, "-p", topo_path, "-o", tpr_path, "-r", input_path, "-v"]
    subprocess.run(grompp_command, check=True)

    mdrun_command = ["gmx", "mdrun", "-v", "-deffnm", tpr_path.replace(".tpr","")]
    subprocess.run(mdrun_command, check=True)
    # break
    # grompp_command = ["gmx", "grompp", "-f", md_mdp, "-c", input_path, "-p", topo_path, "-o", tpr_path.replace(".tpr", "_nbcpu.tpr"), "-r", input_path]
    # subprocess.run(grompp_command, check=True)

    # mdrun_command = ["gmx", "mdrun", "-deffnm", tpr_path.replace(".tpr","_nbcpu"), "-nb", "cpu"]
    # subprocess.run(mdrun_command, check=True)


    # grompp_command = ["gmx", "grompp", "-f", md_mdp, "-c", input_path, "-p", topo_path, "-o", tpr_path.replace(".tpr", "_nbgpu.tpr"), "-r", input_path]
    # subprocess.run(grompp_command, check=True)

    # mdrun_command = ["gmx", "mdrun", "-deffnm", tpr_path.replace(".tpr","_nbgpu"), "-nb", "gpu"]
    # subprocess.run(mdrun_command, check=True)


    print("Done with " + pdbcode)

# %%


# %%
for pdbcode in structures.PDBID:
    
    md_mdp = os.path.join(settings.config, 'md.mdp')
    topo_path = os.path.join(settings.structures_output, "APO_" + pdbcode+ ".top")

    xtc_path = os.path.join(settings.structures_output, "APO_" + pdbcode + "_md.xtc")
    tpr_path = os.path.join(settings.structures_output, "APO_" + pdbcode + "_md.tpr")
    xtc_out = xtc_path.replace(".xtc", "_noPBC.xtc")

    trjconv_command = ['gmx', 'trjconv', 
                       '-f', xtc_path, 
                       '-s', tpr_path,  
                       "-o", xtc_out,
                        '-pbc', 'mol',
                        "-center"]
    
    subprocess.run(trjconv_command, input=b"1\n0\n", check=True)

    trjconv_command = ['gmx', 'trjconv', 
                       '-f', xtc_path, 
                       '-s', tpr_path,  
                       "-o", xtc_out.replace(".xtc", ".pdb"),
                        '-pbc', 'mol',
                        "-center"]
    
    subprocess.run(trjconv_command, input=b"1\n1\n", check=True)


# %%
for pdbcode in structures.PDBID:
    
    md_mdp = os.path.join(settings.config, 'md.mdp')
    topo_path = os.path.join(settings.structures_output, "APO_" + pdbcode+ ".top")

    xtc_path = os.path.join(settings.structures_output, "APO_" + pdbcode + "_md.xtc")
    tpr_path = os.path.join(settings.structures_output, "APO_" + pdbcode + "_md.tpr")
    xtc_out = xtc_path.replace(".xtc", "_noPBC.xtc")

    gmx_rms_command = [
        "gmx", "rms", 
        "-s", tpr_path, 
        "-f", xtc_out, 
        "-o", xtc_out.replace(".xtc", "_rmsd.xvg"),
        "-tu", "ns"
    ]

    subprocess.run(gmx_rms_command, input=b"1\n1\n", check=True)

    plot_xvg(xtc_out.replace(".xtc", "_rmsd.xvg"))

# %%
#Perform free production md of the apo protein

for pdbcode in structures.PDBID:
    # pdbcode = structures.PDBID[1]
    print(pdbcode)
    # break
    md_mdp = os.path.join(settings.config, 'md.mdp')
    topo_path = os.path.join(settings.structures_output, "APO_" + pdbcode+ ".top")

    input_path = os.path.join(settings.structures_output, "APO_" + pdbcode + "_npt.gro")
    tpr_path = os.path.join(settings.structures_output, "APO_" + pdbcode + "_md.tpr")

    grompp_command = ["gmx", "grompp", "-f", md_mdp, "-c", input_path, "-p", topo_path, "-o", tpr_path, "-r", input_path, "-v"]
    subprocess.run(grompp_command, check=True)

    mdrun_command = ["gmx", "mdrun", "-v", "-deffnm", tpr_path.replace(".tpr","")]
    subprocess.run(mdrun_command, check=True)
    # break
    # grompp_command = ["gmx", "grompp", "-f", md_mdp, "-c", input_path, "-p", topo_path, "-o", tpr_path.replace(".tpr", "_nbcpu.tpr"), "-r", input_path]
    # subprocess.run(grompp_command, check=True)

    # mdrun_command = ["gmx", "mdrun", "-deffnm", tpr_path.replace(".tpr","_nbcpu"), "-nb", "cpu"]
    # subprocess.run(mdrun_command, check=True)


    # grompp_command = ["gmx", "grompp", "-f", md_mdp, "-c", input_path, "-p", topo_path, "-o", tpr_path.replace(".tpr", "_nbgpu.tpr"), "-r", input_path]
    # subprocess.run(grompp_command, check=True)

    # mdrun_command = ["gmx", "mdrun", "-deffnm", tpr_path.replace(".tpr","_nbgpu"), "-nb", "gpu"]
    # subprocess.run(mdrun_command, check=True)


    print("Done with " + pdbcode)

# %%
# #Perform free production md of the apo protein - testing for GPUs etc

# for pdbcode in structures.PDBID:
#     md_mdp = os.path.join(settings.config, 'md.mdp')
#     topo_path = os.path.join(settings.structures_output, "APO_" + pdbcode+ ".top")

#     input_path = os.path.join(settings.structures_output, "APO_" + pdbcode + "_npt.gro")
#     tpr_path = os.path.join(settings.structures_output, "APO_" + pdbcode + "_md.tpr")

#     grompp_command = ["gmx", "grompp", "-f", md_mdp, "-c", input_path, "-p", topo_path, "-o", tpr_path, "-r", input_path]
#     subprocess.run(grompp_command, check=True)

#     mdrun_command = ["gmx", "mdrun", "-deffnm", tpr_path.replace(".tpr","")]
#     subprocess.run(mdrun_command, check=True)

#     grompp_command = ["gmx", "grompp", "-f", md_mdp, "-c", input_path, "-p", topo_path, "-o", tpr_path.replace(".tpr", "_nbcpu.tpr"), "-r", input_path]
#     subprocess.run(grompp_command, check=True)

#     mdrun_command = ["gmx", "mdrun", "-deffnm", tpr_path.replace(".tpr","_nbcpu"), "-nb", "cpu"]
#     subprocess.run(mdrun_command, check=True)


#     grompp_command = ["gmx", "grompp", "-f", md_mdp, "-c", input_path, "-p", topo_path, "-o", tpr_path.replace(".tpr", "_nbgpu.tpr"), "-r", input_path]
#     subprocess.run(grompp_command, check=True)

#     mdrun_command = ["gmx", "mdrun", "-deffnm", tpr_path.replace(".tpr","_nbgpu"), "-nb", "gpu"]
#     subprocess.run(mdrun_command, check=True)


#     print("Done with " + pdbcode)


