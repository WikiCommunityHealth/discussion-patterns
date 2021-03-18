from typing import Any, Dict, List
from .. import utils
from ..database.metric_db import MetricDB
from ..database.outputter import send_page_data
from .metric_action_type import MetricActionType
from .metric_user_involved import MetricUserInvolved
from .metric_discussion_depth import MetricDiscussionDepth
from .metric_toxicity import MetricToxicity
from .metric_vandalism import MetricVandalism


class MetricController:
    def __init__(self, database_path: str):
        self.database_path = database_path
        self.output_data_pages: List[MetricDB] = []
        self.MAX_LEN_OUTPUT_LIST = 100000

        self.m_action_type = MetricActionType()
        self.m_user_involved = MetricUserInvolved()
        self.m_discussion_depth = MetricDiscussionDepth()
        self.m_toxicity = MetricToxicity()
        self.m_vandalism = MetricVandalism()

    def add_record(self, record: Dict[str, Any]):
        """
        Add new information to metrics for the current page
        """
        username: str = utils.get_username(record)
        current_year_month: str = utils.get_year_month_from_timestamp(
            record["timestamp"]
        )

        self.m_action_type.add_info(record["type"], current_year_month)
        self.m_user_involved.add_info(username, current_year_month)

        if "indentation" in record:
            self.m_discussion_depth.add_info(
                int(record["indentation"]), current_year_month
            )

        if "score" in record:
            self.m_toxicity.add_info(record["score"], current_year_month)

        if "comment" in record:
            self.m_vandalism.add_info(record["comment"], current_year_month)

    def calculate_and_send(self, page_id: int, force_send: bool = False):
        """
        Calculate and send the result for the record received until
        the last call of this method
        """
        self.output_data_pages.extend(self.m_action_type.calculate(page_id))
        self.output_data_pages.extend(self.m_user_involved.calculate(page_id))
        self.output_data_pages.extend(self.m_discussion_depth.calculate(page_id))
        self.output_data_pages.extend(self.m_toxicity.calculate(page_id))
        self.output_data_pages.extend(self.m_vandalism.calculate(page_id))

        # make as few writes as possible to the database in order to
        # speed up the process
        if (len(self.output_data_pages) > self.MAX_LEN_OUTPUT_LIST) or force_send:
            send_page_data(self.output_data_pages, self.database_path)
            self.output_data_pages.clear()

        self.reset()

    def reset(self):
        """
        Reset all metrics. It is executed before analyzing each new page.
        """
        self.m_action_type.reset()
        self.m_user_involved.reset()
        self.m_discussion_depth.reset()
        self.m_toxicity.reset()
        self.m_vandalism.reset()

