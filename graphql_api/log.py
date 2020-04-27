"""Logging config."""
import os

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored_verbose': {
            '()': 'colorlog.ColoredFormatter',
            'format': (
                '%(log_color)s%(levelname)-5s%(reset)s '
                '%(yellow)s[%(asctime)s]%(reset)s'
                '%(white)s %(name)s %(funcName)s '
                '%(bold_purple)s:%(lineno)d%(reset)s '
                '%(log_color)s%(message)s%(reset)s'
            ),
            'datefmt': '%y-%m-%d %H:%M:%S',
            'log_colors': {
                'DEBUG': 'blue',
                'INFO': 'bold_cyan',
                'WARNING': 'red',
                'ERROR': 'bg_bold_red',
                'CRITICAL': 'red,bg_white',
            },
        },
    },
    'handlers': {
        'colored_console': {
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'class': 'logging.StreamHandler',
            'formatter': 'colored_verbose'
        }
    },
    'loggers': {
        '': {
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'handlers': ['colored_console'],
        }
    }
}
