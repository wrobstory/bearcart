"""For compatibility between Python 2 & 3"""
import sys

PY2 = sys.version_info[0] == 2

def iteritems(d):
    if PY2:
        return d.iteritems()
    else:
        return iter(d.items())

