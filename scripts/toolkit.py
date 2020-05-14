import os
import sys
import inspect
import errno
import logging

LOGGING_LEVEL = logging.ERROR
CONSOLE_LOGGING_LEVEL = logging.ERROR

# colours
RED = "\033[01;31m"
C_NORMAL = "\033[00m"
MAGENTA = "\033[01;35m"


def _placeholder_fn():
    pass


def _silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred


def path():
    """path to *this* file """
    return os.path.dirname(os.path.abspath(
        inspect.getsourcefile(_placeholder_fn)))


def calling_filename():
    """filename of the function that called the function that called htis function"""
    previous_frame = inspect.currentframe().f_back.f_back
    (filename, line_number, function_name, lines,
     index) = inspect.getframeinfo(previous_frame)
    return filename


def init_logger(logger_name=None, verbose=False):

    if not logger_name:
        logger_name = calling_filename()

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.ERROR)

    # file logger
    log_file_name = logger_name + ".log"
    _silentremove(log_file_name)
    fh = logging.FileHandler(log_file_name)
    fh.setLevel(LOGGING_LEVEL)

    # debug logger (only create if different from normal log)
    if LOGGING_LEVEL != logging.DEBUG:
        debug_log_file_name = logger_name + "_debug.log"
        _silentremove(debug_log_file_name)
        debug_fh = logging.FileHandler(debug_log_file_name)
        debug_fh.setLevel(logging.ERROR)

    # console logger
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR if verbose else CONSOLE_LOGGING_LEVEL)

    # formatting
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s:%(levelname)s | %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)

    if debug_fh:
        debug_fh.setFormatter(formatter)
        logger.addHandler(debug_fh)

    return logger
