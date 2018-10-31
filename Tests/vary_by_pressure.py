from Utilities.Simulationv4 import run
import numpy as np
import matplotlib.pyplot as plt

tank_pressures = np.arange(5 * 10 ** 5, # small pressure value 
                            10 * 10 ** 6, # large pressure value 
                            1 * 10 ** 6) # increment, I think 
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



for pressure in tank_pressures:
    config["propellant_pressure"] = pressure
    t = run(config, False)
    y.append(t['time_of_flight'])
    x.append(pressure)

plt.plot(x, y)
plt.ylabel('Time-of-flight, seconds')
plt.xlabel('Pressure, Pa')
plt.title('Time-of-Flight vs Pressure')
plt.ticklabel_format(axis='x', style='sci', scilimits=(-2, 2))
plt.show()
