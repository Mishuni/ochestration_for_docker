
MQTT_CONFIG={
    'mqtt_broker_url': '192.168.1.78',# 'broker.hivemq.com',
    'mqtt_broker_port':1883,
    'mqtt_username':'mishuni',
    'mqtt_password':'1234',
    'mqtt_keepalive':5,
    'mqtt_tls_enabled':False,
    'app_url':'http://192.168.1.78:5000'
}


DB_CONFIG={
    'host': 'mongodb://localhost/cluster',
}

APP_CONFIG={
    'secret':'my secret key',
    'templates_auto_reload':True
}