import logging
import sys
from typing import Union

from loguru import logger

from app.settings import settings


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentation.

    This handler intercepts all log requests and
    passes them to loguru.

    For more info see:
    https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        """
        Propagates logs to loguru.

        :param record: record to log.
        """
        try:
            level: Union[str, int] = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def filter_dummy_logs(record: dict) -> bool:
    """
    Filter out logs from dummy views.
    """
    return record.get("extra", {}).get("type") == "DUMMY"


def configure_logging() -> None:  # pragma: no cover
    """Configures logging."""
    intercept_handler = InterceptHandler()

    logging.basicConfig(handlers=[intercept_handler], level=logging.NOTSET)

    # change handler for default uvicorn logger
    logging.getLogger("uvicorn").handlers = [intercept_handler]
    logging.getLogger("uvicorn.access").handlers = [intercept_handler]

    # set logs output, level and format
    logger.remove()
    if settings.environment == "production":
        logger.add(
            "debug.log",
            level=settings.log_level.value,
            rotation="00:00",  # Once the file is too old, it's rotated
            retention="10 days",  # Cleanup after some time
            compression="zip",  # Save some loved space
            serialize=True,  # serialize to JSON
        )
    else:
        logger.add(
            sys.stderr,
            level=settings.log_level.value,
            colorize=True,  # Colorize the output
            backtrace=True,  # Include tracebacks in the output
        )

    # add other loggers to use in the project
    logger.add("dummy_error.log", level="ERROR", filter=filter_dummy_logs)
