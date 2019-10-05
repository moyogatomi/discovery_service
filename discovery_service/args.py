import argparse
import os
parser = argparse.ArgumentParser(description="Discovery service arguments")
parser.add_argument('typeargs',nargs='*')
parser.add_argument("--heartbeat", help="frequency of heartbeats", type=int, default=30)
parser.add_argument(
    "--diminish", help="timeout warning for device", type=int, default=120
)
parser.add_argument(
    "--unregister",
    help="device unregister because didnt responded for timeout",
    type=int,
    default=240,
)
parser.add_argument("--port", help="broadcast port", type=int, default=6565)
parser.add_argument("--broadcast_address", help="broadcast addr", type=str, default='')
parser.add_argument("--log", help="report", type=str, default='INFO')
parser.add_argument("--id", help="discovery name", type=str, default='')
parser.add_argument("--m", help="Telegram", type=str, default='')
parser.add_argument("--docker", help="Telegram", type=str, default='0')






args = parser.parse_args()


args.typeargs = os.environ.get("TYPE",args.typeargs)
args.heartbeat = int(os.environ.get("HEARTBEAT",args.heartbeat))
args.diminish = int(os.environ.get("DIMINISH",args.diminish))
args.unregister = int(os.environ.get("UNREGISTER",args.unregister))
args.port = int(os.environ.get("PORT",args.port))
args.broadcast_address = os.environ.get("BROADCAST_ADDRESS",args.broadcast_address)
args.log = os.environ.get("LOG",args.log)
args.id = os.environ.get("ID",args.id)
args.m = os.environ.get("M",args.m)
args.docker = int(os.environ.get("DOCKER",args.docker))

print(args,flush=True)
