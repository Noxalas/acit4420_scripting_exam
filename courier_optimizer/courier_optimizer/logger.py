import os
import time
import logging

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(PACKAGE_ROOT, "..", "logs")
LOG_FILE = os.path.join(LOG_DIR, "run.log")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(filename="logs/run.log", level=logging.INFO)


def log_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        duration = end - start
        logging.info(f"Function {func.__name__} ran for {duration:2f}s")

        return result

    return wrapper
