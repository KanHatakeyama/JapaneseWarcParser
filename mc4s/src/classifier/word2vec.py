from typing import Any
import numpy as np
from functools import lru_cache
from gensim.models.fasttext import load_facebook_model


class Word2Vec:
    def __init__(self, model_path):
        self.model = load_facebook_model(model_path)
        self.dim = 300

    @lru_cache(maxsize=10**4)  # 単語ベクトルの計算結果をキャッシュ
    def _word2vec_cached(self, word):
        try:
            return self.model.wv[word]
        except KeyError:
            return np.zeros(self.dim)

    def word2vec(self, word):
        return self._word2vec_cached(word)

    def __call__(self, word):
        return self.word2vec(word)
