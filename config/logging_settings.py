import sys

from .log_filters import DebugInfoLogFilter, WarningCriticalLogFilter, ErrorLogFilter


logging_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "#%(levelname)-8s %(name)s:%(funcName)s - %(message)s"
        },
        "formatter_1": {
            "format": "[%(asctime)s] #%(levelname)-8s %(filename)s:"
                      "%(lineno)d - %(name)s:%(funcName)s - %(message)s"
        },
        "formatter_2": {
            "format": "#%(levelname)-8s [%(asctime)s] - %(filename)s:"
                      "%(lineno)d - %(name)s:%(funcName)s - %(message)s"
        },
        "formatter_3": {
            "format": "#%(levelname)-8s [%(asctime)s] - %(message)s"
        }
    },
    "filters": {
        "warning_critical_filter": {
            "()": WarningCriticalLogFilter,
        },
        "error_filter": {
            "()": ErrorLogFilter,
        },
        "debug_info_filter": {
            "()": DebugInfoLogFilter,
        }
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        },
        "stderr": {
            "class": "logging.StreamHandler",
            "level": "ERROR",
            "formatter": "formatter_3",
        },
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "filters": ["debug_info_filter", ],
            "stream": sys.stdout
        },
        "error_file": {
            "class": "logging.FileHandler",
            "filename": "error.log",
            "mode": "w",
            "level": "DEBUG",
            "formatter": "formatter_1",
            "filters": ["error_filter"]
        },
        "warning_file": {
            "class": "logging.FileHandler",
            "filename": "warning.log",
            "level": "WARNING",
            "mode": "w",
            "formatter": "formatter_3",
            "filters": ["warning_critical_filter"]
        }
    },
    "loggers": {
        "handlers.admin_handlers": {
            "level": "INFO",
            "handlers": [
                "stdout", "stderr", "warning_file", "error_file"
            ]
        },
        "handlers.user_handlers": {
            "level": "INFO",
            "handlers": ["stdout", "stderr", "error_file"]
        },
        "handlers.other_handlers": {
            "level": "INFO",
            "handlers": ["stdout", ]
        },
        "__main__": {
        "level": "INFO",
        "formatter": "default",
        "handlers": ["default"]
        }
    },
    # "root": {
    #     "formatter": "default",
    #     "handlers": ["default"]
    # }
}