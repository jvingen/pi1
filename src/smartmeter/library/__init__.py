import logging
import time
import sys


def get_configured_logger(
        name: str = None,
        level: int = None
) -> logging.Logger:
    """A generic method to create a logger object

     The attached handler will log to stdout, the formatter will use UTC

    :param name:    The name of the logger to use.
                    When left empty the RootLogger will be used
    :type name:     str

    :param level:   The desired level to use.
                    When left empty the default (WARNING) will be used.
                    Valid values:
                        logging.CRITICAL
                        logging.ERROR
                        logging.WARNING
                        logging.INFO
                        logging.DEBUG
                        logging.NOTSET
    :type level:    int

    :rtype:     logging.Logger
    :returns:   Return a logger object with a limited configuration."""

    logger = logging.getLogger(name)

    log_levels = [
        logging.CRITICAL,
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
        logging.NOTSET
    ]

    # Validate the log level, reset to WARNING when not valid:
    log_level = level if level in log_levels else logging.WARNING

    logger.setLevel(log_level)

    handler = logging.StreamHandler(stream=sys.stdout)

    logging_format = "%(asctime)-15s UTC - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(fmt=logging_format)
    formatter.converter = time.gmtime

    handler.setFormatter(formatter)

    # First remove all handlers if any, to prevent multiple handlers:
    logger.handlers = []

    logger.addHandler(handler)

    return logger
