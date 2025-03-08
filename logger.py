# logger.py
import logging
import threading
import os
from datetime import datetime


class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize()
            return cls._instance

    def _initialize(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = f"logs/logfile_{timestamp}.log"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        self.logger = logging.getLogger("ThreadSafeLogger")
        self.logger.setLevel(logging.DEBUG)

        file_formatter = logging.Formatter("%(asctime)s - [%(levelname)s][%(threadName)s]: %(message)s",
                                           datefmt='%Y-%m-%d %H:%M:%S')
        console_formatter = logging.Formatter("%(asctime)s - [%(levelname)s][%(threadName)s]: %(message)s",
                                           datefmt='%Y-%m-%d %H:%M:%S')

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def log(self, msg,  level=logging.INFO):
        # Get the current thread's name directly
        if level == logging.DEBUG:
            self.logger.debug(msg)
        else:
            self.logger.info(msg)
