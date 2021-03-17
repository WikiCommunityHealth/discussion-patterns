from typing import Dict, List
from .metric import Metric
from ..database.metric_db import MetricDB


class MetricToxicity(Metric):
    """
    docstring
    """

    def __init__(self):
        self.toxicity: Dict[str, int] = {}
        self.severe_toxicity: Dict[str, int] = {}
        self.count_toxicity = 0
        self.count_severe_toxicity = 0

    def reset(self):
        self.toxicity.clear()
        self.severe_toxicity.clear()
        self.count_toxicity = 0
        self.count_severe_toxicity = 0

    def calculate(self, page_id: int) -> List[MetricDB]:
        output: List[MetricDB] = []

        cumulative_toxicity = 0
        for year_month, value in self.toxicity.items():
            cumulative_toxicity += value
            output.append(
                MetricDB(
                    page_id=page_id,
                    metric_name="toxicity",
                    year_month=year_month,
                    abs_actual_value=value,
                    rel_actual_value=value / self.count_toxicity,
                    abs_cumulative_value=cumulative_toxicity,
                    rel_cumulative_value=cumulative_toxicity / self.count_toxicity,
                )
            )

        cumulative_severe_toxicity = 0
        for year_month, value in self.severe_toxicity.items():
            cumulative_severe_toxicity += value
            output.append(
                MetricDB(
                    page_id=page_id,
                    metric_name="severe_toxicity",
                    year_month=year_month,
                    abs_actual_value=value,
                    rel_actual_value=value / self.count_severe_toxicity,
                    abs_cumulative_value=cumulative_severe_toxicity,
                    rel_cumulative_value=cumulative_severe_toxicity
                    / self.count_severe_toxicity,
                )
            )

        return output

    def add_info(self, score: Dict[str, float], current_year_month: str):
        # threshold values taken from original wikiconv paper
        if "toxicity" in score and score["toxicity"] >= 0.64:
            self.toxicity[current_year_month] = (
                self.toxicity.get(current_year_month, 0) + 1
            )
            self.count_toxicity += 1

        if "severeToxicity" in score and score["severeToxicity"] >= 0.92:
            self.severe_toxicity[current_year_month] = (
                self.severe_toxicity.get(current_year_month, 0) + 1
            )
            self.count_severe_toxicity += 1
