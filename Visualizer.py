import matplotlib.pyplot as plt

samples = list()

with open('samples_t.txt', 'r') as t_file:
    with open('samples_v.txt', 'r') as v_file:
        with open('samples_dvdt.txt', 'r') as dedt_file:
            with open('samples_inte.txt', 'r') as inte_file:
                samples.append([float(t[:-1]) for t in t_file.readlines()[:-1]])
                samples.append([float(v[:-1]) for v in v_file.readlines()[:-1]])
                samples.append([float(dedt[:-1]) for dedt in dedt_file.readlines()[:-1]])
                samples.append([float(inte[:-1]) for inte in inte_file.readlines()[:-1]])

plt.plot(samples[0], samples[1])
plt.plot(samples[0], samples[2])
plt.plot(samples[0], samples[3])
plt.show()
input()