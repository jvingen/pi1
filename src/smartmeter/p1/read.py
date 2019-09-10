import argparse
import json
import serial


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
    default_config_file = "smartmeter.config"
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


class SerialConfigException(Exception):
    """A placeholder class for all exceptions to the Serial Configuration"""
    pass


class SerialConfig:
    """A class to provide the datastructure for all serial configuration details"""

    def __init__(
            self,
            baudrate: int = None,
            bytesize: int = None,
            parity: str = None,
            stopbits: int = None,
            xonxoff: bool = None,
            rtscts: bool = None,
            timeout: int = None,
            port: str = None
    ):
        """
        Note: see pyserial for detail explaination of parameters

        :param baudrate:    Default value: 9600
        :type baudrate:     int

        :param bytesize:    Default value: 7
        :type bytesize:     int

        :param parity:      Default value: E
        :type parity:       str

        :param stopbits:    Default value: 1
        :type stopbits:     int

        :param xonxoff:     Default value: False
        :type xonxoff:      bool

        :param rtscts:      Default value: False
        :type rtscts:       bool

        :param timeout:     Timeouts in seconds between telegrams. Default value: 20
        :type timeout:      int

        :param port:        Device path for serial device. Default value: /dev/ttyUSB0
        :type port:         str

        """
        # Assign variables:
        self.baudrate = baudrate if baudrate is not None else 9600
        self.bytesize = bytesize if bytesize is not None else serial.SEVENBITS
        self.parity = parity if parity is not None else serial.PARITY_EVEN
        self.stopbits = stopbits if stopbits is not None else serial.STOPBITS_ONE
        self.xonxoff = xonxoff if xonxoff is not None else False
        self.rtscts = rtscts if rtscts is not None else False
        self.timeout = timeout if timeout is not None else 20
        self.port = port if port is not None else "/dev/ttyUSB0"

    @property
    def baudrate(self):
        return self._baudrate

    @baudrate.setter
    def baudrate(self, value: int):
        if value is not None:
            self._baudrate = value
        else:
            raise SerialConfigException("Baudrate invalid")

    @property
    def bytesize(self):
        return self._bytesize

    @bytesize.setter
    def bytesize(self, value: int):
        byte_sizes = [serial.FIVEBITS, serial.SIXBITS, serial.SEVENBITS, serial.EIGHTBITS]
        if value in byte_sizes:
            self._bytesize = value
        else:
            raise SerialConfigException(f"Baudrate invalid. Valid values: {byte_sizes}")

    @property
    def parity(self):
        return self._parity

    @parity.setter
    def parity(self, value: str):
        if value.upper() in serial.PARITY_NAMES.keys():
            self._parity = value.upper()
        else:
            raise SerialConfigException(f"Parity invalid. Valid values: {list(serial.PARITY_NAMES.keys())}")

    @property
    def stopbits(self):
        return self._stopbits

    @stopbits.setter
    def stopbits(self, value: int):
        stopbits = [serial.STOPBITS_ONE, serial.STOPBITS_ONE_POINT_FIVE, serial.STOPBITS_TWO]
        if value in stopbits:
            self._stopbits = value
        else:
            raise SerialConfigException(f"Stopbits invalid. Valid values: {stopbits}")

    @property
    def xonxoff(self):
        return self._xonxoff

    @xonxoff.setter
    def xonxoff(self, value: bool):
        xonxoff_values = [True, False]
        if value in xonxoff_values:
            self._xonxoff = value
        else:
            raise SerialConfigException(f"Xonxoff invalid. Valid values: {xonxoff_values}")

    @property
    def rtscts(self):
        return self._rtscts

    @rtscts.setter
    def rtscts(self, value: int):
        if value is not None:
            self._rtscts = value
        else:
            raise SerialConfigException("rtscts invalid")

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value: str):
        if value is not None:
            self._port = value
        else:
            raise SerialConfigException("Port invalid")


class ReadTelegrams:
    """A class to provide the means to read data from the P1 port"""

    def __init__(self, configuration: dict):
        """
        :param configuration:   A dictionary containing all needed paramters
        :type configuration:    dict
        """
        self.configuration = configuration
