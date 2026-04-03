import logging

from app.logging_config import configure_logging


def test_configure_logging_sets_log_level():
    configure_logging(log_level="WARNING")

    logger = logging.getLogger("app")

    assert logger.level == logging.WARNING


def test_configure_logging_defaults_to_info():
    configure_logging()

    logger = logging.getLogger("app")

    assert logger.level == logging.INFO
