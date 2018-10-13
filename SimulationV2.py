# HydroFly Master Simulation
# Version 1.3
# Adam Benabbou, Thomas Slusser, Russell Weas
import matplotlib

from Grapher import Grapher
from Calculator import Calculator
# from System import System
from PID_Controller import PIDController

import matplotlib.pyplot as plt
graph = Grapher()

from matplotlib import style
from numpy import *


def run(mass_dry):
    # plt.ion()
    flare = False
    style.use('bmh')
    # style.use('fivethirtyeight')
    # style.use('ggplot')
    height_flag = False
    ############ Assumptions ###########
    mass_water = 20  # mass of water [kg]
    # mass_dry = 0.2  # dry mass including stuctures and electronics... will update later
    mass_tot = mass_water + mass_dry
    mass_tot_new = mass_tot

    height = 0
    velocity = 0
    system_has_lost_propulsion = False
    timer_flag = False

    gravity = -9.81
    rho_water = 997

    pressure = 500000     # Original pressure of pressurant [Pa] 0.5 MPa
    # volume_gas_orig = 3  # volume of pressurant [m^3]
    target_height = 2  # mission profile height [m]
    pipe_height = .5  # difference in height between nozzle and pressure tanks [m]

    nozzle_diam = 0.01 /2 # [m]
    nozzle_area = Calculator.nozzle_area(nozzle_diam)

    ###### Simulation Timing ######
    t_plus = 0
    dt_simulation = 0.005
    dt_physical = 0.05
    mission_end_time = 200
    timermode2 = 0

    # sys = System()
    height_PID = PIDController(1, 0, 1, dt_simulation)
    velocity_PID = PIDController(1,1,1, dt_simulation) #@dt-physical = .3, then 0.3,0,0.5

    # Velocity from ascent PDR
    # add up V(dt) over dt getting height
    # calculate potential height from velocity
    # find when potential height = target height
    # find time for slow down to zero velocity (using gravity kinematics)
    # hover mode

    mode = 1
    ue = sqrt(2 * (pressure / rho_water + gravity * pipe_height))
    m_dot_max = Calculator.m_dot(nozzle_area, ue)

    # potential_height = 0

    while t_plus <= mission_end_time:
        # Mode 1    = goto and maintain 2 meters    (target = 2m)
        # Mode 2  = start 10 second timer         (target = 2m)
        # Mode 3    = go back to ground             (target = 0m)

        if height >= target_height and mode == 1:
            clock = t_plus
            mode = 2
            height_PID.integral = 0
            target_height = 2
            # graph.vlines.append(t_plus)
        if mode == 2:
            if t_plus - clock >= 10:
                target_height = 0
                # graph.vlines.append(t_plus)
                mode =3
                height_PID.clean()
                height_PID.KI = 5
                flare = False
        if mode == 3:
            velocity_cv = velocity_PID.get_cv(-0.5, velocity)
            target_dv = velocity_cv
        else:
            # # MODE-INDEPENDENT CALC
            height_cv = height_PID.get_cv(target_height, height)  # target height - height

            tuning_time = dt_simulation * 200

            target_dv = 2 * (height_cv - velocity * tuning_time) / (tuning_time ** 2) /4

        target_d_mass = mass_tot * exp((gravity * dt_simulation / ue) - (target_dv / ue))
        m_dot_target = (mass_tot - target_d_mass) / dt_simulation

        # PWM, PID
        if Calculator.modulus(t_plus, dt_physical) == 0:
            duty_cycle = (m_dot_target / m_dot_max)
            if duty_cycle < 0:
                duty_cycle = 0
            if duty_cycle > 1:
                duty_cycle = 1
        if mass_water <= 0 and system_has_lost_propulsion == False:
            system_has_lost_propulsion = True
            m_dot_max = 0
            graph.vlines.append(t_plus)

        if system_has_lost_propulsion:
            m_dot_max = 0
            mass_water = 0

            if timer_flag == False:
                mission_end_time = t_plus + 10
                timer_flag = True

        m_dot = 4 * duty_cycle * m_dot_max

        mass_tot_new -= m_dot * dt_simulation
        mass_water -= m_dot * dt_simulation

        dv = gravity * dt_simulation + (
                    ue * log(mass_tot / mass_tot_new))  # if mass_tot = mass_tot_new, only gravity effects apply
        mass_tot = mass_tot_new
        velocity += dv
        height += velocity * dt_simulation

        if dv > 0:
            height_flag = True

        if height < 0:
            height = 0
            velocity = 0
            if height_flag:
                graph.vlines.append(t_plus)
                return t_plus

        t_plus += dt_simulation
        # graph.record("height", height, t_plus, "Height", "Height, m", only_positive=True)
        # graph.record("velocity", velocity, t_plus, "Velocity", "Velocity, m/s")
        # graph.record("duty_cycle", duty_cycle, t_plus, "Duty Cycle", "Duty Cycle, %")
        # graph.record("mass_water", mass_water, t_plus, "Mass of Water", "Mass, kg", bottom_at_zero=True)
        # graph.record("dv", dv, t_plus, "dv")
    # graph.show_plots()
