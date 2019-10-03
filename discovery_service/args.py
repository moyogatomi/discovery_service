import argparse

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

args = parser.parse_args()
