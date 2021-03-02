from dataclasses import dataclass


@dataclass
class MetricDB:
    """Class for keeping track of an item in inventory."""

    page_id: int
    page_title: str
    abs_value: float
    rel_value: float
    metric_name: str
    year_month: str

    def unpack(self):
        return (
            self.page_id,
            self.page_title,
            self.abs_value,
            self.rel_value,
            self.metric_name,
            self.year_month,
        )
