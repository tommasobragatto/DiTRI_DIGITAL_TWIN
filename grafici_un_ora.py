import matplotlib.pyplot as plt
plt.style.use('ggplot')
import datetime

# CARICO corresponds to the buses that we would like to monitor
# carico = ["Headquarters", "Slow", "Mazzocchio", "Celi", "Storage", "Fast", "Croci", "PV185", "PV60", "altroSCOV"]
plt.rcParams["axes.edgecolor"]= "0.15"
plt.rcParams["axes.linewidth"]= 1.25
plt.rcParams['axes.facecolor'] = 'w'

tempo=[]
tempo_f=[]
RPF=[]
RPF_f=[]
SOC_BEMS = []
SOC_Celi = []
SOC_Mazzocchio = []
SOC_Croci = []
SOC_Scov = []
SOC_Slow = []
SOC_Fast = []
rami = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\P_giorno.txt", "r")
for line in rami:
    line = line.split(";")
    tempo += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    RPF += [float(line[1][1:5])]
rami.close()

rami2 = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\P_giorno_DR.txt", "r")
for line in rami2:
    line = line.split(";")
    tempo_f += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    RPF_f += [float(line[1][1:5])]
rami2.close()


#print(tempo)


plt.plot(tempo_f[1260:1440], RPF_f[1260:1440], 'r', linewidth=1)
plt.plot(tempo[1260:1440], RPF[1260:1440], 'b', linewidth=1)
font1 = {'family':'Times New Roman','color':'black','size':48}
font2 = {'family':'Times New Roman','color':'black','size':36}
plt.xticks(fontsize=40, color="black", fontname="Times New Roman")
plt.yticks(fontsize=40, color="black", font="Times New Roman")

plt.title("1-hour power flow in the main feeder", fontdict = font1)
plt.xlabel('time [day and hour]', fontdict = font2)
plt.ylabel("Power [kW]", fontdict = font2)



plt.show() #show graph
