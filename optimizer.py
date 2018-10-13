from SimulationV2 import run, graph
import numpy as np
import matplotlib.pyplot as plt


def do_weight_vary():
    dry_weights = np.arange(0.1,20,0.1)
    x=[]
    y=[]
    for weight in dry_weights:
        t=run(weight)
        y.append(t)
        x.append(weight)
    plt.plot(x,y)
    plt.ylabel('Time-of-flight, seconds')
    plt.xlabel('Dry Mass, kg')
    plt.show()