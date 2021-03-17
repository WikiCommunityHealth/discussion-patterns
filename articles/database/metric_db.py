from dataclasses import dataclass


@dataclass
class MetricDB:
    """Class for keeping track of an item in inventory."""

    page_id: int
    metric_name: str
    year_month: str
    abs_actual_value: float
    rel_actual_value: float
    abs_cumulative_value: float
    rel_cumulative_value: float

    def unpack(self):
        return (
            self.page_id,
            self.metric_name,
            self.year_month,
            self.abs_actual_value,
            self.rel_actual_value,
            self.abs_cumulative_value,
            self.rel_cumulative_value,
        )
