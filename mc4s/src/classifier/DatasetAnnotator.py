import os
import random
from sklearn.model_selection import train_test_split
import MeCab
import fasttext
tagger = MeCab.Tagger()


def wakati_sentence(text):
    words = []
    for c in tagger.parse(text).splitlines()[:-1]:
        # surfaceに単語、featureに解析結果が入る
        try:
            surface, feature = c.split('\t')
        except:
            continue
        pos = feature.split(',')[0]
        surface = feature.split(',')[6]  # 原型に直す
        words.append(surface)
        # if pos in ['名詞', '形容詞', '動詞',"記号"]:
        #    words.append(surface)
        # else:
        #    continue
    words = [w for w in words if w != '*']
    return ' '.join(words)


def clean_func(text):
    return text


class DatasetAnnotator:
    def __init__(self, dataset,
                 clean_func=clean_func,
                 out_path="annotations",
                 max_length=300,
                 n_preload=10000,
                 ) -> None:
        self.dataset = dataset
        self.max_id = 0
        self.max_length = max_length
        self.clean_func = clean_func
        self.model = None

        if not os.path.exists(out_path):
            os.makedirs(out_path)

        self.out_path = out_path
        self.fasttext_path = self.out_path+"/text_labels"

        try:
            self.load_annotations()
        except Exception as e:
            self.good = []
            self.bad = []
            self.annotated = []
            print(e)

        # preload data
        self.get_text_by_id(n_preload)

    def get_text_by_id(self, i):
        if i >= self.max_id:
            self._load_dataset(i)
        text = self.clean_func(self.local_data[i]["text"])
        return text

    def _load_dataset(self, i):
        count = 0
        self.local_data = []
        for data in self.dataset:
            self.local_data.append(data)
            count += 1
            if count > i:
                break
        self.max_id += i

    def annotate(self, i):
        if i in self.annotated:
            return False
        text = self.get_text_by_id(i)[:self.max_length]
        if text == "":
            return True
        # print(text)
        label = input(text)
        if label == "q":
            return False

        if label == "":
            with open(f"{self.out_path}/bad.txt", "a") as f:
                f.write(f"{i}\n")
            self.bad.append(i)
        else:
            with open(f"{self.out_path}/good.txt", "a") as f:
                f.write(f"{i}\n")
            self.good.append(i)

        return True

    def load_annotations(self):
        with open(f"{self.out_path}/good.txt", "r") as f:
            good = f.readlines()
        with open(f"{self.out_path}/bad.txt", "r") as f:
            bad = f.readlines()
        self.good = [int(g) for g in good]
        self.bad = [int(b) for b in bad]
        self.annotated = self.good + self.bad

    def get_good_texts(self):
        return [self.get_text_by_id(i) for i in self.good]

    def get_bad_texts(self):
        return [self.get_text_by_id(i) for i in self.bad]

    def get_good_annotations(self):
        good_texts = self.get_good_texts()
        good_texts = [f'__label__0 {wakati_sentence(t)}' for t in good_texts]
        return good_texts

    def get_bad_annotations(self):
        bad_texts = self.get_bad_texts()
        bad_texts = [f'__label__1 {wakati_sentence(t)}' for t in bad_texts]
        return bad_texts

    def get_annotated_texts(self, shuffle=True):
        l = self.get_good_annotations() + self.get_bad_annotations()
        if shuffle:
            random.shuffle(l)

        return l

    def wakati_sentence(self, text):
        return wakati_sentence(text)

    def output_annotations(self):
        annotations = self.get_annotated_texts()
        X_train, X_test = train_test_split(
            annotations, test_size=0.2, random_state=100)
        X_valid, X_test = train_test_split(
            X_test, test_size=0.5, random_state=100)

        out_path = self.out_path+"/text_labels"
        if not os.path.exists(out_path):
            os.makedirs(out_path)

        with open(f'{out_path}/fasttext_train.txt', 'w') as temp_file:
            for text in X_train:
                temp_file.write(f"{text}\n")

        with open(f'{out_path}/fasttext_valid.txt', 'w') as temp_file:
            for text in X_valid:
                temp_file.write(f"{text}\n")
        with open(f'{out_path}/fasttext_test.txt', 'w') as temp_file:
            for text in X_test:
                temp_file.write(f"{text}\n")

        print(f"Annotations saved to {out_path}")

        self.fasttext_path = out_path

    def train_fasttext(self,
                       autotuneDuration=600,
                       # epoch=20,
                       wordNgrams=2,
                       ):
        print("Outputting annotations")
        self.output_annotations()
        print("Training fasttext model")
        model = fasttext.train_supervised(
            input=f"{self.fasttext_path}/fasttext_train.txt",
            autotuneValidationFile=f"{self.fasttext_path}/fasttext_valid.txt",
            autotuneDuration=autotuneDuration,
            # epoch=epoch,
            wordNgrams=wordNgrams,
            verbose=2
        )
        model.save_model(f"{self.fasttext_path}/model.bin")
        print(f"Model saved to {self.fasttext_path}/model.bin")
        print("Testing model")
        model = fasttext.load_model(f"{self.fasttext_path}/model.bin")
        ret = model.test(f"{self.fasttext_path}/fasttext_test.txt")
        print(ret)

        self.model = model

    def predict(self, text, return_raw=False):
        if self.model is None:
            print("Model is not trained. loading model")
            # load model
            self.model = fasttext.load_model(f"{self.fasttext_path}/model.bin")

        text = self.wakati_sentence(text)
        ret = self.model.predict(text)

        if return_raw:
            return ret
        else:
            return int(ret[0][0].split("_")[-1])

    def ask_annotations(self, n_annotations=1000):
        print("""
begin annotations
Enter: annnotate as "bad"
something: annotate as "good"
q: quit
""")
        for i in range(n_annotations):
            id = random.randint(0, self.max_id)
            r = self.annotate(id)
            if not r:
                break
