from volunteer_event_coordination.utils.logger_util import Logger
from volunteer_event_coordination.settings import SettingsService

class ApplicationBase:

    def __init__(self, name="App", logfile_prefix="app"):
        self.settings = SettingsService()
        self.logger = Logger(name, logfile_prefix)
