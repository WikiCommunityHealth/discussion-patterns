# from .metric import Metric
# from .actions_type import ActionsType

# import datetime

# TODO: use a map user->info

# class UserActivity(Metric):
#   """
#   docstring
#   """
#   def __init__(self):
#     self.actions = ActionsType()
#     self.reset()

#   def reset(self):
#     self.actions.reset()
#     self.first_timestamp = datetime.datetime(datetime.MAXYEAR, 1, 1)
#     self.last_timestamp = datetime.datetime(datetime.MINYEAR, 1, 1)

#   def calculate(self):
#     return (
#       self.actions.calculate(),
#       self.first_timestamp,
#       self.last_timestamp
#     )

#   def add_info(self, username, timestamp):
