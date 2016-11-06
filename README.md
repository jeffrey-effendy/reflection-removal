# Running the RPCA

Script below is a MATLAB script:
- [path, files, ref] = filewalk('data/01-lowres', '.png')
- [D, r, c] = flatimages(path, files)
- [A, E] = rpca(D)

A is the low-rank matrix approximating the background layer.
Take the first row and reshape it to (r, c, 3), where r is the pixel height and c is the pixel width 