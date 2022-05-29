# -*- coding: utf-8 -*-
# @Time: 2022/5/22  23:28
# @Author: 2811755762@qq.com
"""
    Description:
        Viterbi分词器
        也是最短路分词，最短路求解采用Viterbi算法
"""
from seg.WordBasedSegment import WordBasedSegment


class ViterbiSegment(WordBasedSegment):
    def __int__(self, custom_path=None, cache=False):
        if custom_path:
            self.load_custom_dic(custom_path, cache)

    def load_custom_dic(self, custom_path, cache):
        # TODO
        pass

    def seg2word(self, text: str):
        pass


if __name__ == "__main__":
    pass
