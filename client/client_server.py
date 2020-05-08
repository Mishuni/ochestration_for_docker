#!/usr/bin/env python
import paho.mqtt.client as mqtt
import os 
import subprocess
import json

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
    command = str(msg.payload.decode("utf-8"))
    print(command)
    print(msg.topic)
    runCmd(command)

commandList = {
    "status":['docker','ps','-a'],
    "pull":['docker','pull','hello-world'],
    "run":['docker','run','hello-world'],
    "images":['docker','images'] 
    }

def runCmd(command):
    data2 = command
    if(command in commandList):
        cmd = commandList.get(command)
        fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout 
        data2 = str(fd_popen.read().strip())
        #print(data2[1:].split('\\n'))
        fd_popen.close()
        data2=data2[2:-1].split('\\n')

        f = open("result.txt", 'w')
        for line in data2:
            f.write(line+"\n")
    
        f.close()
        os.system("python3 $(pwd)/client_publish.py")
    else:
        print("Wrong command")
    
    

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
client.connect('broker.hivemq.com', 1883)
# common topic 으로 메세지 발행
client.subscribe('se_2', 1)
#client.publish('192.168.0.62', json.dumps({"result": "ok"}), 1)
client.loop_forever()