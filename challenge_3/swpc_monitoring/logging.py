"""
Module that handles:
- setting up the logger
- parsing the config.ini file

Logging outputs are printed out on the console and saved to the
swpc_monitoring.msg file.
"""

import logging
import logging.config
import sys

from configparser import ConfigParser
from logging import Logger
from pathlib import Path


def parse_config_ini() -> ConfigParser:
    """Parse config.ini file."""
    config_file = Path(__file__).resolve().parent.joinpath("config.ini")
    config = ConfigParser()
    config.read(config_file)
    return config


def setup_logger(module_name: str) -> Logger:
    """Set up logging."""
    # Path to logging config file
    log_file_path = Path(__file__).resolve().parent.joinpath("logging.conf")
    # Read in logging config file
    logging.config.fileConfig(log_file_path)
    # Create logger
    logger = logging.getLogger(module_name)
    return logger


def initiate_logger(logger: Logger) -> None:
    """Initiate logging."""
    config = parse_config_ini()
    program_version = config.get("app", "version")
    logger.info(f"{config.get('app', 'name')} program starting")
    logger.debug(f"{sys.argv} - v{program_version} - Python:{sys.version}")
    logger.debug(f"CWD: %{Path.cwd()}")
    logger.info(f"Version: {program_version}")
