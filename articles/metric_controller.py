from talkpage_metrics import MetricDB, NewUsersByMonth, ActionsType, MutualChain
import outputter


class MetricController:
    def __init__(self):
        self.output_data_pages = []
        self.MAX_LEN_OUTPUT_LIST = 50

        self.m_actions_type = ActionsType()

    def add_record(self, record: dict):
        """
        Add new information to metrics for the current page
        """
        self.m_actions_type.add_info(record['type'])

    def calculate_and_send(self, pageId: str, force_send=False):
        """
        Calculate and send the result for the record received until
        the last call of this method
        """
        self.output_data_pages.extend(
            self.m_actions_type.calculate(pageId)
        )

        # make as few writes as possible to the database in order to
        # speed up the process
        if (len(self.output_data_pages) > self.MAX_LEN_OUTPUT_LIST) or force_send:
            outputter.send_page_data(self.output_data_pages)
            self.output_data_pages.clear()

        self.reset()

    def reset(self):
        """
        Reset all metrics. It is executed before analyzing each new page.
        """
        self.m_actions_type.reset()
