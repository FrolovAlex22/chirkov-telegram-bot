import logging


class DebugInfoLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname in ("DEBUG", "INFO")


class ErrorLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname == "ERROR"


class WarningCriticalLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname in ("WARNING", 'CRITICAL')
