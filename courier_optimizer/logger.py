import os
import time
import logging
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "run.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_time(func):
    """Decorator to log the execution time and parameters of the decorated function."""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        logging.info(
            f"--- Optimization Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---"
        )
        logging.info(f"Calling function: {func.__name__}")

        if "args" in kwargs:
            logging.info(f"Input File: {kwargs['args'].input}")
            logging.info(f"Depot Location: {kwargs['args'].depot}")
            logging.info(
                f"Mode: {kwargs['args'].mode}, Criterion: {kwargs['args'].criterion}"
            )

        result = func(*args, **kwargs)
        end_time = time.time()

        duration = end_time - start_time
        logging.info(
            f"Function {func.__name__} finished. Total Duration: {duration:.2f}s"
        )
        logging.info(f"--- Optimization End ---")

        return result

    return wrapper
