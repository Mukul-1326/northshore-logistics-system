import logging


def init_logger():
    logging.basicConfig(
        filename="logs/app.log",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )


def write_log(msg):
    logging.info(msg)