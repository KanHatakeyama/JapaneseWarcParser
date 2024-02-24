
from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup
from tqdm import tqdm
import json
import glob
import os


def halfwidth_ratio(s):
    if len(s) == 0:  # 空の文字列の場合は0を返す
        return 0
    halfwidth_count = sum(
        1 for char in s
        if '\u0020' <= char <= '\u007E' or  # 基本的なASCII範囲
           '\uFF61' <= char <= '\uFF9F' or  # 半角カタカナ
           char in ('\u0009', '\u000A', '\u000D')  # タブ、改行、復帰
    )
    return halfwidth_count / len(s)


def pre_clean(soup):
    texts_with_tags = []
    for tag in soup.find_all(True):
        # 特定のタグを除外する場合
        # if tag.name not in ['html', 'body', 'ul']:
        text = tag.get_text(separator="\n", strip=True)
        spl_text = text.split("\n")
        spl_text = [i.strip() for i in spl_text if i.strip()]  # 空の文字列を除外
        for item in spl_text:
            if tag.name == "script" or tag.name == "style":
                continue
            texts_with_tags.append((item, tag.name))  # テキストとタグの名前をタプルとして追加
    return texts_with_tags


def extract_japanese_from_warc(path,
                               save_dir="json",
                               max_num=10**10,
                               ):
    ja_soup_list = []
    path = path.replace("\\", "/")  # for windows env
    filename = path.split("/")[-1].replace(".warc", ".json")
    if os.path.exists(f"{save_dir}/{filename}"):
        print("already done")
        return
    # 途中から再開する用の位置情報の取得
    if len(ja_soup_list) > 0:
        fin_record_id = ja_soup_list[-1]["record_id"]
    else:
        fin_record_id = 0
    # WARCファイルを開く
    record_id = 0
    with open(path, 'rb') as stream:
        for record in tqdm(ArchiveIterator(stream)):
            record_id += 1
            if record_id <= fin_record_id:
                continue
            if record.rec_type == 'response':
                if record.http_headers.get_header('Content-Type') == 'text/html':
                    content = record.content_stream().read()
                    soup = BeautifulSoup(content, 'html.parser')
                    # <html>タグからlang属性を取得
                    html_tag = soup.find('html')
                    if html_tag and html_tag.has_attr('lang'):
                        lang = html_tag['lang']
                        texts = pre_clean(soup)
                        if len(texts) == 0:
                            continue
                        if lang == "ja":
                            if soup.title is not None:
                                title = soup.title.string
                            else:
                                title = ""
                            d = {
                                "record_id": record_id,
                                "url": record.rec_headers.get_header('WARC-Target-URI'),
                                "title": title,
                                "timestamp": record.rec_headers.get_header('WARC-Date'),
                                "text": texts,
                            }
                            ja_soup_list.append(d)
                        if len(ja_soup_list) > max_num:
                            break
    return ja_soup_list
