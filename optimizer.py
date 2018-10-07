from SimulationV2 import run, graph
import numpy as np
import matplotlib.pyplot as plt
dry_weights = np.arange(0.1,2,.1)

# for weight in dry_weights:
#     plt.figure('dry mass = ' + str(weight) + 'kg')
#     run(weight)
#     graph.show_plots()
#     graph.clean_data()

run(10)
graph.show_plots()
