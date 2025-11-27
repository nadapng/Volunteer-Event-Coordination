import logging
import os

class Logger:

    def __init__(self, name, logfile_prefix):
        logs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
        os.makedirs(logs_dir, exist_ok=True)

        logfile = os.path.join(logs_dir, f"{logfile_prefix}.log")

        logging.basicConfig(
            filename=logfile,
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        self.logger = logging.getLogger(name)

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)
