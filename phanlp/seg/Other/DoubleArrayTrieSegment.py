# -*- coding: utf-8 -*-
# @Time: 2022/5/22  23:31
# @Author: 2811755762@qq.com
"""
    Description:
        使用DoubleArrayTrie实现的最长分词器
"""
from seg.DictionaryBasedSegment import DictionaryBasedSegment
from dictionary.CoreDictionary import CoreDictionary
from collection.trie.DoubleArrayTrie import DoubleArrayTrie
from corpus.io.IOUtil import IOUtil
from corpus.tag.Nature import Nature
from seg.common.Term import Term


class DoubleArrayTrieSegment(DictionaryBasedSegment):
    def __init__(self, trie=CoreDictionary.trie):
        super().__init__()
        if isinstance(trie, DoubleArrayTrie):
            self.trie = trie
        elif isinstance(trie, list):
            self.trie = IOUtil.load_dictionary(trie)
        elif isinstance(trie, str):
            self.trie = IOUtil.load_dictionary([trie])
        self.config.use_custom_dictionary = True

    def seg2word(self, text: str):
        word_net = [1] * len(text)
        nature_array = [None] * len(text) if self.config.speech_tagging else None
        self.match_longest(text, word_net, nature_array, self.trie)
        if self.config.use_custom_dictionary:
            self.match_longest(text, word_net, nature_array, self.custom_dictionary.dat)
            if self.custom_dictionary.trie is not None:
                # TODO
                pass
        term_list = []
        self.pos_tag(text, word_net, nature_array)
        i = 0
        while i < len(word_net):
            term = Term(text[i:i+word_net[i]], (Nature.from_string("nz") if nature_array[i] is None else
                        nature_array[i]) if self.config.speech_tagging else None)
            term.offset = i
            term_list.append(term)
            i += word_net[i]
        return term_list

    def match_longest(self, sentence, word_net, nature_array, trie):
        searcher = trie.get_longest_searcher(sentence, 0)
        while searcher.next():
            word_net[searcher.begin] = searcher.length
            if self.config.speech_tagging:
                nature_array[searcher.begin] = searcher.value.nature[0]


if __name__ == "__main__":
    segment = DoubleArrayTrieSegment()
    segment.enable_part_of_speech_tagging(True)
    print(segment.seg("7月21日，渤海海况恶劣，至少发生3起沉船事故，10余名船员危在旦夕。危急时刻，中国海油渤海油田再次行动起来，紧急调配救援力量救起10名遇险人员。"))
