A trivial example of a disk and halo simulation using low-fidelity
adaptive bases.  This will test your build and provide a starting
point of exploring parameters.  The configuration in the ../Better
directory will build a higher resolution, more accurate basis.  The
basis has low resolution and does not take long to compute, so I'm not
supplying a precomputed basis.  The basis in 'Better' takes some time
to compute, so a precomputed basis is supplied.  However, you can
always delete the eof cache and build it again.

Run as follows.  First, change the ldlibdir parameter to point at your
library install directory.  Then, execute the command:

`mpirun -np 6 exp -f config.yml`

assuming that you have a machine with 6 cores.  Since config.yml is
the default, you simply execute the simpler command:

`mpirun -np 6 exp`