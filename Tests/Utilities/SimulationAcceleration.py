# HydroFly Master Simulation
# Version 1.3
# Adam Benabbou, Thomas Slusser, Russell Weas

from Utilities.Grapher import Grapher
from Utilities.Calculator import Calculator
from Utilities.PID_Controller import PIDController
import numpy as np
from numpy import *
import matplotlib.pyplot as plt


class Cannon:
    def __init__(self, y0, v):
        # current x and y coordinates of the missile
        self.y    = y0
        # current value of velocity components
        self.vy  = v
        # acceleration by x and y axes
        #self.ay   = -9.8
        # start time
        self.time = 0
        # these list will contain discrete set of missile coordinates
        self.yarr = [self.y]

    def updateVy(self, dt, newa):
        self.vy = self.vy + newa*dt
        return self.vy

    def updateY(self, dt, newa):
        self.y = self.y + 0.5*(self.vy + self.updateVy(dt, newa))*dt
        return self.y

    def step(self, dt, newa):
        self.yarr.append(self.updateY(dt, newa))
        self.time = self.time + dt



# def main():
#     x0 = 0
#     y0 = 0
#     velocity = 15
#     y6 = makeShoot(y0, velocity)
#     print(y6)
#     plt.plot(y6, 'bo-',
#         #[0, 12], [0, 0], 'k-' # ground
#         )
#     plt.legend(['XX'])
#     plt.xlabel('X coordinate (m)')
#     plt.ylabel('Y coordinate (m)')
#     plt.show()


graph = Grapher()


def run(options):
    # Default Configuration

    rho_water = 997
    gravity = 9.81 

    config = {}

    config.update(options)

    mass_water = config['mass_water']  # mass of water [kg]
    mass_dry = config['dry_mass']
    mass_start = mass_water + mass_dry
    mass_tot_new = mass_start

    weight_start = (mass_start*gravity)

    target_height = config['target_height']  # mission profile height [m]
    pipe_height = config['pipe_height']  # difference in height between nozzle and pressure tanks [m]
    nozzle_diam = config['nozzle_diam']  # [m]
    pressure = config['propellant_pressure']   

    height = 0
    velocity = 0


    t_plus = 0.0
    dt_simulation = 0.05
    mission_end_time = 20

    nozzle_area = Calculator.nozzle_area(nozzle_diam)
    exit_velocity = np.sqrt(2* ((pressure/rho_water) - (9.81*pipe_height)))
    m_dot_max = Calculator.m_dot(nozzle_area, exit_velocity)
    thrust = m_dot_max*exit_velocity#+ ( (pressure-101325)*nozzle_area)
    acceleration = (thrust/mass_tot_new) - gravity

    print("thrust", thrust, "N")
    print(exit_velocity)
    print("weight", weight_start, "N")
    print("initial acceleration", acceleration)

    y0 = 0
    velocity = 0

    hydrofly = Cannon(y0, velocity)
    hydrofly.step(dt_simulation, acceleration)

    ###### THE  INTEGRATION ######
    while hydrofly.y <= 50:
        mass_tot_new = mass_tot_new - (m_dot_max*dt_simulation)
        acceleration = (thrust/mass_tot_new) - gravity
        print("thrust", thrust, "N")
        print("weight", mass_tot_new*gravity, "N")
        print("acceleration", acceleration)
        hydrofly.step(dt_simulation, acceleration)
        t_plus = t_plus + dt_simulation
    ##############################
    #return (cannon.yarr)
    y6 = hydrofly.yarr


    print(y6)
    plt.plot(y6, 'bo-',
        #[0, 12], [0, 0], 'k-' # ground
        )
    plt.legend(['XX'])
    plt.xlabel('X coordinate (m)')
    plt.ylabel('Y coordinate (m)')
    plt.show()










    # while t_plus <= 10.00:
    #     #ascentHeight = (-0.5*gravity*(t_plus**2)) + (exit_velocity*log(original_mass)*t_plus) + ((exit_velocity/m_dot)*(original_mass-(m_dot*t_plus))*(log(original_mass - (m_dot*t_plus)) -1)) - ((exit_velocity/m_dot)*original_mass*(log(original_mass) -1)) 

    #     new_weight = (original_mass- (m_dot*t_plus))*gravity
    #     if new_weight > 0:
    #         acceleration = (thrust-new_weight)/(new_weight)
    #     else:
    #         acceleration = -9.81 
        
    #     #d_acceleration = acceleration - old_acceleration

    #     velocity = acceleration*dt_simulation

    #     d_height = (velocity*dt_simulation)/2
    #     print("change in velocity:", velocity)

    #     #height = 

    #     #dv = (gravity * dt_simulation) + (exit_velocity * log(original_mass / mass_tot_new))
    #     #if(ascentHeight < 0):
    #         #ascentHeight = 0
    #         #dv = 0
    #     #velocity = velocity + dv

        
    #     print("weight", new_weight, "N")
    #     print("acceleration", acceleration, "m/s^2")

    #     graph.record("height", d_height, t_plus, "Height", "Height, m")
    #     graph.record("velocity", velocity, t_plus, "velocity", "velocity, m")
    #     graph.record("mass", (new_weight/gravity), t_plus, "mass", "mass", "kg")
    #     t_plus += dt_simulation




    # graph.show_plots()
    # plt.figure(2)


""" 
    while t_plus <= mission_end_time:
        # mode 1 is ascent
        if mode == 1 and height >= target_height:
            clock = t_plus
            mode = 2
            #height_PID.integral = 0
            target_height = config['target_height']

        # mode 2 is hover
        if mode == 2:
            if t_plus - clock >= 10:
                target_height = 0
                mode = 3
                #height_PID.clean()
                #height_PID.KI = 5

        # mode 3 is descent 
        if mode == 3:
            #velocity_cv = velocity_PID.get_cv(-0.5, velocity)
            #target_dv = velocity_cv

        else:
            height_cv = height_PID.get_cv(target_height, height)  # target height - height
            #tuning_time = dt_simulation * 200
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

    return data """
