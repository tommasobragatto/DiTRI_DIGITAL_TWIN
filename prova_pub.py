import paho.mqtt.client as mqtt
from datetime import datetime
import json

solution = [1,1,1,1,1,1,1,1,1,1,1,1]
Bus_name = ["Bus2","Bus9","Bus10",]
carichiSE = ["Mazzocchio1", "Celi1", "Croci1", "altroSCOV1", "Slow1"]
broker= "185.131.248.7"  #Broker address
port = 1883                         #Broker port
user = "wisegrid"                    #Connection username
password = "wisegrid"            #Connection password

    # # The callback for when the client receives a CONNACK response from the server.
    # def on_connect(client, userdata, flags, rc):
    #     client.subscribe("A2MQTT/W3/Power_P_1_7_0/#")
    #
    # # The callback for when a PUBLISH message is received from the server.
    # def on_message(client, userdata, msg):
    #     f = open("W3_P.json", "w")
    #     f.write(str(msg.payload.decode("utf-8")))
    #     f.close()

#ora_attuale = time.strftime('%Y-%m-%dT%H:%M:%S.%fZ', time.localtime())
ora_attuale = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-3]

Cv = {"d": 0.01899999938905239,
      "dt": 4,
      "ts": ora_attuale,
      "q": 192}
#
# json_object = json.dumps(Cv, indent=4)
#
# print(Cv)
# with open("sample.json", "w") as outfile:
#     outfile.write(json_object)


client = mqtt.Client()
    #client.on_message = on_message
client.username_pw_set(user, password=password)
client.connect(broker, port, 60)
for i in range(5):
    Cv["d"] = solution[2 * i]
    Cv["ts"] = ora_attuale
    json_object = json.dumps(Cv, indent=4)
    client.publish("A2MQTT/" + carichiSE[i] + "/Power_P_1_7_0/Cv", json_object)
    #client.publish("A2MQTT/" + carichiSE[i]+"/Power_P_1_7_0/Cv", "{\"d\":"+str(solution[2 * i])+",\"dt\":4,\"ts\":"+ora_attuale+"Z,\"q\":192}")
    #client.publish("A2MQTT/" + carichiSE[i]+"/Power_Q_3_7_0/Cv", "{\"d\":"+str(solution[2 * i + 1])+",\"dt\":4,\"ts\":"+ora_attuale+"Z,\"q\":192}")


    # dss.loads_write_kvar(float(solution[2 * i + 1]))
    # startTime = time.time()
    # waitTime = 1
    # while True:
    #         client.loop()
    #         elapsedTime = time.time() - startTime
    #         if elapsedTime > waitTime:
    #                 client.disconnect()
    #                 break
