#!/bin/bash

echo "Starting..."

term_handler(){
    echo "Stopping..."
    exit 0
}

# Setup signal handlers
trap 'term_handler' SIGTERM


CONFIG_PATH=/data/options.json

MQTT_BROKER=$(jq --raw-output ".configname" $CONFIG_PATH)
MQTT_USER=$(jq --raw-output ".configname" $CONFIG_PATH)
MQTT_PASS=$(jq --raw-output ".configname" $CONFIG_PATH)
TELEGRAF_TOPIC=$(jq --raw-output ".configname" $CONFIG_PATH)

# Enforces required env variables
required_vars=(MQTT_BROKER MQTT_USER MQTT_PASS TELEGRAF_TOPIC)
for required_var in "${required_vars[@]}"; do
    if [[ -z ${!required_var} ]]; then
        echo >&2 "Error: $required_var env variable not set."
        exit 1
    fi
done


python3 /opt/telegraf2hassio/telegraf2hassio.py
