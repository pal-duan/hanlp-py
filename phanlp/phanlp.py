# -*- coding: utf-8 -*-
# @Time: 2022/4/30  17:50
# @Author: 2811755762@qq.com
"""
    Description:

"""
from typing import Union, TextIO
from pathlib import Path
from mining.word.NewWordDiscover import NewWordDiscover


class Phanlp(object):
    def __init__(self):
        pass

    def extract_words(
            self,
            text: Union[str, TextIO, Path],
            count: int,
            new_word_only: bool = True,
            max_word_len: int = 4,
            min_freq: float = 0.0,
            min_entropy: float = 0.5,
            min_aggregation: float = 100.0):
        discover = NewWordDiscover(new_word_only, max_word_len, min_freq, min_entropy, min_aggregation)
        return discover.discover(text, count)
