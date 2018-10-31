# Simple Run File
import sys
import os.path

from Utilities.Simulationv4 import run

config = {
    "dry_mass": 4, # kg 
    "mass_water": 6, # kg 
    "propellant_pressure": 5000000, # Pa
    "target_height": 2, # m
    "pipe_height": 0.3, # m 
    "nozzle_diam": 0.01 # m
}

run(config, True)
