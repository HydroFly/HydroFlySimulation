from Utilities.Simulation import run
import numpy as np
import matplotlib.pyplot as plt

dry_weights = np.arange(0.1, 10, 0.1)
x = []
y = []
for weight in dry_weights:
    t = run({"dry_mass": 0.1})
    y.append(t["time_of_flight"])
    x.append(weight)
plt.plot(x, y)
plt.ylabel('Time-of-flight, seconds')
plt.xlabel('Dry Mass, kg')
plt.title('Time-of-Flight vs Dry Mass')
plt.show()
