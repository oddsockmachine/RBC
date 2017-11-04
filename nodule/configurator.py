from yaml import load, dump
# try:
#     from yaml import CLoader as Loader, CDumper as Dumper
# except ImportError:
#     from yaml import Loader, Dumper

# Separate files used for each type of config
# Allows us to only write where necessary
conf_types = ['jobs', 'nodule', 'sensors', 'hardware', 'actuators']
conf_file_paths = {c: "./config/{}.yml".format(c) for c in conf_types}

def load_config_from_disk():
    """Load config in from storage.
    Should be called on startup."""
    config = {}
    for c, f in conf_file_paths.items():
        print("Loading config from {}".format(f))
        with open(f, 'r') as conf_file:
            conf = load(conf_file)
            config[c] = conf
    CONFIG = config
    return config

CONFIG = load_config_from_disk()

def write_config_to_disk(topic, conf):
    """Take a section of config and persist it to disk.
    Should be called whenever config is changed, to endure restarts."""
    if topic not in conf_types:
        raise Exception("Config type {} not valid, not writing".format(topic))
    conf_file_path = conf_file_paths[topic]
    with open(conf_file_path, 'w') as conf_file:
        dump(conf, conf_file)
    # Update the shared variable to avoid having to re-read from disk
    CONFIG[topic] = conf

if __name__ == '__main__':
    from pprint import pprint
    pprint(CONFIG)
