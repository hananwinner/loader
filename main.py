from pika_client.factory import create_persistent_async_publisher
import config
import logging
import logging.config
import csv
import sys
from utils.repeated_timer import RepeatedTimer


def parse_line(line):
    final_parts = list(csv.reader([line]))[0]
    sku = final_parts[3]
    try:
        sku = int(float(sku))
    except ValueError:
        raise ValueError("SKU is empty")
    return {
        "product_name": final_parts[0],
        "photo_url": final_parts[1],
        "barcode": int(float(final_parts[2])) if final_parts[2] != "" else "",
        "sku": int(float(final_parts[3])),
        "price_cents": int(float(final_parts[4]))if final_parts[4] != "" else "",
        "producer": final_parts[5]
    }


def operation():
    publisher = create_persistent_async_publisher(config.publisher_config["connection"],
                                                  config.publisher_config["route"],
                                                  exchange=config.publisher_config["route"]["exchange"],
                                                  routing_key=config.publisher_config["route"]["routing_key"]
                                                  , log=log)
    publisher.start()
    l_idx = 0
    log.info("start reading lines")
    with open(config.loader_path, "r") as fdr:
        fdr.readline()
        for line in fdr:
            log.info("line {}: {}".format(l_idx, line))
            l_idx +=1
            try:
                doc = parse_line(line)
                publisher.send(doc)
            except:
                log.exception("{} {}".format(l_idx, line))
    log.info("flushing and stopping publisher")
    publisher.flush()
    publisher.stop()


if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config/config.yaml"

    config.create(config_path)

    logging.config.dictConfig(config.log_dict_config)
    log = logging.getLogger("loader")

    timer = RepeatedTimer(operation, config.interval_min * 60, start_immediately=True)
    timer.start()
    timer.join()



