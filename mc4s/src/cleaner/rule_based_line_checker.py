# https://github.com/lighttransport/japanese-llama-experiment/blob/main/03_clean_step1/clean_text.py

import unicodedata
import re
broken_sentence_endings = """
...
... 
...　
\"
'
[…]
"""

broken_ending_list = broken_sentence_endings.split("\n")
broken_ending_list = [x for x in broken_ending_list if len(x) > 0]

broken_ending_list += [
    '続きを読む', '[続きを読む]', '(続きを読む)', '続きを見る', '続きをみる', '(続く)', '(続きを表示)', '(続きをみる)', '[続きをみる]', '[続きを見る]',
]
broken_ending_list += ['...(続きを表示)', '[ 続きを見る ]',
                       '・・・続きを見る', '... 続きを読む',
                       "詳細はこちら »",
                       "詳細>>>"
                       ]


def clean(sent: str):
    for broken_ending in broken_ending_list:
        # print("aa", broken_ending)
        if sent.endswith(broken_ending):
            return None
        if len(sent) < 2:
            return None
    return sent
