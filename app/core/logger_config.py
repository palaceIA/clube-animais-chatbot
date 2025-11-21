import logging
import os

from pythonjsonlogger import jsonlogger  # opcional, mas show pra prod

LOG_LEVEL = os.getenv("LOGGING_LEVEL", "INFO").upper()
USE_JSON = os.getenv("USE_JSON_LOGGING", "false").lower() in ["true", "1"]


class CustomFormatter(logging.Formatter):
    # Formato colorido para terminal
    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[32m"
    reset = "\x1b[0m"

    format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "color": {
            "()": CustomFormatter,
        },
        "json": {
            "()": jsonlogger.JsonFormatter,
            "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s",
        },
    },
    "handlers": {
        "default": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "json" if USE_JSON else "color",
        },
    },
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["default"],
    },
    "loggers": {
        "uvicorn": {
            "level": LOG_LEVEL,
            "handlers": ["default"],
            "propagate": False,
        },
        "uvicorn.error": {
            "level": LOG_LEVEL,
            "handlers": ["default"],
            "propagate": False,
        },
        "uvicorn.access": {
            "level": LOG_LEVEL,
            "handlers": ["default"],
            "propagate": False,
        },
    },
}
