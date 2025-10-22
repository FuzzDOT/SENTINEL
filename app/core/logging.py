import logging


def configure_logging():
    fmt = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt)
