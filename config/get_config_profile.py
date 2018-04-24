from os import environ
from yaml import load



profile = environ.get("profile", "local")

print("loading {} profile".format(profile))

profile_path = '../config/' + profile + '.yaml'

conf = {}

try:
    with open(profile_path, 'r') as conf_file:
        conf = load(conf_file)
        # print(conf)
        print("Config loaded successfully")
except:
    print("Config profile not found, please check " + profile_path)
    exit(1)
