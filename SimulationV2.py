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
mass_tot_new = mass_tot

height = 0
velocity = 0
ALL_HELL_HAS_BROKE_LOSE = False

gravity = -9.81
rho_water = 997

pressure = 500000  # Original pressure of pressurant [Pa] 0.5 MPa
#volume_gas_orig = 3  # volume of pressurant [m^3]
target_height = 2  # mission profile height [m]
pipe_height = .5  # difference in height between nozzle and pressure tanks [m]

nozzle_diam = 0.01  # [m]
nozzle_area = Calculator.nozzle_area(nozzle_diam)

###### Simulation Timing ######
t_plus = 0
dt_simulation = 0.01
dt_physical = 0.01
mission_end_time = 60
timermode2 = 0

graph = Grapher()
sys = System()
PID = PIDController(1, 0, 0, dt_simulation)

# Velocity from ascent PDR
# add up V(dt) over dt getting height
# calculate potential height from velocity
# find when potential height = target height
# find time for slow down to zero velocity (using gravity kinematics)
# hover mode

mode = 1

#potential_height = 0

while t_plus <= mission_end_time:
    # Mode 1    = goto and maintain 2 meters    (target = 2m)
    # Mode 2  = start 10 second timer         (target = 2m)
    # Mode 3    = go back to ground             (target = 0m)

    if height >=2:
        mode = 2
        #target_velocity = 0 #?
        
    if mode == 2:
        timermode2 += dt_simulation
        if timermode2 >= 10: #time to land
            target_height = 0
            mode = 3 #more of a debugger statement for now
            
            
    height_cv = PID.get_cv(target_height, height) # target height - height
    #height_cv = target_height - height

    ue = sqrt(2 * (pressure / rho_water + gravity * pipe_height))
    m_dot_max = Calculator.m_dot(nozzle_area, ue)

    potential_height = (0.5*((velocity**2)/abs(gravity))) + height
    print(height)

    if (potential_height <= target_height):
        target_velocity = sqrt(9.81 * (target_height - height))
    else:
        target_velocity = 0

    # delta-v = 2 delta-h / delta-t^2
    # delta-h = height-cv - velocity * delta-t

    tuning_time = 3

    target_dv = 2 * (height_cv - velocity * tuning_time) / (tuning_time ** 2)
    target_d_mass = mass_tot * exp((gravity * dt_simulation / ue) - (target_dv / ue))
    m_dot_target = (mass_tot - target_d_mass) / dt_simulation

    # PWM, PID
    if Calculator.modulus(t_plus, dt_physical) == 0:
        duty_cycle = (m_dot_target / m_dot_max)
        if duty_cycle < 0:
            duty_cycle = 0
        if duty_cycle > 1:
            duty_cycle = 1

    if mass_water <= 0:
        ALL_HELL_HAS_BROKE_LOSE = True

        m_dot_max = 0  # oh shit, I'm about to fucking fall
        mass_water = 0
    if ALL_HELL_HAS_BROKE_LOSE:
        m_dot_max = 0

    m_dot = duty_cycle * m_dot_max

    mass_tot_new -= m_dot * dt_simulation
    mass_water -= m_dot * dt_simulation

    dv = gravity * dt_simulation + ue * log(mass_tot / mass_tot_new)
    mass_water -= m_dot * dt_simulation

    mass_tot = mass_tot_new
    velocity += dv
    height += velocity * dt_simulation

    if height < 0:
        height = 0  # yes, the ground surprisingly exists and no it is not a sink hole
        #height_flag = True
        velocity = 0

    #potential_height = height + (velocity + dv)*dt_simulation

    t_plus += dt_simulation
    graph.record("height", height, t_plus, "Height", only_positive=True)
    graph.record("velocity", velocity, t_plus, "Velocity", show_y_axis=True)
    graph.record("duty_cycle", duty_cycle, t_plus, "Duty Cycle")
    graph.record("mass_water", mass_water, t_plus, "Mass of Water")
    graph.record("dv", dv, t_plus, "dv")
    graph.record("potentail height", potential_height, t_plus, "potential height")

graph.show_plots()