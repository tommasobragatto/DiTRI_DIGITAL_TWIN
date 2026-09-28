import datetime

# carico = ["Headquarters", "Slow", "Mazzocchio", "Celi", "Storage", "Fast", "Croci", "PV185", "PV60", "altroSCOV"]

tempo=[]
tempo_f=[]
tempo_soc=[]
Potenza_SE=[]

rami = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\potenza_SE_ottobre", "r")
for line in rami:
    line = line.split(";")
    tempo += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    Potenza_SE += [float(line[1][2:7])]
rami.close()

print(Potenza_SE)
rpf_lun= open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\RPF_lunedi", "w")
for linea in range(678):
    rpf_lun.write(str(tempo[linea])+ "; ")

    rpf_lun.write(str(Potenza_SE[linea]))
    rpf_lun.write("\n")

