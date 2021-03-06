#!/usr/bin/env python
import paho.mqtt.client as mqtt
import os , platform , socket, requests
import subprocess, sys
import json, simplejson
from config import *

#deviceName = os.getenv('DEVICENAME')
deviceName = MQTT_CONFIG['deviceName']
client_path = os.path.dirname(os.path.abspath(__file__))+'/client_publish.py'

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
    print("topic:",msg.topic)
    if(msg.topic=="ACK"):
        print("Received check reqeuset")
        data=deviceName
        client.publish("RST",data,1)
    else:
        command = str(msg.payload.decode("utf-8")).strip().split(' ')
        runCmd(command)

def runCmd(command):
    order = command[0]
    if(order=="remove"):
        if(command[len(command)-1]=="image"):
            order="removeImg"
        del command[len(command)-1]
    if(order in commandList):
        cmd = commandList.get(order).copy()
        for i in range(1,len(command)):
            if(command[i]==' ' or command[i]=='' or command[i]=='/'):
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
        print(url)
        r = requests.get(url)
        result = r.json()
        
        del result['_id']
        del result['register']
        if(result!=data):
            print("The 'deviceName' is duplicated with another device in a Queue,") 
            print("you have to change the value of 'deviceName' in a file named config.py")
            return False
        else:
            print("Waiting permission from master")
            return False
    
    except simplejson.errors.JSONDecodeError:
        # if there is no other device that the devicename is same
        url = MQTT_CONFIG['app_url']+"/registerQueue"
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        r = requests.post(url, data = json.dumps(data), headers=headers)
        return False
        

def checkDuplicateWithRegister(data):
    try:
        # check if the device name is duplicated with other device that is already registered
        url = MQTT_CONFIG['app_url']+"/devices/"+deviceName
        print(url)
        r = requests.get(url)
        result = r.json()
        del result['_id']
        del result['register']
        del result['connected']
        if(result!=data):
            print("The 'deviceName' is duplicated with another device that is already registered,") 
            print("you have to change the value of 'deviceName' in a file named config.py")
            return False
        else:
            return True
    except simplejson.errors.JSONDecodeError:
        # if there is no other device which the name is same
        return checkDuplicateWithQueue(data)

# {"connected":"True"}
def changeConnected(connection):
    url = MQTT_CONFIG['app_url']+"/connected/"+deviceName
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    body = {"connected":connection}
    r = requests.put(url, data = json.dumps(body), headers=headers)
    return r.text

#### MAIN ####
# register request
#os.getenv('DEVICENAME')
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
data = {'name': deviceName, 'ipv4Addr': s.getsockname()[0], 
        'cpu_count':os.cpu_count(), 'os_system':platform.system(), 
        'hostname':socket.gethostname()}
s.close()
print(data)
possible = checkDuplicateWithRegister(data)
print("Register:",possible)
if(possible):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.connect(MQTT_CONFIG['mqtt_broker_url'],MQTT_CONFIG['mqtt_broker_port'])
    # topic subscribe
    client.subscribe(deviceName, 1)
    client.subscribe("ACK", 1)
    client.loop_forever()
    