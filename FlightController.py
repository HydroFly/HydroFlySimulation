from Constants import Constants
from Calculator import Calculator
from PID_Controller import PIDController
from numpy import *


class FlightController:
    mode = 1

    def __init__(self, sys):
        self.sys = sys
        self.PID = PIDController(1, 0, 0, sys.dt_simulation)

        self.target_height = 2
        self.duty_cycle = 1

    def update_cycle(self):
        sys = self.sys
        if self.mode == 1:
            # Test condition to advance modes
            if sys.height >= self.target_height:
                self.mode = 2
                self.PID.clean()

            height = sys.height
            velocity = sys.velocity
            gravity = Constants.gravity
            target_height = self.target_height
            tuning_time = sys.tuning_time
            dt_simulation = sys.dt_simulation
            mass_tot = sys.mass_tot
            ue = sys.ue
            t_plus = sys.t_plus
            m_dot_max = sys.m_dot_max
            dt_physical = sys.dt_physical

            # Find Calculated Value and potentials
            height_cv = self.PID.get_cv(target_height, height)  # target height - height

            target_dv = 2 * (height_cv - velocity * tuning_time) / (tuning_time ** 2)

            target_d_mass = mass_tot * exp((gravity * dt_simulation / ue) - (target_dv / ue))
            m_dot_target = (mass_tot - target_d_mass) / dt_simulation

            # PWM, PID
            if Calculator.modulus(t_plus, dt_physical) == 0:
                self.duty_cycle = (m_dot_target / m_dot_max)
                if self.duty_cycle < 0:
                    self.duty_cycle = 0
                if self.duty_cycle > 1:
                    self.duty_cycle = 1

        if self.mode == 2:
            # Test condition to advance modes
            if sys.height >= self.target_height:
                self.mode = 2

            height = sys.height
            velocity = sys.velocity
            gravity = Constants.gravity
            target_height = self.target_height
            tuning_time = sys.tuning_time
            dt_simulation = sys.dt_simulation
            mass_tot = sys.mass_tot
            ue = sys.ue
            t_plus = sys.t_plus
            m_dot_max = sys.m_dot_max
            dt_physical = sys.dt_physical

            # Find Calculated Value and potentials
            height_cv = self.PID.get_cv(target_height, height)  # target height - height

            target_dv = 2 * (height_cv - velocity * tuning_time) / (tuning_time ** 2)

            target_d_mass = mass_tot * exp((gravity * dt_simulation / ue) - (target_dv / ue))
            m_dot_target = (mass_tot - target_d_mass) / dt_simulation

            # PWM, PID
            if Calculator.modulus(t_plus, dt_physical) == 0:
                self.duty_cycle = (m_dot_target / m_dot_max)
                if self.duty_cycle < 0:
                    self.duty_cycle = 0
                if self.duty_cycle > 1:
                    self.duty_cycle = 1

        if self.mode == 3:
            pass

        return self.duty_cycle