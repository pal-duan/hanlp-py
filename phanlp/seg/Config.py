# -*- coding: utf-8 -*-
# @Time: 2022/5/23  10:58
# @Author: 2811755762@qq.com
"""
    Description:
        分词器配置项
"""


class Config:
    def __init__(self):
        # 是否索引分词（合理的最小分割），indexMode代表全切分词语的最小长度（包含）
        self.index_mode = 0
        self.name_recognize = True  # 是否识别中国人名
        self.translated_name_recognize = True  # 是否识别音译人名
        self.japanese_name_recognize = False  # 是否识别日本人名
        self.place_recognize = False  # 是否识别地名
        self.organization_recognize = False  # 是否识别机构
        self.use_custom_dictionary = True  # 是否加载用户词典
        self.force_custom_dictionary = False  # 用户词典高优先级
        self.speech_tagging = True  # 词性标注
        self.ner = True  # 命名实体识别是否至少有一项被激活
        self.offset = False  # 是否计算偏移量
        self.number_quantifier_recognize = False  # 是否识别数字和量词
        self.thread_number = 1  # 并行分词的线程数

    def update_ner_config(self):
        """
        更新命名实体识别总开关
        """
        self.ner = self.name_recognize or self.translated_name_recognize or self.japanese_name_recognize \
            or self.place_recognize or self.organization_recognize

    def is_index_mode(self) -> bool:
        return self.index_mode > 0
