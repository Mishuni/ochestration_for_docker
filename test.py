
import eventlet
eventlet.monkey_patch()

import os
import subprocess

import json
from flask import Flask, render_template, request, Response, jsonify
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

# DB
from database.db import initialize_db
from database.models import Device


app = Flask(__name__)

# <host-url>/<database-name>
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/cluster'
}

initialize_db(app)


app = Flask(__name__)
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

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

@app.route('/movies', methods=['POST'])
def add_movie():
    body = request.get_json()
    print("body:",body)
    movie = Movie(**body).save()
    id = movie.id
    return {'id': str(id)}, 200

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