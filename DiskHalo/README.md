# A trivial example of a disk and halo simulation 

This will test your build and provide a starting point of exploring 
parameters.  The bases configured here have low resolution and quick to 
compute, so we are not supplying a precomputed basis.  The configuration 
in the `../Nbody` directory will build a higher resolution, more accurate 
basis more typical of a real simulation.

## How to run

First, change the ldlibdir parameter to point at your
library install directory.  Then, execute the command:

    mpirun -np 6 exp -f config.yml

assuming that you have a machine with 6 cores.  Since config.yml is
the default, you simply execute the simpler command:

    mpirun -np 6 exp
