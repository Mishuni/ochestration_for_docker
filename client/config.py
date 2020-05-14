# config.py

MQTT_CONFIG={
    'deviceName':'host203',
    'mqtt_broker_url': '192.168.1.78',# 'broker.hivemq.com',
    'mqtt_broker_port':1883,
    'mqtt_username':'mishuni',
    'mqtt_password':'1234',
    'mqtt_keepalive':5,
    'mqtt_tls_enabled':False,
    'app_url':'http://192.168.1.78:5000'
}

commandList = {
    "status":['docker','ps','-a'],
    "pull":['docker','pull'],
    "run":['docker','run'],
    "images":['docker','images'],
    "stop":['docker','stop'],
    "remove":['docker','rm'] 
}

