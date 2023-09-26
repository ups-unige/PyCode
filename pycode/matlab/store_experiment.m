% -*-MATLAB-*-

function experiment = store_experiment(path, electrodes, save_path)
% Saves data present in PATH, organized the "Spycode way" in a unique .mat file
% Stored data are the time where a spike was found and not the whole raw data,
% ELECTRODES is a list of indices corresponding to the requested electrodes
% data and SAVE_PATH is where to store the output

    % possible_corrupted = 0;
    active_els = electrodes;
    sampling_frequency = 10000; % per ora hard coded
    
    tmp_phases_dirs = listdir(path);
    phases_dirs = {};
    [r, ~] = size(tmp_phases_dirs);
    counter = 0;

    for i=1:r
        % name_dir = tmp_phases_dirs{i, 1};
        % is_dir = tmp_phases_dirs{i, 2};
        if tmp_phases_dirs{i, 2} == 1 && ...
                ~(strcmp(tmp_phases_dirs{i, 1}, '.') || ...
		  strcmp(tmp_phases_dirs{i, 1}, '..'))
            counter = counter + 1;
            phases_dirs{counter} = tmp_phases_dirs{i, 1}; %#ok<AGROW> 
        end
    end

    experiment.phases = {};
    experiment.path = path;
    experiment.matrix_name = false;

    phases = cell(size(phases_dirs));
    for i=1:numel(phases_dirs)
        % Build a temporary struct where to save a phase data
        tmp_struct.name = phases_dirs{i};
        tmp_struct.peaks = cell(numel(active_els), 2);
        tmp_struct.digital = false;
        
        % Build the file path for electrodes data
        % 1. get matrix name
        base_dir = phases_dirs{i};
        matrix_name = extractBefore(base_dir, "_");
        if ~experiment.matrix_name
            experiment.matrix_name = matrix_name;
        end
            
        % 2. get the path for filtered peaks
        mat_dir = strcat(base_dir, '/', matrix_name, ...
                         '_Mat_files/', matrix_name, '_FilteredData/', ...
                         matrix_name, '_PeakDetectionMAT_PLP2ms_RP1ms/ptrain_', ...
                         base_dir, '_');


        % 3. get the digital signal path
        dig_file = strcat(base_dir, '/', base_dir, '/', ...
                         base_dir, '_D1_00.mat');

        % load the peaks of each electrode in a cell array with those data:
        % { num_el: str, data: struct} 
        % data is a struct with a "peak_train" field that is a sparse matrix
        % containing the peak train times

        for j=1:numel(active_els)
            tmp_struct.peaks{j, 1} = active_els(j);
            filename = strcat(mat_dir, string(active_els(j)));
            data = load(filename);
            tmp_struct.peaks{j, 2} = peaks_to_times(data.peak_train, ...
                                                    sampling_frequency);
        end

        % check if digital signal exist and load it in tmp_struct.digital

        if exist(dig_file, 'file')
            data = load(dig_file);
            tmp_struct.digital = data.data;
        end

        % copy the temporary struct reference in the experiment cell array
        phases{i} = tmp_struct;
    end

    experiment.phases = phases;

    save_file_path = strcat(save_path, '/', experiment.matrix_name);
    save(save_file_path, "-struct", "experiment", '-v6');
end
