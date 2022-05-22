# -*- coding: utf-8 -*-
# @Time: 2022/4/30  21:29
# @Author: 2811755762@qq.com
"""
    Description:
        新词发现
"""
from typing import Union
from pathlib import Path
from io import IOBase, StringIO
import re
import pickle

from mining.word.WordInfo import WordInfo
from utility.LexiconUtility import LexiconUtility
from algorithm.Heap import MinHeap, MaxHeap
from algorithm.pytreemap import TreeMap
from config import NORMALIZATION, NEW_WORD_DISCOVER_CACHE
from dictionary.other.CharTable import CharTable
from utility.Predefine import Predefine


class NewWordDiscover(object):
    delimiter = re.compile("[\\s\\d,.<>/?:;'\"\\[\\]{}()\\|~!@#$%^&*\\-_=+，。《》、？：；“”‘’｛｝【】（）…￥！—┄－．]+")

    def __init__(
            self,
            _filter: bool = False,
            max_word_len: int = 6,
            min_freq: float = 0.0,
            min_entropy: float = 0.6,
            min_aggregation: float = 30):
        self._filter = _filter
        self.max_word_len = max_word_len
        self.min_freq = min_freq
        self.min_entropy = min_entropy
        self.min_aggregation = min_aggregation
        self.word_cands = TreeMap()
        self.total_frequency = 0

    def _normalization_text(self, text):
        if isinstance(text, Path):
            if text.is_file():
                text = text.open("r", encoding="utf-8")
            else:
                raise(FileNotFoundError, f"{str(text.absolute())}文件不存在！")
        elif isinstance(text, IOBase):
            text = text
        elif isinstance(text, str):
            text_obj = Path(text)
            if text_obj.is_file():
                text = self._normalization_text(text_obj)
            else:
                text = StringIO(text)
        return text

    def discover(
            self,
            text: Union[str, IOBase, Path],
            count: int):
        text = self._normalization_text(text)

        for line in text:
            line = self.delimiter.sub("\0", line)
            if NORMALIZATION:
                line = CharTable.convert(line)
            length = len(line)
            line_frequency = 0
            for i in range(length):
                end = min(i+1+self.max_word_len, length+1)
                c = 0
                for j in range(i+1, end):
                    word = line[i:j]
                    if "\0" in word:
                        continue
                    word_info = self.word_cands.get(word)
                    if word_info is None:
                        word_info = WordInfo(word)
                        self.word_cands[word] = word_info
                    word_info.update("\0" if i == 0 else line[i-1], line[j] if j < length else "\0")
                    c += 1
                line_frequency += c
            self.total_frequency += line_frequency

        for info in self.word_cands.values():
            info.compute_probability_entropy(self.total_frequency)

        for info in self.word_cands.values():
            info.compute_aggregation(self.word_cands)

        word_info_list = []
        for info in self.word_cands.values():
            if (len(info.text) < 2 or info.p < self.min_freq or info.entropy < self.min_entropy
                    or info.aggregation < self.min_aggregation
                    or (self._filter and LexiconUtility.get_frequency(info.text) > 0)):
                continue
            word_info_list.append(info)
        top_n = MinHeap(count)
        top_n.heapify(word_info_list)

        return top_n.to_list()

    def save(self, path=NEW_WORD_DISCOVER_CACHE.with_suffix(Predefine.BIN_EXT)):
        pickle.dump(self, path)

    def load(self, path=NEW_WORD_DISCOVER_CACHE.with_suffix(Predefine.BIN_EXT)):
        obj = pickle.load(path)
        self.word_cands = obj.word_cands
        self.total_frequency = obj.total_frequency


if __name__ == "__main__":
    # CORPUS_PATH = "D:\\project\\hanlp-py\\data\\test\\红楼梦.txt"
    # discover = NewWordDiscover(
    #     _filter=True,
    #     max_word_len=6,
    #     min_freq=0.0,
    #     min_entropy=1,
    #     min_aggregation=100)
    # a = discover.discover(CORPUS_PATH, 100)
    # print(a)
    # print([i.text for i in a])
    CORPUS_PATH = "D:\\project\\hanlp-py\\data\\test\\weibo-classification"
    for folder in Path(CORPUS_PATH).iterdir():
        print(folder.name)
        line_list = []
        for file in folder.iterdir():
            with open(file, encoding="utf-8") as f:
                for line in f:
                    line_list.append(line)
        lines = "\n".join(line_list)
        discover = NewWordDiscover(
            _filter=True,
            max_word_len=6,
            min_freq=0.0,
            min_entropy=1,
            min_aggregation=100)
        a = discover.discover(lines, 300)
        # print(a)
        print([i.text for i in a])





