# -*- coding: utf-8 -*-
# @Time: 2022/4/30  17:50
# @Author: 2811755762@qq.com
"""
    Description:

"""
from typing import Union, TextIO
from pathlib import Path

from mining.word.NewWordDiscover import NewWordDiscover
from summary.TextRankKeyword import TextRankKeyword
from utility.logger import logger
from seg.Viterbi.ViterbiSegment import ViterbiSegment
from seg.Other.DoubleArrayTrieSegment import DoubleArrayTrieSegment
from seg.NShort.NShortSegment import NShortSegment
from model.crf.CRFLexicalAnalyzer import CRFLexicalAnalyzer
from model.perceptron.PerceptronLexicalAnalyzer import PerceptronLexicalAnalyzer


class IllegalArgumentError(Exception):
    pass


class Phanlp(object):
    def __init__(self):
        pass

    @staticmethod
    def new_segment(algorithm=None):
        if algorithm is None or algorithm.lower() == "viterbi" or algorithm.lower() == "维特比":
            return ViterbiSegment()
        elif algorithm.lower() == "dat" or algorithm.lower() == "双数组trie树":
            return DoubleArrayTrieSegment()
        elif algorithm.lower() == "nshort" or algorithm.lower() == "n最短路":
            return NShortSegment()
        elif algorithm.lower() == "crf" or algorithm.lower() == "条件随机场":
            try:
                return CRFLexicalAnalyzer()
            except IOError as e:
                logger.warning(f"CRF模型加载失败")
                raise RuntimeError(e)
        elif algorithm.lower() == "perceptron" or algorithm.lower() == "感知机":
            try:
                return PerceptronLexicalAnalyzer()
            except IOError as e:
                logger.warning(f"感知机模型加载失败！")
                raise RuntimeError(e)
        else:
            raise IllegalArgumentError(f"非法参数 algorithm == {algorithm}")

    @staticmethod
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

    @staticmethod
    def extract_keyword(document: str, size: int) -> list:
        return TextRankKeyword.get_keyword_list(document, size)
