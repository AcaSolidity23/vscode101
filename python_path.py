import os
import sys

try:
    user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
    for p in sys.path:
        p=p.replace('\\\\','\\')
        print(p)
except KeyError:
    user_paths = []
