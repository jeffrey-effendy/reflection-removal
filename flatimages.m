function [M] = flatimages(url, files)
    files_size = numel(files);
    if (files_size == 0)
        error('There is no files specified');
    end
    for i = 1:files_size
        [~, ~, file_ext] = fileparts(files(i).name);
        if (~strcmp(file_ext, '.png') && ~strcmp(file_ext, '.jpg'))
            error('Only png and jpg are supported');
        end
        file_wdir = fullfile(url, files(i).name);
        img = imread(file_wdir);
        if (i == 1)
            M = zeros(files_size, size(img,1) * size(img,2) * size(img,3));
        end
        M(i,:) = reshape(img, 1, numel(img));
    end    
end

