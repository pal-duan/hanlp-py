# -*- coding: utf-8 -*-
# @Time: 2022/5/22  15:02
# @Author: 2811755762@qq.com
"""
    Description:
        词频统计工具
"""
from summary.KeywordExtractor import KeywordExtractor
from phanlp.phanlp import Phanlp
from algorithm.pytreemap import TreeMap
from algorithm.Heap import MinHeap
from corpus.occurrence.TermFrequency import TermFrequency


class TermFrequencyCounter(KeywordExtractor):
    def __init__(self, segment=Phanlp.new_segment(), filter_stopword: bool = True):
        super().__init__()
        self.default_segment = segment
        self.filter_stopword = filter_stopword
        self.term_frequency_map = TreeMap()

    def add(self, document: str):
        if not document:
            return
        term_list = self.default_segment.lcut(document)
        self.add_from_term_list(term_list)

    def add_from_term_list(self, term_list: list):
        if self.filter_stopword:
            term_list = self.filter_term_list(term_list)

        for term in term_list:
            word = term.word
            frequency = self.term_frequency_map.get(word)
            if frequency is None:
                frequency = TermFrequency(word)
                self.term_frequency_map.put(word, frequency)
            else:
                frequency.increase()

    def top(self, n: int):
        heap = MinHeap(n)
        heap.heapify(self.term_frequency_map.values())
        return heap.to_list()

    def all(self):
        return self.term_frequency_map.values()

    def size(self):
        return self.term_frequency_map.size()

    def is_empty(self):
        return self.term_frequency_map.is_empty()

    def contains(self, o):
        if isinstance(o, str):
            return self.term_frequency_map.contains_key(o)
        elif isinstance(o, TermFrequency):
            return self.term_frequency_map.contains_value(o)
        return False

    def update(self, term_frequency):
        tf = self.term_frequency_map.get(term_frequency.get_term())
        if tf is None:
            self.term_frequency_map.put(term_frequency.get_term(), term_frequency)
            return True
        tf.increase(term_frequency.get_frequency())
        return False

    def remove(self, o):
        return self.term_frequency_map.remove(o) is not None

    def contains_all(self, c):
        for o in c:
            if o not in self:
                return False
        return True

    def update_all(self, c: list):
        for term_frequency in c:
            self.update(term_frequency)
        return bool(len(c))

    def remove_all(self, c: list):
        for o in c:
            self.remove(o)
        return bool(len(c))

    def clear(self):
        self.term_frequency_map.clear()

    def _get_keywords(self, term_list: list, size: int):
        """
        提取关键词（非线程安全）
        :param term_list:
        :param size:
        :return:
        """
        self.clear()
        self.add_from_term_list(term_list)
        top_n = self.top(size)
        return [term_frequency.get_term() for term_frequency in top_n]

    @classmethod
    def get_keyword_list(cls, document: str, size: int):
        return cls().get_keywords(document, size)

    def to_string(self):
        return str(self.top(min(100, self.size())))

    __str__ = to_string


if __name__ == "__main__":
    counter = TermFrequencyCounter()
    counter.add("加油加油中国队！")
    print(counter)
    print(counter.get_keywords("女排夺冠，观众欢呼女排女排女排！"))
