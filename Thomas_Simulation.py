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

gravity = -9.81
rho_water = 997

pressure = 500000  # Original pressure of pressurant [Pa] 0.5 MPa
volume_gas_orig = 3  # volume of pressurant [m^3]
target_height = 2  # mission profile height [m]
pipe_height = .5  # difference in height between nozzle and pressure tanks [m]

nozzle_diam = 0.01  # [m]
nozzle_area = Calculator.nozzle_area(nozzle_diam)

###### Simulation Timing ######
t_plus = 0
dt_simulation = 0.01
mission_end_time = 10

graph = Grapher()
sys = System()


# Velocity from ascent PDR
# add up V(dt) over dt getting height
# calculate potential height from velocity 
# find when potential height = target height
# find time for slow down to zero velocity (using gravity kinematics)
# hover mode

#ascent 
velocity = (gravity*dt) + ue*log(mass_tot/(mass_tot - (m_dot())))

while t_plus <= mission_end_time:
    # Mode 1    = goto and maintain 2 meters    (target = 2m)
    # Mode 1.5  = start 10 second timer         (target = 2m)
    # Mode 2    = go back to ground             (target = 0m)

    height_cv = PID.get_cv(target_height, height)
    ue = sqrt(2 * (pressure / rho_water + gravity * pipe_height))
    m_dot_max = Calculator.m_dot(nozzle_area, ue)

 #blocks of commented code #fml


    # potential_height = height 0.5 * mass_tot * velocity ** 2

    # if potential_height >= target_height or height > target_height: #substitute with PID
    #     target_velocity = 0
    # else:
    # target_velocity = Calculator.delta_v_required(height_cv)
    ##target_velocity = sqrt(abs(2 * 9.81 * height_cv))

    # duty_cycle = 1

    # target_dv = (target_velocity - velocity)/dt_simulation #PID.get_cv(target_velocity, velocity)

    # dv = gravity * dt_simulation + ue * log(mass_tot / (mass_tot - m_dot_max*dt_simulation))
    # if target_dv > dv:
    #     target_dv = dv

    height_cv = PID.get_cv(target_height, height)
    if height >=0:
        target_velocity=0
    
    if(potential_height <= target_height):
        target_velocity = sqrt(g * (target_height - height))
    else:
        target_velocity = 0 
        
   
    # delta-v = 2 delta-h / delta-t^2 
    # delta-h = height-cv - velocity * delta-t


    velocity_cv = Velocity_PID.get_cv(target_velocity, velocity)

    #target_dv = 2 * (height_cv - velocity * 3) / (3 ** 2)

    output_velocity = target_velocity - velocity

    target_d_mass = mass_tot * exp((gravity * dt_simulation / ue) - (velocity_cv / ue))
    m_dot_target = (mass_tot - target_d_mass) / dt_simulation


    #PWM, PID
    if Calculator.modulus(t_plus, dt_physical) == 0:
        duty_cycle = (m_dot_target / m_dot_max)
        if duty_cycle < 0:
            duty_cycle = 0
        if duty_cycle > 1:
            duty_cycle = 1

    if height < 0:
        height = 0  # yes, the ground surprisingly exists and no it is not a sink hole
        velocity = 0


    if mass_water <= 0:
        m_dot_max = 0  # oh shit, I'm about to fucking fall        

    m_dot = duty_cycle*m_dot_max

    mass_tot_new -= m_dot * dt_simulation
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
    graph.record("dv", dv, t_plus, "dv")
    graph.record("m_tot", mass_tot, t_plus, "mass total")

graph.show_plots()