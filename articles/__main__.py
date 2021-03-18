import json
import argparse
import gzip
from tqdm import tqdm
from typing import Dict, Generator, Any

# project specific
from .talkpage_metrics import MetricController
from . import utils

import time


def process_file(file_path: str, input_compression: str, database_path: str) -> None:
    if input_compression == None:
        with open(file_path) as file:
            process_lines((line for line in file), database_path)
    elif input_compression == "gzip":
        with gzip.open(file_path, mode="rt", newline="\n") as file:
            process_lines((line for line in file), database_path)


def process_lines(lines: Generator[str, None, None], database_path: str) -> None:
    records: Generator[Dict[str, Any], None, None] = (
        json.loads(line.split("\t")[1], object_hook=utils.date_hook) for line in lines
    )

    metrics = MetricController(database_path)

    last_line_page_id: int = -1
    is_new_discussion_page: bool = True
    num_lines_current_discussion_page: int = 0

    for record in records:
        is_new_discussion_page = last_line_page_id != int(record["pageId"])

        if is_new_discussion_page and last_line_page_id != -1:
            # STEP #1: save result from previous discussione page to db
            metrics.calculate_and_send(last_line_page_id)
            num_lines_current_discussion_page = 0

        # add info to metrics calculators
        metrics.add_record(record)

        num_lines_current_discussion_page += 1
        last_line_page_id = int(record["pageId"])

    # calculate metrics for the last discussion page and
    # send whatever has not been send to the database
    metrics.calculate_and_send(last_line_page_id, force_send=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", help="dataset file to analyze", nargs="+", type=str)
    parser.add_argument(
        "-c",
        "--compression",
        help="compression used for input files",
        type=str,
        choices=[None, "gzip"],
    )
    parser.add_argument(
        "-db",
        "--database",
        help="name of output db file",
        type=str,
        default="database.db"
    )
    args = parser.parse_args()

    now = time.perf_counter()
    for file in tqdm(args.files):
        print(f"Analyzing file {file}")
        process_file(file, args.compression, args.database)

    print(f"Elapsed time: {time.perf_counter() - now}")
