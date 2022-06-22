

"""
核心同义词词典
"""
from config import CORE_SYNONYM_DICTIONARY_PATH
from dictionary.common.CommonRelationDictionary import CommonRelationDictionary
from spider.baidu_hanyu_spider import BaiduHanyuSpider


class CoreSynonymDictionary:
    dictionary = CommonRelationDictionary.create(CORE_SYNONYM_DICTIONARY_PATH)

    @classmethod
    def get(cls, key):
        res = cls.dictionary[key]
        # 本地词典中不存在，从外部资源获取
        if res is None:
            synonym_list = cls.get_synonym_from_else(key)

        return

    def __getitem__(self, key):
        return self.get(key)

    @classmethod
    def get_synonym_from_else(cls, key):
        res1 = BaiduHanyuSpider.search(key)

    def rewrite_quickly(self, text):
        pass
        # TODO

    def rewrite(self, text):
        pass
        # TODO

    def create_synonym_list(self, sentence, with_undefined_item):
        pass
        # TODO
