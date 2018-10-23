# Simple Run File
import sys
import os.path

#sys.path.append(#)

from Utilities.Simulation import run

config = {
    "dry_mass": 4,
    "mass_water": 18,
    "propellant_pressure": 5500000,
    "propellant_volume": 4,
    "target_height": 2,
    "pipe_height": 0.3,
    "nozzle_diam": 0.01
}

run(config)
