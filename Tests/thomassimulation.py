# Simple Run File
import sys
import os.path

#sys.path.append(#)

from Utilities.SimulationT import run

config = {
    "dry_mass": 6,
    "mass_water": 18,
    "propellant_pressure": 2*10e5, 
    "target_height": 2,
    "pipe_height": 0.3,
    "nozzle_diam": 0.01
}

run(config)
