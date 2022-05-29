# -*- coding: utf-8 -*-
# @Time: 2022/5/29  10:58
# @Author: 2811755762@qq.com
"""
    Description:
        区间
"""


class Interval:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def size(self):
        return self.end - self.start + 1

    def overlaps_with(self, other):
        if isinstance(other, Interval):
            return self.start <= other.get_end() and self.end >= other.get_start()
        elif isinstance(other, int):
            return self.start <= other and self.end >= other

    def __eq__(self, other):
        if not isinstance(other, Interval):
            return False
        return self.start == other.get_start() and self.end == other.get_end()

    def hash_code(self):
        return self.start % 100 + self.end % 100

    __hash__ = hash_code

    def to_string(self):
        return f"{self.start}:{self.end}"


if __name__ == "__main__":
    pass
