import logging
import json
import sys
import time
from typing import Any, Dict, Optional
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
import contextvars
import uuid

request_id = contextvars.ContextVar('request_id', default=None)

class StructuredLogger:
    def __init__(
        self,
        name: str,
        log_dir: str = "logs",
        max_bytes: int = 10485760,  # 10MB
        backup_count: int = 5,
        log_level: int = logging.INFO
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self._setup_handlers(max_bytes, backup_count)
        self.extra_fields: Dict[str, Any] = {}

    def _setup_handlers(self, max_bytes: int, backup_count: int):
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(console_handler)

        # File handlers
        file_handler = RotatingFileHandler(
            self.log_dir / "application.log",
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(file_handler)

        # Error file handler
        error_handler = TimedRotatingFileHandler(
            self.log_dir / "error.log",
            when="midnight",
            interval=1,
            backupCount=30
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(error_handler)

    def _get_formatter(self):
        return JsonFormatter()

    def with_context(self, **kwargs):
        self.extra_fields.update(kwargs)
        return self

    def _log(self, level: int, message: str, *args, **kwargs):
        extra = {
            'timestamp': datetime.utcnow().isoformat(),
            'request_id': request_id.get(),
            **self.extra_fields,
            **kwargs
        }
        self.logger.log(level, message, *args, extra=extra)

    def info(self, message: str, *args, **kwargs):
        self._log(logging.INFO, message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        self._log(logging.ERROR, message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        self._log(logging.WARNING, message, *args, **kwargs)

    def debug(self, message: str, *args, **kwargs):
        self._log(logging.DEBUG, message, *args, **kwargs)

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'logger': record.name,
            'path': record.pathname,
            'line': record.lineno
        }

        if hasattr(record, 'extra'):
            log_data.update(record.extra)

        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_data)
