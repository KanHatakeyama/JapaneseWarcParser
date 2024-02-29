# WARCファイルのダウンロードと前処理

## 概要

CommonCrawlに含まれるWARCファイルをダウンロードし,
日本語データを抽出, 抽出したデータからいらないテキストを
除く処理を行うスクリプトです.

このスクリプトはGENIAC(松尾研究室のプロジェクト)の活動
として作成されました.

なお, このスクリプトの内日本語データの抽出を行うところまでは
Google Colab Notebookになっています. CommonCrawlのデータ数は
膨大であり, 個人だけでは対処しきれません. ぜひ, 分割抽出/加工に
ご協力をお願いいたします.

## 処理に使用するファイルの説明

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

## 環境構築の手順

### docker, docker-composeをインストールされていない場合

setup_commandsに入っているコマンドをターミナルに張り付けて
実行をしてください.

### docker, dokcer-composeがインストールされている場合

dokcer-composeコマンドでコンテナを作成し, そのコンテナをご使用ください

```
docker-compose up -d
```


#### 出力されるtxtファイルが全て同じ中身になってしまうバグが見つかりました.. → 解決しました

