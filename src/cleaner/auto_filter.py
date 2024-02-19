from . import text_normalizer, clean_text, clean_text2, linewise_filtering, freq_filter
from .utils import remove_dup_lines


def do_filter(text):
    # text = text_normalizer.normalize(text)
    text = clean_text.do_clean(text, 100)  # 文末が...などを削除 (webページでよくある)
    text = clean_text2.do_filter(text)  # 繰り返しの多い文を削除
    text = linewise_filtering.do_filter(text)  # ルールベースで行を削除
    text = freq_filter.do_filter(text)  # 単語だらけの行を削除
    for i in range(3):
        text = remove_dup_lines(text)  # 重複行を削除

    return text
