from __future__ import print_function, unicode_literals

import os
import logging
import logging.handlers
import sys
import copy

import easy_helper


class ColoredConsoleHandler(logging.StreamHandler):
    def emit(self, record):
        # Need to make a actual copy of the record
        # to prevent altering the message for other loggers
        myrecord = copy.copy(record)
        levelno = myrecord.levelno
        if(levelno >= 50):  # CRITICAL / FATAL
            color = '\x1b[31m'  # red
        elif(levelno >= 40):  # ERROR
            color = '\x1b[31m'  # red
        elif(levelno >= 30):  # WARNING
            color = '\x1b[33;1m'  # yellow
        elif(levelno >= 20):  # INFO
            color = '\x1b[32m'  # green
        elif(levelno >= 10):  # DEBUG
            color = '\x1b[30;1m'  # pink
        else:  # NOTSET and anything else
            color = '\x1b[0m'  # normal
        myrecord.msg = '{}{}{}'.format(color, myrecord.msg, '\x1b[0m')  # normal
        logging.StreamHandler.emit(self, myrecord)

dot_easy_tst = easy_helper.dot_easy_tst()

logger = logging.getLogger('easy_tst')
logger.setLevel(logging.DEBUG)

term_formatter = logging.Formatter('%(message)s')
stream_handler = ColoredConsoleHandler()
stream_handler.setFormatter(term_formatter)
stream_handler.setLevel(logging.INFO)

log_formatter = logging.Formatter('%(asctime)s - [%(levelname)s]:%(module)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.handlers.RotatingFileHandler(
    os.path.join(dot_easy_tst, 'easy_log'),
    maxBytes=1024*1024,
    backupCount=5)
file_handler.setFormatter(log_formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

##################################################
# GET UNCAUGHT EXCEPTIONS TO LOG FILE
# https://stackoverflow.com/questions/6234405/logging-uncaught-exceptions-in-python
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        logger.debug('User issued KeyboardInterrupt')
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.critical("Uncaught exception: ", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception
##################################################
