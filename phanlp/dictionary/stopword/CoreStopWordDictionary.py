# -*- coding: utf-8 -*-
# @Time: 2022/5/23  18:27
# @Author: 2811755762@qq.com
"""
    Description:
        核心停用词词典
"""
import time

from dictionary.stopword.StopWordDictionary import StopWordDictionary
from utility.logger import logger
from utility.CustomError import CoreStopWordDictionaryLoadError
from utility.Predefine import Predefine
from config import CORE_STOP_WORD_DICTIONARY_PATH


class CoreStopWordDictionary:
    dictionary = StopWordDictionary()

    @classmethod
    def load(cls, core_stop_word_dictionary_path, load_cache_if_possible=True):
        start = time.time()
        if cls.__load(core_stop_word_dictionary_path, load_cache_if_possible):
            logger.info(f"核心停用词词典{core_stop_word_dictionary_path}加载成功，{cls.dictionary._size()}个词条，"
                        f"耗时{time.time() - start}s")
        else:
            raise CoreStopWordDictionaryLoadError(f"核心停用词词典{core_stop_word_dictionary_path}加载失败！")

    @classmethod
    def __load(cls, path, load_cache_if_possible=True):
        logger.info(f"核心停用词词典开始加载：{path}")
        if load_cache_if_possible and cls.load_dat(path):
            return True
        try:
            cls.dictionary = StopWordDictionary(path)
            try:
                cls.dictionary.save(path.with_suffix(Predefine.BIN_EXT))
            except Exception as e:
                logger.warning(f"保存失败！\ndetail: {e}")
                return False
        except FileNotFoundError as e:
            logger.warning(f"核心停用词词典{path}不存在！\ndetail: {e}")
            return False
        except IOError as e:
            logger.warning(f"核心停用词词典{path}读取错误！\ndetail: {e}")
            return False
        return True

    @classmethod
    def load_dat(cls, path):
        try:
            with open(path.with_suffix(Predefine.BIN_EXT), "rb") as f:
                cls.dictionary.read(f)
            logger.info(f"核心停用词词典从缓存文件{path.with_suffix(Predefine.BIN_EXT)}中加载......")
        except FileNotFoundError as e:
            logger.warning(f"缓存文件{path.with_suffix(Predefine.BIN_EXT)}不存在！\ndetail: {e}")
            return False
        except Exception as e:
            logger.warning(f"缓存文件{path.with_suffix(Predefine.BIN_EXT)}读取失败！\ndetail: {e}")
            return False
        return True

    @classmethod
    def reload(cls):
        cls.load(CORE_STOP_WORD_DICTIONARY_PATH, False)

    @classmethod
    def contains(cls, key):
        return cls.dictionary.contains(key)

    __contains__ = contains

    @classmethod
    def should_include(cls, term):
        nature = term.nature.to_string() if term.nature is not None else "空"
        first_char = nature[0]
        if term.word not in cls and first_char not in ["m", "b", "c", "e", "o", "p", "q", "u", "y", "z", "r", "w"]:
            return True
        return False


CoreStopWordDictionary.load(CORE_STOP_WORD_DICTIONARY_PATH)
