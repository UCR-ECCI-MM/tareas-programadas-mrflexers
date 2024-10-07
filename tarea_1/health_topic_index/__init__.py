import os
import nltk
import logging
from datetime import datetime

nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_dir, exist_ok=True)

# Generate a log filename with a timestamp
log_filename = datetime.now().strftime("app_errors_%Y%m%d_%H%M%S.log")
log_file_path = os.path.join(logs_dir, log_filename)

def setup_logger(name):
    # Create a custom logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # Set the overall level

    # Avoid adding multiple handlers if they already exist
    if not logger.handlers:
        # Create handlers
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(log_file_path)

        # Set level for handlers
        console_handler.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)

        # Create formatter and add it to handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    # Disable propagation to avoid duplication if using root loggers elsewhere
    logger.propagate = False

    return logger
