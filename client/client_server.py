#!/usr/bin/env python
import paho.mqtt.client as mqtt
import os , platform , socket, requests
import subprocess, sys
import json, simplejson
from config import *

deviceName = MQTT_CONFIG['deviceName']
client_path = os.path.dirname(os.path.abspath(__file__))+'/client_publish.py'

import socket
print(socket.gethostbyaddr(socket.gethostname()))

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected"+ client.values +str(rc))


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
            if(command[i]==' '):
                continue
            cmd.append(command[i])
        print(cmd)
        fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout 
        data = str(fd_popen.read().strip())
        fd_popen.close()
        #print("data: ",data)
        data=data[2:-1].split('\\n')

        f = open("result.txt", 'w')
        for line in data:
            f.write(line+"\n")
    
        f.close()
        os.system("python3 "+client_path)
    else:
        print("Wrong command")

def checkDuplicateWithQueue(data):
    try:
        # check if the device name is duplicated with other queue
        url = MQTT_CONFIG['app_url']+"/registerQueue/"+deviceName
        r = requests.get(url)
        result = r.json()
        del result['_id']
        del result['register']
        if(result!=data):
            print("The 'deviceName' is duplicated with another device in a Queue,") 
            print("you have to change the value of 'deviceName' in a file named config.py")
            sys.exit()
    
    except simplejson.errors.JSONDecodeError as e:
        url = MQTT_CONFIG['app_url']+"/registerQueue"
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        r = requests.post(url, data = json.dumps(data), headers=headers)

# register request
data = {'name': deviceName, 'ipv4Addr': '123.214.186.236', 
        'cpu_count':os.cpu_count(), 'os_system':platform.system(), 
        'hostname':socket.gethostname()}
try:
    # check if the device name is duplicated with other device that is already registered
    url = MQTT_CONFIG['app_url']+"/devices/"+deviceName
    r = requests.get(url)
    result = r.json()
    del result['_id']
    del result['register']
    if(result!=data):
        print("The 'deviceName' is duplicated with another device that is already registered,") 
        print("you have to change the value of 'deviceName' in a file named config.py")
        sys.exit()

except simplejson.errors.JSONDecodeError as e:
    checkDuplicateWithQueue(data)

# 새로운 클라이언트 생성
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message
# address : localhost, port: 1883 에 연결
client.connect(MQTT_CONFIG['mqtt_broker_url'],MQTT_CONFIG['mqtt_broker_port'])
# topic subscribe
client.subscribe(deviceName, 1)
client.loop_forever()

#print(str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB")