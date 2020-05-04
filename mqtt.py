import paho.mqtt.client as mqtt
 
broker_address="broker.hivemq.com"
broker_port=1883
client = mqtt.Client() 
client.connect_async(host=broker_address, port=broker_port)
client.loop_start()

def on_connect(self, client, userdata, flags, rc):
    print ("connect with result code "+str(rc))
    client.subscribe("XX")

def on_message(self, client, userdata, message):
    print('subscribe data : ', message.payload)

client.publish("XX","pub할 내용")