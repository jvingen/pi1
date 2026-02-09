import argparse

from smartmeter.lib.args import generic


def arguments() -> argparse.ArgumentParser:
    # First get the generic parser:
    parser = generic("SmartMeter Collector")

    group_collection = parser.add_argument_group("Collection")
    group_collection.add_argument(
        "--collect-max",
        dest="collect_max",
        action="store",
        type=int,
        required=False,
        help="Only collect this amount of messages.",
    )

    group_collection.add_argument(
        "--use-valkey",
        action="store_true",
        dest="use_valkey",
        required=False,
        default=False,
        help="Use Valkey as backend to store the collected data.",
    )


    return parser
