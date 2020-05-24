"""This module hold templates for different known Smartmeters

The choosen smartmeter will return a SerialConfig object
with preconfigured connection settings"""

from smartmeter.configuration import SerialConfig

ISKRA_MT382 = SerialConfig(
    baudrate=9600,
    bytesize=7,
    parity="E",
    stopbits=1,
    xonxoff=False,
    rtscts=False,
    timeout=20,
    port="/dev/ttyUSB0"
    )
