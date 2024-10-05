import logging
import traceback
import os
from datetime import datetime

class AppLogger:
    def __init__(self):
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(logs_dir, exist_ok=True)

        # Generate a log filename with a timestamp
        log_filename = datetime.now().strftime("app_errors_%Y%m%d_%H%M%S.log")
        log_file_path = os.path.join(logs_dir, log_filename)

        logging.basicConfig(
            filename=log_file_path,
            level=logging.ERROR,
            format="%(asctime)s %(levelname)s %(message)s",
        )

    @classmethod
    def log_error(cls, message):
        logging.error(message)

    @classmethod
    def log_exception(cls):
        tb = traceback.format_exc()
        cls.log_error(f"Error procesando el archivo: {tb}")
