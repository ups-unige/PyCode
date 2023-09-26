function names = listdir(path, varargin)
%LISTDIR Returns a list of files in a directory
%   Return the names of the file in PATH

print = false;
file_filter = "";

if numel(varargin) == 1
    file_filter = varargin{1};
elseif numel(varargin) == 2
    Wfile_filter = varargin{1};
    print = varargin{2};
end

pushd = cd;
cd (path)
files = dir;
names = cell(numel(files), 2);
i = 1;
for f = 1:numel(files)
    if strcmp(file_filter, "")
        names{f, 1} = files(f).name;
        names{f, 2} = files(f).isdir;
        if print
            display(files(f).name)
        end
    else
        if files(f).isdir
        else
            if strcmp(files(f).name(numel(files(f).name)-numel(file_filter)-1:end), file_filter)
                names{i, 1} = files(f).name;
                names{i, 2} = false;
                i = i + 1;
                if print
                    display(files(f).name)
                end
            end
        end
    end
end
cd (pushd)
end
