import argparse
from typing import Optional


def generic(title: str, parser: Optional[argparse.ArgumentParser] = None) -> argparse.ArgumentParser:

    if parser is None:
        parser = argparse.ArgumentParser()

    parser.title = title

    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Enable debug logging",
    )

    return parser
