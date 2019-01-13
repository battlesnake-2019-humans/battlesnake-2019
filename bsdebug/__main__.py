import sys

from .showboard import showboard
from .sendstate import sendstate


cmd_string = sys.argv[1]

if cmd_string == "showboard":
    showboard(*sys.argv[1:])
elif cmd_string == "sendstate":
    sendstate(*sys.argv[1:])
else:
    print("Unrecognized command")
