from typing import Dict, Set, List
from .metric import Metric
from .metric_db import MetricDB


class NewUsers(Metric):
    """
    docstring
    """

    def __init__(self):
        self.users: Set[str] = set()
        self.new_users_by_month: Dict[str, int] = {}

    def reset(self):
        self.users.clear()
        self.new_users_by_month.clear()

    def calculate(self, page_id: int) -> List[MetricDB]:
        # (page_id integer, page_title text, abs_value real, rel_value real, metric_name text, year_month text)
        # for key, value in self.new_users_by_month.items():
        #     MetricDB(page_id, "", )

        total_users = len(self.users)

        return [
            MetricDB(
                page_id, "", new_users, new_users / total_users, "new users", year_month
            )
            for year_month, new_users in self.new_users_by_month.items()
        ]

    def add_info(self, username: str, current_month_year: str):
        if username not in self.users:
            self.users.add(username)
            self.new_users_by_month[current_month_year] = (
                self.new_users_by_month.get(current_month_year, 0) + 1
            )
