from homeassistant.helpers.entity import Entity
from homeassistant.components.switch import SwitchDevice
from homeassistant.helpers.entity import ToggleEntity
import logging
import json
import binascii
iv = bytes.fromhex('17996d093d28ddb3ba695a2e6f58562e')

# DOMAIN = 'aqara'

_LOGGER = logging.getLogger(__name__)

# DEPENDENCIES = ['pyAqara']
REQUIREMENTS = ['pyCrypto']

SWITCH_TYPES = ['ONE_CLICK', 'DOUBLE_CLICK', 'LONG_PRESS']

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    # # get the gateway object from the hub component
    gateway = hass.data['AqaraGateway']
    devices = gateway.sidsData

    switchItems = []
    for variable in SWITCH_TYPES:
        for device in devices:
            if device['model'] == 'switch':
                switchItems.append(AqaraSwitchSensor(gateway, device['sid'], device['sid'], device['model'],variable))

    for device in devices:
        if 'ctrl_neutral' in device['model']:
            for channel in device['data']:
                switchItems.append(AqaraWallSwitch(gateway, device['sid'], device['sid'], device['model'],channel))
        elif device['model']=='plug':
            switchItems.append(PlugSwitch(gateway, device['sid'], device['sid'], device['model']))

    if len(switchItems)> 0:
        add_devices(switchItems)
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


    def _update_callback(self, model, sid, cmd, data):
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

#    @property
#    def sensor_class(self):
#       """Return the class of this sensor, from SENSOR_CLASSES."""
#        return self.deviceModel

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    def turn_on(self):
        self._state = True
        super().update_ha_state()

    def turn_off(self):
        self._state = False
        super().update_ha_state()

    def pushUpdate(self,model,status):
        if self.deviceVariable == 'ONE_CLICK':
            if status == 'click':
                self._state = not self._state
        elif self.deviceVariable == 'DOUBLE_CLICK':
            if status == 'double_click':
                self._state = not self._state
        elif self.deviceVariable == 'LONG_PRESS':
            if status == 'long_click_press' and self._state == False:
                self._state = True
            elif status == 'long_click_release':
                self._state = False

        super().update_ha_state()

    def update(self):
        pass

class AqaraWallSwitch(ToggleEntity):
    """Representation of a Binary Sensor."""

    def __init__(self, aqaraGateway,deviceName,deviceSID,deviceModel,deviceChannel):
        self.gateway = aqaraGateway
        self.deviceName = deviceName
        self.deviceSID = deviceSID
        self.deviceModel = deviceModel
        self.deviceChannel = deviceChannel
        self.uniqueID = '{} {} {}'.format(deviceModel, deviceChannel, deviceSID)
        self._state = False

        self.gateway.register(self.deviceSID, self._update_callback)

    def _update_callback(self, model,sid, cmd, data):
        if sid == self.deviceSID:
            self.pushUpdate(model, data)
        else:
            _LOGGER.error('Issue to update the sensor ',sid)

    @property
    def should_poll(self):
        """No polling needed for a demo light."""
        return True

    @property
    def unique_id(self):
        """Return the unique id"""
        return self.uniqueID

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.uniqueID

#    @property
#    def sensor_class(self):
#        """Return the class of this sensor, from SENSOR_CLASSES."""
#        return self.deviceModel

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    def turn_on(self):
        self._turn_switch('on')

    def turn_off(self):
        self._turn_switch('off')

    def _turn_switch(self,state):

        from Crypto.Cipher import AES

        password = self.gateway.password
        if password=='':
            _LOGGER.error('Please add "gateway_password:" config under the "aqara: " in config.yaml ')
            return

        token = self.gateway.GATEWAY_TOKEN

        cipher = AES.new(password, AES.MODE_CBC, iv)
        key = binascii.hexlify(cipher.encrypt(token))
        key = key.decode('ascii')

        commandDict = {"cmd":"write","model":self.deviceModel,"sid":self.deviceSID,"data":{}}
        commandDict["data"][self.deviceChannel] = state
        commandDict["data"]["key"] = key

        self.gateway.socketSendMsg(json.dumps(commandDict))


    def pushUpdate(self,model,data):
        if self.deviceChannel in data:
            if data[self.deviceChannel] == 'on':
                self._state = True
            else:
                self._state = False

            super().update_ha_state()

    def update(self):
        self.gateway.socketSendMsg('{"cmd":"read", "sid":"' + self.deviceSID + '"}')

class PlugSwitch(ToggleEntity):

    def __init__(self, aqaraGateway,deviceName,deviceSID,deviceModel):
        self.gateway = aqaraGateway
        self.deviceName = deviceName
        self.deviceSID = deviceSID
        self.deviceModel = deviceModel
        self.uniqueID = '{} {}'.format(deviceModel, deviceSID)
        self._state = False

        self.gateway.register(self.deviceSID, self._update_callback)

    def _update_callback(self, model, sid, cmd, data):
        if sid == self.deviceSID:
            self.pushUpdate(model, data)
        else:
            _LOGGER.error('Issue to update the sensor ',sid)

    @property
    def should_poll(self):
        """No polling needed for a demo light."""
        return True

    @property
    def unique_id(self):
        """Return the unique id"""
        return self.uniqueID

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.uniqueID

    @property
    def icon(self):
       return 'mdi:power-plug'

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    def turn_on(self):
        self._turn_switch('on')

    def turn_off(self):
        self._turn_switch('off')

    def _turn_switch(self,state):

        from Crypto.Cipher import AES

        password = self.gateway.password
        if password=='':
            _LOGGER.error('Please add "gateway_password:" config under the "aqara: " in config.yaml ')
            return

        token = self.gateway.GATEWAY_TOKEN

        cipher = AES.new(password, AES.MODE_CBC, iv)
        key = binascii.hexlify(cipher.encrypt(token))
        key = key.decode('ascii')

        commandDict = {"cmd":"write","model":self.deviceModel,"sid":self.deviceSID,"data":{}}
        commandDict["data"]["status"] = state
        commandDict["data"]["key"] = key

        self.gateway.socketSendMsg(json.dumps(commandDict))

    def pushUpdate(self,model,data):
        if "status" in data:
            if data["status"] == 'on':
                self._state = True
            else:
                self._state = False

            super().update_ha_state()

    def update(self):
        self.gateway.socketSendMsg('{"cmd":"read", "sid":"' + self.deviceSID + '"}')
