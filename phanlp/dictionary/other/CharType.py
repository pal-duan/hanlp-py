import time
import ujson

from utility.logger import logger
from config import CHAR_TYPE_PATH
from utility.CustomError import IllegalArgumentError
from utility.TextUtility import TextUtility
from utility.Predefine import Predefine


class CharType:
    CT_SINGLE = 5  # 单字节
    CT_DELIMITER = CT_SINGLE + 1  # 分隔符
    CT_CHINESE = CT_SINGLE + 2  # 中文字符
    CT_LETTER = CT_SINGLE + 3  # 字母
    CT_NUM = CT_SINGLE + 4  # 数字
    CT_INDEX = CT_SINGLE + 5  # 序号
    CT_CNUM = CT_SINGLE + 6  # 中文数字
    CT_OTHER = CT_SINGLE + 12  # 其他
    char_type = []

    @classmethod
    def load(cls, path):
        logger.info(f"字符类型对应表开始加载{CHAR_TYPE_PATH}")
        start = time.time()
        try:
            with open(CHAR_TYPE_PATH) as f:
                res = ujson.load(f)
            cls.char_type = res
        except Exception as e:
            raise IllegalArgumentError(f"字符类型对应表{path}加载失败：\ndetail: {e}")
        logger.info(f"字符类型对应表加载成功，耗时{time.time()-start}s")

    @classmethod
    def get(cls, c):
        return cls.char_type[ord(c)]

    @classmethod
    def set(cls, c, t):
        cls.char_type[ord(c)] = t


CharType.load(CHAR_TYPE_PATH)


if __name__ == '__main__':
    # with open("D:\模型\hanlp-py\data\dictionary\other\CharType.bin", "rb") as f:
    #     line = f.read()
    #     print(str(line, "utf-8"))
    # CharType.load(CHAR_TYPE_PATH)
    # with open("bak.txt", "w", encoding="utf-8") as f:
    #     for i in range(65536):
    #         try:
    #             a = chr(i)
    #             b = chr(i).encode()
    #             c = b[0]
    #             d = b[1] if len(b) > 1 else 0
    #         except:
    #             a = ""
    #             b = ""
    #             c = ""
    #             d = ""
    #         print(i, a, b, c, d)
    #         f.write(f"{str(i)}    {str(a)}    {str(b)}    {str(c)}    {str(d)}")
    #         f.write("\n")
    import ujson
    with open("../../../data/dictionary/other/CharType.json", "r") as f:
        result = ujson.load(f)
        for i, t in enumerate(result):
            if t == 8:
                print(t, chr(i))
