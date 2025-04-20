import re
from typing import Union
import time

from smartmeter.library.constants import RE_DECIMAL_2, RE_DECIMAL_3


class OBIS:
    OBIS_RE_PATTERN = r"(?P<OBIS_ID>[01]-[01]:[0-9.]+)\((?P<OBIS_VALUE>.*)\)$"

    OBIS_CODES = {
        "0-0:96.1.1": {
            "description": "Serial number",
            "value_regex": r"[A-Z0-9]+",
            "type": "str",
            "metric_type": "Info",
            "metric_name": "serialnumber",
        },
        "1-0:1.8.1": {
            "description": "Meter Reading electricity delivered to client "
            "(Tariff 1) in 0,001 kWh",
            "value_regex": RE_DECIMAL_3,
            "type": "float",
            "metric_type": "Counter",
            "metric_name": "meter_to_client_offpeak_rate",
        },
        "1-0:1.8.2": {
            "description": "Meter Reading electricity delivered to client "
            "(Tariff 2) in 0,001 kWh",
            "value_regex": RE_DECIMAL_3,
            "type": "float",
            "metric_type": "Counter",
            "metric_name": "meter_to_client_day_rate",
        },
        "1-0:2.8.1": {
            "description": "Meter Reading electricity delivered by client "
            "(Tariff 1) in 0,001 kWh",
            "value_regex": RE_DECIMAL_3,
            "type": "float",
            "metric_type": "Counter",
            "metric_name": "meter_from_client_offpeak_rate",
        },
        "1-0:2.8.2": {
            "description": "Meter Reading electricity delivered by client "
            "(Tariff 2) in 0,001 kWh",
            "value_regex": RE_DECIMAL_3,
            "type": "float",
            "metric_type": "Counter",
            "metric_name": "meter_from_client_day_rate",
        },
        "0-0:96.14.0": {
            "description": "Tariff indicator",
            "value_regex": r"[0-9]{4}",
            "type": "int",
            "metric_type": "Gauge",
            "metric_name": "tariff_indicator",
        },
        "1-0:1.7.0": {
            "description": "Actual electricity power delivered(+P) in 1 Watt resolution",
            "value_regex": RE_DECIMAL_2,
            "type": "float",
            "metric_type": "Gauge",
            "metric_name": "power_delivered",
        },
        "1-0:2.7.0": {
            "description": "Actual electricity power received(-P) in 1 Watt resolution",
            "value_regex": RE_DECIMAL_2,
            "type": "float",
            "metric_type": "Gauge",
            "metric_name": "power_received",
        },
        "0-0:17.0.0": {
            "description": "Maximum power per phase in kW resolution",
            "value_regex": RE_DECIMAL_2,
            "type": "float",
            "metric_type": "Gauge",
            "metric_name": "maximim_power_per_phase",
        },
        "0-0:96.3.10": {
            "description": "Switch position (1 is on)",
            "value_regex": r"[0-9]",
            "type": "int",
            "metric_type": "Gauge",
            "metric_name": "switch_position",
        },
        "0-0:96.13.1": {
            "description": "Message numeric",
            "value_regex": r"[0-9]*",
            "type": "int",
            "metric_type": "Info",
            "metric_name": "message_numeric",
        },
        "0-0:96.13.0": {
            "description": "Message string",
            "value_regex": r".*",
            "type": "str",
            "metric_type": "Info",
            "metric_name": "message_string",
        },
    }

    def __init__(self):
        self._raw_value = None
        self._obis_id = None
        self._obis_value = None

    @classmethod
    def from_string(cls, value: str):
        new = cls()
        obis_id, obis_value = cls.obis_tuple(value=value)
        if obis_id is None:
            msg = f"The value in '{value}' is not a valid OBIS string"
            raise ValueError(msg)

        new._obis_id = obis_id
        new._obis_value = obis_value
        new._raw_value = value
        return new

    @classmethod
    def obis_tuple(cls, value: str):
        """Get the OBIS ID and OBIS value from the value parameter

        :param value:   THe OBIS string
        :type value:    Str

        :rtype:         tuple
        :returns:       A tuple containing first the ID and secondly the OBIS value
        """
        matches = re.search(cls.OBIS_RE_PATTERN, value)
        obis_id = obis_value = None
        if matches:
            obis_id, obis_value = matches.groupdict().values()
        return obis_id, obis_value

    @classmethod
    def is_obis(cls, value: str) -> bool:
        """Determine if a string is an OBIS code"""
        if cls.obis_tuple(value)[0] is None:
            return False
        else:
            return True


class Telegram:
    """
    A class representing the P1 data structure
    """

    TELEGRAM_HEADERS = [
        "/ISk5\\",
        "KFM5 KFM5KAIFA-METER",
        "/KFM5KAIFA-METER",
        "/KFM5",
        "/KMP5",
        "/XMX5LG",
        "/Ene5",
    ]

    def __init__(self):
        """
        Create an empty instance of the Telegram class
        """
        # Set the internal variable for storing a telegram to an empty
        # dictionary:
        self._telegram = {"header": "", "data": {}, "updatedatetime": float(0)}

    def add_line(self, line: str):
        """
        Add the parsed content of the line to the class instance

        :param line:    The unparsed line
        :type line:     str
        """
        # Make sure the parameter 'line' is a str:
        line = str(line)

        # Identify the type of line:
        if len(line) == 0:
            # Empty line, we can ignore this one...
            return None

        # Check if the line is a header line:
        for headertype in self.TELEGRAM_HEADERS:
            if line.startswith(headertype):
                # line is a header of type 'headertype'
                self._telegram["header"] = line
                self.__update_datetime()
                return None

        # Check if the line is an OBIS line:
        parsed_line = self.parse_line(line)
        if parsed_line is not None:
            self._telegram["data"].update(
                {parsed_line["obis_id"]: parsed_line["obis_value"]}
            )
            self.__update_datetime()

    @property
    def telegram(self):
        return self._telegram

    def has_header(self):
        if len(self._telegram.get("header", "")) > 0:
            return True
        else:
            return False

    def __update_datetime(self, updatetime: float = None):
        """Update the updatetime time field in the telegram

        :param updatetime:  A float to overwrite the default value: time.time()
        :type updatetime:   float

        """
        self._telegram["updatedatetime"] = (
            updatetime if updatetime is not None else time.time()
        )

    def clear(self):
        """Reset the internal variables, acts as a new instance"""
        self._telegram.clear()
        self.__init__()

    @classmethod
    def parse_line(cls, line: str) -> Union[dict, None]:
        """Parses a OBIS line into a dictionary

        :param line:    The line to parse
        :type line:     str

        :return:        If the line is a valid OBIS key/value pair, a
                        dictionary object containing the following fields
                        are returned:
                        - obis_id
                        - obis_value
                        - data_type
                        - description
                        If the line is not a valuid OBIS key/value pair 'None'
                        is returned
        :rtype:         Union[dict, None]
        """
        matches = re.search(OBIS.OBIS_RE_PATTERN, line)

        if matches:
            # We've found an OBIS key/value pair, get the id and value
            obis_id, obis_value = matches.groupdict().values()

            if obis_id in OBIS.OBIS_CODES.keys():
                # The found OBIS_ID is found in the OBIS_CODES dictionary, lets
                # parse the found value
                parse_regex = OBIS.OBIS_CODES[obis_id]["value_regex"]
                parse_type = OBIS.OBIS_CODES[obis_id]["type"]
                parse_description = OBIS.OBIS_CODES[obis_id]["description"]

                obis_value_match = re.search(parse_regex, obis_value)
                if obis_value_match:
                    value = obis_value_match.group(0)

                    # Convert to the correct type:
                    if parse_type == "float":
                        if value == "":
                            value = "0"

                        return_value = float(value)
                    elif parse_type == "int":
                        if value == "":
                            value = "0"

                        return_value = int(value)
                    else:
                        # Use default str:
                        return_value = value

                    obis_object = {
                        "obis_id": obis_id,
                        "obis_value": return_value,
                        "data_type": type(return_value),
                        "description": parse_description,
                    }
                    return obis_object
        else:
            return None
