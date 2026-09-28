import matplotlib.pyplot as plt
plt.style.use('ggplot')
import statistics
import datetime
from numpy import mean


# CARICO corresponds to the buses that we would like to monitor
# carico = ["Headquarters", "Slow", "Mazzocchio", "Celi", "Storage", "Fast", "Croci", "PV185", "PV60", "altroSCOV"]
font1 = {'family':'Times New Roman','color':'black','size':48}
font2 = {'family':'Times New Roman','color':'black','size':36}
font3 = {'family':'Times New Roman','color':'black','size':28}

tempo=[]
tempo_f=[]

linea=[[],[],[],[],[],[],[],[],[],[],[]]
linea_DR=[[],[],[],[],[],[],[],[],[],[],[]]

rami2 = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\correnti.txt", "r")
for line in rami2:
    line = line.split(";")
    tempo += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    for j in range(11):
        linea[j].append(float(line[j+1][2:10]))
rami2.close()



rami = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\correnti_DR.txt", "r")
for line in rami:
    line = line.split(";")
    tempo_f += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    for j in range(11):
        linea_DR[j].append(float(line[j+1][2:10]))
rami.close()


st_dev = [[],[],[],[],[],[],[],[],[],[],[]]
st_dev_DR = [[],[],[],[],[],[],[],[],[],[],[]]
media = [[],[],[],[],[],[],[],[],[],[],[]]
media_DR = [[],[],[],[],[],[],[],[],[],[],[]]

for j in range(11):
    media[j]=statistics.mean(linea[j])
    media_DR[j]=statistics.mean(linea_DR[j])
    st_dev[j] = statistics.pstdev(linea[j])
    st_dev_DR[j] = statistics.pstdev(linea_DR[j])

print(media)
print(media_DR)
print(st_dev)
print(st_dev_DR)
