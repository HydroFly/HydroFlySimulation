# -*- coding: utf-8 -*-
# Simulation V1.0
# HydroFly Master Simulation File
# Adam Benabbou, Thomas Slusser, Russell Weas
# Last Updated 3 October 2018

# uses underscore_notation for variables
import numpy as np

from Grapher import Grapher
from Calculator import Calculator
from Constants import Constants
from FlightController import FlightController
from HardwareInterfaceDummy import HardwareInterfaceDummy

calc = Calculator()
graph = Grapher()
sys = HardwareInterfaceDummy()
fc = FlightController(sys)


############ INPUTS ###########
mass_water = 18     # mass of water [kg]
mass_structure = 2  # mass of structure [kg]
mass_controls = 1   # mass of control system [kg]
mass_tot = mass_water + mass_structure + mass_controls

pressure_original = 5000000  # Original pressure of pressurant [Pa] 0.5 MPa
volume_gas_orig = 3  # volume of pressurant [m^3]
target_height = 3    # mission profile height [m]
pipe_height = .5     # difference in height between nozzle and pressure tanks [m]

nozzle_diam = 0.01  # [m]

while sys.get_t_plus() <= 300:
    fc.do_execution_cycle()

    m_dot = fc.duty_cycle * fc.m_dot_max
    new_vehicle_mass = fc.mass_total - m_dot * sys.get_delta_time()
    fc.mass_water -= m_dot * sys.get_delta_time()

    fc.propellant_volume += m_dot / Constants.rho_water * sys.get_delta_time()
    fc.pressure *= volume_gas_orig / fc.propellant_volume

    fc.velocity += fc.ue * np.log(fc.mass_total / new_vehicle_mass) + Constants.gravity * sys.get_delta_time()
    fc.height += fc.velocity * sys.get_delta_time()

    # Test Exceptions
    if fc.mass_water <= 0:
        fc.mass_water = 0
        self.fc.dv = 0
        raise Exception('out of water')

    if fc.height <= 0:
        fc.height = 0
        fc.velocity = 0

    sys.next_cycle()

    # Collect data
    graph.record("height", height, sim.get_time(), "Height", only_positive=True)
    graph.record("velocity", velocity, sim.get_time(), "Velocity", show_y_axis=True)
    graph.record("target_velocity", target_velocity, sim.get_time(), "Target Vel")
    graph.record("duty_cycle", duty_cycle, sim.get_time(), "Duty Cycle")
    graph.record("mass_water", mass_water, sim.get_time(), "Mass of Water")
    graph.record("mass total", mass_tot, sim.get_time(), "Mass total")

# Plot data
graph.show_plots()
