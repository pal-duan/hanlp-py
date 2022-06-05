

"""
TF-IDF统计工具兼关键词提取工具
"""
from summary.KeywordExtractor import KeywordExtractor
from tokenizer.StandardTokenizer import StandardTokenizer
from mining.word.TfIdf import TfIdf
from algorithm.Heap import MinHeap


class TfIdfCounter(KeywordExtractor):
    def __init__(self, default_segment=StandardTokenizer.SEGMENT, filter_stop_word=True):
        super().__init__(default_segment)
        self.filter_stop_word = filter_stop_word
        self.tf_map = {}
        self.tf_idf_map = {}
        self.idf = None

    def _get_keywords(self, term_list: list, size: int):
        entry_list = self.get_keywords_with_tf_idf(term_list, size)
        r = []
        for entry in entry_list:
            r.append(entry)
        return r

    def get_keywords_with_tf_idf(self, term_list, size):
        if isinstance(term_list, str):
            term_list = self.preprocess(term_list)

        if self.idf is None:
            self.compute()

        tf_idf = TfIdf.tf_idf(TfIdf.tf(self.convert(term_list)), self.idf)
        return self.top_n(tf_idf, size)

    def add(self, id=None, term_list=""):
        if id is None:
            id = len(self.tf_map)
        if isinstance(term_list, str):
            term_list = self.preprocess(term_list)
        words = self.convert(term_list)
        tf = TfIdf.tf(words)
        self.tf_map[id] = tf
        self.idf = None

    @staticmethod
    def custom_compare(x, y):
        if x[1] == y[1]:
            if x[0] < y[0]:
                return True
            else:
                return False
        elif x[1] < y[1]:
            return True
        else:
            return False

    def top_n(self, tf_idfs, size):
        heap = MinHeap(size, self.custom_compare)
        heap.heapify(tf_idfs.items())
        return heap.to_list()

    def preprocess(self, document):
        term_list = self.default_segment.seg(document)
        if self.filter_stop_word:
            term_list = self.filter_term_list(term_list)
        return term_list

    def compute(self):
        if self.idf is None:
            self.idf = TfIdf.idf(self.tf_map.values())

        for k, v in self.tf_map.items():
            tf_idf = TfIdf.tf_idf(v, self.idf)
            self.tf_idf_map[k] = tf_idf
        return self.tf_idf_map

    @staticmethod
    def convert(term_list):
        words = []
        for term in term_list:
            words.append(term.word)
        return words

    def documents(self):
        return self.tf_map.keys()

    def get_keyword_of(self, id, size=10):
        tf_idfs = self.tf_idf_map.get(id)
        return self.top_n(tf_idfs, size) if tf_idfs is not None else None


if __name__ == '__main__':
    counter = TfIdfCounter()
    counter.add("《女排夺冠》", "女排北京奥运会夺冠");
    counter.add("《羽毛球男单》", "北京奥运会的羽毛球男单决赛");
    counter.add("《女排》", "中国队女排夺北京奥运会金牌重返巅峰，观众欢呼女排女排女排！");
    counter.compute();
    for id in counter.documents():
        print(f"{id}: {counter.get_keyword_of(id, 3)}")
    print(counter.get_keywords("奥运会反兴奋剂", 2))


