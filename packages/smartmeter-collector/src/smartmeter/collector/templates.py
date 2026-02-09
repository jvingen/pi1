"""This module hold templates for different known Smartmeters

The chosen smartmeter will return a SerialConfig object
with preconfigured connection settings"""

from smartmeter.collector.serial import SerialConfig

ISKRA_MT382 = SerialConfig(
    baudrate=9600,
    bytesize=7,
    parity="E",
    stopbits=1,
    xonxoff=False,
    rtscts=False,
    timeout=20,
    port="/dev/ttyUSB0",
)

KAIFA_MA304 = SerialConfig(
    baudrate=115200,
    bytesize=8,
    parity="N",
    stopbits=1,
    timeout=2,
    port="/dev/ttyUSB0",
)
