#!/usr/bin/env python3
import argparse
from collections import OrderedDict
from datetime import datetime
import json
import pathlib
from typing import List
from textwrap import dedent, indent
import sys


def args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output-file",
        action="store",
        type=str,
        required=False,
        default="-",
        help="The filename to send to content to. Specify '-' to use STDOUT. "
        "Default: %(default)s",
    )

    parser.add_argument(
        "--directory",
        action="store",
        type=str,
        required=False,
        default=pathlib.Path().cwd(),
        help="The directory to process. Default: %(default)s",
    )

    parser.add_argument(
        "--prefix",
        action="store",
        type=str,
        required=False,
        default="smartmeter_",
        help="A prefix for the files to process. Default: %(default)s",
    )

    return parser


def get_file_list(directory: pathlib.Path, prefix: str) -> List[pathlib.Path]:
    file_list = list()
    if not directory.is_dir():
        msg = f"'{directory}' is not a directory"
        raise NotADirectoryError(msg)

    for file in directory.glob(f"{prefix}*.json"):
        if file.is_file():
            file_list.append(file)

    return file_list


def data_from_files(file_list: List[pathlib.Path]) -> OrderedDict:
    output_data = OrderedDict()

    for file in file_list:
        with file.open("rt") as fh:
            json_data = json.load(fh)
            datetime_str = json_data.get("datetime")
            datetime_epoch = json_data.get("updatedatetime")
            data = json_data.get("data")

            output_data.update(
                {
                    datetime_str: {
                        "epoch": datetime_epoch,
                        "data": data,
                        "file": file.name,
                    }
                }
            )
    return output_data


def dot2comma(input_str: str, decimals: int = 3) -> str:
    # make a float first:
    f = float(input_str)
    return f"{f:.{decimals}f}".replace(".", ",")


def html_table(data: OrderedDict) -> str:
    html_string = str()
    indentation = "  "

    html_string += "<table>"

    # Header
    html_string += indent(
        dedent("""
    <tr>
        <th>Date</th>
        <th>1.8.1</th>
        <th>1.8.2</th>
        <th>2.8.1</th>
        <th>2.8.2</th>
    </tr>
        """),
        indentation,
    )
    # Data
    for date_str in sorted(data, reverse=True):
        source_file_name = data.get(date_str).get("file")
        epoch = data.get(date_str).get("epoch")
        date_time_string = datetime.fromtimestamp(float(epoch)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        c_181 = dot2comma(data.get(date_str).get("data").get("1-0:1.8.1"))
        c_182 = dot2comma(data.get(date_str).get("data").get("1-0:1.8.2"))
        c_281 = dot2comma(data.get(date_str).get("data").get("1-0:2.8.1"))
        c_282 = dot2comma(data.get(date_str).get("data").get("1-0:2.8.2"))

        html_string += indent(
            dedent(
                f"""
                 <tr>
                   <td><a href="{source_file_name}">{date_time_string}</a></td>
                   <td>{c_181}</td>
                   <td>{c_182}</td>
                   <td>{c_281}</td>
                   <td>{c_282}</td>
                 </tr>
                 """
            ),
            indentation,
        )

    # End
    html_string += "</table>"

    return html_string


def main():
    arguments = args().parse_args()

    file_list = get_file_list(
        directory=pathlib.Path(arguments.directory), prefix=arguments.prefix
    )

    file_data = data_from_files(file_list)

    html = html_table(file_data)

    full_html = dedent(f"""
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
        "http://www.w3.org/TR/html4/loose.dtd">

    <html lang="nl">
      <head>
          <meta http-equiv="content-type" content="text/html; charset=utf-8" />
          <meta name="viewport" content="width=device-width, 
         initial-scale=1.0" />
          <title>View latest</title>
          <link href="styles.css" rel="stylesheet" type="text/css" />
      </head>
      <body>
        {html}
      </body>
    </html>""")

    if arguments.output_file == "-":
        output_handle = sys.stdout
    else:
        output_handle = pathlib.Path(arguments.output_file).open("wt")

    print(full_html, file=output_handle, flush=True)

    output_handle.close()


if __name__ == "__main__":
    main()
