from homeassistant.components.discovery import load_platform
from homeassistant.const import (EVENT_HOMEASSISTANT_START,
                                 EVENT_HOMEASSISTANT_STOP)
from homeassistant.helpers.entity import Entity

import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'aqara'

REQUIREMENTS = ['https://github.com/fooxy/homeassisitant-pyAqara/archive/v0.41-alpha.zip#pyAqara==0.41']

AQARA_COMPONENTS = [
    'sensor','binary_sensor','switch'
]

def setup(hass, config):
    """Your controller/hub specific code."""

    from pyAqara.gateway import AqaraGateway
    gateway = AqaraGateway()   
    gateway.initGateway()
    gateway.listen(timeout=5)

    hass.data['AqaraGateway']= gateway

    def _stop(event):
        """Stop the listener queue and clean up."""
        print('stop event')
        nonlocal gateway
        gateway.stop()
        gateway = None
        _LOGGER.info("Waiting for long poll to Aqara Gateway to time out")

    hass.bus.listen(EVENT_HOMEASSISTANT_STOP, _stop)

    for component in AQARA_COMPONENTS:
        load_platform(hass, component, DOMAIN, {}, config)

    return True