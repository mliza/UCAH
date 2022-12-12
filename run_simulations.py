#!/opt/homebrew/bin/python3
'''
    Date:   12/12/2022
    Author: Martin E. Liza
    File:   main_simulations.py
    Def:    Main file contains all the functions needed to 
        run the parser, at the moment only contains a SU2 version
        another flag can be added in args_flag.  

Author		    Date		Revision
----------------------------------------------------
Martin E. Liza	09/07/2022	Initial version.
Martin E. Liza  09/15/2022  Added a pbs option. 
Martin E. Liza  12/12/2022  Cleaned up and added comments. 
'''
import argparse 
import subprocess 
import shutil 
import os 
import re 

'''
    Define all availble options and modifications in the SU2 file. 
    Extra flags will need to be added if extra simualtions are required. 
    This was developed so it can be run in CLI as a single line command. 
'''
def arg_flags():
    parser = argparse.ArgumentParser() 
    parser.add_argument('--SU2', type=str.lower, required=True,
     help='Creates and runs SU2 simulations. Options are laminar or rans.') 
    # Optional arguments 
    parser.add_argument('-mach',        nargs='*', type=float, required=False,
                        help='Mach number per case. Default is 0.8')
    parser.add_argument('-AoA',         nargs='*', type=float, required=False,
                        help='Angle of attack per case. Default is 0.0')
    parser.add_argument('-pressure',    nargs='*', type=float, required=False,
                        help='Pressure per case. Default is 101325 [Pa]')
    parser.add_argument('-temperature', nargs='*', type=float, required=False,
                        help='Temperature per case. Default is 288.2[K]')
    parser.add_argument('-convergence', nargs='*', type=float, required=False, 
                        help='Convergence criteria, default is -13')
    parser.add_argument('-absOutPath',  nargs='*', type=str,   required=False,
                        help='Absolute output path') 
    parser.add_argument('-outName',     nargs='*', type=str,   required=False,
                        help='Optional output folder name') 
    parser.add_argument('-model',       nargs='*', type=str,   required=False,
            help='Model options for rans only (SA, SA_NEG and SST). Default is SA.') 

    # If optional arguments are empty modified them to default arguments 
    if args.mach        is None: 
        setattr(args, 'mach',        [0.8])
    if args.AoA         is None: 
        setattr(args, 'AoA',         [0.0])
    if args.pressure    is None: 
        setattr(args, 'pressure',    [101325.0] )
    if args.temperature is None: 
        setattr(args, 'temperature', [288.2])
    if args.convergence is None: 
        setattr(args, 'convergence', [13])
    if args.absOutPath  is None:
        setattr(args, 'absOutPath', [os.getcwd()])
    if args.outName     is None:
        setattr(args, 'outName',    ['case'])
    if args.model       is None:
        setattr(args, 'model',      ['SA'])
    return args

# Create cases and mofify the input files 
def create_case(args, cfd_simulation, mesh_name):
    destination_path = f'{args.absOutPath[0]}'
    case_name        = f'{args.outName[0]}'
    cwd_path         = os.getcwd() 
    cfd_path         = os.path.join(cwd_path, cfd_simulation)
    mesh_abs_path    = os.path.join(cfd_path, 'mesh', mesh_name)

    '''
        If the flag is for SU2, if new cases (NEMO) needs to be created 
        new switch and args.SU2 needs to be created.
        If a new simulations needs to be added (Cart3D) a new cfd_simulation flag
        needs to be implemented. 
    '''
    if cfd_simulation == 'SU2':
        switch = {0 : 'laminar',
                  1 : 'rans'}

        # Creates laminar path  
        if args.SU2 == switch[0]:
            src_path = os.path.join(cwd_path, cfd_path, f'{switch[0]}')
            dir_out  = os.path.join(destination_path,   f'{case_name}')

        # Create rans path 
        if args.SU2 == switch[1]: 
            src_path = os.path.join(cwd_path, cfd_path, f'{switch[1]}')
            dir_out  = os.path.join(destination_path,   f'{case_name}')

        # Creates case and calls the SU2 modifier 
        shutil.copytree(src_path, dir_out) 
        mod_SU2(args, dir_out, mesh_abs_path)

'''
    Modify SU2 input file, a new function needs to be created 
    to modify other simulations, if new options are required, they need to be
    added in here.  
'''
def mod_SU2(args, case_to_modify, mesh_abs_path):
    # Strings to replace (Regex is used to find variables in input files)
    mach_str        = 'MACH_NUMBER= \d*[.,]?\d*'     
    aoa_str         = 'AOA= \d*[.,]?\d*'
    pressure_str    = 'FREESTREAM_PRESSRE= \d*[.,]?\d*'
    temperature_str = 'FREESTREAM_TEMPERATURE= \d*[.,]?\d*'
    convergence_str = 'CONV_RESIDUAL_MINVAL= -\d*[.,]?\d*'
    rans_model_str  = 'KIND_TURB_MODEL= .*'
    mesh_str        = 'MESH_FILENAME= .*'

    # Replace strings  
    mach_replace        = f'MACH_NUMBER= {args.mach[0]}'
    aoa_replace         = f'AOA= {args.AoA[0]}'
    pressure_replace    = f'FREESTREAM_PRESSURE= {args.pressure[0]}'
    temperature_replace = f'FREESTREAM_TEMPERATURE= {args.temperature[0]}'
    convergence_replace = f'CONV_RESIDUAL_MINVAL= -{args.convergence[0]}'
    mesh_replace        = f'MESH_FILENAME= {mesh_abs_path}'

    # Reading cfg file, they have to be named rans or laminar. 
    file_to_read        = f'{args.SU2}.cfg'

    # Loading input file in memory  
    reading_file = open(os.path.join(case_to_modify, file_to_read), 'r+') 
    file_open    = reading_file.read() 
    reading_file.close() 

    # Searching and writing new file 
    new_file     = re.sub(mach_str, mach_replace, file_open) 
    new_file     = re.sub(aoa_str, aoa_replace, new_file) 
    new_file     = re.sub(pressure_str, pressure_replace, new_file) 
    new_file     = re.sub(temperature_str, temperature_replace, new_file) 
    new_file     = re.sub(convergence_str, convergence_replace, new_file) 
    new_file     = re.sub(mesh_str, mesh_replace, new_file) 

    # RANS Model's flag 
    if args.SU2 == 'rans':
        rans_model_replace = f'KIND_TURB_MODEL= {args.model[0]}'
        new_file = re.sub(rans_model_str, rans_model_replace, new_file) 
    writing_file = open(os.path.join(case_to_modify, file_to_read), 'r+') 
    writing_file.write(new_file) 

'''
    Modify slurm files, there is a PBS and SLURM file. 
    Renames the hpc script to submit by the case name.
'''
def mod_run_HPC(args, hpc_flag='slurm', abs_path=None):
    case_abs_path = os.path.join(args.absOutPath[0], args.outName[0])
    job_name      = args.outName[0] 
    # PBS flag 
    if hpc_flag == 'pbs':
        hpc_file     = os.path.join(case_abs_path, 'run.pbs') 
        case_str     = '#PBS -N .*'
        path_str     = f'cd {abs_path}'
        path_replace = f'cd {abs_path}/{job_name}' 
        case_replace = f'#PBS -N {job_name}'

    # SLURM flag 
    if hpc_flag == 'slurm':
        hpc_file     = os.path.join(case_abs_path, 'run.slurm') 
        path_str     = f'cd {abs_path}'
        path_replace = f'cd {abs_path}/{job_name}' 
        case_str     = '#SBATCH --job-name=.*'
        case_replace = f'#SBATCH --job-name={job_name}'

    # Modify hpc file  
    open_file    = open(hpc_file, 'r+')
    read_file    = open_file.read()
    open_file.close() 

    # Searching and writing strings 
    new_file      = re.sub(case_str, case_replace, read_file)
    new_file      = re.sub(path_str, path_replace, new_file)
    writing_file  = open(hpc_file, 'r+')
    writing_file.write(new_file) 

# Run Simulations (slurm, pbs or if local_flag=True, runs it locally) 
def run_CFD(args, cfd_simulation, local_flag=False, hpc_flag=False): 
    case_abs_path = os.path.join(args.absOutPath[0], args.outName[0])

    # HPC flag 
    if hpc_flag:
        pwd_cwd = os.getcwd() 
        os.chdir(case_abs_path)
        # run slurm 
        if hpc_flag == 'slurm':
            subprocess.call('sbatch run.slurm', shell=True)
        # run pbs 
        if hpc_flag == 'pbs':
            subprocess.call('qsub run.pbs',     shell=True)
        os.chdir(pwd_cwd)

    # Local Flag 
    if local_flag:
        if cfd_simulation == 'SU2':
            pwd_cwd = os.getcwd() 
            os.chdir(case_abs_path)
            out_file = 'output_print.txt'
            subprocess.call(f'SU2_CFD *.cfg >> {out_file}', shell=True)
            os.chdir(pwd_cwd)

if __name__=='__main__': 
    args = arg_flags() 
    create_case(args, cfd_simulation='SU2', mesh_name='naca0012.su2') 
    mod_run_HPC(args, hpc_flag='slurm') 
    run_CFD(args, cfd_simulation='SU2', local_flag=True, hpc_flag=False)
