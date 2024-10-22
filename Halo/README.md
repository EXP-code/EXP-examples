# A simple spherical halo example

This is a simple example of using an adaptive spherical basis,
sphereSL.  The model only has one component, a spherical halo.

The target halo model is specified here in the ascii file
SLGridSph.model.  The basis parameters are in the parameters node.
The basis will be computed and tabled on a grid from r in $[0.0001,
1.95]$ with $4000$ grid points.  The maximum spherical harmonic order
is $l=6$ and harmonic has 20 radial basis functions.  The radial
interval is scaled to the interval $[-1, 1]$ with a scale factor
r_s=0.0667 using the scaling function

$$ x=(r/r_s - 1)/(r/r_s + 1). $$

Therefore, $r_s$ should be chosen to be roughly the scale parameter of
the model.  The parameter self_consistent tells the code to recompute
the basis at every step.  If false, the gravitational field is fixed
after the first evaluation.  Use the web page documentation for
additional details on these parameters.

## Run instructions

First, change the ldlibdir parameter to point at your
library install directory.  Then, execute the command:

    mpirun -np 6 exp -f config.yml

or

    mpirun -np 6 exp

assuming that you have a machine with 6 cores.  Note: `config.yml` is
the default name.  You only need `-f file` for alternate file names.

## Bonus run

There is a second test config file in this directory: `fixed.yml`.
This one runs the component in a fixed potential using the `userhalo`
external potential.