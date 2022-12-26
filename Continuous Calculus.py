import serial
import npy.nstreamcom
import struct

def deriv(x, x_prev, y, y_prev):
    return (y - y_prev) / (x - x_prev)

def inte(x, x_prev, y, inte_prev):
    return inte_prev + (y * (x - x_prev))

samples = list()

# Testing Code
def f(x):
    if (x < 8):
        return -0.25 * ((x - 4) ** 2) + 4
    if (x <= 16):
        return 0.25 * ((x - 12) ** 2) - 4

for i in range(161):
    x = i / 10
    samples.append([x, f(x)])

with open('samples_t.txt', 'w') as t_file:
    with open('samples_v.txt', 'w') as v_file:
        with open('samples_dvdt.txt', 'w') as dedt_file:
            with open('samples_inte.txt', 'w') as inte_file:
                last_integral = 0
                for i in range(len(samples)):
                    t_file.write(f'{ samples[i][0] }\n')
                    
                    if i != 0:
                        dedt_file.write(f'{ deriv(samples[i][0], samples[i - 1][0], samples[i][1], samples[i - 1][1]) }\n')
                        last_integral = inte(samples[i][0], samples[i - 1][0], samples[i][1], last_integral)
                        inte_file.write(f'{ last_integral }\n')
                    else:
                        dedt_file.write(f'{ 0 }\n')
                        inte_file.write(f'{ 0 }\n')

exit()

with serial.Serial('COM3') as port:
    port.baudrate = 1000000 
    while True:
        received = npy.nstreamcom.parse(bytearray(port.readline()))
        
        if isinstance(received, tuple):
            id, data, size = received
            if id == 1:
                sample_time = float(int.from_bytes(data[0:4], 'little') / 1000)
                sample_value = struct.unpack('f', data[4:8])[0]
                print(f'Sample: { sample_time } | { sample_value }')
                samples.append([sample_time, sample_value])
                if sample_time >= 10:
                    print('Done sampling')
                    break
        else:
            print(f'e')

print('Writing...')
with open('samples_t.txt', 'w') as t_file:
    with open('samples_v.txt', 'w') as v_file:
        with open('samples_dvdt.txt', 'w') as dedt_file:
            with open('samples_inte.txt', 'w') as inte_file:
                last_integral = 0
                for i in range(len(samples)):
                    t_file.write(f'{ samples[i][0] }\n')
                    v_file.write(f'{ samples[i][1] }\n')
                    if i != 0:
                        dedt_file.write(f'{ deriv(samples[i][0], samples[i - 1][0], samples[i][1], samples[i - 1][1]) }\n')
                        last_integral = inte(samples[i][0], samples[i - 1][0], samples[i][1], last_integral)
                        inte_file.write(f'{ last_integral }\n')
                    else:
                        dedt_file.write(f'{ 0 }\n')
                        inte_file.write(f'{ 0 }\n')