############################################################################
#                                                                          #
#                            SUPPORT FOR GATEWAY                           #
#                                                                          #
############################################################################

import socket
import json
import logging

_LOGGER = logging.getLogger(__name__)


class AqaraGateway:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocketMulitcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    gatewayIp = ''
    gatewayPort = ''
    gatewaySid = ''
    multicastAddress = '224.0.0.50'
    multicastPort = 4321

    def __init__(self):
        self.data = None

    def socketSendMulticastMsg(self, cmd):
        ip = self.multicastAddress
        port = self.multicastPort
        sSocket = self.serverSocketMulitcast

        try:
            sSocket.settimeout(5.0)
            sSocket.sendto(cmd.encode(), (ip, port))
            sSocket.settimeout(5.0)
            # buffer size is 1024 bytes / s.recv() for TCP
            recvData, addr = sSocket.recvfrom(1024)
            if len(recvData) is not None:
                decodedJson = recvData.decode()
            else:
                _LOGGER.error("no response from gateway")
                recvData = None
        except socket.timeout:
            _LOGGER.error(
                "Timeout on socket - Failed to connect the ip %s", ip)
            return None
            sSocket.close()

        if recvData is not None:
            try:
                jsonMsg = json.loads(decodedJson)
                if jsonMsg['cmd'] == "iam":
                    return jsonMsg
                else:
                    _LOGGER.info("Got unknown response: %s", decodedJson)
            except:
                _LOGGER.error("Aqara Gateway Failed to manage the json")
        else:
            return None

    def socketSendMsg(self, cmd):
        ip = self.gatewayIp
        port = self.gatewayPort
        sSocket = self.serverSocket
        try:
            sSocket.settimeout(5.0)
            sSocket.sendto(cmd.encode(), (ip, port))
            sSocket.settimeout(5.0)
            # buffer size is 1024 bytes / s.recv() for TCP
            recvData, addr = sSocket.recvfrom(1024)
            if len(recvData) is not None:
                decodedJson = recvData.decode()
            else:
                _LOGGER.error("no response from gateway")
                recvData = None
        except socket.timeout:
            _LOGGER.error(
                "Timeout on socket - Failed to connect the ip %s", ip)
            return None
            sSocket.close()

        if recvData is not None:
            try:
                jsonMsg = json.loads(decodedJson)
                if jsonMsg['cmd'] == "get_id_list":
                    return json.loads(jsonMsg['data'])
                elif jsonMsg['cmd'] == "get_id_list_ack":
                    devices_SID = json.loads(jsonMsg['data'])
                    return devices_SID
                elif jsonMsg['cmd'] == "read_ack":
                    return jsonMsg
                else:
                    _LOGGER.info("Got unknown response: %s", decodedJson)
            except:
                _LOGGER.error("Aqara Gateway Failed to manage the json")
        else:
            return None

    def initGateway(self):
        # Send WhoIs in order to get gateway data
        resp = self.get_whois()
        self.gatewayIp = resp['ip']
        self.gatewayPort = int(resp['port'])
        self.gatewaySid = resp['sid']

    def get_whois(self):
        cmd = '{"cmd":"whois"}'
        resp = self.socketSendMulticastMsg(cmd)
        return resp

    def get_devicesList(self):
        cmd = '{"cmd":"get_id_list"}'
        resp = self.socketSendMsg(cmd)
        return resp

    def get_read(self, SID):
        cmd = '{"cmd":"read", "sid":"' + SID + '"}'
        resp = self.socketSendMsg(cmd)
        return resp

    def get_status(self, SID):
        cmd = '{"cmd":"read", "sid":"' + SID + '"}'
        resp = self.socketSendMsg(cmd)
        return json.loads(resp['data'])['status']

    def get_switchstatus(self, SID):
        cmd = '{"cmd":"read", "sid":"' + SID + '"}'
        resp = self.socketSendMsg(cmd)
        _LOGGER.info("switch response: %s", resp)
        return json.loads(resp['data'])['status']

    def get_temperature(self, SID):
        cmd = '{"cmd":"read", "sid":"' + SID + '"}'
        resp = self.socketSendMsg(cmd)
        temperature = json.loads(resp['data'])['temperature']
        return float(temperature) / 100

    def get_humidity(self, SID):
        cmd = '{"cmd":"read", "sid":"' + SID + '"}'
        resp = self.socketSendMsg(cmd)
        humidity = json.loads(resp['data'])['humidity']
        return float(humidity) / 100
