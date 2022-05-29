# -*- coding: utf-8 -*-
# @Time: 2022/5/29  10:56
# @Author: 2811755762@qq.com
"""
    Description:
        一个模式串匹配结果
"""
from algorithm.ahocorasick.interval.Interval import Interval


class Emit(Interval):
    def __init__(self, start: int, end: int, keyword: str):
        super().__init__(start, end)
        self.keyword = keyword

    def get_keyword(self):
        return self.keyword

    def to_string(self):
        return f"{super().to_string()}={self.keyword}"


if __name__ == "__main__":
    pass
