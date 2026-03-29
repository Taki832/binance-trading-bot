"""
Logging configuration for the trading bot.

Sets up a dual-output logger:
  - Console  : INFO-level, compact format
  - File     : DEBUG-level, detailed format (bot.log)
"""

import logging
import sys
from pathlib import Path

LOG_FILE = Path(__file__).parent / "bot.log"
LOG_FORMAT_FILE = "%(asctime)s | %(levelname)-8s | %(name)-24s | %(message)s"
LOG_FORMAT_CONSOLE = "%(levelname)-8s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging() -> logging.Logger:
    """Create and return the root application logger."""
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)

    # Avoid adding duplicate handlers on repeated calls
    if logger.handlers:
        return logger

    # --- File handler (verbose, DEBUG-level) ---
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(LOG_FORMAT_FILE, datefmt=DATE_FORMAT)
    )

    # --- Console handler (concise, INFO-level) ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter(LOG_FORMAT_CONSOLE, datefmt=DATE_FORMAT)
    )

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Write a visual separator to the log file on each run
    logger.debug("=" * 70)
    logger.debug("NEW SESSION STARTED")
    logger.debug("=" * 70)

    return logger
