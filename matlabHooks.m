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
number_of_cases = '5';            % number of cases the user is creating, n=1 is the default
mach_number     = '0.1 0.3 0.5 0.7 0.9';      % [ ], 0.8 is the default mach 
angle_of_attack = '16 16 16 16 16 16';      % [deg], 0.0 is the default angle
pressure        = '101325 101325 101325 101325 101325'; % [Pa], 101325.0 is the default pressure 
temperature     = '288.2 288.2 288.2 288.2 288.2';      % [K], 273 is the default temperature 
absPath         = 'angle_16'; % No default, needs to be specified  

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

% Parsing output data 
cases_in      = dir(sprintf('%s', absPath));
cases_in(1:2) = [ ]; % Delete hidden files 
cell_cases_in = struct2cell(cases_in); 
% Empty arrays to be populated  
c_D   = [ ]; 
c_L   = [ ];
c_Eff = [ ];
c_Mx  = [ ];
c_My  = [ ];
c_Mz  = [ ];
c_Fx  = [ ];
c_Fy  = [ ];
c_Fz  = [ ];


% Reads and populates data from SU2 history file
for i = 1:length(cases_in) 
    flag_in   = sprintf('%s/%s/output_print.txt', absPath, cell_cases_in{1,i});
    hist_in   = sprintf('%s/%s/history.csv', absPath, cell_cases_in{1,i});
    flag_read = fileread(flag_in); 
    flag      = regexp(flag_read, 'All convergence criteria satisfied');
    if isempty(flag)
        sprintf('%s did not converge properly!', cell_cases_in{1,i}) 
    else 
        history_read = readtable(hist_in, 'PreserveVariableNames', true); 
        c_D(i)   = history_read.CD(end);  
        c_L(i)   = history_read.CL(end);
        c_Eff(i) = history_read.CEff(end);
        c_Mx(i)  = history_read.CMx(end); 
        c_My(i)  = history_read.CMy(end); 
        c_Mz(i)  = history_read.CMz(end); 
        c_Fx(i)  = history_read.CFx(end); 
        c_Fy(i)  = history_read.CFy(end); 
        c_Fz(i)  = history_read.CFz(end); 

    end 

end 


