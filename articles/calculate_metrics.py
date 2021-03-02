import json
import argparse
import gzip
from typing import Dict, Generator, Any

# project specific
from .metric_controller import MetricController
from . import utils


def process_file(file_path: str, input_compression: str) -> None:
    if input_compression == None:
        with open(file_path) as file:
            process_lines((line for line in file))
    elif input_compression == "gzip":
        with gzip.open(file_path, mode="rt", newline="\n") as file:
            process_lines((line for line in file))


def process_lines(lines: Generator[str, None, None]) -> None:
    records: Generator[Dict[str, Any], None, None] = (
        json.loads(line, object_hook=utils.date_hook) for line in lines
    )

    metrics = MetricController()

    last_line_page_id: str = "-1"
    is_new_discussion_page: bool = True
    num_lines_current_discussion_page: int = 0

    for record in records:
        is_new_discussion_page = last_line_page_id != record["pageId"]

        if is_new_discussion_page and last_line_page_id != "-1":
            # STEP #1: save result from previous discussione page to db
            metrics.calculate_and_send(last_line_page_id)

            num_lines_current_discussion_page = 0

        # get metadata about current line
        # username: str = utils.get_username(record)
        # current_month_year: str = utils.get_year_month_from_timestamp(
        #     record["timestamp"]
        # )

        # add info to metrics calculators
        metrics.add_record(record)

        num_lines_current_discussion_page += 1
        last_line_page_id = record["pageId"]

    # calculate metrics for the last discussion page and
    # send whatever has not been send to the database
    metrics.calculate_and_send(last_line_page_id, force_send=True)


def analyze_wiki_conv_file_old(file_path: str):
    with open(file_path) as file:

        last_line_page_id = "-1"
        is_new_discussion_page = True
        num_lines_current_discussion_page = 0

        output_data_pages = []
        output_data_users = []

        # Metric initialization
        # m_new_users_by_month = NewUsersByMonth()
        m_actions_type = ActionsType()
        # m_mutual_chains = MutualChain()

        for line in file:
            record = json.loads(line, object_hook=utils.date_hook)
            is_new_discussion_page = last_line_page_id != record["pageId"]

            if is_new_discussion_page and last_line_page_id != "-1":
                # STEP #1: save result from previous discussione page to db
                print(last_line_page_id, num_lines_current_discussion_page)
                # send_data({
                #   'pageId': int(last_line_page_id),
                #   'numActions': num_lines_current_discussion_page,
                #   'actionsType': m_actions_type.calculate(),
                #   'newUsersByMonth': m_new_users_by_month.calculate(),
                #   'mutualChains': m_mutual_chains.calculate(),
                #   'numMutualChains': m_mutual_chains.num_chains
                # })
                output_data_pages.extend(m_actions_type.calculate(last_line_page_id))

                if len(output_data_pages) > 50:
                    send_page_data(output_data_pages)
                    output_data_pages.clear()

                # STEP #2: recreate structures for metrics calculation
                num_lines_current_discussion_page = 0
                # m_new_users_by_month.reset()
                m_actions_type.reset()
                # m_mutual_chains.reset()

            # get metadata about current line
            username = ""
            if "user" in record and "text" in record["user"]:
                username = record["user"]["text"]
            elif "user" in record and "ip" in record["user"]:
                username = record["user"]["ip"]
            else:
                username = "unknown"

            current_month_year = utils.get_year_month_from_timestamp(
                record["timestamp"]
            )

            # add info to metrics calculators
            # m_new_users_by_month.add_info(username, current_month_year)
            m_actions_type.add_info(record["type"])
            # m_mutual_chains.add_info(record, username)

            num_lines_current_discussion_page += 1
            last_line_page_id = record["pageId"]

        # last discussion page
        print(last_line_page_id, num_lines_current_discussion_page)

        output_data_pages.extend(m_actions_type.calculate(last_line_page_id))
        send_page_data(output_data_pages)
        output_data_pages.clear()
        # send_data({
        #   'pageId': int(last_line_page_id),
        #   'numActions': num_lines_current_discussion_page,
        #   'actionsType': m_actions_type.calculate(),
        #   'newUsersByMonth': m_new_users_by_month.calculate(),
        #   'mutualChains': m_mutual_chains.calculate(),
        #   'numMutualChains': m_mutual_chains.num_chains
        # })


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="dataset file to analyze", type=str)
    parser.add_argument(
        "-c",
        "--compression",
        help="compression used for input files",
        type=str,
        choices=[None, "gzip"],
    )
    args = parser.parse_args()

    process_file(args.file_path, args.compression)
