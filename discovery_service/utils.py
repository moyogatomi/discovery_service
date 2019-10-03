from socket import *
import json
import os
import time
import threading


class BroadcastAddress:
    @staticmethod
    def bca_awk():
        broadcasts_raw = (
            os.popen("ifconfig | awk '/broadcast/ {print $2,\"|\",$6}'")
            .read()
            .split("\n")
        )
        broadcasts_raw = [i.split("|") for i in broadcasts_raw if i]
        broadcasts = [(ip.strip(), bca.strip()) for ip, bca in broadcasts_raw]
        return broadcasts

    @staticmethod
    def get_broadcast_address(ifconfig):
        IP = ifconfig[0]
        MASK = ifconfig[1]

        host = ipaddress.IPv4Address(IP)
        net = ipaddress.IPv4Network(IP + "/" + MASK, False)
        print("IP:", IP)
        print("Mask:", MASK)
        print("Subnet:", ipaddress.IPv4Address(int(host) & int(net.netmask)))
        print("Host:", ipaddress.IPv4Address(int(host) & int(net.hostmask)))
        print("Broadcast:", net.broadcast_address)
        return str(net.broadcast_address)


class UDPTools:
    broadcast_address = ""
    port = 12345
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    def unpack(self, payload):
        return json.loads(payload[0].decode("utf-8"))

    def pack(self, payload):
        return bytes(json.dumps(payload), "utf-8")

    def _send(self, payload, slowdown=0.005):
        self.s.sendto(self.pack(payload), (self.broadcast_address, self.port))
        time.sleep(slowdown)

    def send(self, payload):
        threading.Thread(target=self._send, args=(payload,)).start()

    


