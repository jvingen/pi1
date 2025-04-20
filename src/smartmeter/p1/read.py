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


class P1Connection:
    """A class which provides means to get information from a P1 port"""

    def __init__(self, serial_config=None):
        """Initialize the connection with a SerialConfig object

        :param serial_config:   The object storing the serial configuration. Defaults to an standard SerialConfig object
        :type serial_config:    smartmeter.p1.config.SerialConfig
        """

        # Instantiate a new logger instance:
        self.logger = logging.getLogger(__name__)

        self.logger.debug("New instance of class P1Connection")

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
        if (
            self.serial_connection is not None
            and not self.serial_connection.closed
        ):
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
