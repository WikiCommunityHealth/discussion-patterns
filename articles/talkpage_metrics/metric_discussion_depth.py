from typing import Dict, List
from .metric import Metric
from ..database.metric_db import MetricDB


class MetricDiscussionDepth(Metric):
    """
    docstring
    """

    def __init__(self):
        self.depth_by_month: Dict[str, int] = {}
        self.max_depth = -1

    def reset(self):
        self.depth_by_month.clear()
        self.max_depth = -1

    def calculate(self, page_id: int) -> List[MetricDB]:
        output: List[MetricDB] = []
        current_max_depth = -1

        for year_month, value in self.depth_by_month.items():
            current_max_depth = max(current_max_depth, value)
            output.append(
                MetricDB(
                    page_id=page_id,
                    metric_name="max_depth",
                    year_month=year_month,
                    abs_actual_value=value,
                    rel_actual_value=value / self.max_depth,
                    abs_cumulative_value=current_max_depth,
                    rel_cumulative_value=current_max_depth / self.max_depth,
                )
            )

        return output

    def add_info(self, indentation: int, current_year_month: str):
        # TODO: we must consider DELETION and RESTORATIONS
        if current_year_month not in self.depth_by_month:
            self.depth_by_month[current_year_month] = indentation
        else:
            self.depth_by_month[current_year_month] = max(
                self.depth_by_month[current_year_month], indentation
            )
        self.max_depth = max(self.max_depth, indentation)