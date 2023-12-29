from dataclasses import dataclass, field
import logging
import datetime

@dataclass
class InfrastructureLogger:
    log_file: str
    logger_name: str = "InfrastructureLogger"
    level: int = logging.INFO
    logger: logging.Logger = field(init=False, repr=False)

    def __post_init__(self):
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(self.level)
        file_handler = logging.FileHandler(self.log_file)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        def log(self, message, level=None):
            if level is None:
                level = self.level
            if level == logging.DEBUG:
                self.logger.debug(message)
            elif level == logging.INFO:
                self.logger.info(message)
            elif level == logging.WARNING:
                self.logger.warning(message)
            elif level == logging.ERROR:
                self.logger.error(message)
            elif level == logging.CRITICAL:
                self.logger.critical(message)
            else:
                raise ValueError("Invalid log level")