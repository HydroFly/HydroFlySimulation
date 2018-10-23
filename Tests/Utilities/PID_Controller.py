class PIDController:
    def __init__(self, kp, ki, kd, dt):
        self.KP = kp
        self.KI = ki
        self.KD = kd
        self.prevError = 0
        self.integral = 0
        self.dt = dt
        self.times_cleaned = 0

    def get_cv(self, target, current):
        error = target - current
        self.integral += error * self.dt
        derivative = (error - self.prevError) * self.dt
        self.prevError = error
        return self.KP * error + self.KI * self.integral + self.KD * derivative

    def clean(self):
        self.prevError = 0
        self.integral = 0
        self.times_cleaned += 1



### returns a height CV
### v = dh/dt
### dh = v * dt
### delta-v-goal = delta-height /  1