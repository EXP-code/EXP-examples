# N-body simulation example

A more complex example of a disk and halo simulation using higher
resolution adaptive bases more typical of a real Nbody simulation.
The cylindrical tables will take much longer to compute but provide
better dynamical fidelity.  The cache file can be reused for new runs
with the same Cylinder parameters.

## How to run

First, change the ldlibdir parameter to point at your library install
directory.  Then, execute the command:

    mpirun -np 6 exp -f config.yml

or

    mpirun -np 6 exp

assuming that you have a machine with 6 cores.  Note: `config.yml` is
the default name.  You only need `-f file` for alternate file names.

## A few details

The EJ* parameters in halo.conf and disk.conf instruct the Component
class to adjust the expansion center to follow the gravitational
potential minumum.  Use the web page documentation for additional
details on these parameters.

EXP will look for basis-function cache file when it creates the
cylindrical basis class.  This cache file contains a pre-made set of
disk basis functions.  The EOF cache file is not provided because it
is too big for GitHub.  EXP will make the basis and save it as cache
file on the fly if a cache file is found.  It will be read from the
`outdir` directory.  If you'd like to have a different outdir from
this current working dir, please move the .eof.cache.run0 to your
`outdir`.

Alternatively, you can premake the cache file using pyEXP as follows:

    mpirun python3 make_cyl_basis.py

The disk basis in takes some time to compute, so a precomputed basis is 
supplied.  However, you can delete the eof cache and build it again for
testing.

## Prerun example

The directory `data` contains some snapshots and coefficients for use
with the pyEXP tutorials.
