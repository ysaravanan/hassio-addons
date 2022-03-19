#!/usr/bin/python3

import logging
from paho.mqtt import client as mqtt_client
from parser import telegraf_parser
import argparse

###########################################################

def data_received(client, userdata, data):
    telegraf_data.send(data)

def data_transmit(topic, payload, retain=False):
    # logging.debug(f"Publishing to {topic} the payload {payload}")
    client.publish(topic, payload, retain=retain)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT Broker!")
    else:
        logging.info("Failed to connect, return code %d\n", rc)


# logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%H:%M:%S')


# Construct an argument parser
all_args = argparse.ArgumentParser()

# Add arguments to the parser
all_args.add_argument("--user", required=False)
all_args.add_argument("--pass", required=False)
all_args.add_argument("--broker-ip", required=False, default="192.168.1.5")
all_args.add_argument("--port", required=False, default=1883)
all_args.add_argument("--topic", required=False, default="telegraf/#")

args = vars(all_args.parse_args())

## Configure client
client = mqtt_client.Client("telegraf2mqtt")
# client.enable_logger(logger)
client.username_pw_set(args['user'], args['pass'])
client.on_connect = on_connect
client.on_message = data_received

# Connect to HA broker, and subscribe to telegraf topics
client.connect(args['broker_ip'], int(args['port']))
client.subscribe(args['topic'])

telegraf_data = telegraf_parser(data_transmit)

logging.info("Setup finished")

client.loop_forever()
