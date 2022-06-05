# -*- coding: utf-8 -*-
# @Time: 2022/6/3  21:16
# @Author: 2811755762@qq.com
"""
    Description:
        实词分词器，自动移除停用词
"""
from seg import new_segment
from dictionary.stopword.CoreStopWordDictionary import CoreStopWordDictionary


class NotionalTokenizer:
    SEGMENT = new_segment()

    @classmethod
    def segment(cls, text):
        result_list = cls.SEGMENT.seg(text)
        res = []
        for term in result_list:
            if CoreStopWordDictionary.should_include(term):
                res.append(term)
        return res

    @classmethod
    def seg2sentence(cls, text, shortest=True, filter_array_chain=None):
        sentence_list = cls.SEGMENT.seg2sentence(text, shortest)
        res = []
        for sentence in sentence_list:
            _res = []
            for term in sentence:
                if filter_array_chain is not None:
                    for _filter in filter_array_chain:
                        if not _filter.should_include(term):
                            break
                    else:
                        _res.append(term)
                else:
                    _res.append(term)
            res.append(_res)
        return res


if __name__ == "__main__":
    pass
