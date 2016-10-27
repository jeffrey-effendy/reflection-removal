# Running the RPCA

Script below is a MATLAB script:
- [path, files, ref] = filewalk('data/01-lowres')
- D = flatimages(path, files)
- [A, ~] = pcra(D)

A is the low-rank matrix approximating the background layer.
Take the first row and reshape it to (r, c, 3), where r is the pixel height and y is the pixel width 