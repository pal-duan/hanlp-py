# -*- coding: utf-8 -*-
# @Time: 2022/5/1  10:26
# @Author: 2811755762@qq.com
"""
    Description:
    提取的词语
"""
from collections import defaultdict
import math

from algorithm.pytreemap import TreeMap


class WordInfo(object):
    def __init__(self, text: str):
        self.text = text
        self.left = TreeMap()
        self.right = TreeMap()
        self.aggregation = float("inf")
        self.frequency = 0
        self.p = None
        self.left_entropy = None
        self.right_entropy = None
        self.entropy = None

    def __lt__(self, other):
        return self.p < other.p

    def __gt__(self, other):
        return self.p > other.p

    def __str__(self):
        return f"WordInfo(text={self.text}, entroy={self.entropy}, aggregation={self.aggregation})"

    def __repr__(self):
        return f"WordInfo(text={self.text}, entroy={self.entropy}, aggregation={self.aggregation})"

    def update(self, left: str, right: str):
        self.frequency += 1
        self.increase_frequency(left, self.left)
        self.increase_frequency(right, self.right)

    @staticmethod
    def increase_frequency(word: str, storage: TreeMap):
        freq = storage.get(word)
        if freq is None:
            storage.put(word, 1)
        else:
            storage.put(word, freq+1)

    def compute_entropy(self, storage: TreeMap) -> int:
        _sum = 0
        for num in storage.values():
            p = num / self.frequency
            _sum -= p * math.log(p)
        return _sum

    def compute_probability_entropy(self, total_frequency: int):
        self.p = self.frequency / total_frequency
        self.left_entropy = self.compute_entropy(self.left)
        self.right_entropy = self.compute_entropy(self.right)
        self.entropy = min(self.left_entropy, self.right_entropy)

    def compute_aggregation(self, word_cands: dict):
        if len(self.text) == 1:
            self.aggregation = math.sqrt(self.p)
        else:
            for i in range(1, len(self.text)):
                self.aggregation = min(
                    self.aggregation,
                    self.p / word_cands.get(self.text[0:i]).p / word_cands.get(self.text[i:]).p)
    # def compute_aggregation(self, word_cands: dict):
    #     if len(self.text) == 1:
    #         self.aggregation = math.sqrt(self.p)
    #     else:
    #         for i in range(len(self.text)-1):
    #             for j in range(i+1, len(self.text)):
    #                 for k in range(j+1, len(self.text)+1):
    #                     self.aggregation = min(
    #                                     self.aggregation,
    #                                     self.p / word_cands.get(self.text[i:j]).p / word_cands.get(self.text[j:k]).p)


if __name__ == "__main__":
    pass
