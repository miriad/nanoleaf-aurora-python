#!/usr/bin/env python3


import sys
import argparse
from pprint import pprint

from aurora import Aurora

handlers = {}

def handler(function):
    handlers[function.__name__] = function
    return function

@handler
def get_info(aurora):
    pprint(aurora.get_info())

@handler
def get_effects(aurora):
    pprint(aurora.get_effects())

@handler
def get_auth_token(address, port):
    input("Hold the power button on the Aurora until the LED flashes in a pattern, then press enter")
    pprint(Aurora.get_auth_token(address, port))

@handler
def delete_auth_token(aurora):
    aurora.delete_auth_token()
    print("Token deleted")

@handler
def get_brightness(aurora):
    pprint(aurora.get_brightness())

@handler
def set_brightness(aurora, brightness):
    if type(brightness) == str and brightness[0] in ["-", "+"]:
        pprint(aurora.incrememnt_brightness(brightness))
    else:
        pprint(aurora.set_brightness(brightness))

@handler
def get_hue(aurora):
    pprint(aurora.get_hue())

@handler
def set_hue(aurora, hue):
    if type(hue) == str and hue[0] in ["-", "+"]:
        pprint(aurora.increment_hue(hue))
    else:
        pprint(aurora.set_hue(hue))
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Nanoleaf Aurora API Client")
    parser.add_argument('-a', '--address', help="Aurora  address", required=True, dest="address")
    parser.add_argument('-p', '--port', help="Aurora port", default=16021, type=int, dest="port")
    parser.add_argument('-A', '--auth_token', help="Aurora auth_token", required=False, dest="auth_token")
    parser.add_argument("command", help="Command", choices=handlers.keys(), default='get_info', nargs='?')
    parser.add_argument("arguments", help="Command arguments (optional)", nargs='*')
    args = parser.parse_args()

    if args.command == 'get_auth_token':
        handlers[args.command](args.address, args.port)
    else:
        a = Aurora(args.auth_token, args.address, port=args.port)

        handlers[args.command](a, *args.arguments)
