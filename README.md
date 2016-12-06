# homeassistant-aqara
Home-Assistant custom component

Compatible with temperature and humidity sensors

### INSTALLATION
1. Install Home-Assistant,
2. Enable the developer mode of the gateway.
 - Please follow the steps in this thread: http://bbs.xiaomi.cn/t-13198850 (translated version: https://goo.gl/gEVIrn).
3. Download and place the Aqara.py and pyAqara/__init__.py file in the home-assistant folder like this:

    `.homeassistant/custom_components/sensor/Aqara.py`
    `.homeassistant/custom_components/sensor/Aqara.py`

4. Add the new component in the configuration.yaml:

    ```yaml
    sensor :
      platform: Aqara
      scan_interval: 1
    ```

### CUSTOMIZATION

Since until now there is no way to retrieve the configured names from the
gateway, Home-Assistant will display each sensor like that:
 - sensor.temperature_158d0000fa3793
 - sensor.humidity_158d0000fa3793
 - etc.

To make it readable again, create a customize.yaml file in the home-assistant folder.
You can use step 7 https://goo.gl/gEVIrn to identify the sensors.

 - Example

    ```yaml
     sensor.temperature_158d0000fa3793:
       friendly_name: Living-Room T
     sensor.humidity_158d0000fa3793:
       friendly_name: Living-Room H
       icon: mdi:water-percent

     sensor.temperature_158d000108164f:
       friendly_name: Bedroom 1 T
     sensor.humidity_158d000108164f:
       friendly_name: Bedroom 1 H
       icon: mdi:water-percent

       ... etc.
    ```

5. Add a line in the configuration.yaml:

    ```yaml
homeassistant:
  # Name of the location where Home Assistant is running
   name: Home
...
   time_zone: Europe/Paris
   customize: !include customize.yaml
    ```

### TODO

 - create a custom component as Hub to manage gateway devices.
 - include in the configuration file some options : IP, refresh frequency, etc.
 - generate a yaml file with discovered devices
 - integrate wireless switch, light switches, cube, plug, gateway itself (turn on light / radio / etc.)
