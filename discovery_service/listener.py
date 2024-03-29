import time
import threading
import socket
import json
import argparse
import os
print(os.getcwd(),os.listdir('/'))
from discovery_service.args import args


Lock = threading.Lock()


class UDPBroadcast:
    broadcast_address = args.broadcast_address
    port = args.port
    buffer_multiplier = 10
    hostname = ""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((broadcast_address, port))

    def loop_forever(self):
        thread = threading.Thread(target=self._loop_forever)
        thread.daemon = True
        thread.start()

    def _loop_forever(self):
        counter = 0
        while True:
            payload = self.s.recvfrom(1024 * self.buffer_multiplier)
            counter += 1
            print(f"{counter} -- {payload}")

   


if __name__ == "__main__":
    from discovery_service import logmaster
    
    logger = logmaster.logger_obj("UDP listener", level=args.log)
    logger.info("Initialized sniffer")
    udp_sniff = UDPBroadcast()
    udp_sniff.loop_forever()

    while True:
        time.sleep(1)
