
import MeCab
from collections import Counter

# テキスト
tagger = MeCab.Tagger()


def do_filter(text):
    if text is None:
        return None

    lines = text.split("\n")
    out_lines = []
    for line in lines:
        out_line = frequency_filter(line)
        if out_line is not None:
            out_lines.append(out_line)
    if len(out_lines) == 0:
        return None
    return "\n".join(out_lines)


def frequency_filter(text, threshold=0.8):

    # テキストを解析
    parsed = tagger.parse(text)

    # 品詞をカウントするためのCounterオブジェクト
    pos_counter = Counter()

    # 解析結果を行ごとに処理
    all_counts = 0
    for line in parsed.split('\n'):
        # EOSまたは空行の場合はスキップ
        if line == 'EOS' or line == '':
            continue
        # タブで分割し、形態素情報を取得
        pos_info = line.split('\t')
        # print(pos_info)
        pos = pos_info[1]
        pos = pos.split(",")[0]
        # 品詞をカウント
        pos_counter[pos] += 1
        all_counts += 1
    # print(pos_counter)
    meishi_and_symbol_counts = pos_counter['名詞'] + \
        pos_counter['記号']+pos_counter['補助記号']

    ratio = meishi_and_symbol_counts/all_counts
    # print(ratio, pos_counter)
    if ratio > threshold:
        return None
    else:
        return text
