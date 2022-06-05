# -*- coding: utf-8 -*-
# @Time: 2022/6/3  17:48
# @Author: 2811755762@qq.com
"""
    Description:
        一个三元的词串的频度
"""


from corpus.occurrence.PairFrequency import PairFrequency
from utility.Predefine import Predefine


class TriaFrequency(PairFrequency):
    def __init__(self, term, frequency=1):
        super().__init__(term, frequency)
        self.third = None

    @classmethod
    def create(cls, first, second, third, delimiter):
        if delimiter == Predefine.RIGHT:
            tria_frequency = TriaFrequency(first + delimiter + second + Predefine.RIGHT + third)
        elif delimiter == Predefine.LEFT:
            tria_frequency = TriaFrequency(second + Predefine.RIGHT + third + delimiter + first)
        else:
            tria_frequency = TriaFrequency(first + Predefine.RIGHT + second + Predefine.RIGHT + third)
        tria_frequency.first = first
        tria_frequency.second = second
        tria_frequency.third = third
        tria_frequency.delimiter = delimiter
        return tria_frequency

    def to_string(self):
        return f"{self.get_term().replace(Predefine.LEFT, '<-').replace(Predefine.RIGHT, '->')}= " \
               f"tf={self.get_frequency()} mi={self.mi} le={self.le} re={self.re}"


if __name__ == "__main__":
    pass
