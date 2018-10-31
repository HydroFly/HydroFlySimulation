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
    def __init__(self, x0, y0, v, angle):

        # current x and y coordinates of the missile
        self.x    = x0
        self.y    = y0
        # current value of velocity components
        self.vx  = v*cos(radians(angle))
        self.vy  = v*sin(radians(angle))
        # acceleration by x and y axes
        self.ax   = 0
        self.ay   = -9.8
        # start time
        self.time = 0
        # these list will contain discrete set of missile coordinates
        self.xarr = [self.x]
        self.yarr = [self.y]


    def updateVx(self, dt):
        self.vx = self.vx + self.ax*dt
        return self.vx
    def updateVy(self, dt):
        self.vy = self.vy + self.ay*dt
        return self.vy


    def updateX(self, dt):
        self.x = self.x + 0.5*(self.vx + self.updateVx(dt))*dt
        return self.x
    def updateY(self, dt):
        self.y = self.y + 0.5*(self.vy + self.updateVy(dt))*dt
        return self.y

    def step(self, dt):
        self.xarr.append(self.updateX(dt))
        self.yarr.append(self.updateY(dt))
        self.time = self.time + dt


def makeShoot(x0, y0, velocity, angle):
    """
    Returns a tuple with sequential pairs of x and y coordinates
    """
    cannon = Cannon(x0, y0, velocity, angle)
    dt = 0.05 # time step
    t = 0 # initial time
    cannon.step(dt)
    ###### THE  INTEGRATION ######
    while cannon.y >= 0:
        cannon.step(dt)
        t = t + dt
    ##############################
    return (cannon.xarr, cannon.yarr)

def main():
    x0 = 0
    y0 = 0
    velocity = 10
    x6, y6 = makeShoot(x0, y0, velocity, 45)
    print(y6)
    plt.plot(x6, y6, 'bo-',
        [0, 12], [0, 0], 'k-' # ground
        )
    plt.legend(['60 deg shoot'])
    plt.xlabel('X coordinate (m)')
    plt.ylabel('Y coordinate (m)')
    plt.show()





graph = Grapher()


def run(options):
    # Default Configuration
    config = {
 
    }
    config.update(options)

    has_taken_off = False
    mass_water = config['mass_water']  # mass of water [kg]
    mass_dry = config['dry_mass']
    mass_tot = mass_water + mass_dry
    mass_tot_new = mass_tot
    original_mass = mass_tot
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

    t_plus = 0.0
    t_liftoff = 0
    dt_simulation = 0.05
    dt_physical = 0.05
    mission_end_time = 200



    duty_cycle = 0
    data = {}
    mode = 1
    exit_velocity = np.sqrt(2* ((pressure/997) - (9.81*pipe_height)))
    print(exit_velocity)
    m_dot_max = Calculator.m_dot(nozzle_area, exit_velocity)
    m_dot = m_dot_max
    gravity = 9.81 
    t_plus = 0

    thrust = m_dot*exit_velocity + ( (pressure-101325)*nozzle_area)
    print("thrust", thrust, "N")
    new_weight = (original_mass*gravity)
    print("weight", new_weight, "N")
    velocity = 0 
    old_acceleration = 0 
    old_velocity = 0

    main()






    while t_plus <= 10.00:
        #ascentHeight = (-0.5*gravity*(t_plus**2)) + (exit_velocity*log(original_mass)*t_plus) + ((exit_velocity/m_dot)*(original_mass-(m_dot*t_plus))*(log(original_mass - (m_dot*t_plus)) -1)) - ((exit_velocity/m_dot)*original_mass*(log(original_mass) -1)) 

        new_weight = (original_mass- (m_dot*t_plus))*gravity
        if new_weight > 0:
            acceleration = (thrust-new_weight)/(new_weight)
        else:
            acceleration = -9.81 
        
        #d_acceleration = acceleration - old_acceleration

        velocity = acceleration*dt_simulation

        d_height = (velocity*dt_simulation)/2
        print("change in velocity:", velocity)

        #height = 

        #dv = (gravity * dt_simulation) + (exit_velocity * log(original_mass / mass_tot_new))
        #if(ascentHeight < 0):
            #ascentHeight = 0
            #dv = 0
        #velocity = velocity + dv

        
        print("weight", new_weight, "N")
        print("acceleration", acceleration, "m/s^2")

        graph.record("height", d_height, t_plus, "Height", "Height, m")
        graph.record("velocity", velocity, t_plus, "velocity", "velocity, m")
        graph.record("mass", (new_weight/gravity), t_plus, "mass", "mass", "kg")
        t_plus += dt_simulation




    graph.show_plots()
    plt.figure(2)


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
