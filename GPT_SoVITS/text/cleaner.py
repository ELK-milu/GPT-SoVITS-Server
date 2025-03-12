from text import cleaned_text_to_sequence
import os
# if os.environ.get("version","v1")=="v1":
#     from text import chinese
#     from text.symbols import symbols
# else:
#     from text import chinese2 as chinese
#     from text.symbols2 import symbols

from text import symbols as symbols_v1
from text import symbols2 as symbols_v2

special = [
    # ("%", "zh", "SP"),
    ("￥", "zh", "SP2"),
    ("^", "zh", "SP3"),
    # ('@', 'zh', "SP4")#不搞鬼畜了，和第二版保持一致吧
]


def clean_text(text, language, version=None):
    # 如果未提供版本参数，则从环境变量中获取，默认为 'v2'
    if version is None:
        version = os.environ.get('version', 'v2')

    # 根据版本选择符号集和语言模块映射
    if version == "v1":
        symbols = symbols_v1.symbols  # 使用 v1 版本的符号集
        language_module_map = {"zh": "chinese", "ja": "japanese", "en": "english"}  # v1 版本的语言模块映射
    else:
        symbols = symbols_v2.symbols  # 使用 v2 版本的符号集
        language_module_map = {"zh": "chinese2", "ja": "japanese", "en": "english", "ko": "korean",
                               "yue": "cantonese"}  # v2 版本的语言模块映射

    # 如果传入的语言不在支持的语言列表中，默认设置为英语，并将文本置为空字符串
    if language not in language_module_map:
        language = "en"
        text = " "

    # 检查文本中是否包含特殊符号，如果存在且匹配对应语言，则调用 `clean_special` 函数进行特殊处理
    for special_s, special_l, target_symbol in special:
        if special_s in text and language == special_l:
            return clean_special(text, language, special_s, target_symbol, version)

    # 动态导入对应语言的处理模块
    language_module = __import__("text." + language_module_map[language], fromlist=[language_module_map[language]])

    # 如果语言模块中有 `text_normalize` 方法，则对文本进行规范化处理，否则保持原样
    if hasattr(language_module, "text_normalize"):
        norm_text = language_module.text_normalize(text)
    else:
        norm_text = text

    # 对于中文或粤语，进行特殊的音素转换，并确保转换后的音素长度与原始文本长度一致
    if language == "zh" or language == "yue":
        phones, word2ph = language_module.g2p(norm_text)
        assert len(phones) == sum(word2ph)#"音素长度与单词对应的音素数量总和不一致"
        assert len(norm_text) == len(word2ph)#"规范化后的文本长度与单词对应的音素数量不一致"

    # 对于英文，进行音素转换，如果音素长度小于4，则在开头添加逗号 `,` 音素以确保最小长度
    elif language == "en":
        phones = language_module.g2p(norm_text)
        if len(phones) < 4:
            phones = [','] + phones
        word2ph = None

    # 其他语言直接进行音素转换
    else:
        phones = language_module.g2p(norm_text)
        word2ph = None

    # 将不在符号集中的音素替换为 'UNK'（未知）
    phones = ['UNK' if ph not in symbols else ph for ph in phones]

    # 返回清理后的音素序列、每个单词对应的音素数量以及规范化后的文本
    return phones, word2ph, norm_text


def clean_special(text, language, special_s, target_symbol, version=None):
    if version is None:version=os.environ.get('version', 'v2')
    if version == "v1":
        symbols = symbols_v1.symbols
        language_module_map = {"zh": "chinese", "ja": "japanese", "en": "english"}
    else:
        symbols = symbols_v2.symbols
        language_module_map = {"zh": "chinese2", "ja": "japanese", "en": "english", "ko": "korean","yue":"cantonese"}

    """
    特殊静音段sp符号处理
    """
    text = text.replace(special_s, ",")
    language_module = __import__("text."+language_module_map[language],fromlist=[language_module_map[language]])
    norm_text = language_module.text_normalize(text)
    phones = language_module.g2p(norm_text)
    new_ph = []
    for ph in phones[0]:
        assert ph in symbols
        if ph == ",":
            new_ph.append(target_symbol)
        else:
            new_ph.append(ph)
    return new_ph, phones[1], norm_text


def text_to_sequence(text, language, version=None):
    version = os.environ.get('version',version)
    if version is None:version='v2'
    phones = clean_text(text)
    return cleaned_text_to_sequence(phones, version)


if __name__ == "__main__":
    print(clean_text("你好%啊啊啊额、还是到付红四方。", "zh"))
