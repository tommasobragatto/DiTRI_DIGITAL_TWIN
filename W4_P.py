import paho.mqtt.client as mqtt
import time

def W4_P():

    broker= "172.105.154.83"  #Broker address
    port = 61883                         #Broker port
    user = "mqttUser"                    #Connection username
    password = "mqttUser"            #Connection password

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        client.subscribe("Wally/W4.Power_P_1_7_0.CV/#")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        #print(msg.topic+" "+str(msg.payload))
        f = open("W4_P.json", "w")
        f.write(str(msg.payload.decode("utf-8")))
        f.close()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(user, password=password)  
    client.connect(broker, port, 60)

    startTime = time.time()
    waitTime = 1
    while True:
            client.loop()
            elapsedTime = time.time() - startTime
            if elapsedTime > waitTime:
                    client.disconnect()
                    break
