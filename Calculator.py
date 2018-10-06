import numpy as np
from Constants import Constants
from Environment import Environment


class Calculator:
    @staticmethod
    def nozzle_area(nozzle_diam):
        return np.pi * nozzle_diam ** 2

    @staticmethod
    def potential_height(mass, height, velocity):
        return height + 0.5 * mass * velocity ** 2

    @staticmethod
    def exit_velocity(pressure, pipe_height):
        return np.sqrt(2 * ((pressure / Constants.rho_water) + Constants.gravity * pipe_height))

    @staticmethod
    def m_dot(nozzle_area, exit_velocity):
        m_dot = Constants.rho_water * nozzle_area * exit_velocity
        if m_dot < 0:
            m_dot = 0
        return m_dot

    @staticmethod
    def duty_cycle(m_dot, m_dot_max):
        duty_cycle = m_dot / m_dot_max
        if duty_cycle > 1:
            duty_cycle = 1

        return duty_cycle

    @staticmethod
    def target_d_mass(mass, ue, target_dv, dt):
        return mass * np.exp((Constants.gravity * dt / ue) - (target_dv / ue))

    @staticmethod
    def delta_v_required(delta_height):
        return np.sqrt(abs(2 * 9.81 * delta_height))

    @staticmethod
    def modulus(a, b):
        return round(((round(a % b, 5)) % b), 5)