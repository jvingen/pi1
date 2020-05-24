import argparse
import json
import logging
import serial

# from smartmeter.p1.config import SerialConfig
from smartmeter.configuration import SerialConfig


def load_config(json_file: str) -> dict:
    """Private function to read the JSON configuration file

    :param json_file:   The name (path) to the JSON configuration file
    :type json_file:    str

    :return:            Return a dictionary containing the JSON structure
    :rtype:             dict
    """
    config = {}
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
    default_output_mode = "text"
    
    parser.add_argument(
        "-c",
        "--config",
        action="store",
        default=default_config_file,
        help=f"Location of the configuration file. Default: {default_config_file}"
    )
    
    parser.add_argument(
        "-t",
        "--telegrams",
        action="store",
        default=1,
        help="How many telegrams should be read. 0 is unlimited. Default: 1",
        type=int
    )
    
    parser.add_argument(
        "-v",
        "--verbose",
        "--debug",
        action="store_true",
        help="Show more verbose logging (debug). Default: off",
        default=False
    )
    
    parser.add_argument(
        "-o",
        "--output-mode",
        action="store",
        choices=[
            "json",
            default_output_mode
        ],
        type=str,
        default=default_output_mode,
        help=f"Specify the type of output. Defaults to '{default_output_mode}'"
    )
    return parser.parse_args()


class P1Connection:
    """A class which provides means to get information from a P1 port"""

    def __init__(self, serial_config=None):
        """Initialize the connection with a SerialConfig object

        :param serial_config:   The object storing the serial configuration. Defaults to an standard SerialConfig object
        :type serial_config:    smartmeter.p1.config.SerialConfig
        """

        # Instantiate a new logger instance:
        self.logger = logging.getLogger(__name__)

        self.logger.debug(f"New instance of class P1Connection")

        if serial_config is None:
            self.serial_config = SerialConfig()
        elif isinstance(serial_config, (SerialConfig,)):
            self.serial_config = serial_config
        else:
            msg = "serial_config is not of object type 'SerialConfig' ()"
            raise ValueError(msg)

        self.serial_connection = None

        self.setup_connection()

    def setup_connection(self):
        """Setup a new serial connection, reset old when needed"""
        if self.serial_connection is not None and not self.serial_connection.closed:
            self.serial_connection.close()

        self.serial_connection = serial.Serial()
        self.serial_connection.baudrate = self.serial_config.baudrate
        self.serial_connection.bytesize = self.serial_config.bytesize
        self.serial_connection.parity = self.serial_config.parity
        self.serial_connection.stopbits = self.serial_config.stopbits
        self.serial_connection.xonxoff = self.serial_config.xonxoff
        self.serial_connection.rtscts = self.serial_config.rtscts
        self.serial_connection.timeout = self.serial_config.timeout
        self.serial_connection.port = self.serial_config.port


class ReadTelegrams:
    """A class to provide the means to read data from the P1 port"""

    def __init__(self, configuration: dict):
        """
        :param configuration:   A dictionary containing all needed paramters
        :type configuration:    dict
        """
        self.configuration = configuration
