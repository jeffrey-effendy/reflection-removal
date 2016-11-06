[path, files, ref] = filewalk('data/02-highres', '.png');

[D, r, c] = flatimages(path, files);

ref_arr = imread(fullfile(path, ref.name));
flat_ref = reshape(ref_arr, 1, numel(ref_arr));

[A, ~] = rpca(D);

out = A(1,:);
curr_sum = sum(abs(uint8(A(1,:)) - flat_ref));

for i = 2:size(A,1)
    if (sum(abs(uint8(A(i,:)) - flat_ref)) < curr_sum)
        out = A(i,:);
        curr_sum = sum(abs(uint8(A(i,:)) - flat_ref));
    end
end

unflattened_out = reshape(out, r, c, 3);

imwrite(uint8(unflattened_out), 'out.png');