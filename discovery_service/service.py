import copy
import time
import ipaddress
import json
from socket import *
import threading
from discovery_service import logmaster
import os
from discovery_service import moyogatoming
from discovery_service.args import args
from collections import defaultdict
from discovery_service.utils import BroadcastAddress, UDPTools


lock = threading.Lock()
logger = logmaster.logger_obj("Discovery service")


# colors
reset = "\x1b[0m"
blue = "\x1b[0;49;44m"
red = "\x1b[0;49;41m"


class UDPBroadcast(UDPTools):
    broadcast_address = ""
    port = args.port
    buffer_multiplier = 10
    hostname = ""
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind((broadcast_address, port))

    def loop_forever(self):
        thread = threading.Thread(target=self._loop_forever)
        thread.daemon = True
        thread.start()

    def _loop_forever(self):
        counter = 0
        while True:
            payload = self.sock.recvfrom(1024 * self.buffer_multiplier)
            th = threading.Thread(
                target=self.accept, args=((self.unpack(payload), payload[1]),)
            )
            th.start()


class Discovery(UDPBroadcast):
    broadcast_address = ""
    port = args.port
    devices = defaultdict(type(None))
    period = args.heartbeat
    data = {}

    def __init__(self, id, ip="", broadcast_address=""):
        self.broadcast_address = broadcast_address
        self.id = id
        self.ip = ip
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    def accept(self, payload):
        ip = payload[1][0]
        payload = payload[0]
        if "type" in payload:
            if payload["type"] == "heartbeat":
                logger.info(f'Received heartbeat from {payload["id"]}')
                self.devices[payload["id"]] = {
                    "timestamp": payload["timestamp"],
                    "ip": ip,
                    "status": True,
                }

            if payload["type"] == "discovery":
                logger.info("sending Discovery data")
                self.reveal_discovery()
            if payload["type"] == "data":
                now = time.time()
                logger.info(f"device: {red}{ip}{reset}")
                for device in self.data:
                    if (self.data[device]["timestamp"] + args.diminish) < now and (
                        self.data[device]["timestamp"] + args.unregister
                    ) > now:
                        logger.info(
                            f"device: {red}{device}{reset} with ip: {self.data[device]['ip']} was last reached {now - self.data[device]['timestamp']} ago"
                        )
                    elif (self.data[device]["timestamp"] + args.unregister) < now:
                        logger.info(
                            f"device: {red}{device}{reset} with ip: {self.data[device]['ip']} is propably lost"
                        )
                    else:
                        logger.info(
                            f"device: {blue}{device}{reset} with ip: {self.data[device]['ip']} was reached {now - self.data[device]['timestamp']} ago"
                        )

        else:
            print(payload)

    def reveal_discovery(self):
        self._send({"type": "data", "devices": self.data})
        logger.info(f"Sending heartbeat")

    def heartbeat(self):
        self.send(
            {
                "type": "heartbeat",
                "id": self.id,
                "timestamp": time.time(),
                "ip": self.ip,
            }
        )
        logger.info(f"Sending heartbeat")


class Lighthouse(Discovery):
    def serve_forever(self):
        th = threading.Thread(target=self._serve_forever)
        th.daemon = True
        th.start()

    def _serve_forever(self):
        self.loop_forever()
        time.sleep(1.5)
        logger.info("Looking for devices")
        now = time.time()

        while True:
            time.sleep(self.period)
            self.heartbeat()
            if time.time() - now < 30:
                now = time.time()
                self.data = copy.deepcopy(self.devices)
                for device in self.data:
                    if (self.data[device]["timestamp"] + args.diminish) < now and (
                        self.data[device]["timestamp"] + args.unregister
                    ) > now:
                        logger.info(
                            f"device: {red}{device}{reset} with ip: {self.data[device]['ip']} was last reached {now - self.data[device]['timestamp']} ago"
                        )
                    elif (self.data[device]["timestamp"] + args.unregister) < now:
                        logger.info(
                            f"device: {red}{device}{reset} with ip: {self.data[device]['ip']} is being UNREGISTERED"
                        )
                    else:
                        logger.info(
                            f"device: {blue}{device}{reset} with ip: {self.data[device]['ip']} was reached {now - self.data[device]['timestamp']} ago"
                        )
                with lock:
                    self.devices = self.data
                print(self.data)

def cli():
    try:
        ip, bca = 'Unknown' , args.broadcast_address #BroadcastAddress.bca_awk()[0]
    except:
        raise ValueError('Propably no broadcast found')

    service = Lighthouse(id=moyogatoming.manage_nickname(args.id), ip=ip, broadcast_address=bca)
    service.serve_forever()
    while True:
        time.sleep(1)

if __name__ == '__main__':
    try:
        ip, bca = BroadcastAddress.bca_awk()[0]
    except:
        raise ValueError('Propably no broadcast found')

    service = Lighthouse(id=moyogatoming.manage_nickname(), ip=ip, broadcast_address=bca)
    service.serve_forever()
    while True:
        time.sleep(1)
