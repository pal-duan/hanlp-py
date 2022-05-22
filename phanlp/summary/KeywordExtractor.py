# -*- coding: utf-8 -*-
# @Time: 2022/5/22  15:10
# @Author: 2811755762@qq.com
"""
    Description:
        提取关键词的基类
"""
import abc

from tokenizer.StandardTokenizer import StandardTokenizer


class KeywordExtractor(metaclass=abc.ABCMeta):
    def __init__(self, default_segment=StandardTokenizer.SEGMET):
        self.__default_segment = default_segment


if __name__ == "__main__":
    pass
