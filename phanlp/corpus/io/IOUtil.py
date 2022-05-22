
from pathlib import Path
import re

from algorithm.pytreemap import TreeMap
from corpus.tag.Nature import Nature
from config import NORMALIZATION
from dictionary.other.CharTable import CharTable
from dictionary.CoreDictionary import CoreDictionary
from utility.NatureUtility import NatureUtility
from utility.logger import logger


class IOUtil:
    @classmethod
    def write_custom_nature(cls, out, custom_nature_collector):
        if not custom_nature_collector:
            return
        out.write((str(-len(custom_nature_collector)) + "\n").encode('utf-8'))
        for nature in custom_nature_collector:
            out.write((nature.to_string() + "\n").encode('utf-8'))

    @classmethod
    def load_dictionary(cls, path_list: list):
        _map = TreeMap()
        custom_nature_collector = set()
        for path in path_list:
            file = Path(path) if isinstance(path, str) else path
            file_name = file.name
            cut = file_name.rfind(" ")
            default_nature = Nature.from_string("n")
            if cut > 0:
                nature_str = file_name[cut+1:]
                path = file.parent / file_name[:cut]
                if nature_str and not nature_str.endswith(".txt") and not nature_str.endswith(".csv"):
                    try:
                        default_nature = Nature.create(nature_str)
                    except Exception as e:
                        logger.error(f"文件路径【{path}】写错了！\ndetail: {e}")
                        continue
            logger.info(f"以默认词性[{default_nature}]加载自定义词典{path}中......")
            success = cls._load_dictionary(path, _map, str(path).endswith(".csv"), default_nature,
                                           custom_nature_collector=custom_nature_collector)
            if not success:
                logger.warning(f"词典{path}加载失败！")
            return _map, custom_nature_collector

    @classmethod
    def _load_dictionary(
            cls,
            path,
            storage,
            is_csv,
            default_nature,
            normalization=NORMALIZATION,
            custom_nature_collector=None
    ):
        try:
            with open(path, encoding="utf-8") as f:
                splitter = "," if is_csv else r"\s"
                for line in f:
                    param = re.split(splitter, line.strip())
                    if not param[0]:
                        continue
                    if normalization:
                        param[0] = CharTable.convert(param[0])
                    nature_count = (len(param) - 1) // 2
                    attribute = CoreDictionary.Attribute()
                    if nature_count == 0:
                        attribute.nature.append(default_nature)
                        attribute.frequency.append(1000)
                        attribute.total_frequency = 1000
                    else:
                        for i in range(nature_count):
                            attribute.nature.append(
                                NatureUtility.covert_string2nature(param[1 + 2 * i], custom_nature_collector))
                            attribute.frequency.append(int(param[2 + 2 * i]))
                            attribute.total_frequency += int(param[2 + 2 * i])

                    storage.put(param[0], attribute)
        except Exception as e:
            logger.warning(f"自定义词典{path}读取错误！\ndetail: {e}")
            return False
        return True
