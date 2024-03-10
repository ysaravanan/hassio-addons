# hassio-router
This is a home assistant addon built on top of the linux-router from https://github.com/garywill/linux-router.

It uses its extensive script to bringup an access point, with several customizations and configurations possible, as provided by the linux-router project.
## Installation

To use this repository with your own Hass.io installation please follow [the official instructions](https://www.home-assistant.io/hassio installing_third_party_addons/) on the Home Assistant website with the following URL:

```txt
https://github.com/joaofl/hassio-addons
```

### Configuration

The available configuration options are as bellow. Make sure to edit
according to your needs:

```
{
    "ssid": "WIFI_NAME",
    "passphrase": "WIFI_PASS",
    "channel": "0",
    "address": "192.168.2.1",
    "interface": ""
    "allow_internet": false
    "hide_ssid": false
}

```
When channel set to 0, it will automatically find the best channel. 

When the `interface` option is left blank, a list with the detected wlan
interfaces will be printed on the logs and the addon will terminate. Set
the correct `interface` value on the configuration then restart the addon.
