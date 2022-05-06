%{
    Date:   05/05/2022
    Author: Martin E. Liza
    File:   caller.m
    Def:    Example on how to run parserCaller
    Req:    1) python3 and all packages listed in the runSimulation.py

    Author		    Date		Revision
    ----------------------------------------------------
    Martin E. Liza	01/29/2022	Initial version.
%}

% User inputs 
SU2_simulation  = 'rans';     % inviscid or rans  
mach_number     = '0.5';      % [ ], 0.8 is the default mach 
angle_of_attack = '10';       % [deg], 0.0 is the default angle
abs_path        = false;      % if false creates in current directory 
out_name        = 'tomato';   % always give a name  
model_name      = false;      % only for rans, if false default to SA. Other model are  
                                % SST and SA_NEG 

out = parserCaller(SU2_simulation, model_name, mach_number, angle_of_attack, abs_path, out_name) 

