import json
import requests
from .crashfile import CrashFile


def sendstate(*args):
    with open(args[1], 'r') as crashfile:
        crash = CrashFile.from_json(json.load(crashfile)[0])

    snake_url = args[2]

    print("POSTing state to %s..." % snake_url)
    resp = requests.post(snake_url + "/move", json=crash.state.dump_state_json())
    print("Got response code %d" % resp.status_code)
