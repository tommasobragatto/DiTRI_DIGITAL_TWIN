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
SOC_Celi = []
SOC_Mazzocchio = []
SOC_Croci = []
SOC_Scov = []
SOC_Slow = []
SOC_Fast = []
rami = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\RPF_prova.txt", "r")
for line in rami:
    line = line.split(";")
    tempo += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    RPF += [float(line[1][1:5])]
rami.close()

rami2 = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\RPF_DR_prova.txt", "r")
for line in rami2:
    line = line.split(";")
    tempo_f += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    RPF_f += [float(line[1][1:5])]
rami2.close()

#batterie = ["BEMS", "Celi", "Mazzocchio", "Croci", "Scov", "Slow", "Fast"]
rami2 = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\SOC_DR_prova.txt", "r")
for line in rami2:
    line = line.split(";")
    tempo_soc += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    SOC_BEMS += [float(line[1])]
    SOC_Celi += [float(line[2])]
    SOC_Mazzocchio += [float(line[3])]
    SOC_Croci += [float(line[4])]
    SOC_Scov += [float(line[5])]
    SOC_Slow += [float(line[6])]
    SOC_Fast += [float(line[7])]
rami2.close()

aa=30240
bb=12960
cc=6000

plt.rcParams["axes.edgecolor"]= "0.15"
plt.rcParams["axes.linewidth"]= 1.25
plt.rcParams['axes.facecolor'] = 'w'
plt.tick_params(width=3, length=8)

plt.plot(tempo_f[-aa:-1], RPF_f[-aa:-1], 'r', linewidth=1)
plt.plot(tempo[-aa:-1], RPF[-aa:-1], 'b', linewidth=1)
font1 = {'family':'Times New Roman','color':'black','size':48}
font2 = {'family':'Times New Roman','color':'black','size':36}
font3 = {'family':'Times New Roman','color':'black','size':28}
plt.xticks(fontsize=36, color="black", fontname="Times New Roman")
plt.yticks(fontsize=36, color="black", font="Times New Roman")
plt.title("1-week power flow in the main feeder", fontdict = font1)
plt.xlabel('time [day]', fontdict = font2)
plt.ylabel("Power [kW]", fontdict = font2)
plt.show() #show graph

f=40

plt.plot(tempo_soc[-bb-cc:-1-cc], SOC_BEMS[-bb-cc:-1-cc],label="HVAC bus 8") 
plt.plot(tempo_soc[-bb-cc:-1-cc], SOC_Celi[-bb-cc:-1-cc],label="flexible load bus 11") 
plt.plot(tempo_soc[-bb-cc:-1-cc], SOC_Mazzocchio[-bb-cc:-1-cc],label="flexible load bus 10") 
plt.plot(tempo_soc[-bb-cc:-1-cc], SOC_Croci[-bb-cc:-1-cc],label="EESS bus 9") 
plt.plot(tempo_soc[-bb-cc:-1-cc], SOC_Scov[-bb-cc:-1-cc],label="EESS bus 14") 
#plt.plot(tempo_soc[-bb-cc:-1-cc], SOC_Slow[-bb-cc:-1-cc],label="EVCS bus 22")
#plt.plot(tempo_soc[-bb-cc:-1-cc], SOC_Fast[-bb-cc:-1-cc],label="EVCS bus 16")

plt.xticks(fontsize=f, color="black", fontname="Times New Roman")
plt.yticks(fontsize=f, color="black", font="Times New Roman")
plt.title("Energy available for flexibility resources", fontdict = font2)
plt.xlabel('time [day]', fontdict = font3)
plt.ylabel("En [kWh]", fontdict = font3)
plt.legend(loc="best", fontsize=30)


plt.show() #show graph

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


potenza_SE = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\potenza_SE.txt", "r")
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