import numpy as np
import MeCab
from functools import lru_cache
from gensim.models.fasttext import load_facebook_model
from tqdm import tqdm
from datasets import load_dataset
import numpy as np
from sklearn.cluster import KMeans, MiniBatchKMeans
import joblib

mecab = MeCab.Tagger("")


def extract_nouns(text):

    # 文章を形態素解析し、名詞を抽出
    nodes = mecab.parseToNode(text)
    nouns = []
    while nodes:
        features = nodes.feature.split(",")
        if features[0] == "名詞":
            nouns.append(nodes.surface)
        nodes = nodes.next

    return nouns


class Text2Vec:
    def __init__(self, model):
        self.model = model
        self.dim = 300

    @lru_cache(maxsize=10**4)  # 単語ベクトルの計算結果をキャッシュ
    def _word2vec_cached(self, word):
        try:
            return self.model.wv[word]
        except KeyError:
            return np.zeros(self.dim)

    def word2vec(self, word):
        return self._word2vec_cached(word)

    def text2vec(self, text):
        nouns = extract_nouns(text)
        vecs = [self.word2vec(n) for n in nouns]
        if len(vecs) == 0:
            return np.zeros(self.dim)
        else:
            return np.mean(vecs, axis=0)


class NounClustering:
    def __init__(self, fasttext_path='annotations/text_labels/cc.ja.300.bin',
                 kmeans_path='annotations/text_labels/kmeans.pkl'):

        print("Loading fasttext model")
        model = load_facebook_model(fasttext_path)
        self.text2vec = Text2Vec(model)
        self.kmeans_path = kmeans_path

        try:
            self.load_kmeans()
            print("kmeans loaded:", self.kmeans_path)
        except Exception as e:
            print(e)

    def load_kmeans(self):
        self.kmeans = joblib.load(self.kmeans_path)

    def train_wiki(self,
                   n_cluesters=100,
                   n_samples=10**5,
                   ):

        print("Loading Wikipedia dataset")
        self.wiki_dataset = load_dataset(
            "hpprc/wikipedia-20240101", split="train").shuffle()

        print("Extracting titles")
        title_list = []
        n_samples = min(n_samples, len(self.wiki_dataset))
        for i in tqdm(range(n_samples)):
            try:
                title_list.append(self.wiki_dataset[i]['title'])
            except Exception as e:
                print(i, self.wiki_dataset[i], e)

        print("Extracting vectors")
        self.title_vecs = [self.text2vec.text2vec(
            i) for i in tqdm(title_list[:n_samples])]

        self.title_vecs = np.array(self.title_vecs)
        # k-meansクラスタリング
        print("clustering...")
        self.kmeans = MiniBatchKMeans(
            n_clusters=n_cluesters, random_state=1).fit(self.title_vecs)

        joblib.dump(self.kmeans, self.kmeans_path)

    def predict(self, text):
        vec = self.text2vec.text2vec(text).reshape(1, -1).astype(np.double)
        return self.kmeans.predict(vec)[0]
