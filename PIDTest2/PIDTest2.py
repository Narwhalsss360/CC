import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from npy import terminal

class PID:
    def __init__(self, p_gain, i_gain, d_gain, time_func = None):
        self.p_gain = p_gain
        self.i_gain = i_gain
        self.d_gain = d_gain

        self.error = 0
        self.delta_error = 0

        self.time_func = time_func
        self.delta_time = 0
        self.time_last = time.time() if self.time_func is None else self.time_func()

        self.p = 0
        self.i = 0
        self.d = 0

        self.invert = False
        self.output = 0

    def calculate(self, set, input):
        self.delta_error = (input - set) - self.error
        self.error = input - set

        time_now = time.time() if self.time_func is None else self.time_func()
        self.delta_time = time_now - self.time_last
        self.time_last = time_now

        self.p = self.p_gain * self.error
        self.i = self.i_gain * (self.i + (self.error * self.delta_time)) / self.delta_time if self.delta_time > 0 else self.i
        self.d = self.d_gain * (self.delta_error / self.delta_time) if self.delta_time > 0 else self.d

        self.output = self.p + self.i + self.d
        return -self.output if self.invert else self.output

samples = []

def log_list(l, name, labels = None, r1 = ' ', r2 = ''):
    with open(name, 'w') as log_file:
        if labels is not None:
            log_file.write(f'{ labels }\n')
        for line in enumerate(l):
            log_file.write(f'{ line[1].__str__()[1:-1].replace(r1, r2) }\n')

t_x = float()
def f(x):
    return (-x ** 2) + (5 * x)

def t():
    global t_x
    return t_x

def main():
    global t_x

    fig = plt.figure()

    pid = PID(1, .0936492, 1, t)
    for i in range(51):
        x = i / 10
        t_x = x
        y = f(x)
        pid.calculate(0, y)
        sample_set = [x, y, pid.output, pid.p, pid.i, pid.d, pid.delta_time]
        samples.append(sample_set)
        print(sample_set)
    log_list(samples, 'PIDTest2 Samples.csv', 'x,y,PID output,PID P,PID I,PID D,PID delta_time')

if __name__ == '__main__':
    main()