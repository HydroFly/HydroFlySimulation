import numpy as np

class Calculator:
    @staticmethod
    def nozzle_area(nozzle_diam):
        return np.pi * ((nozzle_diam/2) ** 2)
        #check valid 10/06/18 - Thomas Slusser
    @staticmethod
    def potential_height(mass, height, velocity):
        #return height + 0.5 * mass * velocity ** 2
        return height + (0.5*(velocity**2)/abs(9.81))
        #check valid 10/06/18 - Thomas Slusser
    @staticmethod
    def exit_velocity(pressure, pipe_height):
        return np.sqrt(2 * ((pressure / 997) + -9.81 * pipe_height))
        #return np.sqrt(2* (pressure - (997*9.81*pipe_height)))
        # assumed correct due to work with Chandler - 10/06/18 
    @staticmethod
    def m_dot(nozzle_area, exit_velocity):
        m_dot = 997 * nozzle_area * exit_velocity
        if m_dot < 0:
            m_dot = 0
        return m_dot

    @staticmethod
    def duty_cycle(m_dot, m_dot_max):
        duty_cycle = m_dot / m_dot_max
        if duty_cycle > 1:
            duty_cycle = 1
        if duty_cycle < 0:
            duty_cycle = 0

        return duty_cycle

    @staticmethod
    def target_d_mass(mass, ue, target_dv, dt):
        return mass * np.exp((-9.81 * dt / ue) - (target_dv / ue))

    @staticmethod
    def delta_v_required(delta_height):
        return np.sqrt(abs(2 * 9.81 * delta_height))
 
    @staticmethod
    def modulus(a, b):
        return round(((round(a % b, 5)) % b), 5)
