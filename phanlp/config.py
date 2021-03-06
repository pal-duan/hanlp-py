from pathlib import Path
root_dir = Path(__file__).parent.parent

DEBUG = True

# 核心词典路径
CORE_DICTIONARY_PATH = root_dir / "data/dictionary/CoreNatureDictionary.txt"
# 用户自定义词典路径
CUSTOM_DICTIONARY_PATH = [root_dir / "data/dictionary/custom/CustomDictionary.txt"]
# 用户自定义词典是否自动重新生成缓存（根据词典文件的最后修改时间是否大于缓存文件的时间判断）
CUSTOM_DICTIONARY_AUTO_REFRESH_CACHE = True
# 是否执行字符正规化（繁体->简体，全角->半角, 大写->小写），切换配置后必须删除CustomDictionary.bin缓存
NORMALIZATION = True
# 字符正规化表（全角转半角，繁体转简体）
CHAR_TABLE_PATH = root_dir / "data/dictionary/other/CharTable.txt"
# 新词发现缓存文件默认路径
NEW_WORD_DISCOVER_CACHE = root_dir / "data/dictionary/NewWordDiscover"
# 停用词词典路径
CORE_STOP_WORD_DICTIONARY_PATH = root_dir / "data/dictionary/stopwords.txt"
# 分词结果是否展示词性
SHOW_TERM_NATURE = True
# 字符类型对应表
CHAR_TYPE_PATH = root_dir / "data/dictionary/other/CharType.json"
# 二元语法词典路径
BI_GRAM_DICTIONARY_PATH = root_dir / "data/dictionary/CoreNatureDictionary.ngram.txt"
# 核心同义词词典路径
CORE_SYNONYM_DICTIONARY_PATH = root_dir / "data/dictionary/CoreSynonymDictionary.txt"
