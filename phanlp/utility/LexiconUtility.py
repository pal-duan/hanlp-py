# -*- coding: utf-8 -*-
# @Time: 2022/5/1  17:24
# @Author: 2811755762@qq.com
"""
    Description:
    
"""
from dictionary.CoreDictionary import CoreDictionary
from dictionary.CustomDictionary import CustomDictionary


class LexiconUtility(object):
    @classmethod
    def get_attribute(cls, word: str) -> int:
        attribute = CoreDictionary.get(word)
        if attribute is not None:
            return attribute
        return CustomDictionary.get(word)

    @classmethod
    def get_frequency(cls, word: str) -> int:
        attribute = cls.get_attribute(word)
        if attribute is None:
            return 0
        return attribute.totalFrequency


if __name__ == "__main__":
    pass
