import struct
from npy import nstreamcom, terminal
import time
import serial

class PID:
    def __init__(self, p_gain, i_gain, d_gain, time_func = None, invert = False):
        self.p_gain = p_gain
        self.i_gain = i_gain
        self.d_gain = d_gain

        self.error = 0
        self.delta_error = 0

        self.time_func = time.time if time_func is None else time_func
        self.time_now = self.time_func()
        self.delta_time = 0
        self.time_last = self.time_now

        self.p = 0
        self.i = 0
        self.d = 0

        self.invert = invert
        self.output = 0

    def calculate(self, set, input):
        self.delta_error = (input - set) - self.error
        self.error = input - set

        self.time_now = self.time_func()
        self.delta_time = self.time_now - self.time_last
        self.time_last = self.time_now

        self.p = self.p_gain * self.error
        self.i = self.i_gain * (self.i + (self.error * self.delta_time)) / self.delta_time if self.delta_time > 0 else self.i
        self.d = self.d_gain * (self.delta_error / self.delta_time) if self.delta_time > 0 else self.d

        self.output = self.p + self.i + self.d
        return -1 * self.output if self.invert else self.output

program_start_time = time.time()

def program_time():
    return time.time() - program_start_time

def constrain(low, x, high):
    if x < low:
        return low
    elif x > high:
        return high
    else:
        return x

def log_list(l, name, labels = None, r1 = ' ', r2 = ''):
    with open(name, 'w') as log_file:
        if labels is not None:
            log_file.write(f'{ labels }\n')
        for line in enumerate(l):
            log_file.write(f'{ line[1].__str__()[1:-1].replace(r1, r2) }\n')

def main():
    samples = []
    sample_number = 0
    sample_count = 150
    max_voltage = 0
    min_voltage = 5
    avg_voltage = 0

    voltage_controller = PID(0.51, 0.012, 0.1, program_time, True)
    volage_setpoint = float(3.80)
    voltage_process = float(0.0)
    output = int(0)

    with serial.Serial('COM3') as port:
        port.baudrate = 1000000
        while True:
            try:
                recv = nstreamcom.parse(bytearray(port.readline()))
            except:
                break
            if not isinstance(recv, tuple):
                continue
            recv_id, recv_data, recv_size = recv

            voltage_process = struct.unpack('f', recv_data)[0]
            output += voltage_controller.calculate(volage_setpoint, voltage_process)
            output = constrain(0, output, 255)

            try:
                port.write(nstreamcom.parse((1, int(output).to_bytes(4, 'little'), 4)))
            except:
                continue

            sample_set = [voltage_controller.time_now, voltage_process, volage_setpoint, voltage_controller.error, output, voltage_controller.output,voltage_controller.p, voltage_controller.i, voltage_controller.d, voltage_controller.delta_time]
            samples.append(sample_set)

            if voltage_process > max_voltage:
                max_voltage = voltage_process

            if voltage_process < min_voltage:
                min_voltage = voltage_process

            avg_voltage += voltage_process

            terminal.clear()
            print(f'Sample: { sample_number }')
            print(f'Voltage: { voltage_process }')
            print(f'PWM Output: { output }')
            print(f'Change: { voltage_controller.output }')

            sample_number += 1
            if sample_count == sample_number:
                break

    avg_voltage /= (sample_number + 1)
    print('Finishing up...')
    print(f'Max V: { max_voltage }, Min V: { min_voltage }, Avg V: { avg_voltage }')
    log_list(samples, 'Transistor PID.csv', 'T,V_Proc,V_set,Error,Out,Calc,P,I,D,dt')

if __name__ == '__main__':
    main()