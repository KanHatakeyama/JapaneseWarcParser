from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
import MeCab
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.calibration import CalibratedClassifierCV


def prepare_vector_classifier():
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', CalibratedClassifierCV(LogisticRegression())),

    ])

    return pipeline


# テキストデータの前処理とトークン化のための関数
def tokenize(text):
    mecab = MeCab.Tagger()
    mecab.parse('')  # MeCabのバグ対策
    node = mecab.parseToNode(text)
    tokens = []
    while node:
        if node.surface != '':
            tokens.append(node.surface)
        node = node.next
    return tokens


def prepare_tfid_classifier():
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(tokenizer=tokenize)),
        # ('clf', CalibratedClassifierCV(LinearSVC(), method='sigmoid')),
        # ('clf', CalibratedClassifierCV(RandomForestClassifier())),
        ('clf', CalibratedClassifierCV(LogisticRegression())),
    ])
    return pipeline
