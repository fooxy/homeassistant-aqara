from homeassistant.helpers.entity import Entity
from homeassistant.components.binary_sensor import BinarySensorDevice
import logging
import json

# DOMAIN = 'aqara'

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""

    # # get the gateway object from the hub component
    gateway = hass.data['AqaraGateway']
    devices = gateway.sidsData

    sensorItems = []
    for device in devices:
        if device['model'] in ['motion', 'magnet']:
            sensorItems.append(AqaraBinarySensor(gateway, device['sid'], device['sid'], device['model'],device['data']))

    if len(sensorItems)> 0:
        add_devices(sensorItems)
        return True
    else:
        return False

class AqaraBinarySensor(BinarySensorDevice,Entity):
    """Representation of a Binary Sensor."""
    
    def __init__(self, aqaraGateway,deviceName,deviceSID,deviceModel,deviceData):
        self.gateway = aqaraGateway
        self.deviceName = deviceName
        self.deviceSID = deviceSID
        self.deviceModel = deviceModel
        self.deviceData = deviceData
        self.uniqueID = '{} {}'.format(deviceModel,deviceSID)

        self.gateway.register(self.deviceSID, self._update_callback)

        status = deviceData['status']
        if deviceModel == 'magnet':
            if status =='open':
                self._state = True
            else:
                self._state = False
        elif deviceModel == 'motion': 
            if status =='motion':
                self._state = True
            else:
                self._state = False
        else:
            self._state = False

    def _update_callback(self, model,sid, cmd, data):
        if sid == self.deviceSID:
            if 'status' in data:
                self.pushUpdate(model, data['status'])

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
    def sensor_class(self):
        """Return the class of this sensor, from SENSOR_CLASSES."""
        if self.deviceModel == 'motion':
            return 'motion'
        elif self.deviceModel == 'magnet':
            return 'opening'

    @property
    def is_on(self):
        """Return true if binary sensor is on."""
        return self._state
    
    def pushUpdate(self,model,status):
        if model == 'magnet':
            if status =='open':
                self._state = True
            else:
                self._state = False
        elif model == 'motion':
            if status =='motion':
                self._state = True
            else:
                self._state = False
                
        super().update_ha_state()
