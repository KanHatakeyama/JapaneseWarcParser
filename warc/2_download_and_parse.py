from src.cleaner.LineChecker import remove_dup_lines, remove_multi_headers
from datasets import load_dataset
import sys
from src.cleaner.WordIntegrator import WordIntegrator
from src.cleaner.PerplexityChecker import PerplexityChecker
from src.file_utils import make_dir
from src.parse_warc import extract_japanese_from_warc
from src.downloader import get_cc_path_list, download_warc_file
import random
sys.path.append("../")

"""
download and parse warc file
this script can be done in parallel

"""

if True:
    from mc4s.src.classifier.DatasetAnnotator import DatasetAnnotator
    from mc4s.src.cleaner.auto_cleaner import clean_text

# tagで分割されたテキストを統合するためのintegrator
integrator = WordIntegrator(
    checker=PerplexityChecker("data/lm_sp/ja.arpa.bin",
                              "data/lm_sp/ja.sp.model",
                              ),
    filter_path="dict/header_filter.txt",
    start_filter_path="dict/start_filter.txt",
    end_filter_path="dict/end_filter.txt"
)

# テキストを分類するためのannotator
dataset = load_dataset('mc4', 'ja', split='train', streaming=True)
annotator = DatasetAnnotator(dataset, clean_func=clean_text, n_preload=500,
                             out_path="../mc4s/annotations"
                             )

corpus_dir = "data/corpus"
make_dir(corpus_dir)


def download_and_parse(cc_path):
    # download warc file
    warc_path = download_warc_file(cc_path)

    # parse warc file
    print("parsing "+warc_path)
    try:
        tag_records = extract_japanese_from_warc(warc_path)
    except Exception as e:
        print("fail loading "+warc_path)

    # clean
    cleaned_records = []
    for id in range(len(tag_records)):
        record = tag_records[id]
        lines = [i[0].strip() for i in record["text"]]
        lines = integrator(lines)
        txt = "\n".join(lines)
        if txt != "":
            cleaned_records.append(
                {"url": record["url"], "timestamp": record["timestamp"], "text": txt})

    # classify and save
    for record in cleaned_records:
        is_noise = annotator.predict(record["text"])
        if is_noise == 1:
            continue
        filename = warc_path.split("/")[-1].replace(".warc", "")
        save_path = f"{corpus_dir}/{filename}.txt"
        with open(save_path, "a") as f:
            f.write(str(record)+"\n")

    print("done "+warc_path)
    # clear warc file
    with open(warc_path, "w") as f:
        f.write("")


# get path list
cc_path_list = get_cc_path_list()
random.shuffle(cc_path_list)
for cc_path in cc_path_list:
    download_and_parse(cc_path)
