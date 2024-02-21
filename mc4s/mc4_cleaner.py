# %%

"""
mc4を掃除して､fasttextでgood/badを分類して､テキストを出力するコード
"""
import os
from src.classifier.DatasetAnnotator import DatasetAnnotator
from src.cleaner.auto_cleaner import clean_text
from datasets import load_dataset
from tqdm import tqdm

# mc4の読み込み
mc4_dataset = load_dataset('mc4', 'ja', split='train', streaming=True)

"""
#oscarなども読み込める
#ignore_verifications=Trueをつけないとエラーとなる
oscar_dataset = load_dataset('oscar', 'unshuffled_original_ja', 
                       split='train', 
                       ignore_verifications=True,
                       streaming=True)

"""

dataset = mc4_dataset

# テキストを分類するためのannotator
annotator = DatasetAnnotator(dataset, clean_func=clean_text, n_preload=50000)

# 何行ごとにファイルを分割するか
n_split = 10**6

corpus_dir = "corpus"
if not os.path.exists(corpus_dir):
    os.makedirs(corpus_dir)

cnt = 0
record_id = -1
for record in tqdm(dataset):
    record_id += 1

    try:
        text = record['text']

        # テキストクリーン
        text = clean_text(text)
        if text == "":
            continue

        # 記事の判定
        is_noise = annotator.predict(text)
        if is_noise == 1:
            continue

        d = {
            "id": record_id,
            "text": text,
        }
        file_name = f"{corpus_dir}/{cnt//n_split}.txt"
        with open(file_name, "a") as f:
            f.write(str(d)+"\n")
    except Exception as e:
        print(e)
        continue
