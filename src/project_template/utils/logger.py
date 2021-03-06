import logging
import os
import sys
from logging import Logger


root_logger: Logger = logging.getLogger()
log: Logger = logging.getLogger(__name__)
log_formatter = logging.Formatter(
    "%(asctime)s - "
    "%(levelname)s - "
    "%(processName)s:%(threadName)s - "
    "%(filename)s:%(funcName)s:%(lineno)d - "
    "%(message)s"
)

# Remove all existing log handlers
for handler in root_logger.handlers:
    root_logger.removeHandler(handler)
for handler in log.handlers:
    log.removeHandler(handler)

# Set logging level based on env var
if os.environ.get("DEBUG") == "true" or os.environ.get("ENVIRONMENT") == "local":
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.INFO)

# Add a stream handler to stdout
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(log_formatter)

log.addHandler(stream_handler)
