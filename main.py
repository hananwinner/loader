from pika_client.factory import create_persistent_async_publisher
import config
import logging
import logging.config
import csv


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


if __name__ == "__main__":

    config.create("config/config.yaml")

    logging.config.dictConfig(config.log_dict_config)
    log = logging.getLogger("loader")

    publisher = create_persistent_async_publisher(config.publisher_config["connection"], config.publisher_config["route"],
                                                  exchange=config.publisher_config["route"]["exchange"],
                                                  routing_key=config.publisher_config["route"]["routing_key"])
    publisher.start()
    l_idx = 0
    with open(config.loader_path, "r") as fdr:
        fdr.readline()
        for line in fdr:
            l_idx +=1
            try:
                doc = parse_line(line)
                publisher.send(doc)
            except:
                log.exception("{} {}".format(l_idx, line))
    publisher.flush()
    publisher.stop()
