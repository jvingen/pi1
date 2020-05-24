#!/usr/bin/env python3
import logging
from pprint import pformat
import sys

import smartmeter.configuration.templates
# import smartmeter.p1.config
from smartmeter.p1.data import Telegram
from smartmeter.p1.read import parse_args, load_config, P1Connection


def main():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logging.info("Parsing arguments...")
    arguments = parse_args()

    # Force log level to debug when specified on commandline:
    if arguments.verbose:
        logger.setLevel(logging.DEBUG)
    # logging.info("Reading config file: " + arguments.config)
    # config = load_config(arguments.config)

    # logger.debug("Config:\n" + str(config))

    p1_data = Telegram()

    conn = P1Connection(serial_config=smartmeter.configuration.templates.ISKRA_MT382)

    logger.debug(str(conn.serial_connection))

    # open comm:
    try:
        logger.info("Open connection...")
        conn.serial_connection.open()
        logger.info("Connection is open")
    except Exception as e:
        msg = "Exception while opening serial connection: {}".format(str(e))
        logger.fatal(msg)
        sys.exit(1)

    # Reading lines from ser:
    telegram_counter = 0
    telegram_list = []
    telegram = []

    while True:
        try:
            line = conn.serial_connection.readline().decode(encoding="utf-8").rstrip("\r\n")
        except KeyboardInterrupt as e:
            msg = "Interrupted by keyboard: {}".format(str(e))
            logger.error(msg)
            sys.exit(1)
        except Exception as e:
            msg = "Exception while reading from serial connection: {}".format(str(e))
            logger.fatal(msg)
            sys.exit(1)

        # Add the line to our telegram, but only if it is not the Null character:
        if line != "\x00":
            telegram.append(line)
            p1_data.add_line(line)

        logger.info(line)
        # check if the first character is an exclamation mark
        # (some smartmeter append some text after the exclamation mark)
        if len(line) >= 1 and line[0] == "!":
            # End of telegram found!

            # Check if we also got a header. If not, let wait for another round:
            if not p1_data.has_header():
                logger.debug("End of telegram reached but we don't have a header, wait for another")

            else:

                # add the compiled telegram to our list:
                telegram_list.append(telegram[:])

                logger.debug(f"Content of telegram:\n{pformat(p1_data.telegram, indent=4)}")
                if arguments.output_mode == "json":
                    import json
                    import datetime
                    import sys
                    data = p1_data.telegram
                    data['datetime'] = datetime.datetime.now().isoformat()
                    data['obiscodes'] = p1_data.OBIS_CODES.copy()
                    print(json.dumps(data, indent=4))

                    # Increase the overall counter:
                    telegram_counter += 1

            p1_data.clear()
            # Empty our telegram for reuse:
            telegram.clear()

            # Exit our loop if the desired amount of telegrams has been reached:
            if arguments.telegrams > 0 and arguments.telegrams == telegram_counter:
                # Break from the loop if a telegram limit is set and the limit is reached:
                break

    # Dump our telegram_list to the logger:
    logger.debug(f"Telegram list:\n{telegram_list}")

    logger.info("Closing connection...")
    conn.serial_connection.close()


if __name__ == '__main__':
    main()
