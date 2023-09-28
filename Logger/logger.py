import datetime
import logging
import os

def config_logger():

        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        # New handler and Remove the previous handler
        logger = logging.getLogger()
        if logger.handlers:
            logger.removeHandler(logger.handlers[0])

        #Load logger configurations
        config = {}
        with open("Logger/config_logger.txt", "r") as cf:
            for line in cf:
                key, value = line.strip().split(" = ")
                config[key] = value
        log_dir = config.get("log_dir")
        app_name = config.get("app_name")

        #log file in directory
        log_file_path = os.path.join(log_dir, f"{current_date}_{app_name}_log.txt")

        # Create a new file handler for the logger
        file_handler = logging.FileHandler(log_file_path, mode="a")

        formatter = logging.Formatter("%(asctime)s\t[%(levelname)s]:\t%(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG)

        logging.info("Configured logger.")
