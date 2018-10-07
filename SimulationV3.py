# HydroFly Master Simulation
# Version 1.3
# Adam Benabbou, Thomas Slusser, Russell Weas

from Grapher import Grapher
from Calculator import Calculator
from System import System
from FlightController import FlightController
from PID_Controller import PIDController

from numpy import *
import numpy as np

############ Assumptions ###########
mass_water = 10  # mass of water [kg]
mass_dry = 0.2  # dry mass including stuctures and electronics... will update later
mass_tot = mass_water + mass_dry
mass_tot_new = mass_tot

height = 0
velocity = 0
ALL_HELL_HAS_BROKE_LOSE = False
ALL_HELL_2 = False

gravity = -9.81
rho_water = 997

pressure = 500000  # Original pressure of pressurant [Pa] 0.5 MPa
# volume_gas_orig = 3  # volume of pressurant [m^3]
target_height = 2.1  # mission profile height [m]
pipe_height = .5  # difference in height between nozzle and pressure tanks [m]

nozzle_diam = 0.01  # [m]
nozzle_area = Calculator.nozzle_area(nozzle_diam)

###### Simulation Timing ######
t_plus = 0
dt_simulation = 0.01
dt_physical = 0.1
mission_end_time = 120

graph = Grapher()
sys = System()
fc = FlightController(sys)
PID = PIDController(1, 0, 0, dt_simulation)

# Velocity from ascent PDR
# add up V(dt) over dt getting height
# calculate potential height from velocity
# find when potential height = target height
# find time for slow down to zero velocity (using gravity kinematics)
# hover mode

sys.ue = sqrt(2 * (pressure / rho_water + gravity * pipe_height))
sys.m_dot_max = Calculator.m_dot(nozzle_area, sys.ue)

# potential_height = 0

while sys.t_plus <= mission_end_time:
    # Mode 1    = goto and maintain 2 meters    (target = 2m)
    # Mode 2  = start 10 second timer         (target = 2m)
    # Mode 3    = go back to ground             (target = 0m)

    duty_cycle = fc.update_cycle()

    # MODE-INDEPENDENT CALC
    if sys.mass_water <= 0:
        ALL_HELL_HAS_BROKE_LOSE = True
        sys.m_dot_max = 0

    if ALL_HELL_HAS_BROKE_LOSE:
        sys.m_dot_max = 0

        if ALL_HELL_2 == False:
            mission_end_time = sys.t_plus + 10
            sys.ALL_HELL_2 = True

    m_dot = duty_cycle * sys.m_dot_max
    mass_tot_new -= m_dot * dt_simulation
    sys.mass_water -= m_dot * dt_simulation

    dv = gravity * dt_simulation + (sys.ue * log(sys.mass_tot / mass_tot_new))  # if mass_tot = mass_tot_new, only gravity effects apply
    sys.mass_tot = mass_tot_new
    sys.velocity += dv
    sys.height += sys.velocity * dt_simulation

    if sys.height < 0:
        sys.height = 0  # yes, the ground surprisingly exists and no it is not a sink hole
        sys.velocity = 0

    sys.t_plus += dt_simulation
    graph.record("height", sys.height, sys.t_plus, "Height", only_positive=True)
    graph.record("velocity", sys.velocity, sys.t_plus, "Velocity", show_y_axis=True)
    graph.record("duty_cycle", duty_cycle, sys.t_plus, "Duty Cycle")
    graph.record("mass_water", sys.mass_water, sys.t_plus, "Mass of Water")
    graph.record("dv", dv, sys.t_plus, "dv")

graph.show_plots()