from .metric import Metric

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

  def calculate(self):
    return self.actions

  def add_info(self, action_type):
    if action_type in self.actions:
      self.actions[action_type] += 1
    