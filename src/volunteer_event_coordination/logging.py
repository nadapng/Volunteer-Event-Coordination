import logging
import os
from volunteer_event_coordination.settings import SettingsService

class LoggingService:

    def __init__(self, subclass_name, logfile_prefix_name):
        settings = SettingsService()
        log_dir = settings.log_directory
        log_prefix = settings.log_prefix

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logfile_path = os.path.join(log_dir, f"{log_prefix}.log")

        logging.basicConfig(
            filename=logfile_path,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

        self.logger = logging.getLogger(subclass_name)
        self.logger.addHandler(logging.StreamHandler())

    def log_info(self, msg):
        self.logger.info(msg)

    def log_error(self, msg):
        self.logger.error(msg)

    def log_debug(self, msg):
        self.logger.debug(msg)
