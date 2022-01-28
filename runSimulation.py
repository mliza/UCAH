#!/opt/homebrew/bin/python3.9
'''
    Date:   10/30/2021
    Author: Martin E. Liza
    File:   runSimulation.py
    Def:    ./runSimulation --SU2 inviscid -n 2 -mach 0.5 -AoA 6

    Author		    Date		Revision
    ----------------------------------------------------
    Martin E. Liza	10/30/2021	Initial version.
'''
import argparse 
import subprocess 
import shutil 
import os 
import re 
import IPython 

# Output Folder 
cases_out = 'new_cases'

# Parser Options, Cart3D, LEMAS, etc 
def arg_flags():
    parser = argparse.ArgumentParser() 
    parser.add_argument('--SU2', type=str.lower, required=True,
                        help='Creates and runs SU2 simulations for 
                              inviscid or rans')

    # Optional arguments 
    parser.add_argument('-n', nargs='?', type=int, required=False, 
                        help='Number of cases to be created')
    parser.add_argument('-mach', nargs='?', type=float, required=False)
    parser.add_argument('-AoA', nargs='?', type=float, required=False)
    args = parser.parse_args()  

    # If optional arguments are empty modified them to defaults 
    if args.n is None: 
        setattr(args, 'n', 1)
    if args.mach is None: 
        setattr(args, 'mach', 0.8)
    if args.AoA is None: 
        setattr(args, 'AoA', 0.0)

    return args 

# Create folders with each case 
def create_cases(args): 
    destination_path = os.path.join(os.getcwd(), f'{cases_out}') 
    source_path      = os.getcwd()
    switch = { 0: 'inviscid',
               1: 'rans' }
    # Inviscid Case 
    if (args.SU2 == switch[0]):
        dir_in  = os.path.join('SU2', 'inviscid') 
        source  = os.path.join(source_path, dir_in)
        for i in range(1, args.n + 1):
            dir_out = os.path.join(destination_path, f'case_{i}')
            shutil.copytree(source, dir_out)

    # Rans Case 
    if (args.SU2 == switch[1]):
        dir_in  = os.path.join('SU2', 'rans') 
        source  = os.path.join(source_path, dir_in)
        for i in range(1, args.n + 1):
            dir_out = os.path.join(destination_path, f'case_{i}')
            shutil.copytree(source, dir_out)

# Modify slurm files 
def mod_slurm(args):
    # Creates a direct path to each case 
    for i in os.listdir(cases_out): 
        cases_path = os.path.join(os.getcwd(), cases_out, i)
    # Searching strings and replacing strings 
        job_name_str     = '\#SBATCH --job-name=.*?\n' 
        job_name_replace = f'#SBATCH --job-name={i}\n'
    # Loading slurm file in memory  
        reading_file = open(os.path.join(cases_path, 'puma.slurm'), 'r+') 
        file_open    = reading_file.read() 
        reading_file.close() 
    # Searching and writing new file 
        new_file     = re.sub(job_name_str, job_name_replace, file_open) 
        writing_file = open(os.path.join(cases_path, 'puma.slurm'), 'r+') 
        writing_file.write(new_file) 


if __name__=='__main__': 
    args = arg_flags() 
    create_cases(args) 
    mod_slurm(args)
