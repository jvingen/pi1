import json
import sys

from smartmeter.library import get_configured_logger

from smartmeter.collector.serial import SerialConfig


def load_from_file(filename: str) -> SerialConfig:
    """Load the configuration from a file

    :param filename:    The filename to use
    :type filename:     str

    :rtype:             SerialConfig
    :returns:           A SerialsConfig object with all needed settings

    :exception:         SerialConfigException
    :exception:         OSError
    """

    logger = get_configured_logger()

    try:
        with open(filename) as file_handler:
            configuration_file_content = json.load(file_handler)
    except OSError as e:
        msg = f"Can not process file '{filename}' because of eror: {str(e)}"
        logger.critical(msg)
        sys.exit(1)

    # TODO:
    #  - validate the dict we got from the configuration file
    #  - return dict
