"""Configuration module for logging"""
import logging
from logging import config


dictLogConfig = {
    "version": 1,
    "handlers": {
        "fileHandler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "myFormatter",
            "filename": "file_gen_service/logs/filegenservice.log",
            "when": "midnight",
            "utc": True,
            "backupCount": 2,
        },
        "streamHandler": {
            "class": "logging.StreamHandler",
            "formatter": "myFormatter",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {
        "fileGenApp": {
            "handlers": ["fileHandler"],
            "level": "INFO",
        },
        "": {
            "handlers": ["streamHandler"],
            "level": "INFO",
        }
    },
    "formatters": {
        "myFormatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%d-%b-%y %H:%M:%S"
        }
    }
}

logging.config.dictConfig(dictLogConfig)
logger = logging.getLogger("fileGenApp")
