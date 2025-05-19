import logging


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",
        "INFO": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[41m",
    }
    RESET = "\033[0m"

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        return f"✨{log_color}{super().format(record)}{self.RESET}"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": ColoredFormatter,
        },
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": "logs/prod.log",
            "level": "ERROR",
        }
    },

    "loggers": {
        "dev": {
            "handlers": ["console"],
            "level": "DEBUG",

        },
        "prod": {
            "handlers": ["console", "file"],
            "level": "ERROR",

        },

    },
}
