# config.py

MQTT_CONFIG={
    'deviceName':'miseon',
    'mqtt_broker_url': '127.0.0.1',# 'broker.hivemq.com',
    'mqtt_broker_port':1883,
    'mqtt_username':'mishuni',
    'mqtt_password':'1234',
    'mqtt_keepalive':5,
    'mqtt_tls_enabled':False,
    'app_url':'http://127.0.0.1:5000'
}

DB_CONFIG={
    'host': 'mongodb://localhost/cluster',
}

APP_CONFIG={
    'secret':'my secret key',
    'templates_auto_reload':True
}

commandList = {
    "status":['docker','ps','-a'],
    "pull":['docker','pull'],
    "run":['docker','run'],
    "images":['docker','images'],
    "stop":['docker','stop'],
    "remove":['docker','rm'] 
}

