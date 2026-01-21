#!/usr/bin/env python3
"""
expunits.py

General unit-scale calculator & optional particle-file converter.

Core relation (general):
    G_new = G_old * s_M / (s_L * s_V^2)
so
    s_M = s_L * s_V^2 * G_new / G_old
    s_V = sqrt( s_M * G_old / (s_L * G_new) )
    s_L = s_M * G_old / (s_V^2 * G_new)

Command-line usage notes:
- Provide old/new unit definitions in *the same physical units* (e.g. both
  lengths in kpc, both masses in Msun).

  For example: --old-length 1 --new-length 300  (means old length unit = 1 kpc,
  new length unit = 300 kpc)

- You must supply enough information to determine the three scale factors:
    Provide any two of (s_L, s_V, s_M) by giving the corresponding
    old/new pairs.

    Example ways to provide two:
      * old-length & new-length  AND old-velocity & new-velocity
      * old-length & new-length  AND old-mass & new-mass
      * old-velocity & new-velocity AND old-mass & new-mass

    Optionally, instead of giving two pairs, use the circular-velocity preset
    mode (see README below).

- G_old and G_new are numeric gravitational constants in the old/new numeric unit systems respectively.
  For typical conversions to G_new = 1 set --G_new 1.0 (default).

- Optional: --infile/--outfile to convert a 7-column particle file with columns: m x y z u v w

- Optional: --precision N prints s_* with N decimal digits; --sci prints scientific notation.

Presets:
  --preset gadget   : old_length=1 (kpc), old_mass=1e10 (Msun), G_old=43007.1
  --preset bonsai   : old_length=1 (kpc), old_mass=1.0 (Msun),  G_old=4.5e-06

Examples:

  # Using gadget preset and target new units (L_new = 300 kpc, M_new = 1e12 Msun, want G_new=1)
  python expunits.py --preset gadget --new-length 300 --new-mass 1e12 --G_new 1 --print-scales

  # Provide explicit old/new units (length in kpc, mass in Msun, velocity in km/s):
  python expunits.py --old-length 1 --new-length 300 --old-mass 1 --new-mass 1e12 --G_old 4.5e-06 --G_new 1 --print-scales

  # Convert a particle file (7 cols) using the scales computed above:
  python expunits.py --preset bonsai --new-length 300 --new-mass 1e12 --G_new 1 --infile particles.txt --outfile particles_g1.txt


Notes and guidance:

- Units must be given in the same physical system for old/new comparisons.

  Example:
  * If you treat lengths in kpc, give both --old-length and --new-length in kpc.

  * If you use Msun for mass give both --old-mass and --new-mass in Msun.

- If you use a preset (--preset gadget or --preset bonsai) the preset sets
  old-length, old-mass, and G_old unless you override them on the command line.

- The script is defensive:

  * You must supply at least two old/new pairs (so the third scale can be
    calculated from the G relation)

  * Or supply all three and they must be consistent with the requested G_new.

- For conversions to the usual G_new = 1 choose --G_new 1.0 (default).

- The printed s_L, s_V, s_M are "old-unit-per-1-new-unit". To convert
  numeric particle values: r' = r_old / s_L, v' = v_old / s_V, m' = m_old / s_M

- The particle-file conversion expects 7 whitespace-separated columns per row:
  mass x y z u v w.

"""

import argparse
import sys
import numpy as np
import math

PRESETS = {
    'gadget': {
        'old_length': 1.0,         # kpc
        'old_mass': 1.0e10,        # Msun
        'G_old': 43007.1
    },
    'bonsai': {
        'old_length': 1.0,         # kpc
        'old_mass': 1.0,           # Msun
        'G_old': 4.5e-06
    }
}

def compute_scales(G_old, G_new, s_L, s_V, s_M):
    """
    Given G_old, G_new and any two of (s_L, s_V, s_M) compute the third.
    s_L, s_V, s_M are either floats or None.
    Returns (s_L, s_V, s_M). Raises ValueError if insufficient or inconsistent.
    """
    known = [(s_L is not None), (s_V is not None), (s_M is not None)]
    n_known = sum(known)

    # If all three provided, check consistency with G_old/G_new
    if n_known == 3:
        G_check = (s_L * s_V**2) / (G_old * s_M)
        if not math.isfinite(G_check):
            raise ValueError("Computed G_check is not finite.")
        if abs((G_check - G_new) / (abs(G_new) if G_new != 0 else 1.0)) > 1e-9:
            raise ValueError(f"Inconsistent scales: G_new requested {G_new} but scales give {G_check}.")
        return s_L, s_V, s_M

    if n_known < 2:
        raise ValueError("Insufficient inputs: need at least two of s_L, s_V, s_M (i.e., two old/new pairs).")

    # If s_L and s_V known -> s_M
    if s_L is not None and s_V is not None:
        s_M_calc = s_L * s_V**2 * G_new / G_old
        return s_L, s_V, s_M_calc

    # If s_L and s_M known -> s_V
    if s_L is not None and s_M is not None:
        denom = s_L * G_new / G_old
        if denom <= 0:
            raise ValueError("Non-positive denominator in s_V calculation.")
        s_V_calc = math.sqrt(s_M * G_old / (s_L * G_new))
        return s_L, s_V_calc, s_M

    # If s_V and s_M known -> s_L
    if s_V is not None and s_M is not None:
        denom = s_V**2 * G_new / G_old
        if denom <= 0:
            raise ValueError("Non-positive denominator in s_L calculation.")
        s_L_calc = s_M * G_old / (s_V**2 * G_new)
        return s_L_calc, s_V, s_M

    raise ValueError("Unhandled case in compute_scales.")

def parse_args():
    p = argparse.ArgumentParser(description="Compute unit-scale factors and optionally convert a 7-column particle file.")
    # presets
    p.add_argument("--preset", choices=PRESETS.keys(), help="Optional preset for old units (gadget, bonsai).")

    # old units (user-specified)
    p.add_argument("--old-length", type=float, default=None, help="Old length unit expressed in some physical length units (e.g. kpc).")
    p.add_argument("--old-mass", type=float, default=None, help="Old mass unit expressed in some physical mass units (e.g. Msun).")
    p.add_argument("--old-velocity", type=float, default=None, help="Old velocity unit expressed in some physical velocity units (e.g. km/s).")

    # new units (target)
    p.add_argument("--new-length", type=float, default=None, help="New length unit in same physical units as --old-length (e.g. 300 for 300 kpc).")
    p.add_argument("--new-mass", type=float, default=None, help="New mass unit in same physical units as --old-mass (e.g. 1e12 for 1e12 Msun).")
    p.add_argument("--new-velocity", type=float, default=None, help="New velocity unit in same physical units as --old-velocity (e.g. 1 for 1 km/s).")

    # numeric G values
    p.add_argument("--G_old", type=float, default=None, help="Numeric gravitational constant in OLD numeric units.")
    p.add_argument("--G_new", type=float, default=1.0, help="Numeric gravitational constant in NEW numeric units (default 1.0).")

    # files for conversion
    p.add_argument("--infile", type=str, default=None, help="Optional input particle file (7 columns: m x y z u v w).")
    p.add_argument("--outfile", type=str, default=None, help="If --infile given, write converted particles to this file.")

    # print options
    p.add_argument("--print-scales", action="store_true", help="Print computed scale factors.")
    p.add_argument("--precision", type=int, default=None, help="Number of decimal digits when printing scales (overrides --sci).")
    p.add_argument("--sci", action="store_true", help="Print scales in scientific notation (default formatting if --precision is not set).")
    p.add_argument("--fmt", type=str, default="%.6e %.6e %.6e %.6e %.6e %.6e %.6e", help="Output format string for converted particle file.")
    p.add_argument("--skiprows", type=int, default=0, help="Rows to skip when reading input particle file (e.g. header lines).")
    return p.parse_args()

def resolve_old_new_from_preset(args):
    # Fill args.old-length and args.old-mass and G_old from preset if present
    if args.preset:
        preset = PRESETS[args.preset]
        if args.old_length is None:
            args.old_length = preset['old_length']
        if args.old_mass is None:
            args.old_mass = preset['old_mass']
        if args.G_old is None:
            args.G_old = preset['G_old']

def compute_and_maybe_convert(args):
    # Resolve preset values
    resolve_old_new_from_preset(args)

    # Validate G_old provided
    if args.G_old is None:
        raise SystemExit("G_old must be specified either explicitly (--G_old) or via a preset (--preset).")

    # Compute simple scale candidates from provided old/new unit values
    s_L = None
    s_V = None
    s_M = None

    if args.old_length is not None and args.new_length is not None:
        if args.old_length == 0:
            raise SystemExit("old-length cannot be zero.")
        s_L = args.new_length / args.old_length

    if args.old_mass is not None and args.new_mass is not None:
        if args.old_mass == 0:
            raise SystemExit("old-mass cannot be zero.")
        s_M = args.new_mass / args.old_mass

    if args.old_velocity is not None and args.new_velocity is not None:
        if args.old_velocity == 0:
            raise SystemExit("old-velocity cannot be zero.")
        s_V = args.new_velocity / args.old_velocity

    # Compute missing scale(s)
    try:
        s_L, s_V, s_M = compute_scales(args.G_old, args.G_new, s_L, s_V, s_M)
    except ValueError as e:
        raise SystemExit("Error computing scales: " + str(e))

    # Optionally print scales
    if args.print_scales:
        if args.precision is not None:
            fmt = "{:." + str(args.precision) + "f}"
            print("s_L =", fmt.format(s_L))
            print("s_V =", fmt.format(s_V))
            print("s_M =", fmt.format(s_M))
        elif args.sci:
            print("s_L = {:.6e}".format(s_L))
            print("s_V = {:.6e}".format(s_V))
            print("s_M = {:.6e}".format(s_M))
        else:
            print("s_L =", s_L)
            print("s_V =", s_V)
            print("s_M =", s_M)

        # Print check of G_new
        G_new_check = (s_L * s_V**2) / (s_M * args.G_old)
        print("Check: G_new = (s_L s_V^2) / (G_old * s_M) = {:.12g} (requested G_new = {})".format(G_new_check, args.G_new))

    # If infile specified, convert and write
    if args.infile:
        if not args.outfile:
            raise SystemExit("When --infile is provided you must supply --outfile.")
        try:
            data = np.loadtxt(args.infile, comments="#", skiprows=args.skiprows)
        except Exception as e:
            raise SystemExit("Failed reading infile: " + str(e))

        if data.ndim == 1:
            if data.size == 7:
                data = data.reshape((1,7))
            else:
                raise SystemExit("Input file doesn't have 7 columns per row.")

        if data.shape[1] != 7:
            raise SystemExit("Input file must have 7 columns (m x y z u v w). Found {}".format(data.shape[1]))

        out = np.empty_like(data, dtype=float)
        out[:,0] = data[:,0] / s_M           # mass
        out[:,1:4] = data[:,1:4] / s_L       # positions
        out[:,4:7] = data[:,4:7] / s_V       # velocities

        try:
            np.savetxt(args.outfile, out, fmt=args.fmt)
        except Exception as e:
            raise SystemExit("Failed writing outfile: " + str(e))

        print("Converted {} -> {} using s_L={:.6g}, s_V={:.6g}, s_M={:.6g}".format(args.infile, args.outfile, s_L, s_V, s_M))

    return s_L, s_V, s_M

def main():
    args = parse_args()
    try:
        s_L, s_V, s_M = compute_and_maybe_convert(args)
    except SystemExit as e:
        # argparse or compute_and_maybe_convert can call SystemExit for user errors
        print(e, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
    
