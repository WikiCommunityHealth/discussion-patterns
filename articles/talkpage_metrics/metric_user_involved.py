from typing import Dict, Set, List
from .metric import Metric
from ..database.metric_db import MetricDB


class MetricUserInvolved(Metric):
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
        total_users = len(self.users)
        output: List[MetricDB] = []

        cumulative_num_users = 0
        for year_month, new_users in self.new_users_by_month.items():
            cumulative_num_users += new_users

            output.append(
                MetricDB(
                    page_id=page_id,
                    metric_name="user_involved",
                    year_month=year_month,
                    abs_actual_value=new_users,
                    rel_actual_value=new_users / total_users,
                    abs_cumulative_value=cumulative_num_users,
                    rel_cumulative_value=cumulative_num_users / total_users,
                )
            )

        return output

    def add_info(self, username: str, current_year_month: str):
        if username not in self.users:
            self.users.add(username)
            self.new_users_by_month[current_year_month] = (
                self.new_users_by_month.get(current_year_month, 0) + 1
            )
