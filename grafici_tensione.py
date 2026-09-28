import matplotlib.pyplot as plt
plt.style.use('ggplot')
import datetime

# CARICO corresponds to the buses that we would like to monitor
# carico = ["Headquarters", "Slow", "Mazzocchio", "Celi", "Storage", "Fast", "Croci", "PV185", "PV60", "altroSCOV"]
font1 = {'family':'Times New Roman','color':'black','size':48}
font2 = {'family':'Times New Roman','color':'black','size':36}
font3 = {'family':'Times New Roman','color':'black','size':28}

tempo=[]
tempo_f=[]
tensione_carico=[[],[],[],[],[],[],[],[],[],[]]
tensione_carico_DR=[[],[],[],[],[],[],[],[],[],[]]

RPF=[]
RPF_f=[]
Headquarters=[]
Slow=[]
Mazzocchio=[]
Celi=[]
Storage=[]
Fast=[]
Croci=[]
PV185=[]
PV60=[]

Croci=[]
Storage=[]
Headquarters_DR=[]
Croci_DR=[]
Storage_DR=[]
Celi_DR=[]

rami2 = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\tensioni.txt", "r")
for line in rami2:
    line = line.split(";")
    tempo_f += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    tensione_carico[]
    Headquarters += [float(line[1][2:10])]
    Celi += [float(line[4][2:10])]
    Storage += [float(line[5][2:10])]
    Croci += [float(line[7][2:10])]
rami2.close()


rami = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\tensioni_DR.txt", "r")
for line in rami:
    line = line.split(";")
    tempo_f += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    Headquarters_DR += [float(line[1][2:10])]
    Storage_DR += [float(line[5][2:10])]
    Croci_DR += [float(line[7][2:10])]
    Celi_DR += [float(line[4][2:10])]

rami.close()


aa=2160
f=24
qq=2160-180


plt.rcParams['axes.facecolor'] = 'w'

plt.plot(tempo_f[-aa:-1-qq], Celi[-aa:-1-qq], color="b", label="Bus_11") #, tempo_f2[-140:-10], SOC_f2[-140:-10], 'r')
plt.plot(tempo_f[-aa:-1-qq], Celi_DR[-aa:-1-qq], color="c", label="Bus_11 with DR") #, tempo_f2[-140:-10], SOC_f2[-140:-10], 'r')
plt.plot(tempo_f[-aa:-1-qq], Storage[-aa:-1-qq], color="r", label="Bus_14") #, tempo_f2[-140:-10], SOC_f2[-140:-10], 'r')
plt.plot(tempo_f[-aa:-1-qq], Storage_DR[-aa:-1-qq], color="orange", label="Bus_14 with DR") #, tempo_f2[-140:-10], SOC_f2[-140:-10], 'r')

plt.xticks(fontsize=f, color="black", fontname="Times New Roman")
plt.yticks(fontsize=f, color="black", font="Times New Roman")
plt.title("Voltage", fontdict = font2)
plt.xlabel('time [hour]', fontdict = font3)
plt.ylabel("Voltage [V]", fontdict = font3)
plt.legend(loc="upper left", fontsize=f)


plt.show() #show graph
