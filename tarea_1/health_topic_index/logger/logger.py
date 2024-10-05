import logging
import traceback

class AppLogger:
    def __init__(self, log_file='app_errors.log'):
        logging.basicConfig(
            filename=log_file,
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

