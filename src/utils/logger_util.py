import logging
import os

class Logger:
    def __init__(self, log_name="app_log", log_level=logging.INFO):
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(log_level)

        # Create logs directory if it doesn't exist
        dirname = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        file_handler = logging.FileHandler(os.path.join(dirname, f"{log_name}.log"))
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler.setFormatter(formatter)
        # Avoid adding duplicate handlers
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warn(self, message):
        self.logger.warning(message)
