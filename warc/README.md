# WARCファイルのダウンロードとパース: 掃除中です｡

## 1_download_path_list.py
- CommonCrawl上の指定したsnapshotのpath listをダウンロード

## 2_download_and_parse.py
- path listをもとに...
    - warc.gzファイルをダウンロード
    - warcファイルを解凍
    - 日本語のページを抜き出し
    - ルールベースでクリーニング
    - 機械学習でゴミ記事を除外
    - corpusフォルダにテキストを書き出し
    - warcファイルに""を書き込み(hdd容量の節約)


# 出力されるtxtファイルが全て同じ中身になってしまうバグが見つかりました..