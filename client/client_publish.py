import paho.mqtt.client as mqtt
import json
import sys
from config import MQTT_CONFIG

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_publish(client, userdata, mid):
    print("In on_pub callback mid= ", mid)


if __name__ == '__main__':
    f = open("result.txt", 'r')
    data = f.read()
    print(data)
    #print(type(data))
    f.close()
    # 새로운 클라이언트 생성
    client = mqtt.Client()
    # 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    #client.connect('broker.hivemq.com', 1883)
    client.connect(MQTT_CONFIG['mqtt_broker_url'],MQTT_CONFIG['mqtt_broker_port'])
    
    client.loop_start()
    client.publish(MQTT_CONFIG['deviceName']+'_result',  data, 1)
    client.loop_stop()
    # 연결 종료
    client.disconnect()