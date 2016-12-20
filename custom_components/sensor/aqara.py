from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
import logging
import json

# DOMAIN = 'aqara'

_LOGGER = logging.getLogger(__name__)
SENSOR_TYPES = ['temperature', 'humidity']


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""

    # # get the gateway object from the hub component
    gateway = hass.data['AqaraGateway']
    devices = gateway.sidsData
    
    sensorItems = []
    for variable in SENSOR_TYPES:
        for device in devices:
            if device['model'] == 'sensor_ht':
                sensorItems.append(AqaraSensor(gateway, device['sid'], device['sid'], device['model'], variable,device['data']))

    if len(sensorItems)> 0:
        add_devices(sensorItems)
        return True
    else:
        return False

class AqaraSensor(Entity):
    """Representation of a Binary Sensor."""
    
    def __init__(self, aqaraGateway,deviceName,deviceSID,deviceModel,deviceVariable,deviceData):
        self.gateway = aqaraGateway
        self.deviceName = deviceName
        self.deviceSID = deviceSID
        self.deviceModel = deviceModel
        self.deviceVariable = deviceVariable
        self.uniqueID = '{} {}'.format(deviceVariable, deviceSID)

        self.gateway.register(self.uniqueID, self._update_callback)

        if deviceVariable == 'temperature':
            self._state = float(deviceData['temperature'])/100 
        elif deviceVariable == 'humidity': 
            self._state = float(deviceData['humidity'])/100 
        else:
            self._state = None

    def _update_callback(self, model,sid, cmd, data):
        if sid == self.deviceSID:
            self.pushUpdate(data)
        else:
            _LOGGER.error('Issue to update the sensor ',sid)

    @property
    def should_poll(self):
        """No polling needed for a demo light."""
        return False

    @property
    def unique_id(self):
        """Return the unique id"""
        return self.uniqueID

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.uniqueID

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        if self.deviceVariable == "temperature":
            return TEMP_CELSIUS
        elif self.deviceVariable == "humidity":
            return '%'

    def pushUpdate(self,data):
        if self.deviceVariable == 'temperature':
            if 'temperature' in data:
                self._state = float(data['temperature'])/100
        elif self.deviceVariable == 'humidity':
            if 'humidity' in data:
                self._state = float(data['humidity'])/100
        super().update_ha_state()