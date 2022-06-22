import re

from utility.Predefine import Predefine


class TextUtility:
    @classmethod
    def is_all_chinese(cls, text: str) -> bool:
        """
        是否全是中文
        :param text: 
        :return: 
        """
        return re.fullmatch("[\\u4E00-\\u9FA5]+", text) is not None

    @classmethod
    def is_all_not_chinese(cls, text: str) -> bool:
        """
        是否全部不是中文
        :param text:
        :return:
        """
        return re.match("[\\u4E00-\\u9FA5]+", text) is None

    @classmethod
    def is_all_single_byte(cls, text: str) -> bool:
        """
        是否全是单字节
        :param text:
        :return:
        """
        for i in text:
            if ord(i) > 128:
                return False
        return True

    @classmethod
    def is_all_num(cls, text: str) -> bool:
        """
        是否全是数字
        :param text:
        :return:
        """
        i = 0
        # 判断开头是否是+-之类的符号
        if text[0] in "±+-＋－—":
            i += 1
        # 全角的０１２３４５６７８９ 字符
        while i < len(text) and text[i] in "０１２３４５６７８９":
            i += 1
        if 0 < i < len(text):
            if text[i] in "·∶:，,．.／/":
                i += 1
            while i < len(text) and text[i] in "０１２３４５６７８９":
                i += 1
        if i >= len(text):
            return True

        # 半角的0123456789字符
        while i < len(text) and text[i] in "0123456789":
            i += 1
        if 0 < i < len(text):
            if text[i] in ",./:∶·，．／":
                i += 1
                while i < len(text) and text[i] in "0123456789":
                    i += 1
        if i < len(text):
            if text[i] in "百千万亿佰仟%％‰":
                i += 1
        if i >= len(text):
            return True
        return False
