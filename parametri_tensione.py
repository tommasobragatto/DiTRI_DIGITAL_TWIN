import matplotlib.pyplot as plt
plt.style.use('ggplot')
import statistics
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

rami2 = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\tensioni.txt", "r")
for line in rami2:
    line = line.split(";")
    tempo += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    for i in range(10):
        tensione_carico[i].append(float(line[i+1][2:10]))
rami2.close()

rami = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\tensioni_DR.txt", "r")
for line in rami:
    line = line.split(";")
    tempo_f += [datetime.datetime.strptime(line[0][1:20], '%Y-%m-%d %H:%M:%S')]
    for i in range(10):
        tensione_carico_DR[i].append(float(line[i+1][2:10]))
rami.close()

st_dev = [[],[],[],[],[],[],[],[],[],[]]
st_dev_DR = [[],[],[],[],[],[],[],[],[],[]]
media = [[],[],[],[],[],[],[],[],[],[]]
media_DR = [[],[],[],[],[],[],[],[],[],[]]
massimo = [[],[],[],[],[],[],[],[],[],[]]
massimo_DR = [[],[],[],[],[],[],[],[],[],[]]
for j in range(10):
    media[j]=statistics.mean(tensione_carico[j])
    media_DR[j]=statistics.mean(tensione_carico_DR[j])
    st_dev[j] = statistics.pstdev(tensione_carico[j])
    st_dev_DR[j] = statistics.pstdev(tensione_carico_DR[j])
    massimo[j]=max(tensione_carico[j])
    massimo_DR[j]=max(tensione_carico_DR[j])

print(statistics.mean(media))
print(statistics.mean(media_DR))
print(statistics.mean(st_dev))
print(statistics.mean(st_dev_DR))
print(massimo)
print(massimo_DR)