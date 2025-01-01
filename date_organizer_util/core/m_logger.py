import pathlib

import logging
from logging.handlers import RotatingFileHandler


def create_logger(log_path: pathlib.Path, log_name: str):
    logger = logging.getLogger(log_name)
    for i in logger.handlers:
        if i.get_name() == "organizer_rot_handler":
            logger.debug("Found existing logger")
            return logger
    logger.setLevel(logging.DEBUG)

    # create a file handler
    handler = RotatingFileHandler(log_path / f"{log_name}.log", maxBytes=100000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    handler.set_name("organizer_rot_handler")

    # create a logging format
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    return logger


run_log = create_logger(pathlib.Path.cwd(), "organize_files")
error_log = create_logger(pathlib.Path.cwd(), "organize_files_error")
