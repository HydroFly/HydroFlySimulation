# HydroFly Master Simulation
# Version 1.3
# Adam Benabbou, Thomas Slusser, Russell Weas

from Utilities.Grapher import Grapher
from Utilities.Calculator import Calculator
from Utilities.PID_Controller import PIDController

from numpy import *
import matplotlib.pyplot as plt

graph = Grapher()


def run(options):
    # Default Configuration
    config = {
        "dry_mass": 2,
        "mass_water": 20,
        "propellant_pressure": 500000,
        "propellant_volume": 3,
        "target_height": 2,
        "pipe_height": 0.5,
        "nozzle_diam": 0.005
    }
    config.update(options)

    has_taken_off = False
    mass_water = config['mass_water']  # mass of water [kg]
    mass_dry = config['dry_mass']
    mass_tot = mass_water + mass_dry
    mass_tot_new = mass_tot

    height = 0
    velocity = 0
    system_has_lost_propulsion = False

    gravity = -9.81
    rho_water = 997

    target_height = config['target_height']  # mission profile height [m]
    pipe_height = config['pipe_height']  # difference in height between nozzle and pressure tanks [m]

    nozzle_diam = config['nozzle_diam']  # [m]
    nozzle_area = Calculator.nozzle_area(nozzle_diam)

    pressure = config['propellant_pressure']

    t_plus = 0
    t_liftoff = 0
    dt_simulation = 0.05
    dt_physical = 0.05
    mission_end_time = 200

    height_PID = PIDController(1, 0, 1, dt_simulation)
    velocity_PID = PIDController(1, 1, 1, dt_simulation)

    duty_cycle = 0
    data = {}
    mode = 1
    ue = sqrt(2 * (pressure / rho_water + gravity * pipe_height))
    m_dot_max = Calculator.m_dot(nozzle_area, ue)

    while t_plus <= mission_end_time:
        # mode 1 is ascent
        if mode == 1 and height >= target_height:
            clock = t_plus
            mode = 2
            height_PID.integral = 0
            target_height = config['target_height']

        # mode 2 is hover
        if mode == 2:
            if t_plus - clock >= 10:
                target_height = 0
                mode = 3
                height_PID.clean()
                height_PID.KI = 5

        # mode 3 is descent 
        if mode == 3:
            velocity_cv = velocity_PID.get_cv(-0.5, velocity)
            target_dv = velocity_cv

        else:
            height_cv = height_PID.get_cv(target_height, height)  # target height - height
            tuning_time = dt_simulation * 200
            target_dv = 2 * (height_cv - velocity * tuning_time) / (tuning_time ** 2) / 4

        target_d_mass = mass_tot * exp((gravity * dt_simulation / ue) - (target_dv / ue))
        m_dot_target = (mass_tot - target_d_mass) / dt_simulation

        # PWM, PID
        if Calculator.modulus(t_plus, dt_physical) == 0:
            if m_dot_max != 0:
                duty_cycle = (m_dot_target / m_dot_max)
            else:
                duty_cycle = 0
            if duty_cycle < 0:
                duty_cycle = 0
            if duty_cycle > 1:
                duty_cycle = 1
        if mass_water <= 0 and system_has_lost_propulsion == False:
            system_has_lost_propulsion = True
            m_dot_max = 0
            graph.vlines.append(t_plus)
            mission_end_time = t_plus + 10

        if system_has_lost_propulsion:
            m_dot_max = 0
            mass_water = 0

        m_dot = duty_cycle * m_dot_max

        mass_tot_new -= m_dot * dt_simulation
        mass_water -= m_dot * dt_simulation

        dv = gravity * dt_simulation + (ue * log(mass_tot / mass_tot_new))  # if mass_tot = mass_tot_new, only gravity effects apply
        mass_tot = mass_tot_new
        velocity += dv
        height += velocity * dt_simulation

        if dv > 0.00001:
            has_taken_off = True

        if height < 0:
            height = 0
            velocity = 0
            if has_taken_off:
                graph.vlines.append(t_plus)
                break
            else:
                t_liftoff = t_plus

        t_plus += dt_simulation
        graph.record("height", height, t_plus, "Height", "Height, m", only_positive=True)
        graph.record("velocity", velocity, t_plus, "Velocity", "Velocity, m/s")
        graph.record("duty_cycle", duty_cycle, t_plus, "Duty Cycle", "Duty Cycle, %")
        graph.record("mass_water", mass_water, t_plus, "Mass of Water", "Mass, kg", bottom_at_zero=True)
    graph.show_plots()
    plt.figure(2)

    data['time_of_flight'] = t_plus - t_liftoff

    return data
