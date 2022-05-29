# -*- coding: utf-8 -*-
# @Time: 2022/5/23  10:54
# @Author: 2811755762@qq.com
"""
    Description:
        分词器（分词服务）
        是所有分词器的基类
        分词器的分词方法是线程安全的，但配置方法则不保证
"""
import abc
import multiprocessing

from seg.Config import Config
from dictionary.CustomDictionary import CustomDictionary
from config import NORMALIZATION
from dictionary.other.CharTable import CharTable
from dictionary.other.CharType import CharType
from utility.SentencesUtil import SentencesUtil
from utility.CustomError import IllegalArgumentError
from seg.NShort.Path.AtomNode import AtomNode


class Segment(metaclass=abc.ABCMeta):
    custom_dictionary = CustomDictionary.DEFAULT

    def __init__(self):
        self.config = Config()

    def seg(self, text: str) -> list:
        assert text is not None
        if NORMALIZATION:
            text = CharTable.convert(text)
        return self.seg2word(text)

    @abc.abstractmethod
    def seg2word(self, text: str):
        pass

    def seg2sentence(self, text: str, shortest: bool) -> list:
        result = []
        for sentence in SentencesUtil.to_sentence_list(text, shortest):
            result.append(self.seg2word(sentence))
        return result

    def atom_segment(self):
        """
        原子分词
        :return:
        """
        # TODO
        pass

    def simple_atom_segment(self):
        """
        简易原子分词，将所有字放到一起作为一个词
        :return:
        """
        # TODO
        pass

    @staticmethod
    def quick_atom_segment(text: str, start: int, end: int):
        """
        快速原子分词
        :return:
        """
        atom_node_list = []
        offset_atom = start
        pre_type = CharType.get(text[offset_atom])
        while offset_atom < end:
            cur_type = CharType.get(text[offset_atom])
            if cur_type != pre_type:
                # 浮点数识别
                if pre_type == CharType.CT_NUM and "，,．.".find(text[offset_atom]) != -1:
                    if offset_atom + 1 < end:
                        next_type = CharType.get(text[offset_atom + 1])
                        if next_type == CharType.CT_NUM:
                            offset_atom += 1
                            continue
                atom_node_list.append(AtomNode(text[start:offset_atom], pre_type))
                start = offset_atom
            pre_type = cur_type
            offset_atom += 1
        if offset_atom == end:
            atom_node_list.append(AtomNode(text[start:offset_atom], pre_type))
        return atom_node_list

    def enable_index_mode(self, enable):
        if isinstance(enable, bool):
            self.config.index_mode = 2 if enable else 0
        elif isinstance(enable, int):
            if enable < 1:
                raise IllegalArgumentError("最小长度应当大于等于1")
            self.config.index_mode = enable
        return self

    def enable_part_of_speech_tagging(self, enable: bool):
        """
        开启词性标注
        :param enable:
        :return:
        """
        self.config.speech_tagging = enable
        return self

    def enable_name_recognize(self, enable: bool):
        self.config.name_recognize = enable
        self.config.update_ner_config()
        return self

    def enable_place_recognize(self, enable: bool):
        """
        开启地名识别
        :param enable:
        :return:
        """
        self.config.place_recognize = enable
        self.config.update_ner_config()
        return self

    def enable_organization_recognize(self, enable: bool):
        """
        开启机构名识别
        :param enable:
        :return:
        """
        self.config.organization_recognize = enable
        self.config.update_ner_config()
        return self

    def enable_custom_dictionary(self, enable: bool):
        """
        是否启用用户词典
        :param enable:
        :return:
        """
        self.config.use_custom_dictionary = enable
        return self

    def enable_new_custom_dictionary(self, custom_dictionary):
        """
        启用新的用户词典
        :param custom_dictionary:
        :return:
        """
        self.config.use_custom_dictionary = True
        self.custom_dictionary = custom_dictionary
        return self

    def enable_custom_dictionary_forcing(self, enable: bool):
        """
        是否尽可能强制使用用户词典
        :param enable:
        :return:
        """
        if enable:
            self.enable_custom_dictionary(True)
        self.config.force_custom_dictionary = enable
        return self

    def enable_translated_name_recognize(self, enable: bool):
        """
        是否启用音译人名识别
        :param enable:
        :return:
        """
        self.config.translated_name_recognize = enable
        self.config.update_ner_config()
        return self

    def enable_japanese_name_recognize(self, enable: bool):
        """
        是否启用日本人名识别
        :param enable:
        :return:
        """
        self.config.japanese_name_recognize = enable
        self.config.update_ner_config()
        return self

    def enable_offset(self, enable: bool):
        """
        是否启用偏移量计算
        :param enable:
        :return:
        """
        self.config.offset = enable
        return self

    def enable_number_quantifier_recognize(self, enable: bool):
        """
        是否启用数词和数量词识别
        :param enable:
        :return:
        """
        self.config.number_quantifier_recognize = enable
        return self

    def enable_all_named_entity_recognize(self, enable: bool):
        """
        是否启用所有的命名实体识别
        :param enable:
        :return:
        """
        self.config.name_recognize = enable
        self.config.japanese_name_recognize = enable
        self.config.translated_name_recognize = enable
        self.config.place_recognize = enable
        self.config.organization_recognize = enable
        self.config.update_ner_config()
        return self

    def enable_multithreading(self, thread_number):
        """
        开启多线程
        :param thread_number:
        :return:
        """
        if isinstance(thread_number, bool):
            if thread_number:
                thread_number = multiprocessing.cpu_count()
            else:
                thread_number = 1
        elif isinstance(thread_number, int):
            thread_number = max(1, thread_number)
        self.config.thread_number = thread_number
        return self
