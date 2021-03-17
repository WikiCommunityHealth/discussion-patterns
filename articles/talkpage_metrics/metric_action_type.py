from typing import Dict, List
from .metric import Metric
from ..database.metric_db import MetricDB


class MetricActionType(Metric):
    """
    Number of different types of actions
    """

    def __init__(self):
        self.actions_by_month: Dict[str, Dict[str, int]] = {}
        self.num_total_actions = 0

    def reset(self) -> None:
        self.actions_by_month.clear()
        self.num_total_actions = 0

    def calculate(self, page_id: int) -> List[MetricDB]:
        output: List[MetricDB] = []

        cumulative_values = {
            "CREATION": 0,
            "ADDITION": 0,
            "MODIFICATION": 0,
            "DELETION": 0,
            "RESTORATION": 0,
            "total": 0,
        }

        for year_month, actions in self.actions_by_month.items():
            num_actions_current_month = 0
            for action, value in actions.items():
                cumulative_values[action] += value
                num_actions_current_month += value
                output.append(
                    MetricDB(
                        page_id=page_id,
                        metric_name="num_action_" + action.lower(),
                        year_month=year_month,
                        abs_actual_value=value,
                        rel_actual_value=value / self.num_total_actions,
                        abs_cumulative_value=cumulative_values[action],
                        rel_cumulative_value=cumulative_values[action]
                        / self.num_total_actions,
                    )
                )

            cumulative_values["total"] += num_actions_current_month
            output.append(
                MetricDB(
                    page_id=page_id,
                    metric_name="total_action",
                    year_month=year_month,
                    abs_actual_value=num_actions_current_month,
                    rel_actual_value=num_actions_current_month / self.num_total_actions,
                    abs_cumulative_value=cumulative_values["total"],
                    rel_cumulative_value=cumulative_values["total"]
                    / self.num_total_actions,
                )
            )

        return output

    def add_info(self, action_type: str, current_year_month: str) -> None:
        if current_year_month not in self.actions_by_month:
            self.actions_by_month[current_year_month] = {
                "CREATION": 0,
                "ADDITION": 0,
                "MODIFICATION": 0,
                "DELETION": 0,
                "RESTORATION": 0,
            }

        if action_type in self.actions_by_month[current_year_month]:
            self.actions_by_month[current_year_month][action_type] += 1
            self.num_total_actions += 1
