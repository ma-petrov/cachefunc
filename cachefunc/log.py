from logging import Logger, getLogger
from logging.config import dictConfig


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': { 
        'default': { 
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': { 
        'default': { 
            'level': 'INFO',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'root': {
            'handlers': ['default'],
            'level': 'WARN',
        }
    }
}


dictConfig(LOGGING_CONFIG)


def get_logger(__name__: str) -> Logger:
    return getLogger(__name__)
