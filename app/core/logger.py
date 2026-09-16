"""
Enterprise-grade rotating logger with security sanitization for sensitive credentials.
"""

import logging
import re
import sys
from logging.handlers import RotatingFileHandler
from typing import Any
from app.core.paths import paths

# Sensitive pattern regexes
STREAM_KEY_PATTERN = re.compile(r"(live_\w+|streamkey=[\w\-_]+|rtmp://[^/\s]+/[^/\s]+/)([a-zA-Z0-9_\-\.]+)", re.IGNORECASE)
PASSWORD_PATTERN = re.compile(r"(password|secret|key|token)=([^\s&]+)", re.IGNORECASE)


class SensitiveDataFilter(logging.Filter):
    """Filters out stream keys, secrets, and passwords from log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = self.sanitize(record.msg)
        return True

    @staticmethod
    def sanitize(text: str) -> str:
        """Mask potential secrets in log strings."""
        if not text:
            return ""
        # Mask stream keys in RTMP URLs
        text = STREAM_KEY_PATTERN.sub(r"\1[REDACTED_STREAM_KEY]", text)
        # Mask passwords/tokens
        text = PASSWORD_PATTERN.sub(r"\1=[REDACTED]", text)
        return text


def setup_logger(name: str = "VJStudio", level: int = logging.INFO) -> logging.Logger:
    """Configures application logger with console and rotating file output."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers if setup is called multiple times
    if logger.handlers:
        return logger

    # Formatter
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s.%(module)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    sensitive_filter = SensitiveDataFilter()

    # 1. Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(sensitive_filter)
    logger.addHandler(console_handler)

    # 2. Rotating File Handler (10 MB max, up to 5 backups)
    try:
        log_file = paths.log_file
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)  # File captures DEBUG
        file_handler.setFormatter(formatter)
        file_handler.addFilter(sensitive_filter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Could not initialize file log handler: {e}")

    return logger


# Primary logger instance
logger = setup_logger()
