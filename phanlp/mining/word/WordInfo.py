# -*- coding: utf-8 -*-
# @Time: 2022/5/1  10:26
# @Author: 2811755762@qq.com
"""
    Description:
    提取的词语
"""
from collections import defaultdict
import math


class WordInfo(object):
    def __init__(self, text: str):
        self.text = text
        self.left = defaultdict(int)
        self.right = defaultdict(int)
        self.aggregation = float("inf")
        self.frequency = 0
        self.p = None
        self.left_entropy = None
        self.right_entropy = None
        self.entropy = None

    def update(self, left: str, right: str):
        self.frequency += 1
        self.increase_frequency(left, self.left)
        self.increase_frequency(right, self.right)

    @staticmethod
    def increase_frequency(word: str, storage: dict):
        storage[word] += 1

    def compute_entropy(self, storage: dict) -> int:
        _sum = 0
        for num in storage.values():
            p = num / self.frequency
            _sum -= p * math.log(p)
        return _sum

    def compute_probability_entropy(self, total_length: int):
        self.p = self.frequency / total_length
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
                    math.log(self.p / word_cands.get(self.text[0:i]).p / word_cands.get(self.text[i]).p))


if __name__ == "__main__":
    pass
