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

    def _initialize(self, external_log_file=None):
        if hasattr(self, 'logger'):
            return  # Avoid reinitializing

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = external_log_file or f"logs/logfile_{timestamp}.log"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        self.log_file_path = os.path.abspath(log_file)

        self.logger = logging.getLogger(f"ThreadSafeLogger_{id(self)}")
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

    def get_log_file_path(self):
        return self.log_file_path

    def log(self, msg,  level=logging.INFO):
        # Get the current thread's name directly
        if level == logging.DEBUG:
            self.logger.debug(msg)
        else:
            self.logger.info(msg)
