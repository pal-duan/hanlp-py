# -*- coding: utf-8 -*-
# @Time: 2022/6/3  17:15
# @Author: 2811755762@qq.com
"""
    Description:
        一个二元的词串的频度
"""


from corpus.occurrence.TermFrequency import TermFrequency
from utility.Predefine import Predefine


class PairFrequency(TermFrequency):
    def __init__(self, term, frequency=1):
        super().__init__(term, frequency)
        self.first = None
        self.delimiter = None
        self.second = None
        self.mi = None  # 互信息值
        self.le = None  # 左信息熵
        self.re = None  # 右信息熵
        self.score = None  # 分数

    @classmethod
    def create(cls, first, delimiter, second):
        pair_frequency = PairFrequency(first + delimiter + second)
        pair_frequency.first = first
        pair_frequency.delimiter = delimiter
        pair_frequency.second = second
        return pair_frequency

    def is_right(self):
        return self.delimiter == Predefine.RIGHT

    def to_string(self):
        return f"{self.first}{'->' if self.is_right() else '<-'}{self.second}= tf={self.get_frequency()} mi={self.mi} " \
               f"le={self.le} re={self.re} score={self.score}"

    __str__ = to_string
    __repr__ = to_string


if __name__ == "__main__":
    pass
