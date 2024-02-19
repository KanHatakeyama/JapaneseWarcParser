

## 1_download_path_list.py
- CommonCrawl上の指定したsnapshotのpath listをダウンロード

## 2_download_warc.py
- path listをもとに､warcファイルをダウンロード(gz形式)
- gzを解凍し､warcファイルを生成 (ディスク容量の節約のため､gzの中身は""にする)

## 3_extract_japanese.py
- warcファイルを巡回し､日本語のテキストを抽出して､jap_dumpフォルダ内に､listデータをgzで保存する
- ディスク容量の節約のため､warcファイルの中身は""にする

## TODO
- listデータのクリーニングなど｡