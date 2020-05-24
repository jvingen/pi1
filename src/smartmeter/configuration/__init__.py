import json
import serial
import sys

from smartmeter.lib import get_configured_logger


class SerialConfigException(ValueError):
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
