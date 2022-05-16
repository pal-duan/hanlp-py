# -*- coding: utf-8 -*-
# @Time: 2022/5/1  17:24
# @Author: 2811755762@qq.com
"""
    Description:
    
"""
from dictionary.CoreDictionary import CoreDictionary
from dictionary.CustomDictionary import CustomDictionary
from corpus.tag.Nature import Nature


class LexiconUtility(object):
    @classmethod
    def get_attribute(cls, word: str) -> int:
        attribute = CoreDictionary.get(word)
        if attribute is not None:
            return attribute
        return CustomDictionary.get(word)

    @classmethod
    def get_frequency(cls, word: str) -> int:
        attribute = cls.get_attribute(word)
        if attribute is None:
            return 0
        return attribute.total_frequency

    @classmethod
    def covert_string2nature(cls, name, custom_nature_collector):
        nature = Nature.from_string(name)
        if nature is None:
            nature = Nature.create(name)
            if custom_nature_collector is not None:
                custom_nature_collector.add(nature)
        return nature


if __name__ == "__main__":
    pass
