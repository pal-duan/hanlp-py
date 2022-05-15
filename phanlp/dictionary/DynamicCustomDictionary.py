# -*- coding: utf-8 -*-
# @Time: 2022/5/15  17:31
# @Author: 2811755762@qq.com
"""
    Description:
    
"""
import time
import os
from pathlib import Path

from config import CUSTOM_DICTIONARY_PATH, CUSTOM_DICTIONARY_AUTO_REFRESH_CACHE
from collection.trie.DoubleArrayTrie import DoubleArrayTrie
from collection.trie.BinTrie import BinTrie
from utility.logger import logger
from utility.Predefine import Predefine


class DynamicCustomDictionary:
    def __init__(self, *path):
        if not path:
            path = CUSTOM_DICTIONARY_PATH
        self.dat = DoubleArrayTrie()
        self.trie = BinTrie()
        self.path = None
        self.load(*path)

    def load(self, *path):
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
        # TODO

    @classmethod
    def _load_dat(cls, path, dat):
        cls.load_dat(path, CUSTOM_DICTIONARY_PATH, dat)

    @classmethod
    def load_dat(cls, path, custom_dic_path, dat):
        try:
            if CUSTOM_DICTIONARY_AUTO_REFRESH_CACHE and cls.is_dic_need_update(path, custom_dic_path):
                return False
            # TODO
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
            filename = os.path.basename(p)
            cut = filename.rfind(" ")
            if cut > 0:
                p = p.parent() / filename[0:cut]
            if p.exists() and os.path.getmtime(p) > last_modified:
                os.remove(bin_path)
                logger.info(f"已清除自定义词典缓存文件！")
                return True
        return False










if __name__ == "__main__":
    pass
