
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

@app.route('/devices/<id>', methods=['POST'])
def get_device(id):
    device = Device.objects.get(id=id).to_json()
    return Response(device, mimetype="application/json", status=200)

# db register
@socketio.on('register')
def handle_register(json_str):
    data = json.loads(json_str)
    device = Device(**data).save()
    #ip = device.ipv4Addr
    #print(ip)


@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    #print(data['topic'])
    #print(data['message'])
    mqtt.publish(data['topic'], data['message'])

@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data['topic'])

@socketio.on('unsubscribe_all')
def handle_unsubscribe_all():
    mqtt.unsubscribe_all()


@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    original = message.payload.decode()
    print("original: ",original)
    data2 = str(original)
    ipAddr = message.topic

    data = dict(
        topic=message.topic,
        payload=data2
    )
   
    # print(os.system('docker -H 192.168.0.62:2376 ps -a'))
    socketio.emit('mqtt_message', data=data)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


if __name__ == '__main__':

    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)