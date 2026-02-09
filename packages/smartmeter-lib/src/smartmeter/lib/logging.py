import logging
from time import gmtime
from typing import Optional

__all__ = [
    "configure_logging",
]


def configure_logging(
    logger: Optional[logging.Logger] = None,
    logger_name: Optional[str] = None,
    log_level: Optional[int] = logging.INFO,
    handler: Optional[logging.Handler] = None,
    log_format_string: Optional[str] = None,
    formatter: Optional[object] = None,
) -> logging.Logger:
    """A function to set up the logging

    Can be called multiple times and from all modules.
    Default behavior:
    - the root logger will be set
    - the log level will be set to INFO
    - all time will be in UTC
    - a predefined formatter string will be applied to the handler object

    :param logger:      A logger object to use instead of the root logger.
                        When set to None (default) the root logger will be
                        used.
    :type logger:       logging.Logger

    :param logger_name: A custom logger name. Default: None
    :type logger_name:  str

    :param log_level:   The log level to set initially. When set to None
                        (default) logging.INFO will be used
    :type log_level:    int

    :param handler:     You can specify an alternative handler. When set to
                        None
                        (default) logging. StreamHandler will be used. Note:
                        all handlers will use the same formatter
    :type handler:      logging.Handler

    :param log_format_string:
                        A custom log formatter string. Defaults to:
                        %(asctime)-15s UTC - %(name)s - %(levelname)s - %(message)s
    :type log_format_string:  str

    :param formatter:   The formatter class to use. A custom formatter could be
                        specified. Defaults to 'logging.Formatter'
    :type formatter:    object

    :returns:           A logger object with all needed handlers and formatters
    :rtype:             logging.Logger
    """
    # Get root logger to configure
    logger = logger if logger is not None else logging.getLogger(logger_name)

    if logger_name is not None:
        # Explicitly set the logger name when the parameter has been set:
        logger.name = logger_name

    # Get log level:
    log_level = log_level if log_level is not None else logging.INFO

    # Get handler:
    handler = handler if handler is not None else logging.StreamHandler()

    # Use a sensible date format, and UTC time
    log_format_string = log_format_string if log_format_string is not None else (
        "%(asctime)-15s UTC - %(name)s - %(levelname)s - %(message)s"
    )
    formatter = formatter if formatter is not None else logging.Formatter

    log_formatter = formatter(
        fmt=log_format_string, datefmt="%Y-%m-%d %H:%M:%S UTC"
    )
    log_formatter.converter = gmtime

    # Apply the formatter to the stream handler:
    handler.formatter = log_formatter

    # Remove previously set handlers:
    logger.handlers = []

    # Add our stream handler as the only handler:
    logger.addHandler(handler)
    logger.setLevel(log_level)

    return logger
