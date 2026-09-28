import paho.mqtt.client as mqtt
import time

def W5_Q():

    broker= "185.131.248.7"  #Broker address
    port = 1883                         #Broker port
    user = "wisegrid"                    #Connection username
    password = "wisegrid"            #Connection password

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        client.subscribe("Wally/W5.Power_Q_3_7_0.CV/#")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        #print(msg.topic+" "+str(msg.payload))
        f = open("W5_Q.json", "w")
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
