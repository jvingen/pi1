import argparse
import json

# from smartmeter.p1.config import SerialConfig
from .config import SerialConfig


def load_config(json_file: str) -> dict:
    """Private function to read the JSON configuration file

    :param json_file:   The name (path) to the JSON configuration file
    :type json_file:    str

    :return:            Return a dictionary containing the JSON structure
    :rtype:             dict
    """
    config = None
    try:
        with open(json_file) as jf:
            config = json.load(jf)
    except IOError as e:
        print(f"IOException: {str(e)}")

    return config


def parse_args():
    """Parse all supplied arguments and return an argparse namespace object

    :rtype:             Aargparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()
    default_config_file = "smartmeter.json"
    parser.add_argument('-c',
                        '--config',
                        action='store',
                        default=default_config_file,
                        help=f"Location of the configuration file. Default: {default_config_file}"
                        )
    parser.add_argument('-t',
                        '--telegrams',
                        action='store',
                        default=1,
                        help="How many telegrams should be read. 0 is unlimited. Default: 1",
                        type=int
                        )
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help="Show more verbose logging (debug). Default: off",
                        default=False)
    return parser.parse_args()


class P1Connection:
    """A class which provides means to get information from a P1 port"""

    def __init__(self, serial_config=None):
        """Initialize the connection with a SerialConfig object

        :param serial_config:   The object storing the serial configuration. Defaults to an standard SerialConfig object
        :type serial_config:    smartmeter.p1.config.SerialConfig
        """
        if serial_config is None:
            self.serial_config = SerialConfig()
        elif isinstance(serial_config, (SerialConfig,)):
            self.serial_config = serial_config
        else:
            msg = "serial_config is not of object type 'SerialConfig'"
            raise ValueError(msg)


class ReadTelegrams:
    """A class to provide the means to read data from the P1 port"""

    def __init__(self, configuration: dict):
        """
        :param configuration:   A dictionary containing all needed paramters
        :type configuration:    dict
        """
        self.configuration = configuration
