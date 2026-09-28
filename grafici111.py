import matplotlib.pyplot as plt
plt.style.use('ggplot')
import datetime

# CARICO corresponds to the buses that we would like to monitor
# carico = ["Headquarters", "Slow", "Mazzocchio", "Celi", "Storage", "Fast", "Croci", "PV185", "PV60", "altroSCOV"]

tempo=[]
tempo_f=[]
tempo_soc=[]
RPF=[]
RPF_f=[]
SOC_BEMS = []
SOC_Scov = []
rami = open("results_experiment2/RPF.txt", "r")
for line in rami:
    line = line.split(";")
    tempo += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    RPF += [float(line[1][1:5])]
rami.close()

rami2 = open("results_experiment2/RPF_DR.txt", "r")
for line in rami2:
    line = line.split(";")
    tempo_f += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    RPF_f += [float(line[1][1:5])]
rami2.close()

#batterie = ["BEMS", "Celi", "Mazzocchio", "Croci", "Scov", "Slow", "Fast"]
rami2 = open("results_experiment2/P_storage.txt", "r")
for line in rami2:
    line = line.split(";")
    tempo_soc += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    SOC_BEMS += [float(line[1])]
    SOC_Scov += [float(line[2])]
rami2.close()

aa=0
bb=0
cc=0

plt.rcParams['axes.facecolor'] = 'w'

plt.plot(tempo_f[0:-1], RPF_f[0:-1], 'r', linewidth=1)
plt.plot(tempo[0:-1], RPF[0:-1], 'b', linewidth=1)
font1 = {'family':'Times New Roman','color':'black','size':12}
font2 = {'family':'Times New Roman','color':'black','size':12}
font3 = {'family':'Times New Roman','color':'black','size':12}
plt.xticks(fontsize=36, color="black", fontname="Times New Roman")
plt.yticks(fontsize=36, color="black", font="Times New Roman")
plt.title("1-week power flow in the main feeder", fontdict = font1)
plt.xlabel('time [day]', fontdict = font2)
plt.ylabel("Power [kW]", fontdict = font2)
plt.show() #show graph


plt.plot(tempo_soc[0:-1], SOC_BEMS[0:-1],label="HVAC bus 8")
plt.plot(tempo_soc[0:-1], SOC_Scov[0:-1],label="EESS bus 14")

plt.xticks(fontsize=font3, color="black", fontname="Times New Roman")
plt.yticks(fontsize=font3, color="black", font="Times New Roman")
plt.title("Energy available for flexibility resources", fontdict = font2)
plt.xlabel('time [day]', fontdict = font3)
plt.ylabel("En [kWh]", fontdict = font3)
plt.legend(loc="upper left", fontsize=font3)


plt.show() #show graph

"""
print(len(tempo_f))
print(len(SOC_BEMS))
print("la massima potenza assorbita vale", str(max(RPF)))
print("la minima potenza assorbita vale", str(min(RPF)))
print("la massima potenza assorbita (con flessibilità) vale", str(max(RPF_f)))
print("la minima potenza assorbita (con flessibilità) vale", str(min(RPF_f)))

RPFh=0
for i in RPF[34000:161500]:
    if i < 0:
        RPFh += -i/180
print("l'energia di reverse power flow  vale" + str(RPFh))

RPFh_f=0
for i in RPF_f[32500:160000]:
    if i < 0:
        RPFh_f += -i/180
print("l'energia di reverse power flow (con flessibilità) vale" + str(RPFh_f))


potenza_SE = open("results_experiment2/potenza_SE.txt", "r")
p=potenza_SE.read()
potenza_SE.close()
p=p.split("\n")
numero_righe=len(p)-1
for i in range(numero_righe):
    p[i]=p[i].split(";")

valori_P=[[],[],[],[],[],[],[],[],[],[]]
valori_Q=[[],[],[],[],[],[],[],[],[],[]]
for j in range(numero_righe):  # per ogni riga
    for c in range(10):  # per ogni carico
        p[j][c + 1] = p[j][c + 1].strip("[] ")
        p[j][c+1]=p[j][c+1].split(",")
        att=float(p[j][c + 1][0])
        rea=float(p[j][c + 1][1])
        valori_P[c].append(att)
        valori_Q[c].append(rea)

Energia_prodotta=-(1/6)*(sum(valori_P[7]) + sum (valori_P[8]))
print("energia prodotta= ", str(Energia_prodotta))

Energia_consumata=(1/6)*(sum(valori_P[0]) + sum(valori_P[1]) + sum (valori_P[2]) + sum (valori_P[9]) + sum(valori_P[3]) + sum (valori_P[4]) + sum (valori_P[5]) + sum (valori_P[6]))

autoconsumo=100*(1-RPFh / Energia_prodotta)
print(f"l'autoconsumo vale {autoconsumo}%")

autoconsumo_f=100*(1-RPFh_f / Energia_prodotta)
print(f"l'autoconsumo con flessibiltà vale {autoconsumo_f}%")

autosufficienza=100*(Energia_prodotta - RPFh)/(Energia_consumata + Energia_prodotta - RPFh)
print(f"l'autosufficienza vale {autosufficienza}%")

autosufficienza_f=100*(Energia_prodotta - RPFh)/(Energia_consumata + Energia_prodotta - RPFh_f)
print(f"l'autosufficienza con flessibilità vale {autosufficienza_f}%")

"""