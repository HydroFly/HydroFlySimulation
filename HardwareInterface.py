import time


class HardwareInterface:
    def __init__(self):
        self.start_time = time.time()
        self.current_time = time.time()
        self.prev_time = time.time() - 0.01

    def next_cycle(self):
        self.prev_time = self.current_time
        self.current_time = time.time()

    def get_delta_time(self):
        return self.current_time - self.prev_time

    def get_t_plus(self):
        return self.current_time - self.start_time
