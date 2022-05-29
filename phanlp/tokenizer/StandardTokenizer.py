# -*- coding: utf-8 -*-
# @Time: 2022/5/22  21:54
# @Author: 2811755762@qq.com
"""
    Description:
        标准分词器
"""
from phanlp.phanlp import Phanlp


class StandardTokenizer:
    SEGMENT = Phanlp.new_segment()

    @classmethod
    def segment(cls, text: str) -> list:
        return cls.SEGMENT.seg(text)

    @classmethod
    def seg2sentence(cls, text: str, shortest: bool = False) -> list:
        return cls.SEGMENT.seg2sentence(text, shortest)


if __name__ == "__main__":
    pass
