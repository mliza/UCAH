%{
    Date:   01/29/2022
    Author: Martin E. Liza
    File:   matlabHooks.m
    Def:    
    Req:    1) python3.9 and all packages listed in the runSimulation.py

    Author		    Date		Revision
    ----------------------------------------------------
    Martin E. Liza	01/29/2022	Initial version.
%}

% User inputs 
SU2_simulation  = 'inviscid'; % inviscid or rans  
number_of_cases = '1';        % number of cases the user is creating, n=1 is the default
mach_number     = '0.8';      % [ ], 0.8 is the default mach 
angle_of_attack = '0.0';      % [deg], 0.0 is the default angle
pressure        = '101325.0'; % [Pa], 101325.0 is the default pressure 
temperature     = '273';      % [K], 273 is the default temperature 
absPath         = 'newCases'; % default is same as where the runsSimulation.py 

% Creates string with python inputs to be run  
su2_str   = sprintf('--SU2 %s', SU2_simulation);
n_str     = sprintf('-n %s', number_of_cases); 
mach_str  = sprintf('-mach %s', mach_number); 
aoa_str   = sprintf('-AoA %s', angle_of_attack);
pres_str  = sprintf('-pressure %s', pressure); 
temp_str  = sprintf('-temperature %s', temperature);
path_str  = sprintf('-absOutPath %s', absPath);
flags_str = sprintf('%s %s %s %s %s %s %s', ...
            su2_str, n_str, mach_str, aoa_str, pres_str, temp_str, path_str);
run_str   = sprintf('python3.9 runSimulation.py %s', flags_str')
        
% Calls Python 
system(run_str);
