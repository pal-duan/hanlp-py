# -*- coding: utf-8 -*-
# @Time: 2022/5/1  18:07
# @Author: 2811755762@qq.com
"""
    Description:
    自定义词典
"""
from dictionary.DynamicCustomDictionary import DynamicCustomDictionary
from config import CUSTOM_DICTIONARY_PATH


class CustomDictionary(object):
    DEFAULT = DynamicCustomDictionary(CUSTOM_DICTIONARY_PATH)

    def __init__(self):
        pass

    def get(self, word: str):
        pass


if __name__ == "__main__":
    pass
