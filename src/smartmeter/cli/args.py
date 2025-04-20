import argparse


def parse_args():
    """Parse all supplied arguments and return an argparse namespace object

    :rtype:             Aargparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()
    default_config_file = "smartmeter.json"

    output_modes = ["text", "json"]
    output_modes_default = output_modes[0]

    parser.add_argument(
        "-c",
        "--config",
        action="store",
        default=default_config_file,
        help=f"Location of the configuration file. Default: {default_config_file}",
    )

    parser.add_argument(
        "-t",
        "--telegrams",
        action="store",
        default=1,
        help="How many telegrams should be read. 0 is unlimited. Default: 1",
        type=int,
    )

    parser.add_argument(
        "-v",
        "--verbose",
        "--debug",
        action="store_true",
        help="Show more verbose logging (debug). Default: off",
        default=False,
    )

    parser.add_argument(
        "-o",
        "--output-mode",
        action="store",
        choices=output_modes,
        type=str,
        default=output_modes_default,
        help="Specify the type of output. Defaults to '%(default)s'",
    )
    return parser.parse_args()
