from config import config, logging
from db import init_db
from parser.ttn import ttn_klax_parser


# MQTT Client
import paho.mqtt.client as mqtt


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.debug("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(config.MQTT_TOPIC)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg:mqtt.MQTTMessage):

    # Parse 
    ttn_klax_parser(str(msg.topic), str(msg.payload.decode("utf-8")))

    #Log
    logging.info(f"--- Message received on {msg.topic} -----------------")
    logging.debug(str(msg.payload))

logging.info('----------------------------------------------------------')
logging.info(f'mqtt client start  ....')
logging.debug(f'... running in environment {config}')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.tls_set()
client.username_pw_set(username=config.MQTT_USER, password=config.MQTT_PASSWORD)

client.connect(config.MQTT_HOST, config.MQTT_PORT)
client.loop_start()

# initialize db 
init_db()



