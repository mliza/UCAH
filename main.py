#!/opt/homebrew/bin/python3
'''
    Date:   12/12/2022
    Author: Martin E. Liza
    File:   main.py
    Def:    Creates multiple SU2 cases with different AoA and 
            Mach numbers and runs them in an HPC.

    Author		    Date		Revision
    --------------------------------------------------------
    Martin E. Liza	09/13/2022	Initial version.
    Martin E. Liza  12/12/2022  Cleaned up and add comments.
'''
import run_simulations 
import argparse
import os 

# User inputs 
mach_in         = [1.1]                    #[ ]
AoA             = [2, 6]                   #[degs]
pressure_in     = 5530.0                   #[Pa]
temperature_in  = 217                      #[K]
abs_path        = '/home/u22/mliza/cases'  #path were cases are created
mesh_name       = 'naca0012.su2'           #name of the mesh to be use 
model           = 'SA_NEG'                 #see SU2 for different rans models  
SU2             = 'rans'                   #rans/laminar (laminar folder is missing)
hpc_flag        = 'slurm'                  #slurm/pbs 
convergence     = 8.5                      #SU2 convergence criteria 

# Loads argparse class 
parser = argparse.ArgumentParser() 


'''
 Iterates through mach numebrs and AoA. To iterate through 
 temperature and pressure two additional for loops will need to be added. 
'''
for i in mach_in:
    for j in AoA:
        # Load classes 
        args   = parser.parse_args() 

        # Set attibuts 
        setattr(args, 'mach', [i])  
        setattr(args, 'AoA', [j])  
        setattr(args, 'pressure', [pressure_in])  
        setattr(args, 'temperature', [temperature_in])  
        setattr(args, 'outName', [f'M{i}_AoA{j}']) 
        setattr(args, 'model', [model]) 
        setattr(args, 'SU2', SU2) 
        setattr(args, 'absOutPath', [abs_path]) 
        setattr(args, 'convergence', [convergence])

        # Create cases and modify SU2 input files (*.cfg) 
        run_simulations.create_case(args, cfd_simulation='SU2',
                                    mesh_name=mesh_name) 

        #  Modify slurm or pbs scripts   
        run_simulations.mod_run_HPC(args, hpc_flag=hpc_flag, abs_path=abs_path)

        # Run simulations using a pbs or slurm file  
        run_simulations.run_CFD(args, cfd_simulation='SU2', 
                                local_flag=False, 
                                hpc_flag=hpc_flag) 

        # Destructures, free memory  
        del args 
