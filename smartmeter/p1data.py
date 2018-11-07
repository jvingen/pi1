class P1DataStructure:
    """
    A class representing the P1 data structure
    """

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
        self._telegram = None

    def loadlist(self, telegram_lines: list):
        """
        Load list: Load a list of telegram lines.
        Each list element should be a str object with the 'raw' line

        :param telegram_lines: The list containing all the lines
        :return:
        """

