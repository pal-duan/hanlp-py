# -*- coding: utf-8 -*-
# @Time: 2022/5/1  19:38
# @Author: 2811755762@qq.com
"""
    Description:
    预定义的静态全局变量
"""
import re


class Predefine:
    CHINESE_NUMBERS = "零○〇一二两三四五六七八九十廿百千万亿壹贰叁肆伍陆柒捌玖拾佰仟"
    BIN_EXT = ".bin"
    TOTAL_FREQUENCY = 25146057
    myu = 1 - (1 / TOTAL_FREQUENCY + 0.00001)
    OOV_DEFAULT_FREQUENCY = 10000
    TAG_OTHER = "未##它"  # 其它
    TAG_CLUSTER = "未##串"  # 字符串 x
    TAG_NUMBER = "未##数"  # 数词 m
    TAG_PEOPLE = "未##人"  # 人名 nr
    TAG_PLACE = "未##地"  # 地址
    TAG_GROUP = "未##团"  # 团体名词
    TAG_TIME = "未##时"  # 时间 t
    TAG_PROPER = "未##专"  # 专有名词 nx
    TAG_BIGIN = "始##始"  # 句子的开始 begin
    TAG_END = "末##末"  # 结束 end
    PATTERN_FLOAT_NUMBER = re.compile("^(-?\\d+)(\\.\\d+)?$")

    RIGHT = "\u0000"  # 两个词的正向连接符
    LEFT = "\u0001"  # 两个词的逆向连接符

    MIN_PROBABILITY = 1e-10
    LAMBDA = 0.9  # Unigram 平滑因子

    @classmethod
    def set_total_frequency(cls, total_frequency):
        cls.TOTAL_FREQUENCY = total_frequency
        cls.myu = 1 - (1 / total_frequency + 0.00001)
        cls.OOV_DEFAULT_FREQUENCY = max(1.0, min(cls.OOV_DEFAULT_FREQUENCY / 100, total_frequency))


if __name__ == "__main__":
    pass
