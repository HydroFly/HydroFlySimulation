class PIDController:
    def __init__(self, kp, ki, kd, dt):
        self.KP = kp
        self.KI = ki
        self.KD = kd
        self.prevError = 0
        self.integral = 0
        self.dt = dt

    def get_cv(self, target, current):
        error = target - current
        self.integral += error * self.dt
        derivative = (error - self.prevError) * self.dt
        self.prevError = error
        return self.KP * error + self.KI * self.integral + self.KD * derivative
