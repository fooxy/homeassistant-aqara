from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from datetime import timedelta
from datetime import datetime
# from homeassistant.components.sensor import PLATFORM_SCHEMA

import logging
import json
import socket

DOMAIN = 'Aqara'

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['https://github.com/fooxy/homeassisitant-pyAqara/archive/v0.2-alpha.zip#pyAqara==0.2']
SENSOR_TYPES = ['temperature', 'humidity']

# Return cached results if last scan was less then this time ago
MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=1)

def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Setup the sensor platform."""
        
    _LOGGER.info("Setting Up the Platform")
    
    devices = []
    sensorItems = []

    import pyAqara
    gateway = pyAqara.AqaraGateway()
    devicesList = gateway.get_devicesList()

    #magnet / motion / sensor_ht
    for deviceSID in devicesList:
        model = gateway.get_model(deviceSID)
        if model == 'sensor_ht':
            devices.append({"name":deviceSID,"id":deviceSID})

    try:
        aqaraData = AqaraData()   
    except:
        return False

    for variable in SENSOR_TYPES:
        for device in devices:
            sensorItems.append(HTSensor(aqaraData,device['name'], device['id'],variable))

    add_devices_callback(sensorItems)
    return True

class HTSensor(Entity):
    """Representation of a Sensor."""
    
    def __init__(self, deviceData,deviceName,deviceID,sensor_type):
        self.deviceData = deviceData
        self._state = None
        self.deviceName = deviceName
        self.deviceID = deviceID
        self.type = sensor_type

        self.update()

    @property
    def should_poll(self):
        """No polling needed for a demo light."""
        return True

    # @property
    # def unique_id(self):
    #      return self.deviceID

    @property
    def name(self):
        """Return the name of the sensor."""
        if self.type == "temperature":
            return '{} {}'.format(self.type, self.deviceName)
        elif self.type == "humidity":
            return '{} {}'.format(self.type, self.deviceName)

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        # return TEMP_CELSIUS
        if self.type == "temperature":
            return TEMP_CELSIUS
        elif self.type == "humidity":
            return '%'

    # @property
    # def force_update(self) -> bool:
    #     """Return True if state updates should be forced.
    #     If True, a state change will be triggered anytime the state property is
    #     updated, not just when the value changes.
    #     """
    #     return True

    def update_ha_state(self):
        # Update Home Assistant with current state of entity.
        # If force_refresh == True will update entity before setting state.
        return True

    def update(self):
        """ Gets the latest data and updates the state. """

        try:
            self.deviceData.data = None
            self.deviceData.SID = self.deviceID
            self.deviceData.variable = self.type
            self.deviceData.update()
        except:
            _LOGGER.error("Aqara Entity Failed to Update the device %s, %s",self.deviceName, self.deviceID)
        
        updatedValue = self.deviceData.data
        if updatedValue is not None:
            self._state = updatedValue

    ############################################################################
    #                                                                          #
    #                            HT SENSOR DATA                                #
    #                                                                          #
    ############################################################################

class AqaraData(object):
    """Get data from the Bbox."""

    def __init__(self):
        """Initialize the data object."""
        self.data = None
        self.SID = None
        self.variable = None

    # @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data from the Bbox."""
        
        import pyAqara
        try:  
            gateway = pyAqara.AqaraGateway()
            if self.variable == "temperature":
                self.data = gateway.get_temperature(self.SID)
            elif self.variable =="humidity":
                self.data = gateway.get_humidity(self.SID)
        except :
            self.data = None
            _LOGGER.error("Aqara Data Failed to get data from the device %s", self.deviceID)