from logging import Logger

try:
    from structlog import getLogger
except ModuleNotFoundError:
    from logging import getLogger

def get_logger(__name__: str) -> Logger:
    return getLogger(__name__)
