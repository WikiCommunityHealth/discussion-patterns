from typing import Any, Dict
from .talkpage_metrics import ActionsType, NewUsers, # MutualChain
from . import outputter, utils


class MetricController:
    def __init__(self):
        self.output_data_pages = []
        self.MAX_LEN_OUTPUT_LIST = 50

        self.m_actions_type = ActionsType()
        self.m_new_users = NewUsers()

    def add_record(self, record: Dict[str, Any]):
        """
        Add new information to metrics for the current page
        """
        username: str = utils.get_username(record)
        current_month_year: str = utils.get_year_month_from_timestamp(
            record["timestamp"]
        )

        self.m_actions_type.add_info(record["type"])
        self.m_new_users.add_info(username, current_month_year)

    def calculate_and_send(self, page_id: int, force_send: bool = False):
        """
        Calculate and send the result for the record received until
        the last call of this method
        """
        self.output_data_pages.extend(self.m_actions_type.calculate(page_id))
        self.output_data_pages.extend(self.m_new_users.calculate(page_id))

        # make as few writes as possible to the database in order to
        # speed up the process
        if (len(self.output_data_pages) > self.MAX_LEN_OUTPUT_LIST) or force_send:
            outputter.send_page_data(self.output_data_pages)
            self.output_data_pages.clear()

        self.reset()

    def reset(self):
        """
        Reset all metrics. It is executed before analyzing each new page.
        """
        self.m_actions_type.reset()
