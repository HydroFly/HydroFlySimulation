from Utilities.Simulationv4 import run
import numpy as np
import matplotlib.pyplot as plt



dry_weights = np.arange(0.1, 10, 0.1) # small, large, step
x = []
y = []


config = {
    "dry_mass": 4, # kg 
    "mass_water": 6, # kg 
    "propellant_pressure": 5000000, # Pa
    "target_height": 2, # m
    "pipe_height": 0.3, # m 
    "nozzle_diam": 0.01 # m
}

for weight in dry_weights:
    config["dry_mass"] = weight
    t = run(config, False)
    y.append(t["time_of_flight"])
    x.append(weight)
plt.plot(x, y)
plt.ylabel('Time-of-flight, seconds')
plt.xlabel('Dry Mass, kg')
plt.title('Time-of-Flight vs Dry Mass')
plt.show()
