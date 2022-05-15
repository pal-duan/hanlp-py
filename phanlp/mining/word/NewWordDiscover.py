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

from WordInfo import WordInfo
from utility.LexiconUtility import LexiconUtility
from algorithm.Heap import MinHeap


class NewWordDiscover(object):
    delimiter = re.compile("[\\s\\d,.<>/?:;'\"\\[\\]{}()\\|~!@#$%^&*\\-_=+，。《》、？：；“”‘’｛｝【】（）…￥！—┄－]+")

    def __init__(
            self,
            filter: bool = False,
            max_word_len: int = 4,
            min_freq: float = 0.00005,
            min_entropy: float = 0.4,
            min_aggregation: float = 1.2):
        self.filter = filter
        self.max_word_len = max_word_len
        self.min_freq = min_freq
        self.min_entropy = min_entropy
        self.min_aggregation = min_aggregation

    def _normalization_text(self, text):
        if isinstance(text, Path):
            if text.is_file():
                with text.open("r") as f:
                    text = f
            else:
                raise(FileNotFoundError, f"{str(text.absolute())}文件不存在！")
        elif isinstance(text, IOBase):
            text = text
        elif isinstance(text, str):
            text_obj = Path(text)
            if text_obj.is_file():
                text = self._normalization_text(text)
            else:
                text = StringIO(text)
        return text

    def discover(
            self,
            text: Union[str, IOBase, Path],
            count: int):
        text = self._normalization_text(text)
        word_cands = {}
        total_length = 0
        for line in text.readlines():
            line = self.delimiter.sub("\0", line)
            length = len(line)
            for i in range(length):
                end = min(i+1+self.max_word_len, length+1)
                for j in range(i+1, end):
                    word = line[i:j]
                    if word.index("\0") >= 0:
                        continue
                    word_info = word_cands.get(word, None)
                    if word_info is None:
                        word_info = WordInfo(word)
                        word_cands[word] = word_info
                    word_info.update("\0" if i == 0 else line[i-1], line[j] if j < length else "\0")
            total_length += length

        for info in word_cands.values():
            info.compute_probability_entropy(total_length)

        for info in word_cands.values():
            info.compute_aggregation(word_cands)

        word_info_list = []
        for info in word_cands.values():
            if (len(info.text) < 2 or info.p < self.min_freq or info.entropy < self.min_entropy
                    or info.aggregation < self.min_aggregation
                    or (filter and LexiconUtility.get_frequency(info.text) > 0)):
                continue
            word_info_list.append(info)

        top_n = MinHeap(count)
        top_n.heapify(word_info_list)
        return top_n.to_list()


if __name__ == "__main__":
    pass
