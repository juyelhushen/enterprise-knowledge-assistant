import logging


def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a configured logger instance
    """

    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
