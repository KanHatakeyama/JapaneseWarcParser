from ..cleaner.parts_filter import parts_count
import numpy as np
from .loader import load_annotated_text
import json


def characterize_text(text, max_length=300):
    d = {}
    d["text_length"] = len(text)/max_length
    pos_counter, all_counts, word_counts = parts_count(
        text, return_word_count=True)
    meishi_and_symbol_counts = pos_counter['名詞'] + \
        pos_counter['記号']+pos_counter['補助記号']
    d["meishi_ratio"] = meishi_and_symbol_counts/all_counts

    keyword_counts = {}
    for word, pos in word_counts.keys():
        if pos in ["名詞", "動詞", "形容詞"]:
            keyword_counts[word] = word_counts[(word, pos)]

    # word
    d["keyword_counts"] = keyword_counts

    return d


def descriptor_to_vector(d, w2v):
    keyword_counts = d["keyword_counts"]
    key_sum = 0
    cnt = 0
    for key in keyword_counts:
        key_sum += keyword_counts[key]
        vec = w2v.word2vec(key)*keyword_counts[key]
        if cnt == 0:
            vec_sum = vec
        else:
            vec_sum += vec

    average_vec = vec_sum/key_sum
    average_vec = np.append(average_vec, d["text_length"])
    average_vec = np.append(average_vec, d["meishi_ratio"])

    return average_vec


def texts_to_X(w2v, texts, max_lentgh=300):
    X = []
    for text in texts:
        d = characterize_text(text[:max_lentgh])
        vec = descriptor_to_vector(d, w2v)
        X.append(vec)
    X = np.array(X)
    return X


def annotation_data_to_X_y(w2v,
                           annotation_data_path="annotations/original_data/annotations.txt",
                           characarized_data_path="annotations/characterized_data.json",
                           ):
    texts, label, df = load_annotated_text(annotation_data_path)
    characterized_data_list = []
    for text, label in zip(texts, label):
        d = characterize_text(text)
        d["label"] = label
        characterized_data_list.append(d)

    if characarized_data_path != "":
        with open(characarized_data_path, "w") as f:
            json.dump(characterized_data_list, f, ensure_ascii=False, indent=4)

    # ベクトル化
    X = []
    y = []
    for d in characterized_data_list:
        vec = descriptor_to_vector(d, w2v)
        X.append(vec)
        if d["label"] == "good":
            y.append(1)
        else:
            y.append(0)

    X = np.array(X)
    y = np.array(y)
    return X, y, texts
