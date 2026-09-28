import matplotlib.pyplot as plt
import datetime


fast=[]
slow=[]
tempo = []
rami = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\potenza_SE.txt", "r")
for line in rami:
    line = line.split(";")
    tempo += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    slow += [float(line[2][2:5])]
    fast += [float(line[6][2:5])]
rami.close()

print(fast)

"""
dss_new_load_file = pathlib.Path(script_path).joinpath("Potenza_EVCS.dss")
o = open(dss_new_load_file, "w")
o.write(f"{slow[-12961:-1]}; {fastslow[-12961:-1]}
o.close()
"""
a=7*24*60*3
plt.plot(tempo, fast, 'r', linewidth=1)
plt.show()
