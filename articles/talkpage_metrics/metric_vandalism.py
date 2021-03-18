from typing import Dict, List
from .metric import Metric
from ..database.metric_db import MetricDB


class MetricVandalism(Metric):
    """
    docstring
    """

    def __init__(self):
        self.vandalism: Dict[str, int] = {}
        self.count_vandalism = 0

    def reset(self):
        self.vandalism.clear()
        self.count_vandalism = 0

    def calculate(self, page_id: int) -> List[MetricDB]:
        output: List[MetricDB] = []

        cumulative_vandalism = 0
        for year_month, value in self.vandalism.items():
            cumulative_vandalism += value
            output.append(
                MetricDB(
                    page_id=page_id,
                    metric_name="vandalism",
                    year_month=year_month,
                    abs_actual_value=value,
                    rel_actual_value=value / self.count_vandalism,
                    abs_cumulative_value=cumulative_vandalism,
                    rel_cumulative_value=cumulative_vandalism / self.count_vandalism,
                )
            )

        return output

    def add_info(self, comment: str, current_year_month: str):
        # it - vandalismo
        # es - vandalismo
        # ca - vandalisme
        # en - vandalism

        if "vandalism" in comment.lower():
            self.vandalism[current_year_month] = (
                self.vandalism.get(current_year_month, 0) + 1
            )
            self.count_vandalism += 1
