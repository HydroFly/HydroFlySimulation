import numpy as np

from Calculator import Calculator as calc
from Constants import Constants


class FlightController:
    def __init__(self, system, environment):
        self.sys = system

    def do_execution_cycle(self):
        self.sys.

        

    def get_duty_cycle(self, target_height):
        delta_height = target_height - self.height
        potential_height = calc.potential_height(self.mass, self.height, self.velocity)

        # Calculate target velocity if the rocket is below the target height
        if self.height < target_height:
            target_velocity = calc.delta_v_required(delta_height)

        # Shut off the engine if the rocket's potential height is greater than the target height
        if potential_height > target_height or self.height > target_height:
            target_velocity = 0

        # if Calculator.remainder(dt, dtPWM) == 0:
        ue = calc.exit_velocity(self.pressure, self.pipe_height)
        nozzle_area = calc.nozzle_area(self.nozzle_diam)
        m_dot_max = calc.m_dot(nozzle_area, ue)

        # target_dv = PID.get_cv(target_velocity, velocity)
        target_dv = target_velocity - self.velocity

        # Calculate target delta mass and mass flow rate
        target_d_mass = calc.target_d_mass(self.mass_total, ue, target_dv, self.sys.get_delta_time())
        m_dot = (self.mass - target_d_mass) / self.sys.get_delta_time()

        # Calculate target duty cycle
        duty_cycle = calc.duty_cycle(m_dot, m_dot_max)

        return duty_cycle
