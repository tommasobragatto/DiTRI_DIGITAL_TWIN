import matplotlib.pyplot as plt
plt.style.use('ggplot')
import datetime
from dateutil import parser
from numpy import mean


# CARICO corresponds to the buses that we would like to monitor
# carico = ["Headquarters", "Slow", "Mazzocchio", "Celi", "Storage", "Fast", "Croci", "PV185", "PV60", "altroSCOV"]
font1 = {'family':'Times New Roman','color':'black','size':48}
font2 = {'family':'Times New Roman','color':'black','size':36}
font3 = {'family':'Times New Roman','color':'black','size':28}

tempo=[]
tempo_f=[]

line0=[]
line0_DR=[]
line1=[]
line1_DR=[]
line2=[]
line2_DR=[]
line3=[]
line3_DR=[]
line4=[]
line4_DR=[]
line5=[]
line5_DR=[]
line6=[]
line6_DR=[]
line7=[]
line7_DR=[]
line8=[]
line8_DR=[]
line9=[]
line9_DR=[]
line10=[]
line10_DR=[]



rami2 = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\correnti_prova.txt", "r")
for line in rami2:
    line = line.split(";")
    tempo_f += line[0][1:20]
    tempo_f += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    line0 += [float(line[1][2:10])]
    line1 += [float(line[1][2:10])]
    line2 += [float(line[7][2:10])]
    line3 += [float(line[1][2:10])]
    line4 += [float(line[7][2:10])]
    line5 += [float(line[1][2:10])]
    line6 += [float(line[7][2:10])]
    line7 += [float(line[7][2:10])]
    line8 += [float(line[1][2:10])]
    line9 += [float(line[7][2:10])]
    line10 += [float(line[1][2:10])]
rami2.close()


rami = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\correnti_DR.txt", "r")
for line in rami:
    line = line.split(";")
    tempo_f += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    line0_DR += [float(line[1][2:10])]
    line1_DR += [float(line[1][2:10])]
    line2_DR += [float(line[7][2:10])]
    line3_DR += [float(line[1][2:10])]
    line4_DR += [float(line[7][2:10])]
    line5_DR += [float(line[1][2:10])]
    line6_DR += [float(line[7][2:10])]
    line7_DR += [float(line[7][2:10])]
    line8_DR += [float(line[1][2:10])]
    line9_DR += [float(line[7][2:10])]
    line10_DR += [float(line[1][2:10])]
rami.close()


aa=2160
f=24
qq=2160-180


plt.rcParams["axes.edgecolor"]= "0.15"
plt.rcParams["axes.linewidth"]= 1.25
plt.rcParams['axes.facecolor'] = 'w'
plt.tick_params(width=3, length=8)
plt.rcParams['axes.facecolor'] = 'w'

plt.plot(tempo_f[-aa:-1-qq], line0[-aa:-1-qq], color="b", label="Line_0") #, tempo_f2[-140:-10], SOC_f2[-140:-10], 'r')
plt.plot(tempo_f[-aa:-1-qq], line0_DR[-aa:-1-qq], color="c", label="Line_0 with DR") #, tempo_f2[-140:-10], SOC_f2[-140:-10], 'r')
plt.plot(tempo_f[-aa:-1-qq], line7[-aa:-1-qq], color="r", label="Line_7") #, tempo_f2[-140:-10], SOC_f2[-140:-10], 'r')
plt.plot(tempo_f[-aa:-1-qq], line7_DR[-aa:-1-qq], color="orange", label="Line_7 with DR") #, tempo_f2[-140:-10], SOC_f2[-140:-10], 'r')

plt.xticks(fontsize=f, color="black", fontname="Times New Roman")
plt.yticks(fontsize=f, color="black", font="Times New Roman")
plt.title("Current", fontdict = font2)
plt.xlabel('time [hour]', fontdict = font3)
plt.ylabel("Current [A]", fontdict = font3)
plt.legend(loc="upper left", fontsize=f)

plt.show() #show graph

sovraccarichi = [0,0,0,0,0,0,0,0,0,0,0]
sovraccarichi_DR = [0,0,0,0,0,0,0,0,0,0,0]
k=0.03
LT=[479*k, 173*k, 173*k, 96*k,173*k, 96*k, 96*k, 137*k,119*k,137*k,137*k]
line=[line0,line1,line2,line3,line4,line5,line6,line7,line8,line9,line10]
line_DR=[line0_DR,line1_DR,line2_DR,line3_DR,line4_DR,line5_DR,line6_DR,line7_DR,line8_DR,line9_DR,line10_DR]


for j in range(11):
    for i in range(len(line0_DR)):
        if line[j][i]>LT[0]:
            sovraccarichi[j] += 1
        if line_DR[j][i]>LT[0]:
            sovraccarichi_DR[j] += 1

print(sovraccarichi)
print(sovraccarichi_DR)

