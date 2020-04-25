# hassio-hostapd-mod
Raspberry Pi as hotspot in hass.io

It adds the capability of using USB ralink and other wifi dongles to create an access point to your IoT devices

It is a for of the original hostapd addon, that adds support to external USB dongles. Mainly in order to allow
some stable access point, given that the broadcomm embedded on the rpi is unstable.

### This Hass.io Addon

This add-on allows you  to use the Raspberry Pi as a hotspot to connect the different devices directly to the `hass.io` network without going through the router.

## Installation

To use this repository with your own Hass.io installation please follow [the official instructions](https://www.home-assistant.io/hassio/installing_third_party_addons/) on the Home Assistant website with the following URL:

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
If the interface is left blank, a list with 
the available ones will be printed on the logs

**Note**: _This is just an example, don't copy and paste it! Create your own!_