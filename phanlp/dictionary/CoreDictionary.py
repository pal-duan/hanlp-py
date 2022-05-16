# -*- coding: utf-8 -*-
# @Time: 2022/5/1  18:04
# @Author: 2811755762@qq.com
"""
    Description:
    核心字典
"""
import logging
import time
import re
import pickle
import ujson
import os
from pathlib import Path

from collection.trie.DoubleArrayTrie import DoubleArrayTrie
from config import CORE_DICTIONARY_PATH
from utility.logger import logger
from utility.Predefine import Predefine
from corpus.tag.Nature import Nature
from algorithm.pytreemap import TreeMap


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
        if isinstance(path, str):
            path = Path(path)
        start = time.time()
        if cls.__load(path):
            logger.info(f"{path}加载成功，{cls.trie.count()}个词条，耗时{time.time() - start}s")
        else:
            raise CoreDictionaryLoadError(f"核心词典{path}加载失败！")

    @classmethod
    def __load(cls, path) -> bool:
        logger.info(f"核心词典开始加载：{path}")
        if cls.load_dat(path):
            return True
        _map = TreeMap()
        try:
            br = open(path, "r", encoding="utf-8")
            total_frequency = 0
            start = time.time()
            for line in br.readlines():
                # param = line.strip().split("\t")
                param = re.split(r"\s", line.strip())
                nature_count = (len(param) - 1) // 2
                attribute = cls.Attribute()
                for i in range(nature_count):
                    attribute.nature.append(Nature.create(param[1 + 2 * i]))
                    attribute.frequency.append(int(param[2 + 2 * i]))
                    attribute.total_frequency += attribute.frequency[i]

                _map[param[0]] = attribute
                total_frequency += attribute.total_frequency
            logger.info(f"核心词典读入词条{len(_map)} 全部频次{total_frequency}, 耗时{time.time() - start}s")
            br.close()
            cls.trie.build(_map)
            logger.info(f"核心词典加载成功：{cls.trie.count()}个词条，下面将写入缓存......")

            # 写入缓存
            try:
                with open(path.with_suffix(Predefine.BIN_EXT), "w") as f:
                    attribute_list = _map.values()
                    f.write(str(attribute_list.size()) + "\n")
                    for attribute in attribute_list:
                        f.write(str(attribute.total_frequency) + "\n")
                        f.write(str(len(attribute.nature)) + "\n")
                        for i in range(len(attribute.nature)):
                            f.write(str(attribute.nature[i].ordinal) + "\n")
                            f.write(str(attribute.frequency[i]) + "\n")
                    cls.trie.save(f)
                    f.write(str(total_frequency) + "\n")

                # 直接用pickle缓存
                # cls.trie.total_frequency = total_frequency
                # with(open(path.with_suffix(Predefine.BIN_EXT), "wb")) as f:
                #     pickle.dump(cls.trie, f)

                # 以json格式缓存
                # bin_json = {}
                # attribute_list = cls.trie.v
                # attribute_total_frequency_list = []
                # attribute_nature_list = []
                # attribute_frequency_list = []
                # for attribute in attribute_list:
                #     attribute_total_frequency_list.append(attribute.total_frequency)
                #     attribute_frequency_list.append(attribute.frequency)
                #     nature_list = [nature.name for nature in attribute.nature]
                #     attribute_nature_list.append(nature_list)
                # trie_cache_obj = cls.trie.get_cache_obj()
                # bin_json["attribute_size_list"] = len(attribute_list)
                # bin_json["attribute_total_frequency_list"] = attribute_total_frequency_list
                # bin_json["attribute_nature_list"] = attribute_nature_list
                # bin_json["attribute_frequency_list"] = attribute_frequency_list
                # bin_json["trie_cache_obj"] = trie_cache_obj
                # bin_json["all_total_frequency"] = total_frequency
                # with(open(path.with_suffix(Predefine.BIN_EXT), "w")) as f:
                #     ujson.dump(bin_json, f)
                Predefine.set_total_frequency(total_frequency)
            except Exception as e:
                logger.warning(f"保存失败！\ndetail: {e}")
                return False

        except FileNotFoundError as e:
            logger.warning(f"核心词典{path}不存在！\ndetail: {e}")
            return False
        except IOError as e:
            logger.warning(f"核心词典{path}读取错误！\ndetail: {e}")
            return False
        return True

    @classmethod
    def load_dat(cls, path: Path) -> bool:
        try:
            with open(path.with_suffix(Predefine.BIN_EXT), "r") as f:
                size = int(f.readline().strip())
                attributes = []
                nature_index_array = Nature.values
                for i in range(size):
                    current_total_frequency = int(f.readline().strip())
                    length = int(f.readline().strip())
                    attribute = CoreDictionary.Attribute()
                    attribute.total_frequency = current_total_frequency
                    for j in range(length):
                        index = int(f.readline().strip())
                        attribute.nature.append(nature_index_array[index])
                        attribute.frequency.append(int(f.readline().strip()))
                    attributes.append(attribute)
                if not cls.trie.load(f, attributes):
                    return False
                total_frequency = int(f.readline().strip())
                Predefine.set_total_frequency(total_frequency)

            # 从pickle缓存中加载
            # with open(path.with_suffix(Predefine.BIN_EXT), "rb") as f:
            #     cls.trie = pickle.load(f)
            # Predefine.set_total_frequency(cls.trie.total_frequency)

            # 从json对象中加载
            # with open(path.with_suffix(Predefine.BIN_EXT), "r") as f:
            #     obj = ujson.load(f)
            # v = []
            # assert obj["attribute_size_list"] == len(obj["attribute_total_frequency_list"]) == \
            #     len(obj["attribute_nature_list"]) == len(obj["attribute_frequency_list"])
            # for i in range(obj["attribute_size_list"]):
            #     attribute = cls.Attribute()
            #     nature_list = [Nature.create(nature_name) for nature_name in obj["attribute_nature_list"][i]]
            #     attribute.nature = nature_list
            #     attribute.frequency = obj["attribute_frequency_list"][i]
            #     attribute.total_frequency = obj["attribute_total_frequency_list"][i]
            #     v.append(attribute)
            # trie_attributes = obj["trie_cache_obj"]
            # trie_attributes["v"] = v
            # if not cls.trie.load_from_json(trie_attributes):
            #     return False
            # Predefine.set_total_frequency(obj["all_total_frequency"])
            logger.info(f"核心词典从缓存文件{path.with_suffix(Predefine.BIN_EXT)}中加载......")
        except FileNotFoundError as e:
            logger.warning(f"缓存文件{path.with_suffix(Predefine.BIN_EXT)}不存在！\ndetail: {e}")
            return False
        except Exception as e:
            logger.warning(f"缓存文件{path.with_suffix(Predefine.BIN_EXT)}读取失败！\ndetail: {e}")
            return False
        return True

    @classmethod
    def get(cls, word: str):
        return cls.trie[word]

    @classmethod
    def get_term_frequency(cls, term: str) -> int:
        attribute = cls.trie[term]
        if attribute is None:
            return 0
        return attribute.total_frequency

    @classmethod
    def contains(cls, key: str) -> bool:
        return key in cls.trie

    @classmethod
    def get_word_id(cls, a: str) -> int:
        return cls.trie.exact_match_search(a)

    @classmethod
    def reload(cls) -> bool:
        os.remove(cls.path.with_suffix(Predefine.BIN_EXT))
        return cls.load(cls.path)


CoreDictionary.load(CoreDictionary.path)


if __name__ == "__main__":
    print(CoreDictionary.trie.count())
    # print(CoreDictionary.trie.base)
    print("天空" in CoreDictionary.trie)
