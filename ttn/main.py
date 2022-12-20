from config import config, logging
from db import init_db, NewSession
from db.models import Backend
from parser.ttn import ttn_klax_parser

# gracefull stopping mqtt services
import signal
import time

stopsignal = False

def handler_stop_signals(signum, frame):
    global stopsignal
    stopsignal = True

signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)


# MQTT Client
import paho.mqtt.client as mqtt


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.debug("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg:mqtt.MQTTMessage):

    # Parse 
    ttn_klax_parser(str(msg.topic), str(msg.payload.decode("utf-8")))

    #Log
    logging.info(f"--- Message received on {msg.topic} -----------------")
    logging.debug(str(msg.payload))





""" Main """
def main():

    logging.info('----------------------------------------------------------')
    logging.info(f'mqtt client start  ....')
    logging.debug(f'... running in environment {config}')    
    
    # initialize db 
    init_db()
    

    # retrieve all ttn mqtt credentials
    # Instanciate database engine
    #dbengine = create_engine(config.MYSQL_DATABASE_URI, pool_recycle=config.SQLALCHEMY_POOL_RECYCLE, connect_args={'check_same_thread': False})
    #dbsessionmaker = sessionmaker(bind=dbengine)
    dbsession = NewSession()
    mqtt_credentials = dbsession.query(Backend.backend_user, Backend.backend_password).filter_by(backend=config.MQTT_SERVICE).distinct()

    clients = []

    for mqtt_credential in mqtt_credentials:

        client = mqtt.Client(mqtt_credential.backend_user)
        client.on_connect = on_connect
        client.on_message = on_message

        client.tls_set()
        client.username_pw_set(username=mqtt_credential.backend_user, password=mqtt_credential.backend_password)

        clients.append(client)


    # mqtt loop
    for client in clients:

        client.connect(config.MQTT_HOST, config.MQTT_PORT)
        client.loop_start()

    # endless loop until CTRL-C or CTRL-Z
    while not stopsignal:
        time.sleep(1)

    """ goodby gracefull stop mqqt clients"""
    for client in clients:
        client.loop_stop()


    logging.info(f'mqtt client stopped  ....')
    logging.info('----------------------------------------------------------')

    
""" run main if not imported """
if __name__ == '__main__':
    main()



