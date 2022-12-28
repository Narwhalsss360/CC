import serial
import npy.nstreamcom
import struct

def deriv(x, x_prev, y, y_prev):
    return (y - y_prev) / (x - x_prev)

def inte(x, x_prev, y, inte_prev):
    return inte_prev + (y * (x - x_prev))

samples = list()

# Testing Code1t
def f(x):
    return (-x ** 2) + (5 * x)

for i in range(51):
    x = i / 10
    samples.append([x, f(x)])

with open('samples_t.txt', 'w') as t_file:
    with open('samples_v.txt', 'w') as v_file:
        with open('samples_dvdt.txt', 'w') as dedt_file:
            with open('samples_inte.txt', 'w') as inte_file:
                with open('samples_inte_time.txt', 'w') as inte_time_file:
                    last_integral = 0
                    last_integral_time = 0
                
                    for i in range(len(samples)):
                        t_file.write(f'{ samples[i][0] }\n')
                        v_file.write(f'{ samples[i][1] }\n')

                        if i != 0:
                            dedt_file.write(f'{ deriv(samples[i][0], samples[i - 1][0], samples[i][1], samples[i - 1][1]) }\n')
                            
                            last_integral = inte(samples[i][0], samples[i - 1][0], samples[i][1], last_integral)
                            inte_file.write(f'{ last_integral }\n')

                            last_integral_time = inte(samples[i][0], samples[i -1][0], samples[i][1], last_integral_time)
                            inte_time_file.write(f'{ last_integral_time }\n')
                        else:
                            dedt_file.write(f'{ 0 }\n')

                            inte_file.write(f'{ 0 }\n')

                            inte_time_file.write(f'{ 0 }\n')