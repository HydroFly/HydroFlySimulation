from Utilities.Simulation import run
import numpy as np
import matplotlib.pyplot as plt

tank_pressures = np.arange(5 * 10 ** 5, 10 * 10 ** 6, 1 * 10 ** 4)
x = []
y = []

for pressure in tank_pressures:
    t = run({"propellant_pressure": pressure})
    y.append(t['time_of_flight'])
    x.append(pressure)

plt.plot(x, y)
plt.ylabel('Time-of-flight, seconds')
plt.xlabel('Pressure, Pa')
plt.title('Time-of-Flight vs Pressure')
plt.ticklabel_format(axis='x', style='sci', scilimits=(-2, 2))
plt.show()
