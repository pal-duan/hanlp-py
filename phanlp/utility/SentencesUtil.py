# -*- coding: utf-8 -*-
# @Time: 2022/5/23  14:45
# @Author: 2811755762@qq.com
"""
    Description:
        文本断句
"""


class SentencesUtil:
    @classmethod
    def to_sentence_list(cls, content: str, shortest: bool = True) -> list:
        sb = ""
        sentences = []
        i = 0
        while i < len(content):
            if not sb and content[i].isspace():
                i += 1
                continue
            sb += content[i]
            if content[i] == ".":
                if (i < len(content) - 1) and ord(content[i+1]) > 128:
                    cls.insert_into_list(sb, sentences)
                    sb = ""
            elif content[i] == "…":
                sb += "…"
                i += 1
                cls.insert_into_list(sb, sentences)
                sb = ""
            elif content[i] == "，" or content[i] == "," or content[i] == ";" or content[i] == "；":
                if not shortest:
                    i += 1
                    continue
                else:
                    cls.insert_into_list(sb, sentences)
                    sb = ""
            elif content[i] == " " or content[i] == "	" or content[i] == " " or content[i] == "。" \
                    or content[i] == "!" or content[i] == "！" or content[i] == "?" or content[i] == "？" \
                    or content[i] == "\n" or content[i] == "\r" or content[i] == "\r\n":
                cls.insert_into_list(sb, sentences)
                sb = ""
            i += 1
        if len(sb):
            cls.insert_into_list()
        return sentences

    @classmethod
    def insert_into_list(cls, sb: str, sentences: list):
        content = sb.strip()
        if len(content):
            sentences.append(content)


if __name__ == '__main__':
    print(SentencesUtil.to_sentence_list("逗号把句子切分为意群，表示小于分号大于顿号的停顿。"))
    print(SentencesUtil.to_sentence_list("逗号把句子切分为意群，表示小于分号大于顿号的停顿。", False))
    print(SentencesUtil.to_sentence_list("我白天是一名语言学习者，晚上是一名初级码农。空的时候喜欢看算法和应用数学书，也喜欢悬疑推理小说，ACG方面喜欢型月、轨迹。喜欢有思想深度的事物，讨厌急躁、拜金与安逸的人\r\n目前在魔都某女校学习，这是我的个人博客。闻道有先后，术业有专攻，请多多关照。"))
    print(len(SentencesUtil.to_sentence_list("我白天是一名语言学习者，晚上是一名初级码农。空的时候喜欢看算法和应用数学书，也喜欢悬疑推理小说，ACG方面喜欢型月、轨迹。喜欢有思想深度的事物，讨厌急躁、拜金与安逸的人\r\n目前在魔都某女校学习，这是我的个人博客。闻道有先后，术业有专攻，请多多关照。")))
