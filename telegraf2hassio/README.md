# Telegraf2Hassio

This addon will let you display Telegraf stats of a running instance directly on you Home Assistant dashboard, using self discoverable MQTT sensors.

Differently from most Telegraf integrations approaches out there, this addon does not need InfluxDB neither Grafana dashboards to display Telegraf's data.
Instead, it translates Telegraf's native MQTT messages into Home Assistant self-discoverable ones, such that it can detect and present your data with ease.

## Installation

To use this repository with your own Home Assistant setup please follow [the official instructions](https://www.home-assistant.io/common-tasks/supervised/#installing-third-party-add-ons) on how to configure it.

Below the link to this addons source code @github [https://github.com/joaofl/hassio-addons](https://github.com/joaofl/hassio-addons)

## Configuration

The available configuration options are as bellow. Make sure to edit
according to your setup:

```yaml
options:
  mqtt_broker: localhost
  mqtt_port: 1883
  mqtt_user: mqtt_user_here
  mqtt_pass: mqtt_pass_here
  telegraf_topic: telegraf/#
  calc_rate: host_sensor_measurement_1,host_sensor_measurement_2
  log_level: info
```

The `calc_rate` is an optional argument, but it allows to add calculated rate measurements on top of the measurements already provided by Telegraf.
For example, if you want know the data rate on a given ethernet port, then the `calc_rate` setting should look like below: 

```yaml
myserver_net_enp2s0_12_bytes_recv,nuvem_net_enp2s0_12_bytes_sent
```
where `myserver` is the Telegraf client name, `net` is the sensor name, `enp2s0_12` is the device name, followed by its unique ID (`12`), and finally the measurement name `bytes_sent`.
Having added the settings above to `calc_rate` (adapted to your setup names), another measurement will be announced via MQTT, with the same name ending with `_dt`, containing the calculated rate of change for that specific measurement. 
Multiple rate measurements can be added comma separated.

If you are not sure about the names to expect, start the addon, and check the logs after the first batch of data is received. It will show the host name, as well as of all sensors and measurements discovered.

## Example dashboard

Below an example dashboard I brought up real quick. I really hope to see some much cooler ones once some dedicated people start to play around with it.

![Example dashboard](https://github.com/joaofl/hassio-addons/blob/master/telegraf2hassio/resources/dashboard-example.png)

Find also the source code to it here: [example_dashboard.yaml](https://github.com/joaofl/hassio-addons/blob/master/telegraf2hassio/resources/example_dashboard.yaml)

And the corresponding Telegraf config on my server side: [telegraf.conf](https://github.com/joaofl/hassio-addons/blob/master/telegraf2hassio/resources/telegraf.conf)
Note that this is a reduced config file, only showing the uncommented lines of the original file by `cat /etc/telegraf/telegraf.conf | grep -v "#" | grep .`

It is likely that other addons and sensors may work out of the box with this addon, but I cannot guarantee, since this is the only config I tested so far. If something goes wrong, feel free to make a PR and contribute to this addon :)