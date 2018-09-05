import yaml

publisher_config = None
loader_path = None


def create(config_file):
    global publisher_config
    global loader_path
    with open(config_file, "r") as fdr:
        config = yaml.load(fdr)
    publisher_config = config["publisher"]
    loader_path = config["loader"]["path"]
