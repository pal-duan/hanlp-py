import abc
from enum import Enum

from algorithm.ArrayTool import ArrayTool


class BaseNode(metaclass=abc.ABCMeta):
    class StatusEnum(Enum):
        UNDEFINED_0 = 0
        NOT_WORD_1 = 1
        WORD_MIDDLE_2 = 2
        WORD_END_3 = 3

    def __init__(self, key: str = "", value=None, status=None):
        super().__init__()
        self.key = key
        self.value = value
        self.status = status
        self.children = None

    @abc.abstractmethod
    def add_child(self, node):
        pass

    def has_child(self, key: str) -> bool:
        return self.get_child(key) is not None

    @abc.abstractmethod
    def get_child(self, key: str):
        pass

    def change_child(self, node):
        add = False
        if node.status == self.StatusEnum.UNDEFINED_0 and self.status != self.StatusEnum.NOT_WORD_1:
            self.status = self.StatusEnum.NOT_WORD_1
            self.value = None
            add = True
        elif node.status == self.StatusEnum.NOT_WORD_1 and self.status == self.StatusEnum.WORD_END_3:
            self.status = self.StatusEnum.WORD_MIDDLE_2
        elif node.status == self.StatusEnum.WORD_END_3:
            if self.status != self.StatusEnum.WORD_END_3:
                self.status = self.StatusEnum.WORD_MIDDLE_2
            if self.get_value() is None:
                add = True
            self.set_value(node.get_value())
        return add

    def get_key(self) -> str:
        return self.key

    def get_value(self):
        return self.value

    def get_status(self):
        return self.status

    def set_value(self, value):
        self.value = value

    def __eq__(self, other):
        if isinstance(other, BaseNode):
            other = other.key
        return self.key == other

    def __lt__(self, other):
        if isinstance(other, BaseNode):
            other = other.key
        return self.key < other

    def __le__(self, other):
        if isinstance(other, BaseNode):
            other = other.key
        return self.key <= other

    def __gt__(self, other):
        if isinstance(other, BaseNode):
            other = other.key
        return self.key > other

    def __ge__(self, other):
        if isinstance(other, BaseNode):
            other = other.key
        return self.key >= other

    def walk(self, sb, entry_set):
        sb += self.key
        if self.status == self.StatusEnum.WORD_MIDDLE_2 or self.status == self.StatusEnum.WORD_END_3:
            entry_set.add((sb, self.value))
        if self.children is None:
            return
        for node in self.children:
            if node is None:
                continue
            node.walk(sb, entry_set)

    def __str__(self):
        return f"BaseNode{{status={self.status}, key={self.key}, value={self.value}}}"


class ListChildrenNode(BaseNode):
    def __init__(self, key: str = "", value=None, status=None):
        super().__init__(key, value, status)
        self.children = []

    def add_child(self, node):
        add = False
        index = ArrayTool.binary_search(self.children, node)
        if index >= 0:
            target = self.children[index]
            add = target.change_child(node)
        else:
            self.children.insert(-(index+1), node)
            add = True
        return add

    def get_child(self, key):
        if not self.children:
            return None
        index = ArrayTool.binary_search(self.children, key)
        return self.children[index] if index >= 0 else None

    def __str__(self):
        return f"ListChildrenNode{{status={self.status}, key={self.key}, value={self.value}, " \
               f"children={len(self.children)}}}"


class DictChildrenNode(BaseNode):
    def __init__(self, key: str = "", value=None, status=None):
        super().__init__(key, value, status)
        self.children = {}

    def add_child(self, node: BaseNode):
        add = False
        if node.key in self.children:
            target = self.children[node.key]
            add = target.change_child(node)
        else:
            self.children[node.key] = node
            add = True
        return add

    def get_child(self, key):
        if not self.children:
            return None
        return self.children.get(key)

    def __str__(self):
        return f"DictChildrenNode{{status={self.status}, key={self.key}, value={self.value}, " \
               f"children={len(self.children)}}}"
