import gzip
import shutil
import requests
import os


def make_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"ディレクトリが作成されました: {dir_path}")


def download_file(url, save_path):
    if os.path.exists(save_path):
        print(f"ファイルがすでに存在します: {save_path}")
        return
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)
        print(f"ファイルが正常にダウンロードされました: {save_path}")
    else:
        print(f"ファイルのダウンロードに失敗しました。ステータスコード: {response.status_code}")


def decompress_gz(gz_path, output_path, remove_gz=True, fill_blank_gz=False):
    with gzip.open(gz_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"{gz_path}が解凍され、{output_path}に保存されました。")
    if remove_gz:
        os.remove(gz_path)

    if fill_blank_gz:
        with open(gz_path, 'w') as f:
            f.write("")
