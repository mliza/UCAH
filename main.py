#!/opt/homebrew/bin/python3
'''
    Date:   09/13/2022
    Author: Martin E. Liza
    File:   main.py
    Def:

    Author		Date		Revision
    ----------------------------------------------------
    Martin E. Liza	09/13/2022	Initial version.
'''
import run_simulations 
import IPython 
import argparse
import numpy as np 

# User inputs 
n_cases         = 3
mach_in         = [1.8, 1.2]     
AoA             = [5, 17]  #[Degs] 
pressure_in     = 101325 * np.ones(n_cases)#[Pa]
temperature_in  = 279 * np.ones(n_cases) #[K]
abs_path        = '/Users/martin/Desktop'
case_name       = 'test'
model           = 'SA_NEG'
SU2             = 'rans'
convergence     = 13
i   = 0


# Set attributes 
parser = argparse.ArgumentParser() 
args   = parser.parse_args() 
# for i in range(n_cases): 
setattr(args, 'mach', [mach_in[i]])  
setattr(args, 'AoA', [AoA[i]])  
setattr(args, 'pressure', [pressure_in[i]])  
setattr(args, 'temperature', [temperature_in[i]])  
setattr(args, 'outName', [f'{case_name}_{i}']) 
setattr(args, 'model', [model]) 
setattr(args, 'SU2', SU2) 
setattr(args, 'absOutPath', [abs_path]) 
setattr(args, 'convergence', [convergence])
IPython.embed(colors = 'Linux') 

run_simulations.create_case(args, cfd_simulation='SU2', mesh_name='naca0012.su2')
run_simulations.mod_slurm(case_abs_path='case', job_name=f'{case_name}{i}')
run_simulations.run_CFD(args, cfd_simulation='SU2', local_flag=True, hpc_flag=False)






