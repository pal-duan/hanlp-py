2# -*- coding: utf-8 -*-
# @Time: 2022/5/1  20:27
# @Author: 2811755762@qq.com
"""
    Description:
    
"""
import logging
import os


def get_logger(name, log_file=None, log_level="DEBUG"):
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(log_level.upper())
    formatter = logging.Formatter('[%(levelname)7s %(asctime)s %(module)s:%(lineno)4d] %(message)s',
                                  datefmt='%Y%m%d %I:%M:%S')
    if log_file:
        dirname = os.path.dirname(log_file)
        os.makedirs(dirname, exist_ok=True)
        f_handle = logging.FileHandler(log_file)
        f_handle.setFormatter(formatter)
        logger.addHandler(f_handle)

    handle = logging.StreamHandler()
    handle.setFormatter(formatter)
    logger.addHandler(handle)
    return logger


logger = get_logger(__name__, log_file=None, log_level="DEBUG")


if __name__ == "__main__":
    pass
