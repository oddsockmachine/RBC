# https://home-assistant.io/blog/2016/08/31/esp8266-and-micropython-part2/
# https://www.hackster.io/bucknalla/mqtt-micropython-044e77

import sys
from os import environ

lib_dirs = {'esp': './libs/esp/', 'rpi': './libs/rpi/', 'local': './libs/local'}



# sys.path.append(lib_dirs[target])

def auto():
    target = environ.get('TARGET')

    if not target:
        print("TARGET not set in environment.")
        print("Must be one of:")
        print(lib_dirs.keys())
        exit(1)
    if target not in lib_dirs.keys():
        print("Unknown target, must be one of:")
        print(lib_dirs.keys())
        exit(1)
    add_libs_to_path(target)
    return target

def set(target):
    add_libs_to_path(target)
    return target

def add_libs_to_path(target):
    sys.path.append(lib_dirs[target])
    return
