%{
    Date:   06/14/2022
    Author: Martin E. Liza
    File:   parserCaller.m
    Def:    Calls the python wrapper and process the coefficients, returns 
            and structure. 
    Req:    1) python3 and all packages listed in runSimulation.py 

    Author		    Date		Revision
    ----------------------------------------------------
    Martin E. Liza	05/05/2022	Initial version.
    Martin E. Liza	06/14/2022	Added convergence flag.
%}
function struct_out = parserCaller(SU2_simulation, model_name, ...  
                mach_number, angle_of_attack, convergence, abs_path, out_name)
    % Creates string with python inputs to be run  
    su2_str    = sprintf('--SU2 %s', SU2_simulation);
    mach_str   = sprintf('-mach %s', mach_number); 
    aoa_str    = sprintf('-AoA %s', angle_of_attack);
    path_str   = sprintf('-absOutPath %s', abs_path);
    name_str   = sprintf('-outName %s', out_name);
    rans_str   = sprintf('-model %s', model_name);
    conv_str   = sprintf('-convergence %s', convergence);

    % If rans model 
    if strcmp(SU2_simulation, 'rans')
        if rans_str ~= false 
            su2_str = sprintf('%s %s %s', su2_str, rans_str, conv_str); 
        end 
    end 

    if abs_path == false
        flags_str = sprintf('%s %s %s %s %s', ...
                su2_str, mach_str, aoa_str, name_str, conv_str);
    else 
        flags_str = sprintf('%s %s %s %s %s %s', ...
                su2_str, mach_str, aoa_str, name_str, conv_str, path_str);
    end 

    % Create running string, (can be suppress, add semicolon   
    run_str   = sprintf('python3 runSimulation.py %s', flags_str')
            
    % Calls Python 
    system(run_str);

    % Parsing output data 
    if abs_path == false 
        flag_in = sprintf('%s_1/output_print.txt', out_name);
        hist_in = sprintf('%s_1/history.csv', out_name);
    else 
        flag_in = sprintf('%s/%s_1/output_print.txt', abs_path, out_name);
        hist_in = sprintf('%s/%s_1/history.csv', abs_path, out_name);
    end 

    % Reading file 
    flag_read = fileread(flag_in); 
    flag      = regexp(flag_read, 'All convergence criteria satisfied');
    if isempty(flag)
        sprintf('%s_1 did not converge properly!, check output_print.txt', ...
            out_name) 
    else 
        history_read    = readtable(hist_in, 'PreserveVariableNames', true); 
        struct_out.CD   = history_read.CD(end);  
        struct_out.CL   = history_read.CL(end);
        struct_out.CEff = history_read.CEff(end);
        struct_out.CMx  = history_read.CMx(end); 
        struct_out.CMy  = history_read.CMy(end); 
        struct_out.CMz  = history_read.CMz(end); 
        struct_out.CFx  = history_read.CFx(end); 
        struct_out.CFy  = history_read.CFy(end); 
        struct_out.CFz  = history_read.CFz(end); 
    end 
end 
