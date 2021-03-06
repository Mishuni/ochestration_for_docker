
import eventlet
eventlet.monkey_patch()

import os
import json
import subprocess

# Flask
from flask import Flask, render_template, request, Response, jsonify
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

# Config
from appconfig import *

# DB
from database.db import initialize_db
from database.models import Device,RegisterQueue

app = Flask(__name__)

# <host-url>/<database-name>
app.config['MONGODB_SETTINGS'] = {
    'host': DB_CONFIG['host']
}

initialize_db(app)


app.config['SECRET'] = APP_CONFIG['secret']
app.config['TEMPLATES_AUTO_RELOAD'] = APP_CONFIG['templates_auto_reload']
app.config['MQTT_BROKER_URL'] = MQTT_CONFIG['mqtt_broker_url']
app.config['MQTT_BROKER_PORT'] = MQTT_CONFIG['mqtt_broker_port']
app.config['MQTT_USERNAME'] = MQTT_CONFIG['mqtt_username']
app.config['MQTT_PASSWORD'] = MQTT_CONFIG['mqtt_password']
app.config['MQTT_KEEPALIVE'] = MQTT_CONFIG['mqtt_keepalive']
app.config['MQTT_TLS_ENABLED'] = MQTT_CONFIG['mqtt_tls_enabled']

# Parameters for SSL enabled
#app.config['MQTT_BROKER_PORT'] = 8883
#app.config['MQTT_TLS_ENABLED'] = True
#app.config['MQTT_TLS_INSECURE'] = True
#app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

mqtt = Mqtt(app,mqtt_logging= True)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)

### flask
@app.route('/')
def index():
    return render_template('mqttindex.html')

@app.route('/devices')
def get_devices():
    devices = Device.objects().to_json()
    return Response(devices, mimetype="application/json", status=200)

@app.route('/devices/<id>', methods=['DELETE'])
def delete_device(id):
    Device.objects.get(id=id).delete()
    return '', 200

@app.route('/removeAlldevices', methods=['DELETE'])
def delete_allDevices():
    Device.objects().delete()
    RegisterQueue.objects().delete()
    return Response(Device.objects().to_json(), mimetype="application/json", status=200) 

@app.route('/devices/<name>', methods=['GET'])
def get_device(name):
    device = Device.objects.get(name=name).to_json()
    return Response(device, mimetype="application/json", status=200)

@app.route('/registerQueue', methods=['GET'])
def get_register_devices():
    devices = RegisterQueue.objects().to_json()
    return Response(devices, mimetype="application/json", status=200)

@app.route('/registerQueue', methods=['POST'])
def add_register_device():
    data = request.get_json()
    device = RegisterQueue(**data).save()
    return Response(device, mimetype="application/json", status=200)

@app.route('/registerQueue/<name>', methods=['GET'])
def get_register_device(name):
    device = RegisterQueue.objects.get(name=name).to_json()
    return Response(device, mimetype="application/json", status=200)

@app.route('/removeQueue/<name>', methods=['GET'])
def remove_register_device(name):
    RegisterQueue.objects.get(name=name).delete()
    return Response(RegisterQueue.objects().to_json(), mimetype="application/json", status=200) 

@app.route('/connected/<name>', methods=['PUT'])
def update_connected(name):
    # {"connected":"True"}
    body = request.get_json()
    ori = Device.objects.get(name=name)
    if(body['connected']=='True'):
        ori.update(connected=True)
    elif(body['connected']=='False'):
        ori.update(connected=False)
    
    return Response(Device.objects().get(name=name).to_json(), mimetype="application/json", status=200) 


### socket
@socketio.on('connect') 
def handle_connect():
    mqtt.subscribe('RST')

# db register
@socketio.on('register')
def handle_register(json_str):
    data = json.loads(json_str)
    Device(**data).save()

@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data['topic'], data['message'])

# check mqtt connection
@socketio.on('ack')
def handle_ack(json_str):
    data = json.loads(json_str)
    mqtt.publish(data['topic'])

@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data['topic'])

@socketio.on('unsubscribe_all')
def handle_unsubscribe_all(data):
    print(data)
    mqtt.unsubscribe(data)


### mqtt
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    original = message.payload.decode()
    #print("original: ",original)

    data = dict(
        topic=message.topic,
        payload=str(original)
    )
    
    socketio.emit('mqtt_message', data=data)

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    if level == 'MQTT_LOG_ERR':
        print('Error: {}'.format(buf))
    else:
        print(level, buf)


if __name__ == '__main__':

    socketio.run(app, host='0.0.0.0', port=8002, use_reloader=False, debug=True)

# print(os.system('docker -H 192.168.0.62:2376 ps -a'))
# @mqtt.on_connect()
# def handle_mqtt_connect(client, userdata):
#      print("connected")