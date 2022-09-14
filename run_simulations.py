#!/opt/homebrew/bin/python3
'''
    Date:   09/07/2022
    Author: Martin E. Liza
    File:   main_simulations.py
    Def:

    Author		    Date		Revision
    ----------------------------------------------------
    Martin E. Liza	09/07/2022	Initial version.
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
    parser.add_argument('-mach', nargs='*', type=float, required=False,
                        help='Mach number per case. Default is 0.8')
    parser.add_argument('-AoA', nargs='*', type=float, required=False,
                        help='Angle of attack per case. Default is 0.0')
    parser.add_argument('-pressure', nargs='*', type=float, required=False,
                        help='Pressure per case. Default is 101325 [Pa]')
    parser.add_argument('-temperature', nargs='*', type=float, required=False,
                        help='Temperature per case. Default is 288.2[K]')
    parser.add_argument('-convergence', nargs='*', type=float, required=False, 
                        help='Convergence criteria, default is -13')
    parser.add_argument('-absOutPath', nargs='*', type=str, required=False,
                        help='Absolute output path') 
    parser.add_argument('-outName', nargs='*', type=str, required=False,
                        help='Optional output folder name') 
    parser.add_argument('-model', nargs='*', type=str, required=False,
     help='Model options for rans only (SA, SA_NEG and SST). Default is SA.') 
    args = parser.parse_args()  
    # If optional arguments are empty modified them to defaults 
    if args.mach is None: 
        setattr(args, 'mach', [0.8])
    if args.AoA is None: 
        setattr(args, 'AoA', [0.0])
    if args.pressure is None: 
        setattr(args, 'pressure', [101325.0] )
    if args.temperature is None: 
        setattr(args, 'temperature', [288.2])
    if args.convergence is None: 
        setattr(args, 'convergence', [13])
    if args.absOutPath is None:
        setattr(args, 'absOutPath', [os.getcwd()])
    if args.outName is None:
        setattr(args, 'outName', ['case'])
    if args.model is None:
        setattr(args, 'model', ['SA'])
    return args

# Create cases 
def create_case(args, cfd_simulation, mesh_name):
    destination_path = f'{args.absOutPath[0]}'
    case_name        = f'{args.outName[0]}'
    cwd_path         = os.getcwd() 
    cfd_path         = os.path.join(cwd_path, cfd_simulation)
    mesh_abs_path    = os.path.join(cfd_path, 'mesh', mesh_name)

    # If the flag is for SU2 
    if cfd_simulation == 'SU2':
        switch = {0 : 'inviscid',
                  1 : 'rans'}
        # Copy inviscid folder 
        if args.SU2 == switch[0]:
            src_path = os.path.join(cwd_path, cfd_path, f'{switch[0]}')
            dir_out  = os.path.join(destination_path, f'{case_name}')
            shutil.copytree(src_path, dir_out) 
            # Call the SU2 modifier 
            mod_SU2(args, dir_out, mesh_abs_path)
        # Copy rans folder 
        if args.SU2 == switch[1]: 
            src_path = os.path.join(cwd_path, cfd_path, f'{switch[1]}')
            dir_out  = os.path.join(destination_path, f'{case_name}')
            shutil.copytree(src_path, dir_out) 
            # Call the SU2 modifier 
            mod_SU2(args, dir_out, mesh_abs_path)

# Modify SU2 input file 
def mod_SU2(args, case_to_modify, mesh_abs_path):
    # Strings to replace  
    mach_str        = 'MACH_NUMBER= \d*[.,]?\d*'     
    aoa_str         = 'AOA= \d*[.,]?\d*'
    pressure_str    = 'FREESTREAM_PRESSRE= \d*[.,]?\d*'
    temperature_str = 'FREESTREAM_TEMPERATURE= \d*[.,]?\d*'
    convergence_str = 'CONV_RESIDUAL_MINVAL= -\d*[.,]?\d*'
    rans_model_str  = 'KIND_TURB_MODEL= .*'
    mesh_str        = 'MESH_FILENAME= .*'
    # New variables  
    mach_replace        = f'MACH_NUMBER= {args.mach[0]}'
    aoa_replace         = f'AOA= {args.AoA[0]}'
    pressure_replace    = f'FREESTREAM_PRESSURE= {args.pressure[0]}'
    temperature_replace = f'FREESTREAM_TEMPERATURE= {args.temperature[0]}'
    convergence_replace = f'CONV_RESIDUAL_MINVAL= -{args.convergence[0]}'
    mesh_replace        = f'MESH_FILENAME= {mesh_abs_path}'
    # Reading file 
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

# Modify slurm files
def mod_slurm(case_abs_path, job_name):
    slurm_file   = os.path.join(case_abs_path, 'run.slurm') 

    case_str     = '#SBATCH --job-name=.*'
    case_replace = f'#SBATCH --job-name={job_name}'
    open_file    = open(slurm_file, 'r+')
    read_file    = open_file.read()
    open_file.close() 
    # Searching and writing strings 
    new_file      = re.sub(case_str, case_replace, read_file)
    writing_file  = open(slurm_file, 'r+')
    writing_file.write(new_file) 

# Run Simulations  
def run_CFD(args, cfd_simulation, local_flag=False, hpc_flag=False):
    case_abs_path = os.path.join(args.absOutPath[0], args.outName[0])
    # HPC flag 
    if hpc_flag:
        pwd_cwd = os.getcwd() 
        os.chdir(case_abs_path)
        subprocess.call('sbatch run.slurm', shell=True)
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
    mod_slurm('case', 'case_1') 
    run_CFD(args, cfd_simulation='SU2', local_flag=True, hpc_flag=False)

