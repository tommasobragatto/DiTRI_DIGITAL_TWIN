import matplotlib.pyplot as plt
plt.style.use('ggplot')
import datetime


# CARICO corresponds to the buses that we would like to monitor
# carico = ["Headquarters", "Slow", "Mazzocchio", "Celi", "Storage", "Fast", "Croci", "PV185", "PV60", "altroSCOV"]

plt.rcParams["axes.edgecolor"]= "0.15"
plt.rcParams["axes.linewidth"]= 1.25
plt.rcParams['axes.facecolor'] = 'w'
plt.tick_params(width=3, length=8)

font1 = {'family':'Times New Roman','color':'black','size':48}
font2 = {'family':'Times New Roman','color':'black','size':36}
font3 = {'family':'Times New Roman','color':'black','size':36}

x=[0.1, 0.2, 0.3, 0.5, 0.75, 1]
y=[94.25, 96.38, 96.66, 96.84, 96.67, 96.35]
f=36

plt.rcParams['axes.facecolor'] = 'w'
plt.plot(x, y, color="b")

plt.xticks(fontsize=f, color="black", fontname="Times New Roman")
plt.yticks(fontsize=f, color="black", font="Times New Roman")
plt.title("Inverter Efficiency", fontdict = font2)
plt.xlabel('Power [p.u.]', fontdict = font3)
plt.ylabel("Efficiency [%]", fontdict = font3)

plt.rc('font', size=36)



plt.show() #show graph



