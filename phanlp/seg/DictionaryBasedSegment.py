

import abc

from seg.Segment import Segment
from utility.logger import logger


class DictionaryBasedSegment(Segment, metaclass=abc.ABCMeta):
    def __init__(self):
        super().__init__()

    def enable_part_of_speech_tagging(self, enable: bool):
        return super().enable_part_of_speech_tagging(enable)

    def enable_custom_dictionary(self, enable: bool):
        if enable:
            logger.warning(f"为基于词典的分词器开启用户词典太浪费了，建议直接将所有词典的路径传入构造函数，这样速度更快、内存更省")
        return super().enable_custom_dictionary(enable)

    def pos_tag(self, text, word_net, nature_array):
        if self.config.speech_tagging:
            i = 0
            while i < len(nature_array):
                if nature_array[i] is None:
                    j = i + 1
                    while j < len(nature_array):
                        if nature_array[j] is not None:
                            break
                        j += 1
                    atom_node_list = self.quick_atom_segment(text, i, j)
                    for atom_node in atom_node_list:
                        if len(atom_node.s_word) >= word_net[i]:
                            word_net[i] = len(atom_node.s_word)
                            nature_array[i] = atom_node.get_nature()
                            i += word_net[i]
                    i = j
                else:
                    i += 1
