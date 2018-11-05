#!/usr/bin/env python3
import argparse
import json
import logging
import sys
import serial
from p1data import P1DataStructure


def parse_args():
    parser = argparse.ArgumentParser()
    default_config_file = "smartmeter.config"
    parser.add_argument('-c',
                        '--config',
                        action='store',
                        default=default_config_file,
                        help="Location of the configuration file. Default: {}".format(default_config_file)
                        )
    parser.add_argument('-t',
                        '--telegrams',
                        action='store',
                        default=1,
                        help="How many telegrams should be read. 0 is unlimited. Default: 1",
                        type=int
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

    # Reading lines from ser:
    telegram_counter=0
    while True:
        try:
            line = ser.readline().decode(encoding="utf-8").rstrip("\r\n")
        except KeyboardInterrupt as e:
            msg = "Interrupted by keyboard: {}".format(str(e))
            logger.error(msg)
            sys.exit(1)
        except Exception as e:
            msg = "Exception while reading from serial connection: {}".format(str(e))
            logger.fatal(msg)
            sys.exit(1)
        logger.info(line)
        if line == "!":
            # End of telegram found!
            telegram_counter += 1
            if arguments.telegrams > 0 and arguments.telegrams == telegram_counter:
                # Break from the loop if a telegram limit is set and the limit is reached:
                break


    logger.info("Closing connection...")
    ser.close()

if __name__ == '__main__':
    main()
