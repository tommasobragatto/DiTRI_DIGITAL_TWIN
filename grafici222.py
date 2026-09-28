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
Potenza_SE=[]

rami = open("data/results/RPF_ottobre", "r")
for line in rami:
    line = line.split(";")
    tempo += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    RPF += [float(line[1][1:5])]
rami.close()

rami2 = open("results_experiment/potenza_SE.txt", "r")
for line in rami2:
    line = line.split(";")
    #tempo_f += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    Potenza_SE += [float(line[1][2:6])]
rami2.close()

plt.rcParams['axes.facecolor'] = 'w'
f=12
font1 = {'family':'Times New Roman','color':'black','size':12}
font2 = {'family':'Times New Roman','color':'black','size':12}
font3 = {'family':'Times New Roman','color':'black','size':12}
plt.xticks(fontsize=f, color="black", fontname="Times New Roman")
plt.yticks(fontsize=f, color="black", font="Times New Roman")
plt.title("1-week power flow in the main feeder", fontdict = font1)
plt.xlabel('time [day]', fontdict = font2)
plt.ylabel("Power [kW]", fontdict = font2)

#plt.plot(tempo_f[0:227], RPF_f[0:227], 'r', linewidth=1)
#plt.plot(tempo[0:227], RPF[0:227], 'b', linewidth=1)


#plt.show() #show graph

#print(RPF)

plt.plot(tempo[0:227], Potenza_SE[0:227], 'r', linewidth=1)
plt.show()
