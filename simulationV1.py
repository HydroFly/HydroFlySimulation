# HydroFly Master Simulation
# Version 1.3
# Adam Bennabou, Thomas Slusser, Russell Weas

from Grapher import Grapher
from Calculator import Calculator
from System import System
from PID_Controller import PIDController

from numpy import *

############ Assumptions ###########
mass_water = 18  # mass of water [kg]
mass_dry = 0  # dry mass including stuctures and electronics... will update later
mass_tot = mass_water + mass_dry

gravity = -9.81
rho_water = 997

height = 0
velocity = 0

pressure = 500000  # Original pressure of pressurant [Pa] 0.5 MPa
volume_gas_orig = 3  # volume of pressurant [m^3]
target_height = 3  # mission profile height [m]
pipe_height = .5  # difference in height between nozzle and pressure tanks [m]

nozzle_diam = 0.01  # [m]
nozzle_area = Calculator.nozzle_area(nozzle_diam)

###### Simulation Timing ######
t_plus = 0
dt_simulation = 0.001
dt_physical = 0.02
mission_end_time = 60

graph = Grapher()
sys = System()
PID = PIDController(1, 0, 0, dt_physical)

while t_plus <= mission_end_time:
    # Mode 1    = goto and maintain 2 meters    (target = 2m)
    # Mode 1.5  = start 10 second timer         (target = 2m)
    # Mode 2    = go back to ground             (target = 0m)

    target_height = 2
    height_cv = PID.get_cv(target_height, height)
    ue = sqrt(2 * (pressure / rho_water + gravity * pipe_height))

    delta_height = target_height - height
    potential_height = Calculator.potential_height(mass_tot, height, velocity)

    if potential_height >= target_height or height > target_height:
        target_velocity = 0
    else:
        target_velocity = Calculator.delta_v_required(delta_height)
        # duty_cycle = 1

    m_dot_max = Calculator.m_dot(nozzle_area, ue)
    if mass_water <= 0:
        m_dot_max = 0  # oh shit, I'm about to fucking fall

    target_dv = PID.get_cv(target_velocity, velocity)

    target_d_mass = Calculator.target_d_mass(mass_tot, ue, target_dv, dt_simulation)
    m_dot_target = mass_tot / target_d_mass / dt_simulation

    duty_cycle = Calculator.duty_cycle(m_dot_target, m_dot_max)

    # PWM, PID
    if Calculator.modulus(t_plus, dt_physical) == 0:
        m_dot = duty_cycle * m_dot_max

    if height < 0:
        height = 0  # yes, the ground surprisingly exists and no it is not a sink hole
        velocity = 0

    mass_tot_new = mass_tot - m_dot * dt_simulation
    mass_water -= m_dot * dt_simulation

    dv = gravity * dt_simulation + ue * log(mass_tot / mass_tot_new)
    mass_tot = mass_tot_new
    velocity += dv
    height += velocity * dt_simulation

    t_plus += dt_simulation
    graph.record("height", height, t_plus, "Height", only_positive=True)
    graph.record("velocity", velocity, t_plus, "Velocity", show_y_axis=True)
    graph.record("duty_cycle", duty_cycle, t_plus, "Duty Cycle")
    graph.record("mass_water", mass_water, t_plus, "Mass of Water")

graph.show_plots()