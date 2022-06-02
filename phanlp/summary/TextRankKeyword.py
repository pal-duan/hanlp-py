# -*- coding: utf-8 -*-
# @Time: 2022/5/22  14:49
# @Author: 2811755762@qq.com
"""
    Description:
        基于TextRank算法的关键词提取，适用于单文档
"""
from collections import OrderedDict
import math

from summary.KeywordExtractor import KeywordExtractor
from algorithm.Heap import MinHeap
from algorithm.pytreemap import TreeMap, TreeSet
from tokenizer.StandardTokenizer import StandardTokenizer


class TextRankKeyword(KeywordExtractor):
    d = 0.85  # 阻尼系数
    max_iter = 200  # 最大迭代次数
    min_diff = 0.001

    def __init__(self, default_segment=StandardTokenizer.SEGMENT):
        super().__init__(default_segment)

    @classmethod
    def get_keyword_list(cls, document: str, size: int):
        text_rank_keyword = cls()
        return text_rank_keyword.get_keywords(document, size)

    def get_keyword(self, content):
        return self.get_keywords(content)

    @staticmethod
    def custom_compare(x, y):
        if x[1] < y[1]:
            return True
        else:
            return False

    def top(self, size: int, _map):
        result = OrderedDict()
        heap = MinHeap(size, self.custom_compare).heapify(_map.items()).to_list()
        for entry in heap:
            result[entry[0]] = entry[1]
        return result

    def get_term_and_rank(self, term_list, size=None):
        """
        使用已经分好的词来计算rank
        :param term_list:
        :return:
        """
        if isinstance(term_list, str):
            term_list = self.default_segment.seg(term_list)

        word_list = []
        for t in term_list:
            if self.should_include(t):
                word_list.append(t.word)

        words = TreeMap()
        que = []
        for w in word_list:
            if not words.contains_key(w):
                words.put(w, TreeSet())
            if len(que) >= 5:
                que = que[1:]
            for q_word in que:
                if w == q_word:
                    continue
                words.get(w).add(q_word)
                words.get(q_word).add(w)
            que.append(w)

        score = {}
        for k, v in words.items():
            score[k] = self.sigmoid(len(v))
        for i in range(self.max_iter):
            m = {}
            max_diff = 0
            for k, v in words.items():
                m[k] = 1 - self.d
                for element in v:
                    size = len(words.get(element))
                    if k == element or size == 0:
                        continue
                    m[k] = m.get(k) + self.d / size * (0 if score.get(element) is None else score.get(element))
                max_diff = max(max_diff, abs(m.get(k) - (0 if score.get(k) is None else score.get(k))))
            score = m
            if max_diff <= self.min_diff:
                break
        if size:
            score = self.top(size, score)
        return score

    @staticmethod
    def sigmoid(value):
        return 1 / (1 + math.exp(-value))

    def _get_keywords(self, term_list: list, size: int):
        entry_set = self.top(size, self.get_term_and_rank(term_list))
        result = []
        for entry in entry_set:
            result.append(entry)
        return result


if __name__ == "__main__":
    print(TextRankKeyword.get_keyword_list("来源：中国科学报本报讯（记者肖洁）又有一位中国科学家喜获小行星命名殊荣！4月19日下午，中国科学院国家天文台在京举行“周又元星”颁授仪式，" \
           "我国天文学家、中国科学院院士周又元的弟子与后辈在欢声笑语中济济一堂。国家天文台党委书记、" \
           "副台长赵刚在致辞一开始更是送上白居易的诗句：“令公桃李满天下，何须堂前更种花。”" \
           "据介绍，这颗小行星由国家天文台施密特CCD小行星项目组于1997年9月26日发现于兴隆观测站，" \
           "获得国际永久编号第120730号。2018年9月25日，经国家天文台申报，" \
           "国际天文学联合会小天体联合会小天体命名委员会批准，国际天文学联合会《小行星通报》通知国际社会，" \
           "正式将该小行星命名为“周又元星”。", 3))
    print(TextRankKeyword().get_keyword("中国队女排夺北京奥运会金牌重返巅峰，观众欢呼女排女排女排！"))
    print(TextRankKeyword().get_term_and_rank("中国队女排夺北京奥运会金牌重返巅峰，观众欢呼女排女排女排！"))