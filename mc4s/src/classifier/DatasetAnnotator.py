import os


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

        if not os.path.exists(out_path):
            os.makedirs(out_path)

        self.out_path = out_path

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
