from abc import ABC, abstractmethod
from typing import List
from .metric_db import MetricDB


class Metric(ABC):
    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def calculate(self, page_id: int) -> List[MetricDB]:
        pass
