% Reader will read all files within that folder
% Data must be in either png or jgp
% For simplification reason, the original image is always noreflection
function [file_path, files, ref] = filewalk(path, extension)
    files = []; ref = '';
    full_path = fullfile(pwd, path);
    if (exist(full_path, 'dir') == 0)
        error('Path does not exist');
    end
    file_path = full_path;
    file_list = dir(full_path);
    file_list_size = numel(file_list);
    for i = 1:file_list_size
        [~, filename, ext] = fileparts(file_list(i).name);
        if (strcmp(ext, extension) || strcmp(ext, extension))
            if (strcmp(filename, 'noreflection'))
                ref = file_list(i);
            else
                files = [files, file_list(i)];
            end
        end
    end
end