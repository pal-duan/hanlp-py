

"""
词频-倒排文档词频统计
"""
from enum import Enum
import math


class TfIdf:
    class TfType(Enum):
        """
        词频统计方式
        """
        NATURAL = 0  # 普通词频
        LOGARITHM = 1  # 词频的对数并加1
        BOOLEAN = 2  # 01词频

    class Normalization(Enum):
        """
        tf-idf 向量的正规化算法
        """
        NONE = 0  # 不正规化
        COSINE = 1  # cosin正规化

    @classmethod
    def tf(cls, document, tf_type=TfType.NATURAL):
        tf = {}
        for term in document:
            f = tf.get(term, 0.0)
            tf[term] = f + 1

        if tf_type != cls.TfType.NATURAL:
            for term in tf:
                if tf_type == cls.TfType.LOGARITHM:
                    tf[term] = 1 + math.log(tf.get(term))
                elif tf_type == cls.TfType.BOOLEAN:
                    tf[term] = 0.0 if tf.get(term) == 0.0 else 1.0
        return tf

    @classmethod
    def tfs(cls, documents, tf_type=TfType.NATURAL):
        tfs = []
        for document in documents:
            tfs.append(cls.tf(document, tf_type))
        return tfs

    @staticmethod
    def idf(document_vocabularies, smooth=True, add_one=True):
        df = {}
        d = 1 if smooth else 0
        a = 1 if add_one else 0
        n = d
        for document_vocabulary in document_vocabularies:
            n += 1
            for term in document_vocabulary:
                t = df.get(term, d)
                df[term] = t + 1
        idf = {}
        for term, f in df.items():
            idf[term] = math.log(n / f) + a
        return idf

    @classmethod
    def tf_idf(cls, tf, idf, normalization=Normalization.NONE):
        tf_idf = {}
        for term in tf:
            _tf = tf.get(term, 1)
            _idf = idf.get(term, 1)
            tf_idf[term] = _tf * _idf

        if normalization == cls.Normalization.COSINE:
            n = 0
            for x in tf_idf.values():
                n += x * x
            n = math.sqrt(n)
            for term in tf_idf:
                tf_idf[term] = tf_idf.get(term) / n

        return tf_idf




