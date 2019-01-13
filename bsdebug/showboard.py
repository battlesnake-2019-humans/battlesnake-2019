import json

from .crashfile import CrashFile
from .board import BoardGraph


def showboard(*args):
    with open(args[1], 'r') as crashfile:
        crash = CrashFile.from_json(json.loads(crashfile))

    # TODO: use tblib to serialize/unserialize tracebacks?
    print(crash.trace)

    graph = BoardGraph(crash.state)
    graph.show()
