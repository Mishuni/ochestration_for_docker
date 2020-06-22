
MQTT_CONFIG={
    'mqtt_broker_url': 'broker.hivemq.com', # 'broker.hivemq.com','127.0.0.1',
    'mqtt_broker_port':1883,
    'mqtt_username':'mishuni',
    'mqtt_password':'1234',
    'mqtt_keepalive':5,
    'mqtt_tls_enabled':False,
}


DB_CONFIG={
    'host': 'mongodb://mongodb/cluster',
    #'host': 'mongodb://localhost/cluster',
}

APP_CONFIG={
    'secret':'my secret key',
    'templates_auto_reload':True
}