# Binary star example

A simple simulation of a binary star system, to exercise the code and give some experience with the file formats. The example takes two stars and evolves them under direct interaction. The initial conditions for the stars are specified in `binary.bods`, which follows standard `EXP` input format: the first line is the number of bodies (followed by two integers that specify the number of extra integer and double fields -- here set to be zero). Lines after the first line specify, for each body, the mass, xyz position, and xyz velocity.

## How to run

Run as follows.  The YAML configuration file is set for the Docker container. If you are using a native build and installation, change the ldlibdir parameter to point at your library install directory.  Then, execute the command: `mpirun -np 1 exp binary.yml`.

## A fixed potential example

There is also an example where the stars no longer feel mutual self-gravity, but instead are evolved in an external logarithmic potential. This may be run using `mpirun -np 1 exp logpot.yml`. This example demonstrates `noforce`.

## Viewing results

Each example creates a trajectory file names `ORBTRACE.runX` where `X`
is either `1` or `2`, for `binary.yml` or `logpot.yml`
respectively. These may be plotted using the command:

``` bash
python3 plotOrbit.py --input=ORBTRACE.runX
```

## Additional exploration

A first exercise to extend these examples would be to instead use the `usermw` module to simulate the orbit of the sun in the MW.
