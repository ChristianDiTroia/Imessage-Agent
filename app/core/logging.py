import os
import sys
from loguru import logger


def _configure_logging(json_format: bool = False):
    """Configure Loguru for the application.

    Args:
        json_format: If True, output logs as JSON. If False, use readable plaintext.

    Returns:
        Configured logger instance.
    """

    # Remove default handler
    logger.remove()

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    if json_format:
        fmt = "{message}"
        logger.add(
            sys.stdout,
            level=log_level,
            format=fmt,
            serialize=True,
        )
    else:
        fmt = "<level>{level: <8}</level> | <green>{time:HH:mm:ss}</green> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        logger.add(
            sys.stdout,
            level=log_level,
            format=fmt,
            colorize=True,
        )

    return logger


# Export configured logger
logger = _configure_logging(json_format=bool(os.getenv("LOG_JSON", False)))
