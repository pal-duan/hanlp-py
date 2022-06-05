# -*- coding: utf-8 -*-
# @Time: 2022/5/22  23:27
# @Author: 2811755762@qq.com
"""
    Description:
    
"""

from seg.Viterbi.ViterbiSegment import ViterbiSegment
from seg.Other.DoubleArrayTrieSegment import DoubleArrayTrieSegment
from seg.NShort.NShortSegment import NShortSegment
from model.crf.CRFLexicalAnalyzer import CRFLexicalAnalyzer
from model.perceptron.PerceptronLexicalAnalyzer import PerceptronLexicalAnalyzer
from utility.logger import logger
from utility.CustomError import IllegalArgumentError


def new_segment(algorithm=None):
    if algorithm is None or algorithm.lower() == "viterbi" or algorithm.lower() == "维特比":
        return DoubleArrayTrieSegment()
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


if __name__ == "__main__":
    pass
