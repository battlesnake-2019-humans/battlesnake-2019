import sys

from .showboard import showboard


cmd_string = sys.argv[1] if len(sys.argv) > 1 else "showboard"

if cmd_string == "showboard":
    showboard(sys.argv[1:])
else:
    print("Unrecognized command")
