
import pickle
import sys
import json


def unpickle_traceback(tb_str):
    """Traceback object is pickled and stored as Base64 in json."""
    tb_pickled = tb_str.encode("ASCII")
    return pickle.loads(tb_pickled)


with open(sys.argv[1]) as crash_file:
    crash_data = json.load(crash_file)

# Use 0th crash for now. Add support for more tracebacks later...
crash = crash_data[0]

# TODO: use tblib to serialize/unserialize tracebacks?
trace = crash["trace"]
print(trace)
