#!/usr/bin/env python3
import argparse
import json
import logging
import sys
import serial
from p1data import P1DataStructure


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c',
                        '--config',
                        action='store',
                        default="smartmeter.config"
                        )
    return parser.parse_args()


def read_config(json_file):

    config = None
    try:
        with open(json_file) as jf:
            config = json.load(jf)
    except IOError as e:
        print("IOException: "+str(e))

    return config


def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    logging.info("Parsing arguments...")
    arguments = parse_args()
    logging.info("Reading config file" + arguments.config)
    config = read_config(arguments.config)

    logger.debug("Config:\n" + str(config))

    p1_data = P1DataStructure()

    # Setup the serial connection:
    ser = serial.Serial()
    ser.baudrate = config['p1']['baudrate']
    ser.bytesize = config['p1']['bytesize']
    ser.parity = config['p1']['parity']
    ser.stopbits = config['p1']['stopbits']
    ser.xonxoff = config['p1']['xonxoff']
    ser.rtscts = config['p1']['rtscts']
    ser.timeout = config['p1']['timeout']
    ser.port = config['p1']['port']

    logger.debug(str(ser))

    # open comm:
    try:
        logger.info("Open connection...")
        ser.open()
        logger.info("Connection is open")
    except Exception as e:
        msg = "Exception while opening serial connection: {}".format(str(e))
        logger.fatal(msg)
        sys.exit(1)

    logger.info("Closing connection...")
    ser.close()

if __name__ == '__main__':
    main()
