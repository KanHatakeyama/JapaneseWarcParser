import pandas as pd


def load_annotated_text(annot_path):

    df = pd.read_csv(annot_path, delimiter="\t", header=None,
                     on_bad_lines="warn",
                     names=["text", "label"])

    # df["label"] = df["label"].str.replace("bad", "1")
    df["label"] = df["label"].fillna("bad")
    # df["label"] = df["label"].str.replace("good", "0").astype(int)

    # textがnanのものを削除
    df = df.dropna(subset=["text"])

    texts = df["text"].tolist()
    labels = df["label"].tolist()
    # texts = [i[i.find("---")+3:] for i in texts]

    return texts, labels, df
