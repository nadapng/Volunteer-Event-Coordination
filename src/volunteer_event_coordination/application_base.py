from volunteer_event_coordination.custom_logging import Logger
from volunteer_event_coordination.settings import SettingsService

class ApplicationBase:

    def __init__(self, subclass_name, logfile_prefix_name):
        self.settings = SettingsService()
        self.logger = Logger(subclass_name, logfile_prefix_name)
