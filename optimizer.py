from SimulationV2 import run, graph
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as matplotlib


def do_weight_vary():
    dry_weights = np.arange(0.1,10,0.1)
    x=[]
    y=[]
    for weight in dry_weights:
        t=run(mass_dry=weight)
        y.append(t)
        x.append(weight)
    plt.plot(x,y)
    plt.ylabel('Time-of-flight, seconds')
    plt.xlabel('Dry Mass, kg')
    plt.title('Time-of-Flight vs Dry Mass')
    plt.show()

def do_pressure_vary():
    # tank_pressures = np.logspace(5*10**5, 5*10**6)
    tank_pressures = np.arange(5*10**5, 10*10**6, 1*10**4)
    x=[]
    y=[]
    for pressure in tank_pressures:
        t=run(pressure=pressure)
        y.append(t)
        x.append(pressure)
    plt.plot(x,y)
    plt.ylabel('Time-of-flight, seconds')
    plt.xlabel('Pressure, Pa')
    plt.title('Time-of-Flight vs Pressure')
    plt.ticklabel_format(axis='x', style='sci', scilimits=(-2,2))
    plt.show()


# do_weight_vary()
do_pressure_vary()