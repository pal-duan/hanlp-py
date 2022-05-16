# -*- coding: utf-8 -*-
# @Time: 2022/5/1  19:38
# @Author: 2811755762@qq.com
"""
    Description:
    预定义的静态全局变量
"""


class Predefine:
    BIN_EXT = ".bin"
    TOTAL_FREQUENCY = 25146057
    myu = 1 - (1 / TOTAL_FREQUENCY + 0.00001)
    OOV_DEFAULT_FREQUENCY = 10000
    TAG_OTHER = "未##它"  # 其它

    @classmethod
    def set_total_frequency(cls, total_frequency):
        cls.TOTAL_FREQUENCY = total_frequency
        cls.myu = 1 - (1 / total_frequency + 0.00001)
        cls.OOV_DEFAULT_FREQUENCY = max(1.0, min(cls.OOV_DEFAULT_FREQUENCY / 100, total_frequency))


if __name__ == "__main__":
    pass
