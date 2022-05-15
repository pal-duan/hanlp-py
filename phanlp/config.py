from pathlib import Path
root_dir = Path(__file__).parent.parent

# 核心词典路径
CORE_DICTIONARY_PATH = root_dir / "data/dictionary/CoreNatureDictionary.txt"
# 用户自定义词典路径
CUSTOM_DICTIONARY_PATH = [root_dir / "data/dictionary/custom/CustomDictionary.txt"]
# 用户自定义词典是否自动重新生成缓存（根据词典文件的最后修改时间是否大于缓存文件的时间判断）
CUSTOM_DICTIONARY_AUTO_REFRESH_CACHE = True
