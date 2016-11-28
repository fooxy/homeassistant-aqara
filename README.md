# homeassistant-aqara
Home-Assistant custom component

Compatible with temperature and humidity sensors

### Installation
1. Install Home-Assistant,
2. Enable the developer mode of the gateway.
 - Please follow the steps in this thread: http://bbs.xiaomi.cn/t-13198850. 
It's in Chinese so you might need a translator to read it.
3. Download and place the Aqara.py file in the home-assistant folder like so:

    `.homeassistant/custom_components/sensor/Aqara.py`

4. Customize the Aqara.py file with your sensor Ids:
 - Example

    ```python
    devices = [
    {"name":"Living-room","id":"XYXYXYXYX"},
    {"name":"Bedroom 1","id":"XYXYXYXYX"},
    {"name":"Bedroom 2","id":"XYXYXYXYX"},
    {"name":"Bedroom 3","id":"XYXYXYXYX"},
    {"name":"Outdoor West","id":"XYXYXYXYX"},
    {"name":"Outdoor East","id":"XYXYXYXYX"}
    ] 
 ```

5. Customize the IP in the pyAqara/__init.__.py

  `.homeassistant/deps/pyAqara/__init__.py`

5. Add the new component in the configuration.yaml:

    ```yaml
    sensor :
      platform: Aqara
    ```

### TODO

 - create a custom component as Hub to manage sensors, swith, etc.
 - include in the configuration file some options : IP, refresh frequency, etc.
 - generate a yaml file with discovered devices
 - integrate motion and contact sensor
 - etc.
