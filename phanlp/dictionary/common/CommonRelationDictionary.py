

"""
一个没有指定资源位置的通用同义词词典
"""
import os
import time
from pathlib import Path

from collection.trie.DoubleArrayTrie import DoubleArrayTrie
from collection.trie.BinTrie import BinTrie
from utility.logger import logger
from utility.CustomError import RelationDictionaryLoadError
from utility.Predefine import Predefine
from algorithm.pytreemap import TreeMap, TreeSet


class CommonRelationDictionary:
    def __init__(self):
        self.trie = DoubleArrayTrie()
        self.bin_trie = BinTrie()

    class RelationItem:
        def __init__(self, entry, word_list, rela_type):
            self.entry = entry
            self.word_list = word_list
            self.rela_type = rela_type

        def to_string(self):
            return f"{self.entry}  {self.rela_type}  {self.word_list}"

        __str__ = to_string
        __repr__ = to_string

        def save(self, out):
            out.write((str(self.entry) + "\n").encode("utf-8"))
            out.write((",".join(self.word_list.to_list()) + "\n").encode("utf-8"))

        @classmethod
        def load(cls, out, rela_type):
            relation_item = CommonRelationDictionary.RelationItem()
            relation_item.entry = out.readline().strip()
            relation_item.rela_type = rela_type
            ts = TreeSet()
            word_list = out.readline().split(",")
            ts.add_all(word_list)
            relation_item.word_list = ts
            return relation_item

    @classmethod
    def create(cls, path, rela_type):
        dictionary = CommonRelationDictionary()
        if dictionary.load(path, rela_type):
            return dictionary
        return None

    def load(self, path: str, rela_type):
        if isinstance(path, str):
            path = Path(path)
        start = time.time()
        if self.__load(path, rela_type):
            logger.info(f"{path}加载成功，{self.trie.count()}个词条，耗时{time.time() - start}s")
        else:
            raise RelationDictionaryLoadError(f"{rela_type}词典{path}加载失败！")

    def __load(self, path, rela_type):
        logger.info(f"{rela_type}词典开始加载：{path}")
        if self.load_dat(path, rela_type):
            return True
        tree_map = TreeMap()
        line = 0
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    ts = TreeSet()
                    word_list = line.strip().split(" ")
                    if len(word_list) < 2:
                        continue
                    ts.add_all(word_list[1:])
                    tree_map.put(word_list[0], self.RelationItem(word_list[0], ts, rela_type))

            result_code = self.trie.build(tree_map)
            if result_code:
                logger.warning(f"构建{path}失败，错误码：{result_code}")
                return False
            logger.info(f"{rela_type}词典加载成功：{self.trie.count()}个词条，下面将写入缓存......")
            # 写入缓存
            try:
                with open(path.with_suffix(Predefine.BIN_EXT), "wb") as f:
                    relation_item_list = tree_map.values()
                    f.write((str(relation_item_list.size()) + "\n").encode('utf-8'))
                    for item in relation_item_list:
                        item.save(f)
                    self.trie.save(f)

                # 直接用pickle缓存
                # with(open(path.with_suffix(Predefine.BIN_EXT), "wb")) as f:
                #     pickle.dump(self.trie, f)

            except Exception as e:
                logger.warning(f"{path}缓存失败！\ndetail: {e}")
                return False
        except Exception as e:
            logger.warning(f"读取{path}失败，可能由行{line}造成")
            return False
        return True

    def load_dat(self, path, rela_type):
        try:
            with open(path.with_suffix(Predefine.BIN_EXT), "rb") as fp:
                size = int(fp.readline().strip())
                relation_item_list = []
                for i in range(size):
                    relation_item = self.RelationItem.load(fp, rela_type)
                    relation_item_list.append(relation_item)
                if not self.trie.load(fp, relation_item_list):
                    return False

            # 从pickle缓存中加载
            # with open(path.with_suffix(Predefine.BIN_EXT), "rb") as f:
            #     self.trie = pickle.load(f)

            logger.info(f"{rela_type}词典从缓存文件{path.with_suffix(Predefine.BIN_EXT)}中加载......")
        except FileNotFoundError as e:
            logger.warning(f"缓存文件{path.with_suffix(Predefine.BIN_EXT)}不存在！\ndetail: {e}")
            return False
        except Exception as e:
            logger.warning(f"缓存文件{path.with_suffix(Predefine.BIN_EXT)}读取失败！\ndetail: {e}")
            return False
        return True

    @staticmethod
    def is_dic_need_update(path):
        bin_path = path.with_suffix(Predefine.BIN_EXT)
        if not bin_path.exists():
            return True
        last_modified = os.path.getmtime(bin_path)
        if path.exists() and os.path.getmtime(path) > last_modified:
            os.remove(bin_path)
            logger.info(f"已清除缓存文件{bin_path}！")
            return True
        return False

    def get(self, key):
        item = self.trie[key]
        if item is not None:
            return item
        return self.bin_trie[key]

    def __getitem__(self, key):
        return self.get(key)
