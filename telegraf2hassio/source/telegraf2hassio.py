import random
import logging
import json
from paho.mqtt import client as mqtt_client
from parser import telegraf_parser

logger = logging.getLogger(__name__)
# if "DEBUG" in os.environ:
#     logger.setLevel(logging.DEBUG)

logger.setLevel(logging.INFO)

logging.basicConfig(level=logging.DEBUG)

class settings:
    broker = 'localhost'
    port = 1883
    telegraf_topic = "telegraf/#"
    client_id = f'python-mqtt-{random.randint(0, 1000)}'

###########################################################

def data_received(client, userdata, data):
    logging.debug(f"Data received: {json.loads(data.payload.decode())}")

    telegraf_data.announce_new(data)
    telegraf_data.send(data)

def data_transmit(topic, payload):
    logging.debug(f"Publishing to {topic} the payload {payload}")
    client.publish(topic, payload)
    
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT Broker!")
    else:
        logging.info("Failed to connect, return code %d\n", rc)


logger = logging.getLogger(__name__)

## Configure client
client = mqtt_client.Client(settings.client_id)
# client.enable_logger(logger)
client.username_pw_set(settings.username, settings.password)
client.on_connect = on_connect
client.on_message = data_received

# Connect to HA broker, and subscribe to telegraf topics
client.connect(settings.broker, settings.port)
client.subscribe(settings.telegraf_topic)

telegraf_data = telegraf_parser(data_transmit)

logging.info("Setup finished")

client.loop_forever()
