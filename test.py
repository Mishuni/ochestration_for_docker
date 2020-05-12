
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
from client.config import *

# DB
from database.db import initialize_db
from database.models import Device

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
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

mqtt = Mqtt(app)
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
    return Response(Device.objects().to_json(), mimetype="application/json", status=200) 

@app.route('/devices/<id>', methods=['GET'])
def get_device(id):
    device = Device.objects.get(id=id).to_json()
    return Response(device, mimetype="application/json", status=200)

@app.route('/register', methods=['POST'])
def add_device():
    body = request.get_json()
    device = Device(**data).save()
    deviceName = device.deviceName
    return {'deviceName':str(deviceName)}, 200


### socket
# db register
@socketio.on('register')
def handle_register(json_str):
    data = json.loads(json_str)
    device = Device(**data).save()

@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data['topic'], data['message'])

@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data['topic'])

@socketio.on('unsubscribe_all')
def handle_unsubscribe_all():
    mqtt.unsubscribe_all()


### mqtt
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    original = message.payload.decode()
    print("original: ",original)

    data = dict(
        topic=message.topic,
        payload=str(original)
    )
   
    # print(os.system('docker -H 192.168.0.62:2376 ps -a'))
    socketio.emit('mqtt_message', data=data)

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


if __name__ == '__main__':

    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)