# HydroFly Master Simulation
# Version 1.3
# Adam Benabbou, Thomas Slusser, Russell Weas
import matplotlib

from Grapher import Grapher
from Calculator import Calculator
# from System import System
from PID_Controller import PIDController

from numpy import *
import matplotlib.pyplot as plt
graph = Grapher()

from matplotlib import style


def run(mass_dry):
    # plt.ion()
    flare = False
    style.use('bmh')
    # style.use('fivethirtyeight')
    # style.use('ggplot')
    height_flag = False
    ############ Assumptions ###########
    mass_water = 10  # mass of water [kg]
    # mass_dry = 0.2  # dry mass including stuctures and electronics... will update later
    mass_tot = mass_water + mass_dry
    mass_tot_new = mass_tot

    height = 0
    velocity = 0
    system_has_lost_propulsion = False
    timer_flag = False

    gravity = -9.81
    rho_water = 997

    pressure = 500000*20     # Original pressure of pressurant [Pa] 0.5 MPa
    # volume_gas_orig = 3  # volume of pressurant [m^3]
    target_height = 2  # mission profile height [m]
    pipe_height = .5  # difference in height between nozzle and pressure tanks [m]

    nozzle_diam = 0.01  # [m]
    nozzle_area = Calculator.nozzle_area(nozzle_diam)

    ###### Simulation Timing ######
    t_plus = 0
    dt_simulation = 0.1
    dt_physical = 0.5
    mission_end_time = 200
    timermode2 = 0

    # sys = System()
    PID = PIDController(1, 1, 1, dt_simulation)

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
            PID.integral = 0
            target_height = 2
            graph.vlines.append(t_plus)
        if mode == 2:
            if t_plus - clock >= 10:
                target_height = 0
                graph.vlines.append(t_plus)
                mode =3
                PID.clean()
                flare = False
        if mode == 3:
            if height < 1:
                flare = True
            if flare:
                target_dv = -0.5 - velocity
        if not flare:
            # # MODE-INDEPENDENT CALC
            height_cv = PID.get_cv(target_height, height)  # target height - height

            tuning_time = dt_simulation * 100

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
        if mass_water <= 0 and system_has_lost_propulsion == False:
            system_has_lost_propulsion = True
            m_dot_max = 0
            graph.vlines.append(t_plus)

        if system_has_lost_propulsion:
            m_dot_max = 0
            mass_water = 0

            if timer_flag == False:
                mission_end_time = t_plus
                timer_flag = True

        m_dot = duty_cycle * m_dot_max

        mass_tot_new -= m_dot * dt_simulation
        mass_water -= m_dot * dt_simulation

        dv = gravity * dt_simulation + (
                    ue * log(mass_tot / mass_tot_new))  # if mass_tot = mass_tot_new, only gravity effects apply
        mass_tot = mass_tot_new
        velocity += dv
        height += velocity * dt_simulation

        if height < 0:
            height = 0
            if height_flag == False:
                graph.vlines.append(t_plus)
            height_flag = True
            velocity = 0

        t_plus += dt_simulation
        graph.record("height", height, t_plus, "Height", only_positive=True)
        graph.record("velocity", velocity, t_plus, "Velocity")
        graph.record("duty_cycle", duty_cycle, t_plus, "Duty Cycle")
        graph.record("mass_water", mass_water, t_plus, "Mass of Water", bottom_at_zero=True)
        graph.record("dv", dv, t_plus, "dv")
    # graph.show_plots()
