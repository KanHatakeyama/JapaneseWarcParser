import pandas as pd
import numpy as np
from tqdm import tqdm
from ..cleaner.auto_cleaner import clean_text
from .text_characterizer import texts_to_X


def naive_generate_questions(dataset, out_path="annotations/original_data/just_texts.txt",
                             max_lines=300):
    # simply output the first 300 characters of each text
    cleaned_text_list = []
    cnt = 0
    for record in tqdm(dataset):
        cnt += 1
        if cnt > max_lines:
            break
        original_text = record["text"]
        text = clean_text(original_text)
        if text != "":
            first_line = text.split("\n")[0]
            cleaned_text_list.append(first_line[:300])
        # print(original_text)

    with open(out_path, "w") as f:
        for text in cleaned_text_list:
            f.write(text + "\n")
    print("output to", out_path)


def generate_uncertain_questions(dataset,
                                 pipeline,
                                 w2v=None,
                                 out_path="annotations/original_data/uncertain_questions.txt",
                                 start_num=300,
                                 n_problems=100,
                                 cut_threshold=0.3,
                                 annot_texts=[],
                                 ):
    problem_list = []
    text_list = []
    cnt = 0
    i = 0
    for record in tqdm(dataset):
        i += 1
        if i % 10 != 0:
            continue
        cnt += 1
        if cnt < start_num:
            continue
        text = record["text"]
        text = clean_text(text)
        if text not in annot_texts:
            if text == "":
                continue

            if w2v is not None:
                x = texts_to_X(w2v, [text])[0]
            else:
                x = text
            problem_list.append(x)
            text_list.append(text)
        if len(problem_list) > n_problems:
            break

    new_X = np.array(problem_list)
    predicted_probabilities = pipeline.predict_proba(new_X)

    df = pd.DataFrame({"probability": predicted_probabilities[:, 1],
                       "text": text_list,

                       })
    df = df.sort_values(by="probability", ascending=False)
    df = df[df["probability"] > cut_threshold]
    df = df[df["probability"] < 1-cut_threshold]

    question_texts = df["text"].tolist()
    with open(out_path, "w") as f:
        f.write("\n".join(question_texts))
    print("output to", out_path)
