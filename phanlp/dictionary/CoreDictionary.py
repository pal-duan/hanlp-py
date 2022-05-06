# -*- coding: utf-8 -*-
# @Time: 2022/5/1  18:04
# @Author: 2811755762@qq.com
"""
    Description:
    核心字典
"""
import logging
import time

from collection.trie.DoubleArrayTrie import DoubleArrayTrie
from config import CORE_DICTIONARY_PATH
from utility.logger import logger
from corpus.tag.Nature import Nature


class CoreDictionaryLoadError(Exception):
    pass


class CoreDictionary(object):
    trie = DoubleArrayTrie()
    path = CORE_DICTIONARY_PATH

    class Attribute:
        def __init__(self):
            self.nature = []
            self.frequency = []
            self.total_frequency = 0

    @classmethod
    def load(cls, path: str):
        start = time.time()
        if cls.__load(path):
            logger.info(f"{path}加载成功，{cls.trie.size()}个词条，耗时{time.time() - start}ms")
        else:
            raise CoreDictionaryLoadError(f"核心词典{path}加载失败！")

    @classmethod
    def __load(cls, path: str) -> bool:
        logger.info(f"核心词典开始加载：{path}")
        if cls.load_dat(path):
            return True
        _map = {}
        try:
            br = open(path, "r")
            total_frequency = 0
            start = time.time()
            for line in br.readlines():
                param = line.strip().split("\t")
                nature_count = (len(param) - 1) // 2
                attribute = cls.Attribute()
                for i in range(nature_count):
                    attribute.nature.append(Nature.create(param[1 + 2 * i]))
                    attribute.frequency.append(int(param[2 + 2 * i]))
                    attribute.total_frequency += attribute.frequency[i]

                _map[param[0]] = attribute
                total_frequency += attribute.total_frequency
            logger.info(f"核心词典读入词条{len(_map)} 全部频次{total_frequency}, 耗时{time.time() - start}ms")
            br.close()
            cls.trie.build(_map)
            logger.info(f"核心词典加载成功：{cls.trie.size()}个词条，下面将写入缓存......")

            # 写入缓存
            # TODO

        except:
            pass

    @classmethod
    def load_dat(cls, path: str) -> bool:
        # TODO
        pass

    @classmethod
    def get(cls, word: str):
        # TODO
        pass


CoreDictionary.load(CoreDictionary.path)


if __name__ == "__main__":
    pass
