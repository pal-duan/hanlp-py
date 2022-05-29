# -*- coding: utf-8 -*-
# @Time: 2022/5/28  22:24
# @Author: 2811755762@qq.com
"""
    Description:
    
"""


class TrieConfig:
    def __init__(self):
        self.allow_overlaps = True  # 允许重叠
        self.remain_longest = False  # 只保留最长匹配

    def is_allow_overlaps(self):
        return self.allow_overlaps

    def set_allow_overlaps(self, allow_overlaps):
        self.allow_overlaps = allow_overlaps


if __name__ == "__main__":
    pass
