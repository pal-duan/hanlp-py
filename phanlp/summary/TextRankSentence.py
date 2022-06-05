

import re
from functools import cmp_to_key

from summary.BM25 import BM25
from algorithm.pytreemap import TreeMap
from tokenizer.StandardTokenizer import StandardTokenizer
from dictionary.stopword.CoreStopWordDictionary import CoreStopWordDictionary


StandardTokenizer.SEGMENT.enable_part_of_speech_tagging(True)


class TextRankSentence:
    d = 0.85
    max_iter = 200
    min_diff = 0.001
    default_sentence_separator = "[,，。：:“”?？！!;；]"

    def __init__(self, docs):
        self.docs = docs
        self.bm25 = BM25(docs)
        self.D = len(docs)
        self.weight = []
        self.weight_sum = []
        self.vertex = []
        self.top = TreeMap()
        self.solve()

    def solve(self):
        cnt = 0
        for sentence in self.docs:
            scores = self.bm25.sim_all(sentence)
            self.weight.append(scores)
            self.weight_sum.append(sum(scores) - scores[cnt])
            self.vertex.append(1.0)
            cnt += 1
        for buffer in range(self.max_iter):
            m = []
            max_diff = 0
            for i in range(self.D):
                m.append(1 - self.D)
                for j in range(self.D):
                    if j == i or self.weight_sum[j] == 0:
                        continue
                    m[i] += (self.d * self.weight[j][i] / self.weight_sum[j] * self.vertex[j])
                diff = abs(m[i] - self.vertex[i])
                if diff > max_diff:
                    max_diff = diff
            self.vertex = m
            if max_diff <= self.min_diff:
                break

        for i in range(self.D):
            self.top.put(self.vertex[i], i)

    def get_top_sentence(self, size):
        values = self.top.values()
        size = min(size, len(values))
        it = values.iterator()
        index_array = []
        for i in range(size):
            index_array.append(it.next())
        return index_array

    @staticmethod
    def split_sentence(document, sentence_separator=default_sentence_separator):
        sentences = []
        for line in re.split("[\r\n]", document):
            line = line.strip()
            if not len(line):
                continue
            for sent in re.split(sentence_separator, line):
                sent = sent.strip()
                if not len(sent):
                    continue
                sentences.append(sent)
        return sentences

    @classmethod
    def convert_sentence_list2document(cls, sentence_list):
        docs = []
        for sentence in sentence_list:
            term_list = StandardTokenizer.segment(sentence)
            word_list = []
            for term in term_list:
                if CoreStopWordDictionary.should_include(term):
                    word_list.append(term.word)
            docs.append(word_list)
        return docs

    @classmethod
    def get_top_sentence_list(cls, document, size, sentence_separator=default_sentence_separator):
        sentence_list = cls.split_sentence(document, sentence_separator)
        docs = cls.convert_sentence_list2document(sentence_list)
        text_rank = TextRankSentence(docs)
        top_sentence = text_rank.get_top_sentence(size)
        result = []
        for i in top_sentence:
            result.append(sentence_list[i])
        return result

    @classmethod
    def get_summary(cls, document, max_length, sentence_separator=default_sentence_separator):
        sentence_list = cls.split_sentence(document, sentence_separator)
        sentence_count = len(sentence_list)
        document_length = len(document)
        sentence_length_avg = document_length / sentence_count
        size = int(max_length / sentence_length_avg + 1)
        docs = cls.convert_sentence_list2document(sentence_list)
        text_rank = TextRankSentence(docs)
        top_sentence = text_rank.get_top_sentence(size)
        result = []
        for i in top_sentence:
            result.append(sentence_list[i])

        result = cls.permutation(result, sentence_list)
        result = cls.pick_sentences(result, max_length)
        return "。".join(result) + "。"

    @classmethod
    def permutation(cls, result, sentence_list):
        def custom_compare(x, y):
            num1 = sentence_list.index(x)
            num2 = sentence_list.index(y)
            return (num1 - num2) > 0
        return list(sorted(result, key=cmp_to_key(custom_compare)))

    @classmethod
    def pick_sentences(cls, result, max_length):
        summary = []
        count = 0
        for res in result:
            if count + len(res) <= max_length:
                summary.append(res)
                count += len(res)
        return summary


if __name__ == '__main__':
    s = "7月21日，渤海海况恶劣，至少发生3起沉船事故，10余名船员危在旦夕。危急时刻，中国海油渤海油田再次行动起来，紧急调配救援力量救起10名遇险人员。" \
        + "21日一早，一阵急促的铃声，在渤海石油管理局总值班室骤然响起。这是天津海上搜救中心打来的电话。正在值班的作业协调部主管邬礼凯心里“咯噔”一下——天津海上搜救中心称，"\
        + "在“海洋石油932”平台西南方7海里处，一艘货轮遇险、处于倾覆边缘，4名船员命悬一线。时间就是生命！邬礼凯立即组织海上救援力量，立即驰奔事故发生地点。"\
        + "“滨海264”船接到任务单后，仅一个小时便抵达事故现场。此时，货船已完全倾覆。“滨海264”立刻开展救援工作，仅25分钟便将4人全部救出。"
    separator = "[。?？!！]"
    print(TextRankSentence.get_top_sentence_list(s, 2))
    print(TextRankSentence.get_top_sentence_list(s, 2, separator))
    print(TextRankSentence.get_summary(s, 100))
    print(TextRankSentence.get_summary(s, 100, separator))
