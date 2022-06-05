# -*- coding: utf-8 -*-
# @Time: 2022/6/3  16:24
# @Author: 2811755762@qq.com
"""
    Description:
        词共现统计，最多统计到三阶共现
"""


import math

from collection.trie.BinTrie import BinTrie
from utility.Predefine import Predefine
from corpus.occurrence.PairFrequency import PairFrequency
from corpus.occurrence.TermFrequency import TermFrequency
from corpus.occurrence.TriaFrequency import TriaFrequency
from seg.common.Term import Term
from tokenizer.NotionalTokenizer import NotionalTokenizer
from dictionary.CoreDictionary import CoreDictionary


class Occurrence:
    RIGHT = Predefine.RIGHT   # 两个词的正向连接符
    LEFT = Predefine.LEFT  # 两个词的逆向连接符

    def __init__(self):
        self.trie_pair = BinTrie()  # 2 gram的pair
        self.trie_single = BinTrie()  # 词频统计用的储存结构
        self.trie_tria = BinTrie()  # 三阶储存结构
        self.total_term = 0  # 全部单词数量
        self.total_pair = 0  # 全部接续数量，包括正向和逆向
        self.entry_set_pair = set()

    def add_pair(self, first, second, delimiter=RIGHT):
        key = first + delimiter + second
        value = self.trie_pair.get(key)
        if value is None:
            value = PairFrequency.create(first, delimiter, second)
            self.trie_pair[key] = value
        else:
            value.increase()
        self.total_pair += 1

    def add_term(self, key):
        value = self.trie_single.get(key)
        if value is None:
            value = TermFrequency(key)
            self.trie_single[key] = value
        else:
            value.increase()
        self.total_term += 1

    def add_tria(self, first, second, third):
        key = first + self.RIGHT + second + self.RIGHT + third
        value = self.trie_tria.get(key)
        if value is None:
            value = TriaFrequency.create(first, second, third, self.RIGHT)
            self.trie_tria[key] = value
        else:
            value.increase()
        key = second + self.RIGHT + third + self.LEFT + first
        value = self.trie_tria.get(key)
        if value is None:
            value = TriaFrequency.create(first, second, third, self.LEFT)
            self.trie_tria[key] = value
        else:
            value.increase()

    def get_term_frequency(self, term):
        term_frequency = self.trie_single.get(term)
        if term_frequency is None:
            return 0
        return term_frequency.get_frequency()

    def get_pair_frequency(self, first, second):
        term_frequency = self.trie_pair.get(first + self.RIGHT + second)
        if term_frequency is None:
            return 0
        return term_frequency.get_frequency()

    def add_all(self, term_list):
        if not term_list:
            return
        if isinstance(term_list, str):
            self.add_all(NotionalTokenizer.segment(term_list))
        elif isinstance(term_list[0], Term):
            res = []
            for term in term_list:
                res.append(term.word)
            term_list = res
        for term in term_list:
            self.add_term(term)

        first  = None
        for current in term_list:
            if first is not None:
                self.add_pair(first, current)
            first = current

        for i in range(2, len(term_list)):
            self.add_tria(term_list[i-2], term_list[i-1], term_list[i])

    def _get_phrase(self):
        pair_frequency_list = []
        for entry in self.entry_set_pair:
            pair_frequency_list.append(entry[1])
        return pair_frequency_list

    def get_phrase_by_mi(self):
        pair_frequency_list = self._get_phrase()
        pair_frequency_list.sort(key=lambda x: x.mi, reverse=True)
        return pair_frequency_list

    def get_phrase_by_le(self):
        pair_frequency_list = self._get_phrase()
        pair_frequency_list.sort(key=lambda x: x.le, reverse=True)
        return pair_frequency_list

    def get_phrase_by_re(self):
        pair_frequency_list = self._get_phrase()
        pair_frequency_list.sort(key=lambda x: x.re, reverse=True)
        return pair_frequency_list

    def get_phrase_by_score(self):
        pair_frequency_list = self._get_phrase()
        pair_frequency_list.sort(key=lambda x: x.score, reverse=True)
        return pair_frequency_list

    def to_string(self):
        res = f"二阶共现：\n"
        for entry in self.trie_pair.entry_set():
            res += f"{entry[1]}\n"
        res += "三阶共现：\n"
        for entry in self.trie_tria.entry_set():
            res += f"{entry[1]}\n"
        return res

    __str__ = to_string
    __repr__ = to_string

    def compute_mutual_information(self, first, second):
        return math.log(max(Predefine.MIN_PROBABILITY, self.get_pair_frequency(first, second) / (self.total_pair / 2))
                        / max(Predefine.MIN_PROBABILITY, (self.get_term_frequency(first) / self.total_term *
                                                          self.get_term_frequency(second) / self.total_term)))

    def compute_mutual_information_pair(self, pair):
        return math.log(max(Predefine.MIN_PROBABILITY, pair.get_frequency() / self.total_pair) /
                        max(Predefine.MIN_PROBABILITY, (CoreDictionary.get_term_frequency(pair.first) /
                                                        Predefine.TOTAL_FREQUENCY * CoreDictionary.get_term_frequency(
                                    pair.second) / Predefine.TOTAL_FREQUENCY)))

    def compute_left_entropy(self, pair):
        entry_set = self.trie_tria.prefix_search(pair.get_term() + self.LEFT)
        return  self.compute_entropy(entry_set)

    def compute_right_entropy(self, pair):
        entry_set = self.trie_tria.prefix_search(pair.get_term() + self.RIGHT)
        return self.compute_entropy(entry_set)

    def compute_entropy(self, entry_set):
        total_frequency = 0
        for entry in entry_set:
            total_frequency += entry[1].get_frequency()
        le = 0
        for entry in entry_set:
            p = entry[1].get_frequency() / total_frequency
            le += -p * math.log(p)
        return le

    def compute(self):
        self.entry_set_pair = self.trie_pair.entry_set()
        total_mi, total_le, total_re = 0, 0, 0
        for entry in self.entry_set_pair:
            value = entry[1]
            value.mi = self.compute_mutual_information_pair(value)
            value.le = self.compute_left_entropy(value)
            value.re = self.compute_right_entropy(value)
            total_mi += value.mi
            total_le += value.le
            total_re += value.re

        for entry in self.entry_set_pair:
            value = entry[1]
            value.score = self.safe_divide(value.mi, total_mi) + self.safe_divide(value.le, total_le) + \
                          self.safe_divide(value.re, total_re)
            value.score *= len(self.entry_set_pair)

    @staticmethod
    def safe_divide(x, y):
        return 0 if y == 0 else x / y

    def get_uni_gram(self):
        return self.trie_single.entry_set()

    def get_bi_gram(self):
        return self.trie_pair.entry_set()

    def get_tri_gram(self):
        return self.trie_tria.entry_set()


if __name__ == "__main__":
    pass
