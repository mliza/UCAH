#!/opt/homebrew/bin/python3
'''
    Date:   09/13/2022
    Author: Martin E. Liza
    File:   main.py
    Def:

    Author		    Date		Revision
    ----------------------------------------------------
    Martin E. Liza	09/13/2022	Initial version.

'''
import run_simulations 
import argparse
import os 
import numpy as np 

# User inputs 
mach_in         = range(2, 10)           #[ ] 
AoA             = range(0, 30, 5)        #[Degs] 
pressure_in     = 5530.0                 #[Pa]
temperature_in  = 217                    #[K]
abs_path        = '/p/home/mliza/cases'
mesh_name       = 'naca0012.su2'
mesh_name       = 'dell_try3.su2'
model           = 'SA_NEG'
SU2             = 'rans'
convergence     = 13

# Set attributes and run Simulations  
for i in mach_in:
    for j in AoA:
        parser = argparse.ArgumentParser() 
        args   = parser.parse_args() 
        setattr(args, 'mach', [i])  
        setattr(args, 'AoA', [j])  
        setattr(args, 'pressure', [pressure_in])  
        setattr(args, 'temperature', [temperature_in])  
        setattr(args, 'outName', [f'M{i}_AoA{j}']) 
        setattr(args, 'model', [model]) 
        setattr(args, 'SU2', SU2) 
        setattr(args, 'absOutPath', [abs_path]) 
        setattr(args, 'convergence', [convergence])
        run_simulations.create_case(args, cfd_simulation='SU2',
                                    mesh_name=mesh_name) 
        run_simulations.mod_run_HPC(args, hpc_flag='pbs')
        run_simulations.run_CFD(args, cfd_simulation='SU2', 
                            local_flag=False, 
                                hpc_flag='pbs') 
