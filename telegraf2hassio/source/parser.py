import json
import logging
import hashlib
# from os import getgrouplist
# import yaml
# import paho.mqtt.client as mqtt

VERSION = "0.1"
HA_PREFIX = "homeassistant/sensor"
STATE_PREFIX = "telegraf2ha"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class telegraf_parser():
    def __init__(self, transmit_callback) -> None:
        self.hosts = {}
        self.transmit_callback = transmit_callback

    def __get_host_name(self, jdata):
        # Build the host name of the current meassage
        return jdata['tags']['host']

    def __get_sensor_name(self, jdata):
        # Build up the sensor name
        sensor_name = jdata['name']

        if len(jdata['tags']) > 1: 
            sensor_name += ('_' + jdata['tags'].get('device', "")).rstrip("_")
            sensor_name += ('_' + jdata['tags'].get('interface', "")).rstrip("_")
            sensor_name += ('_' + jdata['tags'].get('feature', "")).rstrip("_")


        # Append this unique suffix to differ same-sensor-named topics
        # that contain different tags, that confuse hassio
        uid = hashlib.sha1(str(jdata['fields'].keys()).encode()).hexdigest()[0:2]
        sensor_name += f"_{uid}"

        return sensor_name

    def __get_measurements_list(self, jdata):
        return jdata['fields'].keys()

    def announce_new(self, data) -> int:
        jdata = json.loads(data.payload.decode())
        host_name = self.__get_host_name(jdata)
        sensor_name = self.__get_sensor_name(jdata)

        # Add current host if unknown
        current_host, is_new_h = self.add_host(host_name)
        # Add unknown sensors to host
        current_sensor, is_new_s = current_host.add_sensor(sensor_name)
        # Add unknown measurements to each sensor 
        for measurement_name in self.__get_measurements_list(jdata):
            _, is_new_m = current_sensor.add_measurement(measurement_name)

        return (is_new_s | is_new_h | is_new_m)

    def send(self, data):
        # After unknown are announced,
        # send their data
        jdata = json.loads(data.payload.decode())
        host_name = self.__get_host_name(jdata)
        sensor_name = self.__get_sensor_name(jdata)

        topic = f"{STATE_PREFIX}/{host_name}/{sensor_name}/state"

        self.transmit_callback(topic, json.dumps(jdata['fields']))

        return

    def add_host(self, host_name):
        current_host = self.hosts.get(host_name)
        if current_host is None:
            current_host = host(self, host_name)
            self.hosts[host_name] = current_host
            return current_host, True

        return current_host, False


class host():
    def __init__(self, parent_listener, name) -> None:
        self.name = name
        self.sensors = {}
        self.parent_listener = parent_listener

        # dev = Device("deadbeef", "nuvem", "1.0", "telegraf2mqtt", "influx", client)

        self.info = {}
        self.info["identifiers"] = "bridge"
        self.info["model"] = "your_bridge"
        self.info["name"] = self.name
        self.info["sw_version"] = VERSION
        self.info["manufacturer"] = "telegraf2ha"

    def add_sensor(self, sensor_name):
        # To create the sensor name, also check for extra tags (for the case of disks for example)
        current_sensor = self.sensors.get(sensor_name)
        if current_sensor is None:
            current_sensor = sensor(self, sensor_name)
            self.sensors[sensor_name] = current_sensor
            return current_sensor, True

        return current_sensor, False


class sensor():
    def __init__(self, parent_host, name) -> None:
        self.name = name
        self.measurements = {}
        self.parent_host = parent_host

    def add_measurement(self, measurement_name):
        current_measurement = self.measurements.get(measurement_name)
        if current_measurement is None:
            current_measurement = measurement(self, measurement_name)
            self.measurements[measurement_name] = current_measurement
            return current_measurement, True
        
        return current_measurement, False

class measurement():    
    def __init__(self, parent_sensor, name) -> None:
        self.name = name
        self.parent_sensor = parent_sensor
        self.topic = f"{HA_PREFIX}/{self.parent_sensor.parent_host.name}/{self.parent_sensor.name}_{self.name}"

        config = {
            # "~": self.topic,
            "name": f"{self.parent_sensor.parent_host.name}_{self.parent_sensor.name[0:-3]}_{self.name}",
            "state_topic": f"{STATE_PREFIX}/{self.parent_sensor.parent_host.name}/{self.parent_sensor.name}/state",
            "unit_of_measurement": "",
            "device": self.parent_sensor.parent_host.info,
            "unique_id": f"{self.parent_sensor.parent_host.name}_{self.parent_sensor.name}_{self.name}",
            "platform": "mqtt",
            # Make the template such that we can use the telegraph topic straight
            "value_template": f"{{{{ value_json.{self.name} }}}}",
        }

        # If it is a new measumente, announce it to hassio
        self.parent_sensor.parent_host.parent_listener.transmit_callback(f"{self.topic}/config", json.dumps(config))
