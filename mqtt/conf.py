from yaml import load

def load_config(path="./config.yml"):
    conf = {}
    with open(path, 'r') as conf_file:
        conf = load(conf_file)
    return conf
