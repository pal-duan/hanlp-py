# -*- coding: utf-8 -*-
# @Time: 2022/5/22  23:28
# @Author: 2811755762@qq.com
"""
    Description:
        Viterbi分词器
        也是最短路分词，最短路求解采用Viterbi算法
"""
from pathlib import Path

from seg.WordBasedSegment import WordBasedSegment
from utility.logger import logger
from collection.trie.DoubleArrayTrie import DoubleArrayTrie
from seg.common.WordNet import WordNet


class ViterbiSegment(WordBasedSegment):
    def __int__(self, custom_path=None, cache=False):
        if custom_path:
            self.load_custom_dic(custom_path, cache)

    def load_custom_dic(self, custom_path, cache):
        if not custom_path:
            return
        logger.info(f"开始加载自定义词典：{custom_path}")
        custom_path = custom_path.split(";")
        main_path = Path(custom_path[0].strip())
        dat = DoubleArrayTrie()
        main_path = main_path.parent() / hash("".join([p.strip() for p in custom_path]))
        self.custom_dictionary.load_main_dictionary(main_path, custom_path, dat, cache)

    def get_dat(self):
        return self.custom_dictionary.dat

    def set_dat(self, dat):
        self.custom_dictionary.dat = dat

    def seg2word(self, text: str):
        word_net_all = WordNet(text)


if __name__ == "__main__":
    pass
