class System:
    ue = 0
    height = 0
    velocity = 0
    target_height = 0
    gravity = 0
    tuning_time = .5
    mass_dry = 0.5
    t_plus = 0
    m_dot_max = 0
    dt_simulation = 0.01
    dt_physical = 0.1
    mass_water = 13

    def __init__(self):
        self.mass_tot = self.mass_dry + self.mass_water