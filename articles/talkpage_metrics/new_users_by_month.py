from .metric import Metric


class NewUsersByMonth(Metric):
    """
    docstring
    """

    def __init__(self):
        self.users = set()
        self.new_users_by_month = {}

    def reset(self):
        self.users.clear()
        self.new_users_by_month.clear()

    def calculate(self):
        return self.new_users_by_month

    def add_info(self, username, current_month_year):
        if username not in self.users:
            self.users.add(username)
            self.new_users_by_month[current_month_year] = self.new_users_by_month.get(
                current_month_year, 0) + 1
