# -*- coding: utf-8 -*-
# @Time: 2022/5/28  16:13
# @Author: 2811755762@qq.com
"""
    Description:
        原子分词节点
"""
from corpus.tag.Nature import Nature
from dictionary.other.CharType import CharType
from utility.Predefine import Predefine


class AtomNode:
    def __init__(self, s_word, n_pos):
        self.s_word = s_word
        self.n_pos = n_pos

    def get_nature(self):
        nature = Nature.from_string("nz")
        if self.n_pos == CharType.CT_CNUM or self.n_pos == CharType.CT_NUM or self.n_pos == CharType.CT_INDEX:
            nature = Nature.from_string("m")
            self.s_word = Predefine.TAG_NUMBER
        elif self.n_pos == CharType.CT_DELIMITER:
            nature = Nature.from_string("w")
        elif self.n_pos == CharType.CT_LETTER:
            nature = Nature.from_string("nx")
            self.s_word = Predefine.TAG_CLUSTER
        elif self.n_pos == CharType.CT_SINGLE:
            if Predefine.PATTERN_FLOAT_NUMBER.match(self.s_word):
                nature = Nature.from_string("m")
                self.s_word = Predefine.TAG_NUMBER
            else:
                nature = Nature.from_string("nx")
                self.s_word = Predefine.TAG_CLUSTER
        return nature

    def to_string(self):
        return f"AtomNode{{word={self.s_word}, nature={self.n_pos}"






if __name__ == "__main__":
    pass
