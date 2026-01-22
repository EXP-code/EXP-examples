# EXP unit conversion for G=1

## Motivation

Many N-body simulation codes, including EXP, work most efficiently when the gravitational constant G is set to 1 in the simulation units. This directory provides tools and examples for converting physical data (e.g., in CGS or astronomical units) to a scaled unit system where G=1, which simplifies equations of motion and improves numerical stability.

We provide a brief derivation of phase-space conversion formulae to convert from an arbitrary set of custom units with a particular value of gravitational constant G to a new set of optionally scaled units with G=1.  We provide a Python script to compute unit-scale factors and optionally convert a 7-column (m, x, y, z, u, v, w) phase-space particle file.  We provide a simple example described below based on the Earth-Sun two-body system.

## This directory contains:

| File | Contents |
| ---  | ---      |
|earth_sun_cgs.txt | two-particle file (Sun + Earth) in CGS units |
|earth_sun_scaled.txt | expected converted file in scaled units (AU, M_sun, v'=1) |
| expunits.py | conversion script (compute scales + optional conversion) |
| expunits.tex | description of unit scaling formulae used in the script |
| expunits.pdf | PDF document produced by: 'pdflatex expunits.tex' |
|README.md | this file |

## Quick example

- The Python3 script requires numpy (e.g. pip install numpy)
- A Gadget example.  From this directory run:  ```python3 expunits.py --preset gadget --new-length 300 --new-mass 1e12 --G_new 1 --print-scales```  The result will be the set of scaling factors: ```s_L = 300.0 s_V = 119.73178358314053 s_M = 100.0``` that you would use to divide your Gadget input to get EXP input.  Note that time scale scaling is ```s_T = s_L/s_V = 2.51```, or one new system time unit is 1/2.51 Gyr
- To run the Earth-Sun example run: ```python3 expunits.py --old-length 1 --new-length 1.495978707e13 --old-mass 1 --new-mass 1.98847e33 --G_old 6.67430e-8 --G_new 1 --infile earth_sun_cgs.txt --outfile earth_sun_scaled_by_script.txt --print-scales --sci```.  See the details below for more explanation.

### Explanation of flags

- ```--old-length 1``` and ```--new-length 1.495978707e13```: Interpret old-length unit = 1 cm, new-length unit = 1 AU = 1.495978707e13 cm, so s_L = new_length / old_length = 1.495978707e13.
- ```--old-mass 1``` and ```--new-mass 1.98847e33```: Interpret old-mass unit = 1 g, new-mass unit = 1 M_sun = 1.98847e33 g, so s_M = 1.98847e33.
- ```--G_old 6.67430e-8``` is the cgs gravitational constant (cm^3 g^-1 s^-2).
- ```--G_new 1``` requests that numeric G in the new numeric units equals 1.
- The script computes ```s_V``` from the relation ```s_M = s_L * s_V^2 * (G_new/G_old)```. Thus ```V_new``` (the new velocity unit) is chosen so that ```v_earth_old / s_V = 1.0```.

## Expected checks

The script prints ```s_L, s_V, s_M```. 

	Expected approximate values: s_L ≈ 1.4959787e13 s_M ≈ 1.98847e33 s_V ≈ 2.978e6 (cm/s per one new velocity unit)

After conversion, earth_sun_scaled_by_script.txt should match
earth_sun_scaled.txt to within rounding:

	Sun: m' ≈ 1.0, r' ≈ 0.0, v' ≈ -3.00349e-6
	Earth: m' ≈ 3.00349e-6, r' ≈ 1.0, v' ≈ 1.0
