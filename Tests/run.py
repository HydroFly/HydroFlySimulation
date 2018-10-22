# Simple Run File

from Utilities.Simulation import run

config = {
    "dry_mass": 2,
    "mass_water": 20,
    "propellant_pressure": 500000,
    "propellant_volume": 3,
    "target_height": 2,
    "pipe_height": 0.5,
    "nozzle_diam": 0.005
}

run(config)
