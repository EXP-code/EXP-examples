A simple simulation of a binary star system, to exercise the code and give some experience with the file formats. The example takes two stars and evolves them under direct interaction. The initial conditions for the stars are specified in `binary.bods`, which follows standard `EXP` input format: the first line is the number of bodies (followed by two integers that specify the number of extra integer and double fields -- here set to be zero). Lines after the first line specify, for each body, the mass, xyz position, and xyz velocity.

Run as follows.  First, change the ldlibdir parameter to point at your library install directory.  Then, execute the command: `mpirun -np 1 exp binary.yml`.

There is also an example where the stars no longer feel mutual self-gravity, but instead are evolved in an external logarithmic potential. This may be run using `mpirun -np 1 exp binary.yml`. This example demonstrates `noforce`.

A first exercise to extend these examples would be to instead use the `usermw` module to simulate the orbit of the sun in the MW.
