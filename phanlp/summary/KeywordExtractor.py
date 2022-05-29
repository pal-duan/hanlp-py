# -*- coding: utf-8 -*-
# @Time: 2022/5/22  15:10
# @Author: 2811755762@qq.com
"""
    Description:
        提取关键词的基类
"""
import abc

from tokenizer.StandardTokenizer import StandardTokenizer
from dictionary.stopword.CoreStopWordDictionary import CoreStopWordDictionary


class KeywordExtractor(metaclass=abc.ABCMeta):
    def __init__(self, default_segment=StandardTokenizer.SEGMENT):
        self.__default_segment = default_segment

    @staticmethod
    def should_include(term) -> bool:
        return CoreStopWordDictionary.should_include(term)

    def set_setment(self, segment):
        self.__default_segment = segment
        return self

    def get_segment(self):
        return self.__default_segment

    def get_keywords(self, document: str, size: int = 10) -> list:
        return self._get_keywords(self.__default_segment.seg(document), size)

    def filter_term_list(self, term_list: list):
        result = []
        for term in term_list:
            if self.should_include(term):
                result.append(term)
        return result

    @abc.abstractmethod
    def _get_keywords(self, term_list: list, size: int):
        pass


if __name__ == "__main__":
    pass
