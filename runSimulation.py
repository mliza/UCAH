#!/opt/homebrew/bin/python3.9
'''
    Date:   01/29/2022
    Author: Martin E. Liza
    File:   runSimulation.py
    Def:    Create and runs SU2 cases (inviscid and rans), at the moment 
            the pressure and temperature are kept constant at STD conditions. 
            Only the mach number and angle of attack are able to be modified.
   Req:     1) SU2 folder with inviscid and rans cases. 
            2) SU2 exports should be in the ~/.bashrc. 

    Ex. ./runSimulation --SU2 inviscid -n 2 -mach 0.5 0.6 -AoA 6 20 
                        -pressure 10134.0 24521.0 -temperature 280 300
                        -absOutPath ~/Desktop 

    Author		    Date		Revision
    ----------------------------------------------
    Martin E. Liza	01/29/2021	Initial version.
'''
import argparse 
import subprocess 
import shutil 
import os 
import re 
import IPython 

# Parser Options, Cart3D, LEMAS, etc 
def arg_flags():
    parser = argparse.ArgumentParser() 
    parser.add_argument('--SU2', type=str.lower, required=True,
            help='Creates and runs SU2 simulations. Options are inviscid or rans.') 
    # Optional arguments 
    parser.add_argument('-n', nargs='?', type=int, required=False, 
                        help='Number of cases to be created. Default is 1')
    parser.add_argument('-mach', nargs='*', type=float, required=False,
                        help='Mach number per case. Default is 0.8')
    parser.add_argument('-AoA', nargs='*', type=float, required=False,
                        help='Angle of attack per case. Default is 0.0')
    parser.add_argument('-pressure', nargs='*', type=float, required=False,
                        help='Pressure per case. Default is 101325 [Pa]')
    parser.add_argument('-temperature', nargs='*', type=float, required=False,
                        help='Temperature per case. Default is 288.2[K]')
    parser.add_argument('-absOutPath', nargs='*', type=str, required=False,
                        help='Absolute output path') 
    parser.add_argument('-model', nargs='*', type=str, required=False,
                        help='Model options for rans only (SA, SA_NEG and SST). Default is SA.') 
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
        setattr(args, 'temperature', [288.2])
    if args.absOutPath is None:
        setattr(args, 'absOutPath', [os.getcwd()])
    if args.model is None:
        setattr(args, 'model', ['SA'])
    return args

# Create folders with each case 
def create_cases(args): 
    destination_path = f'{args.absOutPath[0]}' 
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
    cases_out   = f'{args.absOutPath[0]}'
    list_filter = [x for x in os.listdir(cases_out) if x.startswith('case')]
    cases_list  = sorted(list_filter)
    for i, val in enumerate(cases_list): 
        cases_path = os.path.join(cases_out, val)
    # Strings to replace  
        mach_str        = 'MACH_NUMBER= \d*[.,]?\d*'     
        aoa_str         = 'AOA= \d*[.,]?\d*'
        pressure_str    = 'FREESTREAM_PRESSURE= \d*[.,]?\d*'
        temperature_str = 'FREESTREAM_TEMPERATURE= \d*[.,]?\d*'
        rans_model_str  = 'KIND_TURB_MODEL= SA'
    # New variables  
        mach_replace        = f'MACH_NUMBER= {args.mach[i]}'
        aoa_replace         = f'AOA= {args.AoA[i]}'
        pressure_replace    = f'FREESTREAM_PRESSURE= {args.pressure[i]}'
        temperature_replace = f'FREESTREAM_TEMPERATURE= {args.temperature[i]}'
        if args.SU2 == 'rans':
            rans_model_replace  = f'KIND_TURB_MODEL= {args.model[0]}'
        file_to_read        = f'{args.SU2}.cfg'
    # Loading input file in memory  
        reading_file = open(os.path.join(cases_path, file_to_read), 'r+') 
        file_open    = reading_file.read() 
        reading_file.close() 
    # Searching and writing new file 
        new_file     = re.sub(mach_str, mach_replace, file_open) 
        new_file     = re.sub(aoa_str, aoa_replace, new_file) 
        new_file     = re.sub(pressure_str, pressure_replace, new_file) 
        new_file     = re.sub(temperature_str, temperature_replace, new_file) 
    # RANS Model's flag 
        if args.SU2 == 'rans':
            new_file     = re.sub(rans_model_str, rans_model_replace, new_file) 
        writing_file = open(os.path.join(cases_path, file_to_read), 'r+') 
        writing_file.write(new_file) 

# Modify slurm files 
def mod_slurm(args):
    # Creates a direct path to each case 
    cases_out   = f'{args.absOutPath[0]}'
    list_filter = [x for x in os.listdir(cases_out) if x.startswith('case')]
    cases_list  = sorted(list_filter)
    for i, val in enumerate(cases_list):  
        cases_path = os.path.join(cases_out, val)
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
    cases_out   = f'{args.absOutPath[0]}'
    list_filter = [x for x in os.listdir(cases_out) if x.startswith('case')]
    cases_list  = sorted(list_filter)
    for i, val in enumerate(cases_list):
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
