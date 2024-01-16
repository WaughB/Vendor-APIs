# logger.py
import logging
import os
from datetime import datetime


class log_this:
    """
    A logging utility class for creating and managing loggers with both file and console handlers.

    Attributes
    ----------
    logger : logging.Logger
        The logger instance used for logging messages.

    Methods
    -------
    info(message)
        Logs an info message.
    debug(message)
        Logs a debug message.
    warning(message)
        Logs a warning message.
    error(message)
        Logs an error message.
    critical(message)
        Logs a critical message.

    Parameters
    ----------
    name : str
        Name for the logger, usually __name__ of the module where it's used.
    log_file : str or None, optional
        Path to the log file. If None, logs are written to a file in './logs' directory with a timestamp.
    level : int, optional
        Logging level, e.g., logging.INFO, logging.DEBUG. Default is logging.INFO.
    """

    def __init__(self, name, log_file=None, level=logging.INFO):
        """
        Initializes the log_this instance by setting up file and console handlers for logging.

        Parameters
        ----------
        name : str
            Name for the logger, usually __name__ of the module where it's used.
        log_file : str or None, optional
            Path to the log file. If None, logs are written to a file in './logs' directory with a timestamp.
        level : int, optional
            Logging level, e.g., logging.INFO, logging.DEBUG. Default is logging.INFO.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # File handler to log messages in a file
        if log_file is None:
            os.makedirs("./logs", exist_ok=True)
            log_file = f"logs/{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Console handler to log messages to the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def info(self, message):
        """
        Logs an info message.

        Parameters
        ----------
        message : str
            The message to be logged.
        """
        self.logger.info(message)

    def debug(self, message):
        """
        Logs a debug message.

        Parameters
        ----------
        message : str
            The message to be logged.
        """
        self.logger.debug(message)

    def warning(self, message):
        """
                Logs a warning message.

                Parameters
                ----------

        message : str
        The message to be logged.
        """
        self.logger.warning(message)

    def error(self, message):
        """
        Logs an error message.

        Parameters
        ----------
        message : str
            The message to be logged.
        """
        self.logger.error(message)

    def critical(self, message):
        """
        Logs a critical message.

        Parameters
        ----------
        message : str
            The message to be logged.
        """
        self.logger.critical(message)
