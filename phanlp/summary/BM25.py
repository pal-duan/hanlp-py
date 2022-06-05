

import math

from algorithm.pytreemap import TreeMap


class BM25:
    k1 = 1.5
    b = 0.75

    def __init__(self, docs):
        self.docs = docs
        self.D = len(docs)  # 文档句子的个数
        self.avgdl = 0  # 文档句子的平均长度
        for sentence in docs:
            self.avgdl += len(sentence)
        self.avgdl /= self.D
        self.f = {}  # 文档中每个句子中的每个词与词频
        self.df = TreeMap()  # 文档中全部词语与出现在几个句子中
        self.idf = TreeMap()
        self.init()

    def init(self):
        """
        在构造时初始化自己的所有参数
        :return:
        """
        index = 0
        for sentence in self.docs:
            tf = TreeMap()
            for word in sentence:
                freq = tf.get(word)
                freq = (0 if freq is None else freq) + 1
                tf.put(word, freq)
            self.f[index] = tf
            for entry in tf:
                freq = self.df.get(entry)
                freq = (0 if freq is None else freq) + 1
                self.df.put(entry, freq)
            index += 1
        for k, v in self.df.items():
            self.idf.put(k, math.log(self.D - v + 0.5) - math.log(v + 0.5))

    def sim(self, sentence, index):
        score = 0
        for word in sentence:
            if not self.f[index].contains_key(word):
                continue
            d = len(self.docs[index])
            tf = self.f[index].get(word)
            score += (self.idf.get(word) * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * d / self.avgdl)))
        return score

    def sim_all(self, sentence):
        scores = []
        for i in range(self.D):
            scores.append(self.sim(sentence, i))
        return scores
