import logging
import sys
from pathlib import Path

from helpers.files import create_dir_if_not_exists


def get_logger(logger_name: str, log_filepath=None, log_format=None, log_level=None, log_filemode=None,
               root_logger=None, std_out=False, logs_folder=None) -> logging.Logger:
    """
    Returns the requested logger or creates a new one, if it doesn't already exist.

    log_filepath and logs_folder shouldn't be used on conjunction. The priority in choosing the location of the .log is:
    1. log_filepath: The exact and final location of the .log
    2. logs_folder: The path to the folder. A 'logs' folder and the final .log file will be automatically created
    3. current working directory: A 'logs' folder and the final .log file will be automatically created

    :param logger_name: The name of the logger to return/create
    :param log_filepath: The exact filepath to the .log
    :param log_format: The format the logger records will be printed in. Defaults to '%(asctime)s:%(filename)s:%(funcName)s:%(levelname)s - %(message)s'
    :param log_level: The logger level. Defaults to INFO
    :param log_filemode: The mode in which to open the log file. Defaults to 'a'
    :param root_logger: The parent logger. Defaults to logging
    :param std_out: Whether to also write in sys.stdout. Defaults to False
    :param logs_folder: The path to the logs' folder
    :return:
    """

    if not root_logger:
        root_logger = logging

    if not log_format:
        log_format = '%(asctime)s:%(filename)s:%(funcName)s:%(levelname)s - %(message)s'

    if not log_filepath:  # If no filepath was provided, create one in cwd
        log_folder = Path("logs")
        log_filepath = log_folder / f"{logger_name}.log"

    if logs_folder:  # If logs folder was provided, build the directory there
        log_folder_path = Path("logs")
        log_filepath = Path(logs_folder) / log_folder_path / f"{logger_name}.log"
    # Else, use the provided filepath

    if not log_level:
        log_level = root_logger.INFO

    if not log_filemode:
        log_filemode = 'a'

    logger = root_logger.getLogger(logger_name)
    if not logger.handlers:  # If the logger doesn't already exist
        create_dir_if_not_exists(log_filepath)
        logger.setLevel(log_level)
        h = root_logger.FileHandler(log_filepath, log_filemode, encoding="utf-8")
        fmt = root_logger.Formatter(log_format)
        h.setFormatter(fmt)
        add_handler(logger, h)

    if std_out:
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

    return logger


def get_effective_log_format(logger):
    handler_formatter = None
    for handler in logger.handlers:
        handler_formatter = handler.formatter
        if handler_formatter:
            break

    return handler_formatter


def add_handler(logger: logging.Logger, *custom_handlers: logging.Handler):
    """
    Add custom handlers to the logger. If formatter and logging level have not been set for the handler,
    they will be inherited from logger

    :param logger: The logger
    :param custom_handlers: The custom handlers to add to logger
    :return:
    """

    for handler in custom_handlers:
        if not handler.formatter:
            handler_formatter = get_effective_log_format(logger)
            handler.setFormatter(handler_formatter)

        if not handler.level:
            handler.setLevel(logger.level)
        logger.addHandler(handler)
