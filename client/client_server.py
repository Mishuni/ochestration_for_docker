#!/usr/bin/env python
import paho.mqtt.client as mqtt
import os , platform , socket
import subprocess
import json
from config import MQTT_CONFIG, commandList

deviceName = MQTT_CONFIG['deviceName']
client_path = os.path.dirname(os.path.abspath(__file__))+'/client_publish.py'
#print(client_path)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    command = str(msg.payload.decode("utf-8")).strip().split(' ')
    #print(msg.topic)
    runCmd(command)


def runCmd(command):
    order = command[0]
    if(order in commandList):
        cmd = commandList.get(order).copy()
        for i in range(1,len(command)):
            cmd.append(command[i])
        print(cmd)
        fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout 
        data = str(fd_popen.read().strip())
        fd_popen.close()
        data=data[2:-1].split('\\n')

        f = open("result.txt", 'w')
        for line in data:
            f.write(line+"\n")
    
        f.close()
        os.system("python3 "+client_path)
    else:
        print("Wrong command")
    
    
print(os.cpu_count())
print(os.uname())
print(platform.processor())
print(socket.gethostname())
print(socket.gethostbyname(socket.gethostname()))
#print(str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB")

# 새로운 클라이언트 생성
client = mqtt.Client()
# 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_subscribe(topic 구독),
# on_message(발행된 메세지가 들어왔을 때)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message
#client.on_publish = on_publish
# address : localhost, port: 1883 에 연결
client.connect(MQTT_CONFIG['mqtt_broker_url'],MQTT_CONFIG['mqtt_broker_port'])
# topic subscribe
client.subscribe(deviceName, 1)
#client.publish('192.168.0.62', json.dumps({"result": "ok"}), 1)
client.loop_forever()

