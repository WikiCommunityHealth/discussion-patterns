from .metric import Metric
from .metric_db import MetricDB


class ActionsType(Metric):
    """
    docstring
    """

    def __init__(self):
        self.actions = {
            'CREATION': 0,
            'ADDITION': 0,
            'MODIFICATION': 0,
            'DELETION': 0,
            'RESTORATION': 0
        }

    def reset(self):
        for key, value in self.actions.items():
            self.actions[key] = 0

    def calculate(self, page_id):
        # (page_id integer, page_title text, abs_value real, rel_value real, metric_name text, year_month text)
        page_id = int(page_id)
        return [
            MetricDB(
                page_id, "", self.actions['CREATION'], -1, 'CREATION', ''),
            MetricDB(
                page_id, "", self.actions['ADDITION'], -1, 'ADDITION', ''),
            MetricDB(
                page_id, "", self.actions['MODIFICATION'], -1, 'MODIFICATION', ''),
            MetricDB(
                page_id, "", self.actions['DELETION'], -1, 'DELETION', ''),
            MetricDB(
                page_id, "", self.actions['RESTORATION'], -1, 'RESTORATION', '')
        ]

    def add_info(self, action_type):
        if action_type in self.actions:
            self.actions[action_type] += 1
