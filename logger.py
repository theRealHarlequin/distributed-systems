import logging
import threading
import os
from datetime import datetime


class ThreadSafeLogger:
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
        self.name_dict = {}

        file_formatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
        console_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt='%Y-%m-%d %H:%M:%S')

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def log(self, message, name, level=logging.INFO):
        thread_name = threading.current_thread().name
        self.name_dict[thread_name] = name
        log_message = f"[{thread_name} - {name}]: {message}"

        if level == logging.DEBUG:
            self.logger.debug(log_message)
        else:
            self.logger.info(log_message)


# Example usage:
if __name__ == "__main__":
    def worker(thread_name, logger):
        logger.log("This is an info message.", thread_name, logging.INFO)
        logger.log("This is a debug message.", thread_name, logging.DEBUG)


    logger = ThreadSafeLogger()
    threads = []
    logger.log("start_Tool", "main", logging.INFO)
    for i in range(5):
        t = threading.Thread(target=worker, args=(f"Worker-{i}", logger), name=f"Thread-{i}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
