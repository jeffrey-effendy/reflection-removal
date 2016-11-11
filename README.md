# Reflection Removal

**Python**

Assuming your machine is a LINUX/UNIX machine with python installed,
- To run averaging, simply run `runAveragingTest.sh` or `runAveragingAll.sh`
- To run RPCA, simply run `runRpcaTest.sh`  

The main python file is `removal.py`, with all the arguments and definition in the file.
Look at the shell scripts mentioned above to see the available arguments and settings.

**MATLAB**

Only for RPCA.

Script below is a MATLAB script:
- [path, files, ref] = filewalk('data/01-lowres', '.png')
- [D, r, c] = flatimages(path, files)
- [A, E] = rpca(D)

A is the low-rank matrix approximating the background layer.
Take the first row and reshape it to (r, c, 3), where r is the pixel height and c is the pixel width 