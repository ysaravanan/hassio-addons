# hassio-hostapd-extended
Enables an access point using USB Wifi dongle for your IoT devies on Home Assistant.

It has the capability of using **USB Ralink and other wifi dongles** to create an access point to your IoT devices. It is a fork of the original hostapd addon (`https://github.com/davidramosweb/hassio-addons`), that adds support to external USB dongles in order to allow some stable access point, given that the Broadcomm embedded on the rpi is has unstable operation and does not provide the reliability needed.

### This Hass.io Addon

This add-on allows you to use your Wifi connection as an access point to connect your different devices directly to Hassio network without access to the internet, without the need of a router.

## Installation

To use this repository with your own Hass.io installation please follow [the official instructions](https://www.home-assistant.io/hassio installing_third_party_addons/) on the Home Assistant website with the following URL:

```txt
https://github.com/joaofl/hassio-addons
```

### Configuration

The available configuration options are as follows (this is filled in with some example data):

```
{
    "ssid": "WIFI_NAME",
    "wpa_passphrase": "WIFI_PASSWORD",
    "channel": "6",
    "address": "192.168.99.1",
    "netmask": "255.255.255.0",
    "broadcast": "192.168.99.254"
    "interface": ""
}
```
Set channel to 0 for automatically finding channels. 

If the interface is left blank, a list with 
the available ones will be printed on the logs
to choose from.

**Note**: _This is just an example, don't copy and paste it! Create your own!_
