#!/opt/homebrew/bin/python3.9
'''
    Date:   01/28/2022
    Author: Martin E. Liza
    File:   runSimulation.py
    Def:    Create and runs SU2 cases (inviscid and rans), at the moment 
            the pressure and temperature are kept constant at STD conditions. 
            Only the mach number and angle of attack are able to be modified.
   Req:     1) SU2 folder with inviscid and rans cases. 
            1) SU2 exports should be in the ~/.bashrc. 

    Ex. ./runSimulation --SU2 inviscid -n 2 -mach 0.5 0.6 -AoA 6 20 

    Author		    Date		Revision
    ------------------------------------------------
    Martin E. Liza	10/30/2021	Initial version.
'''
import argparse 
import subprocess 
import shutil 
import os 
import re 
import IPython 

# Output Folder absolute path 
cases_out = 'new_cases'

# Parser Options, Cart3D, LEMAS, etc 
def arg_flags():
    parser = argparse.ArgumentParser() 
    parser.add_argument('--SU2', type=str.lower, required=True,
         help='Creates and runs SU2 simulations for inviscid or rans')
    # Optional arguments 
    parser.add_argument('-n', nargs='?', type=int, required=False, 
                        help='Number of cases to be created')
    parser.add_argument('-mach', nargs='*', type=float, required=False)
    parser.add_argument('-AoA', nargs='*', type=float, required=False)
    parser.add_argument('-pressure', nargs='*', type=float, required=False)
    parser.add_argument('-temperature', nargs='*', type=float, required=False)
    args = parser.parse_args()  
    # If optional arguments are empty modified them to defaults 
    if args.n is None: 
        setattr(args, 'n', 1)
    if args.mach is None: 
        setattr(args, 'mach', [0.8])
    if args.AoA is None: 
        setattr(args, 'AoA', [0.0])
    if args.pressure is None: 
        setattr(args, 'pressure', [101325.0] )
    if args.temperature is None: 
        setattr(args, 'temperature', [273.0])
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

def mod_input(args):
    # Creates a direct path to each case 
    cases_list = sorted(os.listdir(cases_out)) 
    for i, val in enumerate(cases_list): 
        cases_path = os.path.join(os.getcwd(), cases_out, val)
    # Strings to replace  
        mach_str        = 'MACH_NUMBER= \d*[.,]?\d*'     
        aoa_str         = 'AOA= \d*[.,]?\d*'
        pressure_str    = 'FREESTREAM_PRESSURE= \d*[.,]?\d*'
        temperature_str = 'FREESTREAM_TEMPERATURE= \d*[.,]?\d*'
    # New variables  
        mach_replace        = f'MACH_NUMBER= {args.mach[i]}'
        aoa_replace         = f'AOA= {args.AoA[i]}'
        pressure_replace    = f'FREESTREAM_PRESSURE= {args.pressure[i]}'
        temperature_replace = f'FREESTREAM_TEMPERATURE= {args.temperature[i]}'
        file_to_read = f'{args.SU2}.cfg'
    # Loading input file in memory  
        reading_file = open(os.path.join(cases_path, file_to_read), 'r+') 
        file_open    = reading_file.read() 
        reading_file.close() 
    # Searching and writing new file 
        new_file     = re.sub(mach_str, mach_replace, file_open) 
        new_file     = re.sub(aoa_str, aoa_replace, new_file) 
        new_file     = re.sub(pressure_str, pressure_replace, new_file) 
        new_file     = re.sub(temperature_str, temperature_replace, new_file) 
        writing_file = open(os.path.join(cases_path, file_to_read), 'r+') 
        writing_file.write(new_file) 

# Modify slurm files 
def mod_slurm(args):
    # Creates a direct path to each case 
    cases_list = sorted(os.listdir(cases_out)) 
    for i in cases_list:  
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

#  Run Cases 
def run_cases(args):
    # Set up for bash call 
    cases        = sorted(os.listdir(cases_out)) 
    for i, val in enumerate(cases):
        running_case = os.path.join(f'{cases_out}', val) 
        output_file  = 'output_print.txt'
        cwd          = os.getcwd() 
        change_dir   = os.chdir(running_case) 
        subprocess.call(f'SU2_CFD *.cfg >> {output_file}', shell=True)
        original_dir = os.chdir(cwd) 

if __name__=='__main__': 
    args = arg_flags() 
    create_cases(args) 
    mod_input(args) 
    mod_slurm(args)
    run_cases(args) 
