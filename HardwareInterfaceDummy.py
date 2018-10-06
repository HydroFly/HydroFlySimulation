class HardwareInterfaceDummy:
    def __init__(self):
        self.t_plus = 0
        self.dt = 0.01
        self.height = 0

    def start_cycle(self):
        pass

    def get_t_plus(self):
        return self.t_plus

    def get_delta_time(self):
        return self.dt

    def next_cycle(self):
        self.t_plus += self.dt

    def get_height(self):
        return self.height
