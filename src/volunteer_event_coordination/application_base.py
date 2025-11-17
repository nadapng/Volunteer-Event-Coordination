from volunteer_event_coordination.logging import LoggingService
from volunteer_event_coordination.settings import SettingsService

class ApplicationBase:

    def __init__(self, subclass_name, logfile_prefix_name):
        self.settings = SettingsService()
        self.logger = LoggingService(subclass_name, logfile_prefix_name)
