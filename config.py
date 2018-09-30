import yaml

publisher_config = None
loader_path = None
log_dict_config = None


def create(config_file):
    global publisher_config
    global loader_path
    global log_dict_config
    with open(config_file, "r") as fdr:
        config = yaml.load(fdr)
    publisher_config = config["publisher"]
    loader_path = config["loader"]["path"]
    log_dict_config = config["log"]
