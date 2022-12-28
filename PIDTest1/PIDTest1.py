import npy.nstreamcom
import serial
import struct

ID_UPTIME = 1
ID_POSITION = 2
ID_PREVIOUS = 3

pos = 0
p = 0
i = 0
d = 0
ctrl = 0

def integral(error, prev_integral, delta_time):
    return prev_integral + (error * delta_time)

def derivative(delta_error, delta_time):
    return delta_error / delta_time

def PIDLoop(gain_p, gain_i, gain_d, error, previous_error, time, previous_time, previous_integral):
    global pos
    global p
    global i
    global d
    global ctrl

    p = gain_p * error
    output = p

    i = gain_i * (((1 / (time - previous_time)) * integral(error, previous_integral, time - previous_time))) if time - previous_time > 0 else previous_integral

    output += i

    d = gain_d * (derivative(error - previous_error, time - previous_time)) if time - previous_time > 0 else d
    output += d
    ctrl = output
    return (output, i)

def f(x):
    return -(x**2) + (5 * x)

def main():
    global pos
    global p
    global i
    global d
    global ctrl

    prev_position = 0
    time = 0
    prev_time = 0
    prev_integral = 0

    with open('PIDLogger.csv', 'w') as logger:
        for i_1 in range(51):
            time = i_1 / 10
            position = f(time)
            outputs = PIDLoop(1, .0936492, 1, position, prev_position, time, prev_time, prev_integral)
            prev_integral = outputs[1]
            prev_position = position
            prev_time = time
            print(f'{ time } | { position } | { ctrl }')
            logger.write(f'{ time },{ position },{ p },{ i },{ d },{ ctrl }\n')

    exit()
    with serial.Serial('COM3') as port:
        with open('PIDLogger.csv', 'w') as logger:
            port.baudrate = 1000000
            prev_position = 0
            time = 0
            prev_time = 0
            prev_integral = 0
            while True:
                try:
                    recv = npy.nstreamcom.parse(bytearray(port.readline()))
                except:
                    exit()
                if isinstance(recv, tuple):
                    recv_id, recv_data, recv_size = recv
                    if recv_id == ID_POSITION:
                        position = int(struct.unpack('f', recv_data)[0])
                        outputs = PIDLoop(1, 1, 1, position, prev_position, time, prev_time, prev_integral)
                        prev_integral = outputs[1]
                        prev_position = position
                        print(f'{ time } | { position } | { ctrl }')
                        logger.write(f'{ time },{ position },{ p },{ i },{ d },{ ctrl }\n')
                    if recv_id == ID_UPTIME:
                        time = float(int.from_bytes(recv_data, 'little') / 1000)
                    if recv_id == ID_PREVIOUS:
                        prev_time = float(int.from_bytes(recv_data, 'little') / 1000)

if __name__ == '__main__':
    main()