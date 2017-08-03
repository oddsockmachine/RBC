# https://home-assistant.io/blog/2016/08/31/esp8266-and-micropython-part2/
# https://www.hackster.io/bucknalla/mqtt-micropython-044e77

import sys
from os import environ

libs = {'esp': './libs/esp/', 'rpi': './libs/rpi/', 'local': './libs/local'}

target = environ.get('TARGET')

if not target:
    print("TARGET not set in environment.")
    print("Must be one of:")
    print(libs.keys())
    exit(1)
if target not in libs.keys():
    print("Unknown target, must be one of:")
    print(libs.keys())
    exit(1)

sys.path.append(libs[target])
