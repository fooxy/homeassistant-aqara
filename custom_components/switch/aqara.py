from homeassistant.helpers.entity import Entity
from homeassistant.components.switch import SwitchDevice
from homeassistant.helpers.entity import ToggleEntity
import logging
import json

# DOMAIN = 'aqara'

_LOGGER = logging.getLogger(__name__)

# DEPENDENCIES = ['pyAqara']

SWITCH_TYPES = ['ONE_CLICK', 'DOUBLE_CLICK']

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""

    # # get the gateway object from the hub component
    gateway = hass.data['AqaraGateway']
    devices = gateway.sidsData

    sensorItems = []
    for variable in SWITCH_TYPES:
        for device in devices:
            if device['model'] == 'switch':
                sensorItems.append(AqaraSwitchSensor(gateway, device['sid'], device['sid'], device['model'],variable))

    if len(sensorItems)> 0:
        add_devices(sensorItems)
        return True
    else:
        return False

class AqaraSwitchSensor(ToggleEntity):
    """Representation of a Binary Sensor."""
    
    def __init__(self, aqaraGateway,deviceName,deviceSID,deviceModel,deviceVariable):
        self.gateway = aqaraGateway
        self.deviceName = deviceName
        self.deviceSID = deviceSID
        self.deviceModel = deviceModel
        self.deviceVariable = deviceVariable
        self.uniqueID = '{} {} {}'.format(deviceModel, deviceVariable, deviceSID)
        self._state = False
        
        self.gateway.register(self.deviceSID, self._update_callback)


    def _update_callback(self, model,sid, cmd, data):
        if sid == self.deviceSID:
            self.pushUpdate(model, data['status'])
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
    def sensor_class(self):
        """Return the class of this sensor, from SENSOR_CLASSES."""
        return self.deviceModel

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state
    
    def pushUpdate(self,model,status):
        if self.deviceVariable == 'ONE_CLICK':
            if status == 'click' and self._state == False:
                self._state = True
            else:
                self._state = False
        elif self.deviceVariable == 'DOUBLE_CLICK':
            if status == 'double_click' and self._state == False:
                self._state = True
            else:
                self._state = False
                
        super().update_ha_state()
