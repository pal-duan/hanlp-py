# -*- coding: utf-8 -*-
# @Time: 2022/5/15  17:31
# @Author: 2811755762@qq.com
"""
    Description:
    
"""
import time
import os
import re
from pathlib import Path

from config import CUSTOM_DICTIONARY_PATH, CUSTOM_DICTIONARY_AUTO_REFRESH_CACHE, NORMALIZATION
from collection.trie.DoubleArrayTrie import DoubleArrayTrie
from collection.trie.BinTrie import BinTrie
from utility.logger import logger
from utility.Predefine import Predefine
from algorithm.pytreemap import TreeMap
from corpus.tag.Nature import Nature
from utility.NatureUtility import NatureUtility
from dictionary.other.CharTable import CharTable
from dictionary.CoreDictionary import CoreDictionary
from corpus.io.IOUtil import IOUtil


class DynamicCustomDictionary:
    def __init__(self, path):
        if not path:
            path = CUSTOM_DICTIONARY_PATH
        self.dat = DoubleArrayTrie()
        self.trie = BinTrie()
        self.path = None
        self.load(path)

    def load(self, path):
        start = time.time()
        if not self._load_dictionary(path[0]):
            logger.warning(f"自定义词典{path}加载失败")
            return False
        else:
            logger.info(f"自定义词典加载成功：{len(self.dat)}个词条，耗时{time.time()-start}s")
            self.path = path
            return True

    def _load_dictionary(self, main_path):
        return self.load_main_dictionary(main_path, CUSTOM_DICTIONARY_PATH, self.dat, True)

    @classmethod
    def load_main_dictionary(cls, main_path, path, dat, is_cache):
        logger.info(f"自定义词典开始加载：{main_path}")
        if cls._load_dat(main_path, dat):
            return True
        _map = TreeMap()
        custom_nature_collector = set()
        try:
            for p in path:
                default_nature = Nature.from_string("n")
                filename = p.name
                cut = filename.rfind(" ")
                if cut > 0:
                    nature = filename[cut+1:]
                    p = p.parent / filename[:cut]
                    try:
                        default_nature = NatureUtility.covert_string2nature(nature, custom_nature_collector)
                    except Exception as e:
                        logger.error(f"配置文件【{p}】写错了！\ndetail: {e}")
                        continue
                logger.info(f"以默认词性[{default_nature}]加载自定义词典{p}中......")
                success = cls.a_load(p, default_nature, _map, custom_nature_collector)
                if not success:
                    logger.warning(f"失败{p}")
            if _map.size() == 0:
                logger.warning(f"没有加载到任何词条")
                _map.put(Predefine.TAG_OTHER, None)
            logger.info(f"正在构建DoubleArrayTrie......")
            dat.build(_map)
            if is_cache:
                logger.info(f"正在缓存字典为dat文件......")
                with open(main_path.with_suffix(Predefine.BIN_EXT), "wb") as f:
                    attribute_list = _map.values()
                    if not custom_nature_collector:
                        i = Nature.from_string("begin").ordinal + 1
                        length = len(Nature.values)
                        while i < length:
                            custom_nature_collector.add(Nature.values[i])
                            i += 1
                    IOUtil.write_custom_nature(f, custom_nature_collector)
                    f.write((str(attribute_list.size()) + "\n").encode('utf-8'))
                    for attribute in attribute_list:
                        attribute.save(f)
                    dat.save(f)

        except FileNotFoundError as e:
            logger.warning(f"自定义词典{main_path}不存在！\ndetail: {e}")
            return False
        except IOError as e:
            logger.warning(f"自定义词典{main_path}读取错误！\ndetail: {e}")
            return False
        except Exception as e:
            logger.warning(f"自定义词典{main_path}缓存失败！\ndetail: {e}")
            return False
        return True

    @classmethod
    def _load_dat(cls, path, dat):
        return cls.load_dat(path, CUSTOM_DICTIONARY_PATH, dat)


    @classmethod
    def load_dat(cls, path, custom_dic_path, dat):
        try:
            if CUSTOM_DICTIONARY_AUTO_REFRESH_CACHE and cls.is_dic_need_update(path, custom_dic_path):
                return False
            with open(path.with_suffix(Predefine.BIN_EXT), "rb") as f:
                size = int(f.readline().strip())
                if size < 0:
                    while size <= 0:
                        Nature.create(f.readline().strip().decode("utf-8"))
                        size += 1
                    size = int(f.readline().strip())
                attributes = []
                nature_index_array = Nature.values
                for i in range(size):
                    attribute = CoreDictionary.Attribute.load(f, nature_index_array)
                    attributes.append(attribute)
                if not dat.load(f, attributes):
                    return False

        except Exception as e:
            logger.warning(f"读取失败, \ndetail: {e}")
            return False
        return True

    @classmethod
    def is_dic_need_update(cls, main_path, path):
        bin_path = main_path.with_suffix(Predefine.BIN_EXT)
        if not bin_path.exists():
            return True
        last_modified = os.path.getmtime(bin_path)
        for p in path:
            filename = p.name
            cut = filename.rfind(" ")
            if cut > 0:
                p = p.parent / filename[0:cut]
            if p.exists() and os.path.getmtime(p) > last_modified:
                os.remove(bin_path)
                logger.info(f"已清除自定义词典缓存文件！")
                return True
        return False

    @classmethod
    def a_load(cls, path, default_nature, _map, custom_nature_collector):
        try:
            splitter = r"\s"
            if path.suffix == ".csv":
               splitter = ","
            with open(path, encoding="utf-8") as f:
                for line in f:
                    param = re.split(splitter, line.strip())
                    if not param[0]:
                        continue
                    if NORMALIZATION:
                        param[0] = CharTable.convert(param[0])
                    nature_count = (len(param) - 1) // 2
                    attribute = CoreDictionary.Attribute()
                    if nature_count == 0:
                        attribute.nature.append(default_nature)
                        attribute.frequency.append(1000)
                        attribute.total_frequency = 1000
                    else:
                        for i in range(nature_count):
                            attribute.nature.append(NatureUtility.covert_string2nature(param[1+2*i], custom_nature_collector))
                            attribute.frequency.append(int(param[2+2*i]))
                            attribute.total_frequency += int(param[2+2*i])

                    _map.put(param[0], attribute)
        except Exception as e:
            logger.warning(f"自定义词典{path}读取错误！\ndetail: {e}")
            return False
        return True

    def get(self, word: str):
        if NORMALIZATION:
            word = CharTable.convert(word)
        attribute = self.dat.get(word)
        if attribute is not None:
            return attribute
        if self.trie is None:
            return None
        return self.trie.get(word)

    def contains(self, word):
        if self.dat.exact_match_search(word) >= 0:
            return True
        return self.trie is not None and word in self.trie


if __name__ == "__main__":
    pass
