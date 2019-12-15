import re


class Telegram:
    """
    A class representing the P1 data structure
    """

    TELEGRAM_HEADERS = [
        "/ISk5\\",
        "KFM5 KFM5KAIFA-METER",
        "/KFM5",
        "/KMP5",
        "/XMX5LG",
        "/Ene5"
    ]

    OBIS_CODES = {
        "0-0:96.1.1":
            {
                "description": "Serial number",
                "value_regex": r"[A-Z0-9]+",
                "type": "str"
            },
        "1-0:1.8.1":
            {
                "description": "Meter Reading electricity delivered to client (Tariff 1) in 0,001 kWh",
                "value_regex": r"[0-9]+\.[0-9]{3}",
                "type": "float"
            },
        "1-0:1.8.2":
            {
                "description": "Meter Reading electricity delivered to client (Tariff 2) in 0,001 kWh",
                "value_regex": r"[0-9]+\.[0-9]{3}",
                "type": "float"
            },
        "1-0:2.8.1":
            {
                "description": "Meter Reading electricity delivered by client (Tariff 1) in 0,001 kWh",
                "value_regex": r"[0-9]+\.[0-9]{3}",
                "type": "float"
            },
        "1-0:2.8.2":
            {
                "description": "Meter Reading electricity delivered by client (Tariff 2) in 0,001 kWh",
                "value_regex": r"[0-9]+\.[0-9]{3}",
                "type": "float"
            },
        "0-0:96.14.0":
            {
                "description": "Tariff indicator",
                "value_regex": r"[0-9]{4}",
                "type": "int"
            },
        "1-0:1.7.0":
            {
                "description": "Actual electricity power delivered(+P) in 1 Watt resolution",
                "value_regex": r"[0-9]+\.[0-9]{2}",
                "type": "float"
            },
        "1-0:2.7.0":
            {
                "description": "Actual electricity power received(-P) in 1 Watt resolution",
                "value_regex": r"[0-9]+\.[0-9]{2}",
                "type": "float"
            },
        "0-0:17.0.0":
            {
                "description": "Maximum power per phase in kW resolution",
                "value_regex": r"[0-9]+\.[0-9]{2}",
                "type": "float"
            },
        "0-0:96.3.10":
            {
                "description": "Switch position (1 is on)",
                "value_regex": r"[0-9]",
                "type": "int"
            },
        "0-0:96.13.1":
            {
                "description": "Message numeric",
                "value_regex": r"[0-9]*",
                "type": "int"
            },
        "0-0:96.13.0":
            {
                "description": "Message string",
                "value_regex": r".*",
                "type": "str"
            }
    }

    def __init__(self):
        """
        Create an empty instance of the P1DataStructure class
        """
        # Set the internal variable for storing telegrams to an empty dictionary:
        self._telegram = {"header": "",
                          "data": {}
                          }

    def add_line(self, line: str):
        """
        Add the parsed content of the line to the class instance

        :param line: The unparsed line
        :return:
        """

        # Identify the type of line:
        if len(line) == 0:
            # Empty line, we can ignore this one...
            pass

        # Check if the line is a header line:
        for headertype in self.TELEGRAM_HEADERS:
            if line.startswith(headertype):
                # line is a header of type 'headertype'
                self._telegram['header'] = line
                pass

        # Check if the line is an OBIS line:
        parsed_line = self.parse_line(line)
        if parsed_line is not None:
            self._telegram['data'].update({parsed_line['obis_id']: parsed_line['obis_value']})

    @property
    def telegram(self):
        return self._telegram

    def clear(self):
        """ Reset the internal variables, acts as a new instance
        """
        self._telegram.clear()
        self.__init__()

    def parse_line(self, line: str):
        """

        :param line:
        :return:
        """
        # Set empty variables:
        obis_id = ""
        obis_value = ""

        matches = re.search(r'(?P<OBIS_ID>[01]-[01]:[0-9.]+)\((?P<OBIS_VALUE>.+)\)$', line)

        if matches:
            # We've found an OBIS key/value pair, get the id and value
            obis_id, obis_value = matches.groupdict().values()

            if obis_id in self.OBIS_CODES.keys():
                # The found OBIS_ID is found in the OBIS_CODES dictionary, lets parse the found value
                parse_regex = self.OBIS_CODES[obis_id]['value_regex']
                parse_type = self.OBIS_CODES[obis_id]['type']
                parse_description = self.OBIS_CODES[obis_id]['description']

                obis_value_match = re.search(parse_regex, obis_value)
                if obis_value_match:
                    # Convert to the correct type:
                    if parse_type == 'float':
                        return_value = float(obis_value_match.group(0))
                    elif parse_type == 'int':
                        return_value = int(obis_value_match.group(0))
                    else:
                        # Use default str:
                        return_value = obis_value_match.group(0)

                    return {"obis_id": obis_id,
                            "obis_value": return_value,
                            "data_type": type(return_value),
                            "description": parse_description
                            }
        else:
            return None
