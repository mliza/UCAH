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

# User inputs 
mach_in         = [1.1, 2, 3, 4, 5, 6, 7, 8, 9]          #[ ] 
AoA             = [0, 5, 10, 15, 18, 20, 22, 25]       #[Degs] 
mach_in         = [1.1]
AoA             = [0] 
pressure_in     = 5530.0                 #[Pa]
temperature_in  = 217                    #[K]
abs_path        = '/p/work1/mliza/angle_22'
abs_path        = '/p/work1/mliza/angle_45'
mesh_name       = 'naca0012.su2'
mesh_name       = 'pw_mesh2.su2'
mesh_name       = 'pw_mesh2_22p5.su2'
mesh_name       = 'pw_mesh2_45.su2'
model           = 'SA'
SU2             = 'rans'
convergence     = 8.5

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
        run_simulations.mod_run_HPC(args, hpc_flag='pbs', abs_path=abs_path)
        run_simulations.run_CFD(args, cfd_simulation='SU2', 
                            local_flag=False, 
                                hpc_flag='pbs') 
