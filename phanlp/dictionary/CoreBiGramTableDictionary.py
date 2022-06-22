import time
import re
import pickle
import os

from config import BI_GRAM_DICTIONARY_PATH
from utility.logger import logger
from utility.CustomError import IllegalArgumentError
from utility.Predefine import Predefine
from algorithm.pytreemap import TreeMap
from dictionary.CoreDictionary import CoreDictionary


class CoreBiGramTableDictionary:
    start = []
    pair = []

    @classmethod
    def load(cls):
        path = BI_GRAM_DICTIONARY_PATH
        logger.info(f"开始加载二元词典：{path}.table")
        start = time.time()
        if not cls.__load(path):
            raise IllegalArgumentError("二元词典加载失败")
        else:
            logger.info(f"{path}.table加载成功，耗时{time.time() - start}s")

    @classmethod
    def __load(cls, path):
        dat_path = f"{BI_GRAM_DICTIONARY_PATH}.table{Predefine.BIN_EXT}"
        if cls.load_dat(dat_path):
            return True
        _map = TreeMap()
        try:
            total = 0
            max_word_id = CoreDictionary.trie.count()
            with open(path, encoding="utf-8") as f:
                for line in f:
                    params = re.split("\\s", line)
                    a, b = params[0].split("@", maxsplit=2)
                    id_a = CoreDictionary.trie.exact_match_search(a)
                    if id_a == -1:
                        continue
                    id_b = CoreDictionary.trie.exact_match_search(b)
                    if id_b == -1:
                        continue
                    freq = int(params[1])
                    bi_map = _map.get(id_a)
                    if bi_map is None:
                        bi_map = TreeMap()
                        _map.put(id_a, bi_map)
                    bi_map.put(id_b, freq)
                    total += 2
            cls.start = [0] * (max_word_id + 1)
            cls.pair = [0] * total
            offset = 0
            for i in range(max_word_id):
                b_map = _map.get(i)
                if b_map is not None:
                    for k, v in b_map.items():
                        index = offset << 1
                        cls.pair[index] = k
                        cls.pair[index+1] = v
                        offset += 1
                cls.start[i+1] = offset
            logger.info(f"二元词典读取完毕：{path},构建为TableBin结构")
        except FileNotFoundError as e:
            logger.error(f"二元词典{path}不存在！\ndetail: {e}")
            return False
        except IOError as e:
            logger.error(f"二元词典{path}读取错误！\ndetail:{e}")
            return False
        logger.info(f"开始缓存二元词典到{dat_path}")
        if not cls.save_dat(dat_path):
            logger.warning(f"缓存二元词典到{dat_path}失败！")
        return True

    @classmethod
    def load_dat(cls, path):
        try:
            with open(path, "rb") as f:
                obj = pickle.load(f)
                cls.start = obj["start"]
                if CoreDictionary.trie.count() != len(cls.start) - 1:
                    logger.warning(f"缓存文件有误！")
                    return False
                cls.pair = obj["pair"]
        except Exception as e:
            logger.warning(f"尝试载入缓存文件{path}发生异常【{e}】, 下面将载入源文件并自动缓存......")
            return False
        return True

    @classmethod
    def save_dat(cls, path):
        try:
            with open(path, "wb") as f:
                pickle.dump({"pair": cls.pair, "start": cls.start}, f)
        except Exception as e:
            logger.warning(f"在缓存{path}时发生异常，\ndetail{e}")
            return False
        return True

    @staticmethod
    def binary_search(a, from_index, length, key):
        low = from_index
        high = from_index + length - 1
        while low <= high:
            mid = (low + high) // 2
            mid_val = a[mid << 1]
            if mid_val < key:
                low = mid + 1
            elif mid_val > key:
                high = mid - 1
            else:
                return mid
        return -(low + 1)

    @classmethod
    def get_bi_frequency(cls, a, b):
        id_a = CoreDictionary.trie.exact_match_search(a)
        if id_a == -1:
            return 0
        id_b = CoreDictionary.trie.exact_match_search(b)
        if id_b == -1:
            return 0
        index = cls.binary_search(cls.pair, cls.start[id_a], cls.start[id_a+1]-cls.start[id_a], id_b)
        if index < 0:
            return 0
        index <<= 1
        return cls.pair[index+1]

    @classmethod
    def reload(cls):
        path = BI_GRAM_DICTIONARY_PATH
        os.remove(f"{path}.table{Predefine.BIN_EXT}")
        return cls.load()


CoreBiGramTableDictionary.load()


if __name__ == '__main__':
    print(CoreBiGramTableDictionary.get_bi_frequency("高性能", "计算"))
