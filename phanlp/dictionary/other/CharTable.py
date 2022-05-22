import time
from pathlib import Path
import string
import pickle

from utility.logger import logger
from utility.Predefine import Predefine
from config import  CHAR_TABLE_PATH


class CharTableLoadError(Exception):
    pass


class CharTable:
    CONVERT = [chr(i) for i in range(65536)]

    @classmethod
    def load(cls, path):
        start = time.time()
        if not cls.__load(path):
            raise CharTableLoadError("字符正规化表加载失败")
        logger.info(f"字符正规化表加载成功, 耗时{time.time()-start}s")

    @classmethod
    def __load(cls, path):
        if isinstance(path, str):
            path = Path(path)
        bin_path = path.with_suffix(Predefine.BIN_EXT)
        if cls.load_bin(bin_path):
            return True
        with open(path, encoding="utf-8") as f:
            for line in f:
                if len(line) != 3:
                    continue
                cls.CONVERT[ord(line[0])] = cls.CONVERT[ord(line[2])]
        for c in string.whitespace:
            cls.CONVERT[ord(c)] = " "
        logger.info(f"正在缓存字符正则化表到{bin_path}")
        with open(bin_path, "wb") as fp:
            pickle.dump(cls.CONVERT, fp)
        return True

    @classmethod
    def load_bin(cls, path):
        try:
            with open(path, "rb") as fp:
                cls.CONVERT = pickle.load(fp)
        except Exception as e:
            logger.warning(f"字符正规化表缓存{path}加载失败，\ndetail: {e}")
            return False
        return True

    @classmethod
    def convert(cls, sentence):
        assert sentence is not None
        res = ""
        for s in sentence:
            res += cls.CONVERT[ord(s)]
        return res


CharTable.load(CHAR_TABLE_PATH)


if __name__ == '__main__':
    pass
