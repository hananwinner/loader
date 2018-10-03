import yaml

publisher_config = None
loader_path = None
log_dict_config = None
interval_min = None
start_immediately = None


def create(config_file):
    global publisher_config
    global loader_path
    global log_dict_config
    global interval_min
    global start_immediately
    with open(config_file, "r") as fdr:
        config = yaml.load(fdr)
    publisher_config = config["publisher"]
    loader_path = config["loader"]["path"]
    log_dict_config = config["log"]
    interval_min = config["loader"]["interval_min"]
    start_immediately = config["loader"]["start_immediately"]
