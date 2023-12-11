# Cube example

The directory contains everything you need to run a cube simulation
The current body file is named `cube.bods` and has 10,000 bodies.

You can generate new initial conditions using the `cubeics` command
line tool.  For example, this command will generate a body file with
100,000 particles: `cubeics -o cube.bods -N 100000`.  See `cubeics
--help` for details.

