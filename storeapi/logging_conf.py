import logging
from logging.config import dictConfig

from storeapi.config import DevConfig, config


def obfuscated(email: str, obfuscated_lengh: int) -> str:
    username, domain = email.split("@")
    return f"{username[:obfuscated_lengh]}...@{domain}"


class EmailObfuscationFilter(logging.Filter):
    def __init__(self, name: str = "", obfuscated_lengh: int = 2):
        super().__init__(name)

    def filter(self, record: logging.LogRecord) -> bool:
        if "email" in record.__dict__:
            record.email = obfuscated(record.email, self.obfuscated_lengh)
        return True


# filter = asgi_correlation_id.CorrelationIdFilter(uuid_length=8, default_value="-")
def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 8 if isinstance(config, DevConfig) else 32,
                    "default_value": "-",
                }
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(correlation_id)s:%(levelname)s:%(asctime)s:%(name)s:%(lineno)d:%(message)s",
                },
                "file": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(levelname)s.%(msecs)03dZ%(asctime)s%(name)s%(lineno)d%(message)s",
                    # "format": "%(levelname)s.%(msecs)03dZ:%(asctime)s:%(name)s-8s:%(lineno)d:%(message)s",
                },
            },
            "handlers": {
                "default": {
                    # "class": "logging.StreamHandler",
                    "class": "rich.logging.RichHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id"],
                },
                "rotating_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "file",
                    "filename": "storeapi.log",
                    "maxBytes": 1024 * 1024 * 5,  # 5MB
                    "backupCount": 3,
                    "encoding": "utf8",
                },
            },
            "loggers": {
                "storeapi": {
                    "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                    "handlers": ["default", "rotating_file"],
                    "propagate": False,  # root.storeapi.router.post dont propagate to parent.
                },
                "uvicorn": {
                    "handlers": ["default", "rotating_file"],
                    "level": "INFO",
                    "propagate": False,
                },
                "databases": {
                    "handlers": ["default"],
                    "level": "WARNING",
                    "propagate": False,
                },
                "aiosqlite": {
                    "handlers": ["default"],
                    "level": "WARNING",
                    "propagate": False,
                },
            },
        }
    )
