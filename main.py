from pika_client.factory import create_persistent_async_publisher
from config import publisher_config, loader_path


def parse_line(line):
    parts = line.split(',')
    return {
        "product_name": parts[0],
        "photo_url": parts[1],
        "barcode": int(parts[2]) if parts[2] != "" else "",
        "sku": int(parts[3]),
        "price_cents": int(parts[4])if parts[4] != "" else "",
        "producer": parts[5]
    }


if __name__ == "__main__":

    publisher = create_persistent_async_publisher(publisher_config["connection"], publisher_config["route"],
                                                  exchange=publisher_config["route"]["exchange"],
                                                  routing_key=publisher_config["route"]["routing_key"])
    publisher.start()
    with open(loader_path, "r") as fdr:
        fdr.readline()
        for line in fdr:
            publisher.send(parse_line(line))
    publisher.flush()
    publisher.stop()
