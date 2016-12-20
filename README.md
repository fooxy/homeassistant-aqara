# homeassistant-aqara
Home-Assistant implementation for the Xiaomi (Aqara) gateway
Supported sensors:
  - Temperature / Humidity
  - Magnet (Door / Window)
  - Motion

### INSTALLATION
1. Install Home-Assistant,
2. Enable the developer mode of the gateway.
 - Please follow the steps in the wiki:
 https://github.com/fooxy/homeassistant-aqara/wiki/Enable-dev-mode
3. Download and place aqara.py files in the home-assistant folder like this:

    `.homeassistant/custom_components/aqara.py
    .homeassistant/custom_components/sensor/aqara.py
    .homeassistant/custom_components/binary_sensor/aqara.py`

4. Add the new component in the configuration.yaml:
lowcase is important

    ```yaml
    sensor :
      platform: aqara
    ```

### CUSTOMIZATION

Since until now there is no way to retrieve the configured names from the
gateway, Home-Assistant will display each sensor like that:
 - sensor.temperature_SENSORID
 - sensor.humidity_SENSORID
 - sensor.magnet_SENSORID
 - sensor.motion_SENSORID
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

### Magnet Automation example

 - Example configuration.yaml

 ```yaml
 binary_sensor:
   - platform: template
     sensors:
       door:
         friendly_name: Frontdoor
         value_template: "{{ states.sensor.magnet_158d0001179ae9.state == 'open' }}"
         sensor_class: opening
         entity_id:
             - sensor.magnet_158d0001179ae9

automation:
  - alias: FrontDoorClosed
    trigger:
      platform: state
      entity_id: binary_sensor.door
      to: 'off'
    action:
      service: notify.TelegramNotifier
      data:
       message: Door closed
  - alias: FrontDoorOpened
    trigger:
      platform: state
      entity_id: binary_sensor.door
      to: 'on'
    action:
      service: notify.TelegramNotifier
      data:
       message: Door opened
 ```


### TODO

 - create a custom component as Hub to manage gateway devices.
 - include some options in the configuration file : IP, refresh frequency, etc.
 - generate a yaml file with discovered devices
 - integrate wireless switch, light switches, cube, plug, gateway itself (turn on light / radio / etc.)
